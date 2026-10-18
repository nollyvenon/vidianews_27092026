"""ASGI middleware that times each API request and hands it to the usage recorder.

The endpoint is recorded as its route template (for example ``/api/v1/content/{content_id}``), not the
concrete path, so every content id counts toward the same endpoint. Templates are resolved with the
application's own route table and cached, so the table is scanned once per distinct concrete path.
"""

import time
from typing import Any, Awaitable, Callable, Dict, Iterable, Optional, Tuple

from starlette.routing import Match

from app.core.security import decode_token
from app.services.api_usage_recorder import ApiUsageRecorder

RESOLVE_CACHE_LIMIT = 4096
UNMATCHED_ENDPOINT = "(unmatched)"


class ApiUsageMiddleware:
    def __init__(
        self,
        app: Callable[..., Awaitable[None]],
        recorder: ApiUsageRecorder,
        routes: Callable[[], Iterable[Any]],
        prefix: str,
    ) -> None:
        self.app = app
        self.recorder = recorder
        self._routes = routes
        self._prefix = prefix
        self._cache: Dict[Tuple[str, str], str] = {}

    def resolve_template(self, method: str, path: str, scope: dict) -> str:
        key = (method, path)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        template = UNMATCHED_ENDPOINT
        for route in self._routes():
            match, _ = route.matches(scope)
            if match == Match.FULL:
                template = getattr(route, "path", UNMATCHED_ENDPOINT)
                break
        if len(self._cache) >= RESOLVE_CACHE_LIMIT:
            self._cache.clear()
        self._cache[key] = template
        return template

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] != "http" or not scope.get("path", "").startswith(self._prefix):
            await self.app(scope, receive, send)
            return

        status: Optional[int] = None
        response_bytes = 0

        async def send_wrapper(message: dict) -> None:
            nonlocal status, response_bytes
            if message["type"] == "http.response.start":
                status = message["status"]
            elif message["type"] == "http.response.body":
                response_bytes += len(message.get("body", b""))
            await send(message)

        started = time.perf_counter()
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration_ms = (time.perf_counter() - started) * 1000
            method = scope.get("method", "GET")
            template = self.resolve_template(method, scope.get("path", ""), scope)
            await self.recorder.record(
                method,
                template,
                status or 500,
                duration_ms,
                user_id=user_id_from_scope(scope),
                response_bytes=response_bytes,
            )


def user_id_from_scope(scope: dict) -> Optional[int]:
    """The signed-in user behind the request's bearer token, without a database lookup."""
    for name, value in scope.get("headers", []):
        if name == b"authorization":
            scheme, _, token = value.decode("latin-1").partition(" ")
            if scheme.lower() != "bearer" or not token:
                return None
            claims = decode_token(token.strip())
            user_id = (claims or {}).get("user_id")
            return int(user_id) if isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit()) else None
    return None
