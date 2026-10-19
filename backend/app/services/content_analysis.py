"""Model-backed proofreading and brand voice analysis.

The model is asked for structured JSON. Results are checked against the document before they are
stored: a proofreading issue is kept only when its quoted text occurs in the document, so every
stored position points at real text.
"""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from app.services.ai_chat_service import complete_json

PROOFREAD_INSTRUCTIONS = """You are a careful copy editor. Find problems in the document in these categories: {categories}.
Return a JSON array. Each item is an object with keys:
- "type": one of grammar, spelling, punctuation, style
- "severity": one of info, warning, error
- "text": the exact problematic text, copied character for character from the document
- "suggestion": the corrected text
- "explanation": a short reason
Report only real problems. Return [] when there are none."""

BRAND_VOICE_INSTRUCTIONS = """You check a document against a brand voice guide.
Guide: {guide}
Return one JSON object with keys:
- "consistency_score": number 0-100, how consistently the document follows the guide
- "compliance_score": number 0-100, how many rules the document meets
- "tone_match_score": number 0-100, how closely the tone matches the guide
- "recommendations": array of short, concrete suggestions (may be empty)"""

PROOFREAD_TYPES = {"grammar", "spelling", "punctuation", "style"}
SEVERITIES = {"info", "warning", "error"}


def _unreadable() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="AI provider returned an analysis that could not be used",
    )


async def find_proofreading_issues(text: str, grammar: bool, spelling: bool, style: bool) -> List[Dict[str, Any]]:
    """Return proofreading issues whose quoted text appears in the document, with positions."""
    categories = [name for name, enabled in (("grammar", grammar), ("spelling", spelling), ("style", style)) if enabled]
    if not categories:
        return []

    data = await complete_json(
        PROOFREAD_INSTRUCTIONS.format(categories=", ".join(categories) + ", punctuation"),
        text,
    )
    if not isinstance(data, list):
        raise _unreadable()

    issues: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        quoted = str(item.get("text") or "")
        position = text.find(quoted) if quoted else -1
        issue_type = str(item.get("type") or "").lower()
        severity = str(item.get("severity") or "").lower()
        if position < 0 or issue_type not in PROOFREAD_TYPES:
            continue
        issues.append(
            {
                "type": issue_type,
                "severity": severity if severity in SEVERITIES else "info",
                "text": quoted,
                "suggestion": str(item.get("suggestion") or ""),
                "explanation": str(item.get("explanation") or ""),
                "position": position,
                "length": len(quoted),
            }
        )
    return issues


def _score(value: Any) -> float:
    try:
        return max(0.0, min(100.0, float(value)))
    except (TypeError, ValueError) as err:
        raise _unreadable() from err


async def analyze_brand_voice(text: str, guide_description: str) -> Dict[str, Any]:
    """Score a document against a brand voice guide."""
    data = await complete_json(BRAND_VOICE_INSTRUCTIONS.format(guide=guide_description), text)
    if not isinstance(data, dict):
        raise _unreadable()
    recommendations = data.get("recommendations") or []
    return {
        "consistency_score": _score(data.get("consistency_score")),
        "compliance_score": _score(data.get("compliance_score")),
        "tone_match_score": _score(data.get("tone_match_score")),
        "recommendations": [str(item) for item in recommendations if item][:20],
    }


def brand_voice_result(compliance_score: float) -> str:
    """Map a compliance score to the stored check result."""
    if compliance_score >= 85:
        return "compliant"
    if compliance_score >= 60:
        return "partial"
    if compliance_score > 0:
        return "non_compliant"
    return "needs_review"


def describe_guide(guide: Optional[Any]) -> str:
    """Plain-text summary of a guide's tone and traits for the prompt."""
    if guide is None:
        return "No guide"
    tone = ", ".join(f"{key}: {value}" for key, value in (guide.tone or {}).items()) or "not specified"
    traits = ", ".join(str(trait) for trait in (guide.personality_traits or [])) or "not specified"
    return f"{guide.name}. Tone: {tone}. Personality traits: {traits}. Vocabulary level: {guide.vocabulary_level or 'not specified'}."
