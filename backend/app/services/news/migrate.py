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
}


async def ensure_columns(engine: AsyncEngine) -> None:
    try:
        async with engine.begin() as conn:
            for name, ddl in _COLUMNS.items():
                await conn.execute(text(f"ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS {name} {ddl}"))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_news_articles_enriched_at ON news_articles (enriched_at)"
            ))
    except Exception as exc:  # noqa: BLE001 - table may not exist yet on a first run
        _log.warning("news column migration skipped: %r", exc)
