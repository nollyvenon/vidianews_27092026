"""Text generation through the Anthropic Messages API.

Used for chat replies, proofreading, and brand voice analysis. Requires ``ANTHROPIC_API_KEY``;
without it every call is refused with 503 rather than answered with invented content.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import HTTPException, status

from app.core.config import settings

ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
REQUEST_TIMEOUT_SECONDS = 60.0


def _unavailable(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=message)


def _alternating_messages(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Keep user/assistant turns only and merge consecutive turns from the same role.

    The Messages API expects alternating roles, and a chat may contain several user messages
    in a row before a reply was requested.
    """
    merged: List[Dict[str, str]] = []
    for item in history:
        role, content = item.get("role"), (item.get("content") or "").strip()
        if role not in ("user", "assistant") or not content:
            continue
        if merged and merged[-1]["role"] == role:
            merged[-1]["content"] += "\n\n" + content
        else:
            merged.append({"role": role, "content": content})
    return merged


async def complete_text(
    messages: List[Dict[str, str]],
    system: Optional[str] = None,
    max_tokens: Optional[int] = None,
) -> Tuple[str, int]:
    """Send a conversation to the model and return its text and the tokens it consumed."""
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        raise _unavailable("AI features are not configured: set ANTHROPIC_API_KEY on the server")

    turns = _alternating_messages(messages)
    if not turns or turns[-1]["role"] != "user":
        raise _unavailable("There is no user message to answer")

    payload: Dict[str, Any] = {
        "model": settings.AI_CHAT_MODEL,
        "max_tokens": max_tokens or settings.AI_CHAT_MAX_TOKENS,
        "messages": turns,
    }
    if system:
        payload["system"] = system
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        try:
            response = await client.post(ANTHROPIC_MESSAGES_URL, json=payload, headers=headers)
        except httpx.HTTPError as exc:
            raise _unavailable(f"AI provider is unreachable: {exc.__class__.__name__}") from exc

    if response.status_code >= 400:
        raise _unavailable(f"AI provider rejected the request (HTTP {response.status_code})")

    data = response.json()
    text = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
    if not text.strip():
        raise _unavailable("AI provider returned an empty reply")

    usage = data.get("usage") or {}
    tokens = int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))
    return text.strip(), tokens


async def generate_reply(history: List[Dict[str, str]]) -> Tuple[str, int]:
    """Return the assistant's chat reply to the latest user message."""
    return await complete_text(history, system=settings.AI_CHAT_SYSTEM_PROMPT)


async def complete_json(instructions: str, document: str, max_tokens: int = 2048) -> Any:
    """Ask the model for JSON about a document and parse the answer.

    The model is asked to return only JSON; the first JSON object or array in the reply is used.
    A reply without parseable JSON is refused rather than guessed at.
    """
    prompt = f"{instructions}\n\nRespond with only the JSON, no commentary.\n\n<document>\n{document}\n</document>"
    text, _ = await complete_text([{"role": "user", "content": prompt}], max_tokens=max_tokens)
    match = re.search(r"(\[.*\]|\{.*\})", text, re.DOTALL)
    if not match:
        raise _unavailable("AI provider returned an unreadable analysis")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise _unavailable("AI provider returned an unreadable analysis") from exc
