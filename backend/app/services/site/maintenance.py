"""Daily housekeeping: drop analytics older than the retention window and dead admin sessions."""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import delete

from app.db.session import AsyncSessionLocal
from app.models.site import AdminLoginAttempt, AdminSession
from app.services.site import analytics
from app.services.site.sitesettings import load_settings

_log = logging.getLogger(__name__)
_task: Optional[asyncio.Task] = None


async def run_once() -> dict:
    site = await load_settings(fresh=True)
    purged = await analytics.purge_old(int(site["analytics_retention_days"]))
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        sessions = await db.execute(delete(AdminSession).where(
            (AdminSession.expires_at < now - timedelta(days=7)) | (AdminSession.revoked_at < now - timedelta(days=7))))
        attempts = await db.execute(delete(AdminLoginAttempt).where(AdminLoginAttempt.at < now - timedelta(days=30)))
        await db.commit()
    return {"page_views": purged, "sessions": sessions.rowcount or 0, "login_attempts": attempts.rowcount or 0}


async def _loop() -> None:
    await asyncio.sleep(60)
    while True:
        try:
            _log.info("maintenance: %s", await run_once())
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            _log.exception("maintenance failed")
        await asyncio.sleep(24 * 3600)


def start() -> None:
    global _task
    if _task is None:
        _task = asyncio.create_task(_loop(), name="site-maintenance")


async def stop() -> None:
    global _task
    if _task:
        _task.cancel()
        try:
            await _task
        except asyncio.CancelledError:
            pass
        _task = None
