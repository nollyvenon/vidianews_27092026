import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from app.models.advanced_platform import (
    WebSocketConnection, RealtimeEvent, BackgroundJob, JobSchedule,
    DataPipeline, PipelineExecution, CacheEntry, CacheMetrics,
    APIDocumentation, APIEndpoint, APIUsageMetrics,
    WebSocketConnectionStatus, JobStatus
)
from app.services.advanced_platform_service import (
    WebSocketService, BackgroundJobService, DataPipelineService,
    CacheService, APIDocumentationService
)


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def websocket_service(mock_db):
    return WebSocketService(mock_db)


@pytest.fixture
def job_service(mock_db):
    return BackgroundJobService(mock_db)


@pytest.fixture
def pipeline_service(mock_db):
    return DataPipelineService(mock_db)


@pytest.fixture
def cache_service(mock_db):
    return CacheService(mock_db)


@pytest.fixture
def api_service(mock_db):
    return APIDocumentationService(mock_db)


# WebSocket Tests
@pytest.mark.asyncio
async def test_register_connection(websocket_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    connection = await websocket_service.register_connection(
        user_id=123,
        connection_id="conn123",
        subscriptions=["all"],
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_unregister_connection(websocket_service, mock_db):
    mock_conn = Mock(spec=WebSocketConnection)
    mock_conn.user_id = 123
    mock_conn.status = WebSocketConnectionStatus.CONNECTED

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_conn
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await websocket_service.unregister_connection("conn123")

    assert result is True
    assert mock_conn.status == WebSocketConnectionStatus.DISCONNECTED


@pytest.mark.asyncio
async def test_heartbeat(websocket_service, mock_db):
    mock_conn = Mock(spec=WebSocketConnection)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_conn
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await websocket_service.heartbeat("conn123")

    assert result is True
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_broadcast_event(websocket_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    event = await websocket_service.broadcast_event(
        event_type="update",
        event_source="system",
        user_ids=[123, 456],
        payload={"data": "test"},
    )

    mock_db.add.assert_called_once()


# Background Job Tests
@pytest.mark.asyncio
async def test_create_job(job_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    job = await job_service.create_job(
        job_type="email",
        payload={"email": "test@example.com"},
        user_id=123,
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_pending_jobs(job_service, mock_db):
    mock_jobs = [
        Mock(id=1, status=JobStatus.PENDING),
        Mock(id=2, status=JobStatus.PENDING),
    ]
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_jobs
    mock_db.query.return_value = mock_query

    jobs = await job_service.get_pending_jobs()

    assert len(jobs) == 2


@pytest.mark.asyncio
async def test_start_job(job_service, mock_db):
    mock_job = Mock(spec=BackgroundJob)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_job
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await job_service.start_job(1)

    assert result is not None
    assert result.status == JobStatus.RUNNING


@pytest.mark.asyncio
async def test_complete_job(job_service, mock_db):
    mock_job = Mock(spec=BackgroundJob)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_job
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await job_service.complete_job(1, {"result": "success"})

    assert result is not None
    assert result.status == JobStatus.COMPLETED


@pytest.mark.asyncio
async def test_fail_job(job_service, mock_db):
    mock_job = Mock(spec=BackgroundJob)
    mock_job.retry_count = 0
    mock_job.max_retries = 3
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_job
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await job_service.fail_job(1, "Connection timeout")

    assert result is not None


# Data Pipeline Tests
@pytest.mark.asyncio
async def test_create_pipeline(pipeline_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    pipeline = await pipeline_service.create_pipeline(
        name="user_sync",
        source_type="database",
        destination_type="warehouse",
        config={"source": "prod_db"},
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_activate_pipeline(pipeline_service, mock_db):
    mock_pipeline = Mock(spec=DataPipeline)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_pipeline
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await pipeline_service.activate_pipeline(1)

    assert result is not None
    assert result.is_active is True


@pytest.mark.asyncio
async def test_execute_pipeline(pipeline_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    execution = await pipeline_service.execute_pipeline(1)

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_add_pipeline_stage(pipeline_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    stage = await pipeline_service.add_pipeline_stage(
        pipeline_id=1,
        stage_name="extract",
        stage_order=1,
        stage_type="source",
        config={"query": "SELECT * FROM users"},
    )

    mock_db.add.assert_called_once()


# Cache Tests
@pytest.mark.asyncio
async def test_set_cache(cache_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    entry = await cache_service.set_cache(
        cache_key="user:123",
        cache_value={"id": 123, "name": "John"},
        ttl_seconds=3600,
    )

    mock_db.add.assert_called_once()
    assert "user:123" in cache_service.local_cache


@pytest.mark.asyncio
async def test_get_cache(cache_service, mock_db):
    cache_service.local_cache["user:123"] = {"id": 123}

    mock_entry = Mock(spec=CacheEntry)
    mock_entry.cache_value = {"id": 123}
    mock_entry.expires_at = None
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_entry
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await cache_service.get_cache("user:123")

    assert result == {"id": 123}


@pytest.mark.asyncio
async def test_invalidate_cache(cache_service, mock_db):
    cache_service.local_cache["user:123"] = {"id": 123}

    mock_entry = Mock(spec=CacheEntry)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_entry
    mock_db.query.return_value = mock_query
    mock_db.delete = Mock()
    mock_db.commit = Mock()

    result = await cache_service.invalidate_cache("user:123")

    assert result is True
    assert "user:123" not in cache_service.local_cache


# API Documentation Tests
@pytest.mark.asyncio
async def test_create_documentation(api_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    doc = await api_service.create_documentation(
        name="Vidi API",
        format="openapi3",
        spec={"openapi": "3.0.0"},
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_add_endpoint(api_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    endpoint = await api_service.add_endpoint(
        doc_id=1,
        path="/users/{id}",
        method="GET",
        summary="Get user by ID",
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_record_usage(api_service, mock_db):
    mock_metrics = Mock(spec=APIUsageMetrics)
    mock_metrics.call_count = 0
    mock_metrics.error_count = 0
    mock_metrics.average_response_time_ms = 0
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_metrics
    mock_db.query.return_value = mock_query
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await api_service.record_usage(
        endpoint="/users",
        method="GET",
        response_time_ms=125.5,
    )

    assert result is not None
