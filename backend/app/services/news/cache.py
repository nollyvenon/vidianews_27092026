"""Small response cache: Redis when reachable, in-process otherwise.

Keys carry a version number that is bumped whenever new articles are ingested,
so cached listings never outlive the data they were built from.
"""

import json
import logging
import time
from typing import Any, Dict, Optional, Tuple

from app.core.config import settings

_log = logging.getLogger(__name__)

_redis = None
_redis_down_until = 0.0
_local: Dict[str, Tuple[float, str]] = {}
_local_version = 0
_PREFIX = "news:"


async def _client():
    global _redis, _redis_down_until
    if time.time() < _redis_down_until:
        return None
    if _redis is None:
        try:
            import redis.asyncio as aioredis
            _redis = aioredis.from_url(settings.REDIS_URL, socket_connect_timeout=1, socket_timeout=1,
                                       decode_responses=True)
        except Exception as exc:  # noqa: BLE001
            _log.warning("redis unavailable: %r", exc)
            _redis_down_until = time.time() + 60
            return None
    return _redis


async def _version() -> str:
    global _redis_down_until
    r = await _client()
    if r is not None:
        try:
            return str(await r.get(_PREFIX + "ver") or 0)
        except Exception as exc:  # noqa: BLE001
            _log.warning("redis read failed, using local cache: %r", exc)
            _redis_down_until = time.time() + 60
    return f"L{_local_version}"


async def cache_get(key: str) -> Optional[Any]:
    full = f"{_PREFIX}{await _version()}:{key}"
    r = await _client()
    if r is not None:
        try:
            raw = await r.get(full)
            return json.loads(raw) if raw else None
        except Exception:  # noqa: BLE001
            pass
    hit = _local.get(full)
    if hit and hit[0] > time.time():
        return json.loads(hit[1])
    return None


async def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    full = f"{_PREFIX}{await _version()}:{key}"
    raw = json.dumps(value, default=str)
    r = await _client()
    if r is not None:
        try:
            await r.set(full, raw, ex=ttl)
            return
        except Exception:  # noqa: BLE001
            pass
    if len(_local) > 500:
        _local.clear()
    _local[full] = (time.time() + ttl, raw)


async def cache_invalidate() -> None:
    """Bump the version so every cached listing becomes unreachable."""
    global _local_version
    _local_version += 1
    _local.clear()
    r = await _client()
    if r is not None:
        try:
            await r.incr(_PREFIX + "ver")
        except Exception:  # noqa: BLE001
            pass
