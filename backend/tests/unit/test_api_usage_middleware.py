"""Unit tests for the API usage middleware: route templates, the path prefix and status capture."""

from starlette.routing import Route

from app.core.api_usage_middleware import UNMATCHED_ENDPOINT, ApiUsageMiddleware


class _RecordingRecorder:
    def __init__(self) -> None:
        self.calls = []
        self.users = []

    async def record(self, method, endpoint, status_code, duration_ms, user_id=None, response_bytes=0):
        self.calls.append((method, endpoint, status_code))
        self.users.append((user_id, response_bytes))


async def _ok_endpoint(request):  # pragma: no cover - only used to build routes
    return None


def _scope(method: str, path: str) -> dict:
    return {"type": "http", "method": method, "path": path, "query_string": b"", "headers": [], "root_path": ""}


async def _run(middleware, scope, status=200):
    async def app(scope, receive, send):
        await send({"type": "http.response.start", "status": status, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    middleware.app = app

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    sent = []

    async def send(message):
        sent.append(message)

    await middleware(scope, receive, send)
    return sent


def _middleware(recorder, routes):
    return ApiUsageMiddleware(app=None, recorder=recorder, routes=lambda: routes, prefix="/api/v1")


async def test_a_parameterised_path_is_recorded_under_its_route_template():
    recorder = _RecordingRecorder()
    routes = [Route("/api/v1/content/{content_id}", _ok_endpoint, methods=["GET"])]
    middleware = _middleware(recorder, routes)

    await _run(middleware, _scope("GET", "/api/v1/content/42"))
    await _run(middleware, _scope("GET", "/api/v1/content/43"))

    assert recorder.calls == [("GET", "/api/v1/content/{content_id}", 200), ("GET", "/api/v1/content/{content_id}", 200)]


async def test_the_resolved_template_is_cached_per_concrete_path():
    recorder = _RecordingRecorder()
    routes = [Route("/api/v1/x", _ok_endpoint, methods=["GET"])]
    middleware = _middleware(recorder, routes)
    middleware.resolve_template("GET", "/api/v1/x", _scope("GET", "/api/v1/x"))

    middleware._routes = lambda: []  # a second lookup must not scan the table again
    assert middleware.resolve_template("GET", "/api/v1/x", _scope("GET", "/api/v1/x")) == "/api/v1/x"


async def test_a_path_no_route_matches_is_recorded_as_unmatched():
    recorder = _RecordingRecorder()
    middleware = _middleware(recorder, [])

    await _run(middleware, _scope("GET", "/api/v1/nowhere"), status=404)

    assert recorder.calls == [("GET", UNMATCHED_ENDPOINT, 404)]


async def test_traffic_outside_the_api_prefix_is_not_recorded():
    recorder = _RecordingRecorder()
    middleware = _middleware(recorder, [])

    sent = await _run(middleware, _scope("GET", "/health"))

    assert recorder.calls == []
    assert sent[0]["status"] == 200


async def test_websocket_scopes_pass_through_unrecorded():
    recorder = _RecordingRecorder()
    middleware = _middleware(recorder, [])
    passed = []

    async def app(scope, receive, send):
        passed.append(scope["type"])

    middleware.app = app
    await middleware({"type": "websocket", "path": "/api/v1/websocket/ws"}, None, None)

    assert passed == ["websocket"]
    assert recorder.calls == []


async def test_an_error_raised_by_the_endpoint_is_recorded_as_a_server_error():
    recorder = _RecordingRecorder()
    routes = [Route("/api/v1/boom", _ok_endpoint, methods=["GET"])]
    middleware = _middleware(recorder, routes)

    async def failing_app(scope, receive, send):
        raise RuntimeError("boom")

    middleware.app = failing_app
    try:
        await middleware(_scope("GET", "/api/v1/boom"), None, None)
    except RuntimeError:
        pass

    assert recorder.calls == [("GET", "/api/v1/boom", 500)]
