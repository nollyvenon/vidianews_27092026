"""Advanced platform: realtime, jobs, pipelines, cache and API documentation, on the real database (async)."""

from datetime import datetime, timedelta, timezone

import pytest
from starlette.websockets import WebSocketDisconnect as StarletteWebSocketDisconnect

from app.core.security import create_access_token
from app.models.advanced_platform import (
    BackgroundJob,
    CacheEntry,
    CacheStrategy,
    DocumentationFormat,
    JobStatus,
    RealtimeEvent,
    WebSocketConnectionStatus,
)
from app.models.user import User
from app.services.advanced_platform_service import (
    APIDocumentationService,
    BackgroundJobService,
    CacheService,
    DataPipelineService,
    WebSocketService,
)
from app.utils.exceptions import NotFoundError


def _naive_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


@pytest.fixture
def platform_admin(reference_data, reset_test_database):
    """User 1 holds the platform admin role; returns their bearer headers."""
    from sqlalchemy.orm import Session

    from app.models.user import Role, user_roles

    with Session(reset_test_database) as session:
        role = Role(name="admin", description="Administrator")
        session.add(role)
        session.flush()
        session.execute(user_roles.insert().values(user_id=1, role_id=role.id))
        session.commit()
        email = session.get(User, 1).email
    token = create_access_token({"sub": email, "user_id": 1})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def pipeline(session):
    return await DataPipelineService(session).create_pipeline("Nightly export", "postgres", "s3", {"bucket": "b"})


@pytest.fixture
async def documentation(session):
    return await APIDocumentationService(session).create_documentation("Public API", DocumentationFormat.OPENAPI3, {"openapi": "3.0.0"})


class TestWebSocketService:
    async def test_register_connection(self, session):
        service = WebSocketService(session)
        connection = await service.register_connection(1, "conn-1", ["all"], ip_address="10.0.0.1", user_agent="ua")
        assert connection.user_id == 1
        assert connection.connection_id == "conn-1"
        assert "conn-1" in service.active_connections[1]

    async def test_unregister_connection(self, session):
        service = WebSocketService(session)
        await service.register_connection(1, "conn-2", ["all"])
        assert await service.unregister_connection("conn-2") is True
        stored = await service._connection("conn-2")
        assert stored.status == WebSocketConnectionStatus.DISCONNECTED
        assert stored.disconnected_at is not None
        assert "conn-2" not in service.active_connections[1]
        assert await service.unregister_connection("missing") is False

    async def test_heartbeat(self, session):
        service = WebSocketService(session)
        await service.register_connection(1, "conn-3", ["all"])
        assert await service.heartbeat("conn-3") is True
        assert (await service._connection("conn-3")).last_heartbeat is not None
        assert await service.heartbeat("missing") is False

    async def test_broadcast_event_is_stored(self, session):
        event = await WebSocketService(session).broadcast_event("alert", "system", [1, 2], {"msg": "hi"}, priority=3)
        stored = await session.get(RealtimeEvent, event.id)
        assert stored.user_ids == [1, 2]
        assert stored.payload == {"msg": "hi"}
        assert stored.priority == 3

    async def test_recent_events_are_newest_first(self, session):
        service = WebSocketService(session)
        first = await service.broadcast_event("a", "src", [1], {})
        second = await service.broadcast_event("b", "src", [1], {})
        assert [e.id for e in await service.list_recent_events(10)] == [second.id, first.id]

    async def test_presence_counts_online_and_idle(self, session):
        service = WebSocketService(session)
        await service.register_connection(1, "fresh", ["all"])
        await service.register_connection(2, "stale", ["all"])
        stale = await service._connection("stale")
        stale.last_heartbeat = _naive_utc() - timedelta(hours=1)
        await session.commit()
        presence = await service.presence(_naive_utc(), timedelta(minutes=5))
        assert presence == {"online": 2, "idle": 1}

    async def test_publish_event_marks_it_published(self, session):
        service = WebSocketService(session)
        event = await service.broadcast_event("a", "src", [1], {})
        published = await service.publish_event(event.id)
        assert published.status == "published"
        assert published.published_at is not None
        assert await service.publish_event(999999) is None

    async def test_connections_for_user_only_lists_connected_sockets(self, session):
        service = WebSocketService(session)
        await service.register_connection(1, "live", ["all"])
        await service.register_connection(1, "gone", ["all"])
        await service.unregister_connection("gone")
        connections = await service.get_connections_for_user(1)
        assert [c.connection_id for c in connections] == ["live"]


class TestBackgroundJobService:
    async def test_create_job(self, session):
        job = await BackgroundJobService(session).create_job("email", {"to": "a@example.com"}, user_id=1, priority=2)
        stored = await session.get(BackgroundJob, job.id)
        assert stored.status == JobStatus.PENDING
        assert stored.user_id == 1
        assert stored.priority == 2

    async def test_pending_jobs_skip_future_and_running_jobs(self, session):
        service = BackgroundJobService(session)
        low = await service.create_job("low", {}, priority=1)
        high = await service.create_job("high", {}, priority=9)
        await service.create_job("later", {}, scheduled_at=_naive_utc() + timedelta(days=1))
        running = await service.create_job("running", {})
        await service.start_job(running.id)
        pending = await service.get_pending_jobs(limit=10)
        assert [j.id for j in pending] == [high.id, low.id]

    async def test_pending_jobs_can_be_limited_to_one_user(self, session):
        service = BackgroundJobService(session)
        mine = await service.create_job("mine", {}, user_id=1)
        await service.create_job("theirs", {}, user_id=2)
        assert [j.id for j in await service.get_pending_jobs(10, user_id=1)] == [mine.id]

    async def test_start_and_complete_job(self, session):
        service = BackgroundJobService(session)
        job = await service.create_job("report", {})
        started = await service.start_job(job.id)
        assert started.status == JobStatus.RUNNING and started.started_at is not None
        completed = await service.complete_job(job.id, {"rows": 5})
        assert completed.status == JobStatus.COMPLETED
        assert completed.result == {"rows": 5}
        assert await service.start_job(999999) is None
        assert await service.complete_job(999999) is None

    async def test_failed_job_is_retried_until_its_limit(self, session):
        service = BackgroundJobService(session)
        job = await service.create_job("flaky", {})
        first = await service.fail_job(job.id, "timeout")
        assert first.status == JobStatus.PENDING
        assert first.retry_count == 1
        assert first.scheduled_at > _naive_utc()
        assert first.error_message == "timeout"
        for _ in range(first.max_retries - 1):
            await service.fail_job(job.id, "timeout")
        final = await session.get(BackgroundJob, job.id)
        assert final.status == JobStatus.FAILED
        assert final.completed_at is not None
        assert await service.fail_job(999999, "x") is None

    async def test_create_schedule(self, session):
        schedule = await BackgroundJobService(session).create_schedule("sync", "0 * * * *", description="hourly")
        assert schedule.id is not None
        assert schedule.payload == {}


class TestDataPipelineService:
    async def test_create_pipeline(self, session):
        pipeline = await DataPipelineService(session).create_pipeline("Import", "csv", "postgres", {"path": "/tmp/x"})
        assert pipeline.id is not None
        assert pipeline.transformation_rules == {}

    async def test_activate_pipeline(self, session, pipeline):
        activated = await DataPipelineService(session).activate_pipeline(pipeline.id)
        assert activated.is_active is True
        assert activated.status == "active"
        assert await DataPipelineService(session).activate_pipeline(999999) is None

    async def test_execute_pipeline_records_a_run(self, session, pipeline):
        execution = await DataPipelineService(session).execute_pipeline(pipeline.id)
        assert execution.status == "running"
        await session.refresh(pipeline)
        assert pipeline.last_run is not None

    async def test_execute_unknown_pipeline_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await DataPipelineService(session).execute_pipeline(999999)

    async def test_complete_execution_marks_success(self, session, pipeline):
        service = DataPipelineService(session)
        execution = await service.execute_pipeline(pipeline.id)
        completed = await service.complete_execution(execution.id, records_processed=10, records_failed=1, execution_time_ms=250)
        assert completed.status == "success"
        assert completed.records_processed == 10
        await session.refresh(pipeline)
        assert pipeline.last_success is not None
        assert await service.complete_execution(999999, records_processed=0) is None

    async def test_add_pipeline_stage_and_list_in_order(self, session, pipeline):
        service = DataPipelineService(session)
        await service.add_pipeline_stage(pipeline.id, "load", 2, "sink", {})
        await service.add_pipeline_stage(pipeline.id, "extract", 1, "source", {})
        stages = await service.get_pipeline_stages(pipeline.id)
        assert [s.stage_name for s in stages] == ["extract", "load"]

    async def test_stage_for_unknown_pipeline_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await DataPipelineService(session).add_pipeline_stage(999999, "x", 1, "source", {})

    async def test_pipelines_list_most_recently_run_first(self, session):
        service = DataPipelineService(session)
        older = await service.create_pipeline("Older", "a", "b", {})
        newer = await service.create_pipeline("Newer", "a", "b", {})
        await service.execute_pipeline(older.id)
        await service.execute_pipeline(newer.id)
        await service.execute_pipeline(older.id)
        names = [p.name for p in await service.list_pipelines()]
        assert names[0] == "Older"


class TestCacheService:
    async def test_set_cache_records_its_size(self, session):
        entry = await CacheService(session).set_cache("k1", {"a": 1}, ttl_seconds=60)
        assert entry.size_bytes == len(b'{"a": 1}')
        assert entry.expires_at is not None
        assert entry.strategy == CacheStrategy.TTL

    async def test_get_cache_counts_hits_and_misses(self, session):
        service = CacheService(session)
        await service.set_cache("k2", {"v": "x"})
        assert await service.get_cache("k2") == {"v": "x"}
        assert await service.get_cache("absent") is None
        metrics = await service.get_cache_metrics()
        assert metrics["total_requests"] == 2
        assert metrics["total_hits"] == 1
        assert metrics["total_misses"] == 1

    async def test_expired_entry_is_removed_on_read(self, session):
        service = CacheService(session)
        entry = await service.set_cache("stale", {"v": 1}, ttl_seconds=60)
        entry.expires_at = _naive_utc() - timedelta(seconds=1)
        await session.commit()
        assert await service.get_cache("stale") is None
        assert await session.get(CacheEntry, entry.id) is None

    async def test_invalidate_cache(self, session):
        service = CacheService(session)
        await service.set_cache("k3", {"v": 3})
        assert await service.invalidate_cache("k3") is True
        assert await service.invalidate_cache("k3") is False
        assert "k3" not in service.local_cache

    async def test_summary_reports_entries_hits_and_memory(self, session):
        service = CacheService(session)
        await service.set_cache("s1", {"a": 1})
        await service.get_cache("s1")
        summary = await service.cache_summary()
        assert summary["entries"] == 1
        assert summary["total_hits"] == 1
        assert summary["memory_usage_mb"] >= 0


class TestAPIDocumentationService:
    async def test_create_documentation(self, session):
        doc = await APIDocumentationService(session).create_documentation(
            "Partner API", DocumentationFormat.SWAGGER2, {"swagger": "2.0"}, servers=["https://api.example.com"],
        )
        assert doc.format == DocumentationFormat.SWAGGER2
        assert doc.servers == ["https://api.example.com"]

    async def test_add_endpoint_and_list_them(self, session, documentation):
        service = APIDocumentationService(session)
        await service.add_endpoint(documentation.id, "/posts", "GET", summary="List posts")
        endpoints = await service.get_endpoints(documentation.id)
        assert [(e.path, e.method) for e in endpoints] == [("/posts", "GET")]
        assert (await service.get_documentation(documentation.id)).name == "Public API"

    async def test_endpoint_for_unknown_documentation_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await APIDocumentationService(session).add_endpoint(999999, "/x", "GET")

    async def test_record_usage_for_a_new_endpoint(self, session):
        metrics = await APIDocumentationService(session).record_usage("/posts", "GET", 120.0)
        assert metrics.call_count == 1
        assert metrics.error_count == 0
        assert metrics.average_response_time_ms == 120.0
        assert metrics.max_response_time_ms == 120.0
        assert metrics.min_response_time_ms == 120.0

    async def test_record_usage_accumulates_averages_and_errors(self, session):
        service = APIDocumentationService(session)
        await service.record_usage("/posts", "GET", 100.0)
        metrics = await service.record_usage("/posts", "GET", 300.0, is_error=True)
        assert metrics.call_count == 2
        assert metrics.error_count == 1
        assert metrics.average_response_time_ms == 200.0
        assert metrics.max_response_time_ms == 300.0
        assert metrics.min_response_time_ms == 100.0

    async def test_usage_listing_and_lookup(self, session):
        service = APIDocumentationService(session)
        await service.record_usage("/a", "GET", 10.0)
        await service.record_usage("/b", "POST", 10.0)
        await service.record_usage("/b", "POST", 10.0)
        listed = await service.list_usage()
        assert listed[0].endpoint == "/b"
        assert [m.method for m in await service.get_usage("/a")] == ["GET"]


class TestAdvancedPlatformRoutes:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/jobs/pending")).status_code == 401

    async def test_users_queue_jobs_for_themselves_only(self, async_client, platform_admin, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post(
            "/api/v1/jobs/create", json={"job_type": "export", "payload": {}, "user_id": 1}, headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["user_id"] == 2

    async def test_pending_jobs_are_scoped_to_the_caller_unless_administrator(
        self, async_client, platform_admin, reference_data, session,
    ):
        await BackgroundJobService(session).create_job("mine", {}, user_id=2)
        await BackgroundJobService(session).create_job("theirs", {}, user_id=1)
        customer = await async_client.get("/api/v1/jobs/pending", headers=await _headers_for(session, 2))
        admin = await async_client.get("/api/v1/jobs/pending", headers=platform_admin)
        assert [row["job_type"] for row in customer.json()] == ["mine"]
        assert len(admin.json()) == 2

    @pytest.mark.parametrize("method, path, body", [
        ("post", "/api/v1/websocket/broadcast", {"event_type": "x", "event_source": "y", "user_ids": [1], "payload": {}}),
        ("get", "/api/v1/websocket/events", None),
        ("post", "/api/v1/jobs/1/start", None),
        ("post", "/api/v1/jobs/1/complete", None),
        ("post", "/api/v1/jobs/schedules", {"job_type": "x", "cron_expression": "* * * * *"}),
        ("post", "/api/v1/pipelines/", {"name": "p", "source_type": "a", "destination_type": "b", "config": {}}),
        ("post", "/api/v1/pipelines/1/activate", None),
        ("post", "/api/v1/pipelines/1/execute", None),
        ("post", "/api/v1/pipelines/1/stages?stage_name=s&stage_order=1&stage_type=t", {}),
        ("delete", "/api/v1/cache/invalidate/k", None),
        ("post", "/api/v1/api-docs/", {"name": "d", "format": "openapi3", "spec": {}}),
        ("post", "/api/v1/api-docs/1/endpoints", {"path": "/x", "method": "GET"}),
        ("post", "/api/v1/api-docs/usage/record?endpoint=/x&method=GET&response_time_ms=1", None),
    ])
    async def test_platform_operations_are_for_administrators(
        self, async_client, reference_data, session, method, path, body,
    ):
        headers = await _headers_for(session, 2)
        kwargs = {"headers": headers}
        if body is not None:
            kwargs["json"] = body
        response = await getattr(async_client, method)(path, **kwargs)
        assert response.status_code == 403

    async def test_administrator_runs_a_pipeline_through_the_routes(self, async_client, platform_admin, reference_data, session):
        created = await async_client.post("/api/v1/pipelines/", json={
            "name": "Routed", "source_type": "api", "destination_type": "warehouse", "config": {},
        }, headers=platform_admin)
        assert created.status_code == 201
        pipeline_id = created.json()["id"]
        assert (await async_client.post(f"/api/v1/pipelines/{pipeline_id}/activate", headers=platform_admin)).status_code == 200
        run = await async_client.post(f"/api/v1/pipelines/{pipeline_id}/execute", headers=platform_admin)
        assert run.status_code == 200
        assert run.json()["status"] == "running"
        listed = await async_client.get("/api/v1/pipelines/", headers=await _headers_for(session, 2))
        assert [p["name"] for p in listed.json()] == ["Routed"]

    async def test_pipeline_execution_for_unknown_pipeline_is_not_found(self, async_client, platform_admin, reference_data):
        response = await async_client.post("/api/v1/pipelines/999999/execute", headers=platform_admin)
        assert response.status_code == 404

    async def test_cache_round_trip_through_the_routes(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        stored = await async_client.post("/api/v1/cache/set", json={"cache_key": "home", "cache_value": {"x": 1}}, headers=headers)
        assert stored.status_code == 200
        assert stored.json()["cache_key"] == "home"
        assert (await async_client.get("/api/v1/cache/get/home", headers=headers)).json() == {"x": 1}
        assert (await async_client.get("/api/v1/cache-summary", headers=headers)).json()["entries"] == 1
        assert (await async_client.get("/api/v1/cache-metrics", headers=headers)).status_code == 200

    async def test_api_documentation_is_readable_by_signed_in_users(self, async_client, platform_admin, reference_data, session):
        created = await async_client.post("/api/v1/api-docs/", json={
            "name": "Docs", "format": "openapi3", "spec": {"openapi": "3.0.0"},
        }, headers=platform_admin)
        assert created.status_code == 201
        doc_id = created.json()["id"]
        customer = await _headers_for(session, 2)
        assert (await async_client.get(f"/api/v1/api-docs/{doc_id}", headers=customer)).json()["name"] == "Docs"
        assert (await async_client.get(f"/api/v1/api-docs/{doc_id}/endpoints", headers=customer)).json() == []
        assert (await async_client.get("/api/v1/api-docs/999999", headers=customer)).status_code == 404

    async def test_invalid_cache_strategy_is_refused(self, async_client, reference_data, session):
        response = await async_client.post("/api/v1/cache/set", json={
            "cache_key": "bad", "cache_value": {}, "strategy": "nonsense",
        }, headers=await _headers_for(session, 2))
        assert response.status_code == 422

    async def test_presence_is_readable_by_signed_in_users(self, async_client, reference_data, session):
        response = await async_client.get("/api/v1/websocket/presence", headers=await _headers_for(session, 2))
        assert response.status_code == 200
        assert set(response.json()) == {"online", "idle"}


class TestRealtimeSocketAuthentication:
    """The socket refuses connections without a token that belongs to the path user, before it accepts them."""

    def test_socket_without_a_token_is_refused(self, client):
        with pytest.raises(StarletteWebSocketDisconnect) as info:
            with client.websocket_connect("/api/v1/websocket/ws/2/conn-x") as socket:
                socket.receive_json()
        assert info.value.code == 1008

    def test_token_for_another_user_is_refused(self, client):
        token = create_access_token({"sub": "other@example.com", "user_id": 1})
        with pytest.raises(StarletteWebSocketDisconnect) as info:
            with client.websocket_connect(f"/api/v1/websocket/ws/2/conn-y?token={token}") as socket:
                socket.receive_json()
        assert info.value.code == 1008

    def test_garbage_token_is_refused(self, client):
        with pytest.raises(StarletteWebSocketDisconnect) as info:
            with client.websocket_connect("/api/v1/websocket/ws/2/conn-z?token=not-a-jwt") as socket:
                socket.receive_json()
        assert info.value.code == 1008
