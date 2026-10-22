"""Add columns introduced after the first release to an existing news_articles table.

`create_all` never alters an existing table, and the stored articles must survive
upgrades, so new columns are added in place.
"""

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

_log = logging.getLogger(__name__)

_COLUMNS = {
    "image_source": "VARCHAR(16)",
    "image_credit": "VARCHAR(500)",
    "image_credit_url": "VARCHAR(2048)",
    "full_content": "TEXT",
    "enriched_at": "TIMESTAMP WITH TIME ZONE",
    "is_published": "BOOLEAN NOT NULL DEFAULT TRUE",
    "deleted_at": "TIMESTAMP WITH TIME ZONE",
    "edited_at": "TIMESTAMP WITH TIME ZONE",
    "cleaned_at": "TIMESTAMP WITH TIME ZONE",
    "content_issue": "VARCHAR(32)",
    "edited_by": "VARCHAR(255)",
    "meta_title": "VARCHAR(200)",
    "meta_description": "VARCHAR(320)",
}


async def ensure_columns(engine: AsyncEngine) -> None:
    try:
        async with engine.begin() as conn:
            for name, ddl in _COLUMNS.items():
                await conn.execute(text(f"ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS {name} {ddl}"))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_news_articles_enriched_at ON news_articles (enriched_at)"
            ))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_news_articles_is_published ON news_articles (is_published)"
            ))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_news_articles_content_issue ON news_articles (content_issue)"
            ))
            # A fetch that was running when the process stopped will never finish.
            await conn.execute(text(
                "UPDATE news_fetch_cycles SET status = 'interrupted', finished_at = now() WHERE status = 'running'"
            ))
    except Exception as exc:  # noqa: BLE001 - table may not exist yet on a first run
        _log.warning("news column migration skipped: %r", exc)
