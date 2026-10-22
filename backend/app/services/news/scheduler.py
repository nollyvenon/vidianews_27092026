"""Background scheduler: fetch all sources periodically."""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.news import NewsArticle
from app.services.news.ingest import run_fetch

_log = logging.getLogger(__name__)
_task: Optional[asyncio.Task] = None


async def _latest_fetch_age() -> Optional[timedelta]:
    async with AsyncSessionLocal() as session:
        latest = (await session.execute(select(func.max(NewsArticle.fetched_at)))).scalar_one()
    return datetime.now(timezone.utc) - latest if latest else None


async def _loop() -> None:
    interval = max(5, settings.NEWS_FETCH_INTERVAL_MINUTES) * 60
    await asyncio.sleep(5)  # let the app finish starting
    try:
        age = await _latest_fetch_age()
    except Exception as exc:  # noqa: BLE001
        _log.warning("news scheduler: could not read last fetch time: %r", exc)
        age = None
    if settings.NEWS_FETCH_ON_STARTUP and (age is None or age.total_seconds() > interval):
        await _safe_run()
    while True:
        await asyncio.sleep(interval)
        await _safe_run()


async def _safe_run() -> None:
    try:
        await run_fetch()
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 - the loop must survive any failure
        _log.exception("scheduled news fetch failed")


def start() -> None:
    global _task
    if settings.NEWS_ENABLE_SCHEDULER and _task is None:
        _task = asyncio.create_task(_loop(), name="news-scheduler")
        _log.info("news scheduler started (every %s min)", settings.NEWS_FETCH_INTERVAL_MINUTES)


async def stop() -> None:
    global _task
    if _task:
        _task.cancel()
        try:
            await _task
        except asyncio.CancelledError:
            pass
        _task = None
