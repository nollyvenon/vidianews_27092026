"""One-off and repeatable clean-up of articles that were stored before cleaning existed.

Safety: the first time an article is touched, its original title/body/summary/description is
copied into `news_article_originals`. Later runs always clean from that original, so improving
the rules can never compound earlier changes, and nothing is ever lost. Source name, URL and
all other provenance columns are left alone.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict

from sqlalchemy import select, text, update

from app.db.session import AsyncSessionLocal
from app.models.news import NewsArticle as A
from app.services.news import nlp
from app.services.news.cache import cache_invalidate
from app.services.news.cleaning import clean_body, clean_summary, clean_title

_log = logging.getLogger(__name__)

BATCH = 100

_ORIGINALS_DDL = """
CREATE TABLE IF NOT EXISTS news_article_originals (
    article_id INTEGER PRIMARY KEY,
    title VARCHAR(500),
    content TEXT,
    full_content TEXT,
    summary TEXT,
    description TEXT,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT now()
)
"""


async def clean_existing(force: bool = False) -> Dict[str, int]:
    """Clean stored articles; `force` re-cleans ones already done (e.g. after the rules changed)."""
    stats = {"checked": 0, "changed": 0}
    async with AsyncSessionLocal() as session:
        await session.execute(text(_ORIGINALS_DDL))
        await session.commit()

    last_id = 0
    while True:
        async with AsyncSessionLocal() as session:
            query = select(A).where(A.id > last_id).order_by(A.id).limit(BATCH)
            if not force:
                query = query.where(A.cleaned_at.is_(None))
            rows = (await session.execute(query)).scalars().all()
            if not rows:
                break
            ids = [r.id for r in rows]
            last_id = ids[-1]

            await session.execute(text(
                "INSERT INTO news_article_originals (article_id, title, content, full_content, summary, description) "
                "SELECT id, title, content, full_content, summary, description FROM news_articles WHERE id = ANY(:ids) "
                "ON CONFLICT (article_id) DO NOTHING"), {"ids": ids})
            originals = {r[0]: r for r in (await session.execute(text(
                "SELECT article_id, title, content, full_content FROM news_article_originals WHERE article_id = ANY(:ids)"),
                {"ids": ids})).all()}

            now = datetime.now(timezone.utc)
            for a in rows:
                stats["checked"] += 1
                _, o_title, o_content, o_full = originals[a.id]
                edited = a.edited_at is not None  # a person has rewritten this story: keep their headline and summary
                title = a.title if edited else (clean_title(o_title, a.source_key) or a.title)
                content = clean_body(a.content if edited else o_content, a.source_key)
                full = clean_body(a.full_content if edited else o_full, a.source_key) or None
                values = {"cleaned_at": now}
                if not edited:
                    # summary and description are generated, so rebuild them from the cleaned text
                    res = await asyncio.to_thread(nlp.analyze, title, content, source_name="", published_at=a.published_at)
                    summary = clean_summary(res.summary, a.source_key) or ""
                    values.update(summary=summary, description=res.description)
                if (title, content, full) != (a.title, a.content, a.full_content):
                    stats["changed"] += 1
                values.update(title=title[:500], content=content, full_content=full)
                await session.execute(update(A).where(A.id == a.id).values(**values))
            await session.commit()

    if stats["changed"]:
        await cache_invalidate()
    _log.info("news clean-up: %s", stats)
    return stats
