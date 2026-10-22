"""Content-quality gate: stories that are too short, cut off, or only promotion are held back.

A held article is stored (so a re-fetch does not bring it back and an admin can review it) but
`is_published` is False and `content_issue` records why, so every public query already skips it.
The gate looks at the best text we have (the extracted page text when there is more than the feed
teaser) after publisher boilerplate has been removed.
"""

import re
from typing import Optional

from app.core.config import settings
from app.services.news.cleaning import clean_body

ISSUE_EMPTY = "empty"
ISSUE_PROMO = "promo_only"
ISSUE_SHORT = "too_short"
ISSUE_INCOMPLETE = "incomplete"

ISSUE_LABELS = {
    ISSUE_EMPTY: "No article text",
    ISSUE_PROMO: "Only promotional text",
    ISSUE_SHORT: "Too short",
    ISSUE_INCOMPLETE: "Cut off / incomplete",
}

_TRUNCATED = re.compile(r"(\.{3}|…|\[\s*(\.{3}|…)\s*\]|\bread more|\bcontinue reading|\bclick to read)\W*$", re.I)


def min_chars_default() -> int:
    return max(1, int(settings.NEWS_MIN_CONTENT_CHARS))


def best_body(content: Optional[str], full_content: Optional[str]) -> str:
    """The text a reader would see: the page text when it is longer than the feed teaser."""
    if full_content and len(full_content) > len(content or ""):
        return full_content
    return content or ""


def assess(content: Optional[str], full_content: Optional[str], min_chars: int,
           source_key: Optional[str] = None) -> Optional[str]:
    """Return the reason this text should not be published, or None when it is complete enough.

    Text is cleaned again here so a body that was mostly promotion is judged on what is left.
    """
    raw = best_body(content, full_content).strip()
    if not raw:
        return ISSUE_EMPTY
    text = clean_body(raw, source_key).strip()
    if not text:
        return ISSUE_PROMO
    if len(text) < min_chars:
        return ISSUE_INCOMPLETE if _TRUNCATED.search(text) else ISSUE_SHORT
    if _TRUNCATED.search(text) and len(text) < 2 * min_chars:
        return ISSUE_INCOMPLETE
    return None


async def current_min_chars() -> int:
    from app.services.site.sitesettings import load_settings  # local: the settings module is optional at import time
    try:
        return int((await load_settings())["news_min_content_chars"])
    except Exception:  # noqa: BLE001 - never block publishing on a settings read
        return min_chars_default()


async def sweep(min_chars: Optional[int] = None) -> dict:
    """Hold back stored articles that fail the gate and release held ones that now pass.

    Articles an editor has touched (`edited_at`) and deleted ones are never changed: a person's
    decision to publish, unpublish or restore wins over the automatic check.
    """
    from sqlalchemy import select, update

    from app.db.session import AsyncSessionLocal
    from app.models.news import NewsArticle as A
    from app.services.news.cache import cache_invalidate

    limit = min_chars or await current_min_chars()
    stats = {"checked": 0, "held": 0, "released": 0}
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(
            select(A.id, A.source_key, A.content, A.full_content, A.is_published, A.content_issue)
            .where(A.deleted_at.is_(None), A.edited_at.is_(None))
        )).all()
        for article_id, source_key, content, full, published, issue in rows:
            stats["checked"] += 1
            found = assess(content, full, limit, source_key)
            if found and (published or issue != found):
                values = {"is_published": False, "content_issue": found, "is_featured": False}
                stats["held"] += 1 if published else 0
            elif not found and issue:
                values = {"is_published": True, "content_issue": None}
                stats["released"] += 1
            else:
                continue
            await session.execute(update(A).where(A.id == article_id).values(**values))
        await session.commit()
    if stats["held"] or stats["released"]:
        await cache_invalidate()
    return stats
