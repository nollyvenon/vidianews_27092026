"""Records how often each API endpoint is called, how long it takes and how often it fails, and how much
each signed-in user calls the API and downloads.

Calls are aggregated in memory and written in batches, so a request never waits on a database write.
Endpoint totals go to ``APIUsageMetrics`` (per method and route template); per-user totals go to
``QuotaUsage`` (API calls and response bandwidth). A batch is written every FLUSH_THRESHOLD calls, when
FLUSH_INTERVAL_SECONDS has passed since the last write, and on the periodic and shutdown flushes driven by
the application lifespan. A failed write puts its counts back, so nothing is lost silently.
"""

import asyncio
import logging
import time
from typing import Callable, Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.advanced_platform import APIUsageMetrics
from app.models.security_performance import QuotaUsage
from app.models.user import User

logger = logging.getLogger(__name__)

FLUSH_THRESHOLD = 50
FLUSH_INTERVAL_SECONDS = 30.0
ENDPOINT_COLUMN_LENGTH = 500
BYTES_PER_GB = 1024 ** 3


class _Bucket:
    """Running totals for one endpoint since the last write."""

    __slots__ = ("calls", "errors", "total_ms", "max_ms", "min_ms")

    def __init__(self) -> None:
        self.calls = 0
        self.errors = 0
        self.total_ms = 0.0
        self.max_ms = 0.0
        self.min_ms = 0.0

    def add(self, duration_ms: float, is_error: bool) -> None:
        self.min_ms = duration_ms if self.calls == 0 else min(self.min_ms, duration_ms)
        self.max_ms = max(self.max_ms, duration_ms)
        self.calls += 1
        self.errors += 1 if is_error else 0
        self.total_ms += duration_ms

    def merge(self, other: "_Bucket") -> None:
        if other.calls == 0:
            return
        self.min_ms = other.min_ms if self.calls == 0 else min(self.min_ms, other.min_ms)
        self.max_ms = max(self.max_ms, other.max_ms)
        self.calls += other.calls
        self.errors += other.errors
        self.total_ms += other.total_ms


class ApiUsageRecorder:
    def __init__(
        self,
        session_factory: async_sessionmaker,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._session_factory = session_factory
        self._clock = clock
        self._pending: Dict[Tuple[str, str], _Bucket] = {}
        self._pending_users: Dict[int, List[int]] = {}  # user id -> [api calls, response bytes]
        self._pending_calls = 0
        self._last_flush = clock()
        self._lock: Optional[asyncio.Lock] = None

    def _guard(self) -> asyncio.Lock:
        # Created on first use so the lock binds to the event loop that actually serves requests.
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    async def record(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration_ms: float,
        user_id: Optional[int] = None,
        response_bytes: int = 0,
    ) -> None:
        key = (method.upper(), endpoint[:ENDPOINT_COLUMN_LENGTH])
        async with self._guard():
            self._pending.setdefault(key, _Bucket()).add(duration_ms, status_code >= 500)
            if user_id is not None:
                totals = self._pending_users.setdefault(user_id, [0, 0])
                totals[0] += 1
                totals[1] += max(response_bytes, 0)
            self._pending_calls += 1
            due = (
                self._pending_calls >= FLUSH_THRESHOLD
                or self._clock() - self._last_flush >= FLUSH_INTERVAL_SECONDS
            )
        if due:
            await self.flush()

    def discard_pending(self) -> None:
        """Forget counts that have not been written yet (used to isolate tests from one another)."""
        self._pending = {}
        self._pending_users = {}
        self._pending_calls = 0

    async def flush(self) -> int:
        """Write the pending totals. Returns how many calls were written."""
        async with self._guard():
            pending, self._pending = self._pending, {}
            pending_users, self._pending_users = self._pending_users, {}
            written = self._pending_calls
            self._pending_calls = 0
            self._last_flush = self._clock()
        if not pending and not pending_users:
            return 0
        try:
            async with self._session_factory() as session:
                await self._write_endpoints(session, pending)
                await self._write_users(session, pending_users)
                await session.commit()
        except Exception:
            logger.exception("API usage could not be saved; %d calls kept for the next write", written)
            async with self._guard():
                for key, bucket in pending.items():
                    self._pending.setdefault(key, _Bucket()).merge(bucket)
                for user_id, (calls, size) in pending_users.items():
                    totals = self._pending_users.setdefault(user_id, [0, 0])
                    totals[0] += calls
                    totals[1] += size
                self._pending_calls += written
            return 0
        return written

    @staticmethod
    async def _write_endpoints(session: AsyncSession, pending: Dict[Tuple[str, str], _Bucket]) -> None:
        for (method, endpoint), bucket in pending.items():
            row = (await session.execute(
                select(APIUsageMetrics).where(
                    APIUsageMetrics.endpoint == endpoint,
                    APIUsageMetrics.method == method,
                )
            )).scalar_one_or_none()
            if row is None:
                row = APIUsageMetrics(
                    endpoint=endpoint,
                    method=method,
                    call_count=0,
                    error_count=0,
                    average_response_time_ms=0.0,
                    max_response_time_ms=0.0,
                    min_response_time_ms=0.0,
                )
                session.add(row)
            prior_calls = row.call_count or 0
            prior_total = (row.average_response_time_ms or 0.0) * prior_calls
            row.call_count = prior_calls + bucket.calls
            row.error_count = (row.error_count or 0) + bucket.errors
            row.average_response_time_ms = (prior_total + bucket.total_ms) / row.call_count
            row.max_response_time_ms = max(row.max_response_time_ms or 0.0, bucket.max_ms)
            row.min_response_time_ms = (
                bucket.min_ms if prior_calls == 0 else min(row.min_response_time_ms or 0.0, bucket.min_ms)
            )

    @staticmethod
    async def _write_users(session: AsyncSession, pending_users: Dict[int, List[int]]) -> None:
        if not pending_users:
            return
        # A token can outlive its account; only accounts that still exist can own a quota row.
        existing = set((await session.execute(
            select(User.id).where(User.id.in_(list(pending_users)))
        )).scalars().all())
        for user_id, (calls, size) in pending_users.items():
            if user_id not in existing:
                continue
            row = (await session.execute(
                select(QuotaUsage).where(QuotaUsage.user_id == user_id)
            )).scalar_one_or_none()
            if row is None:
                row = QuotaUsage(user_id=user_id, api_calls=0, storage_gb=0.0, bandwidth_gb=0.0)
                session.add(row)
            row.api_calls = (row.api_calls or 0) + calls
            row.bandwidth_gb = (row.bandwidth_gb or 0.0) + size / BYTES_PER_GB
