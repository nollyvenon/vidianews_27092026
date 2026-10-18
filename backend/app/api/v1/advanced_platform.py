"""Advanced platform endpoints: realtime sockets, background jobs, data pipelines, cache and API documentation (async).

Access rules:
- Operating the platform (broadcasting realtime events, starting or completing jobs, scheduling, creating and running
  pipelines, invalidating cache entries, publishing API documentation) requires platform administrator access.
- Reads that expose one user's data are scoped: a user sees their own jobs, and only administrators see the
  realtime event stream.
- The realtime socket authenticates with the bearer token passed as ``token`` and must belong to the user in the path.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import is_admin, require_admin
from app.core.security import decode_token, get_current_user
from app.db.session import get_db
from app.models.advanced_platform import CacheStrategy, DocumentationFormat
from app.models.user import User
from app.services.advanced_platform_service import (
    APIDocumentationService,
    BackgroundJobService,
    CacheService,
    DataPipelineService,
    WebSocketService,
)
from app.utils.exceptions import NotFoundError

require_platform_admin = require_admin("platform")


def _utcnow() -> datetime:
    """Naive UTC, matching the naive DateTime columns"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Pydantic Schemas
class WebSocketConnectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    connection_id: str
    status: str
    event_subscriptions: List[str]
    connected_at: datetime


class RealtimeEventRequest(BaseModel):
    event_type: str
    event_source: str
    user_ids: List[int]
    payload: dict
    priority: int = 0


class RealtimeEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_type: str
    status: str
    created_at: datetime


class BackgroundJobRequest(BaseModel):
    job_type: str
    payload: dict
    user_id: Optional[int] = None
    priority: int = 0


class BackgroundJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    status: str
    user_id: Optional[int]
    priority: int
    created_at: datetime


class JobScheduleRequest(BaseModel):
    job_type: str
    cron_expression: str
    payload: Optional[dict] = None
    description: Optional[str] = None


class PipelineRequest(BaseModel):
    name: str
    source_type: str
    destination_type: str
    config: dict
    transformation_rules: Optional[dict] = None
    schedule: Optional[str] = None
    description: Optional[str] = None


class PipelineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    source_type: str
    destination_type: str
    status: str
    is_active: bool
    created_at: datetime


class PipelineExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pipeline_id: int
    status: str
    records_processed: int
    records_failed: int
    started_at: datetime


class CacheEntryRequest(BaseModel):
    cache_key: str
    cache_value: dict
    ttl_seconds: Optional[int] = None
    strategy: CacheStrategy = CacheStrategy.TTL


class CacheEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cache_key: str
    hit_count: int
    size_bytes: int
    created_at: datetime


class CacheMetricsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_requests: int
    total_hits: int
    total_misses: int
    average_response_time_ms: float
    memory_usage_mb: float


class APIDocumentationRequest(BaseModel):
    name: str
    format: DocumentationFormat
    spec: dict
    version: str = "1.0.0"
    description: Optional[str] = None
    base_path: Optional[str] = None
    servers: Optional[List[str]] = None


class APIEndpointRequest(BaseModel):
    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[dict] = None
    request_schema: Optional[dict] = None
    response_schema: Optional[dict] = None


class APIUsageMetricsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    endpoint: str
    method: str
    call_count: int
    error_count: int
    average_response_time_ms: float
    measured_at: datetime


# Routers
websocket_router = APIRouter(prefix="/websocket", tags=["websocket"])
jobs_router = APIRouter(prefix="/jobs", tags=["background-jobs"])
pipeline_router = APIRouter(prefix="/pipelines", tags=["data-pipeline"])
cache_router = APIRouter(prefix="/cache", tags=["caching"])
api_docs_router = APIRouter(prefix="/api-docs", tags=["api-documentation"])


async def _is_platform_admin(db: AsyncSession, user: User) -> bool:
    return await is_admin(db, user.id, "platform")


# WebSocket Endpoints
@websocket_router.websocket("/ws/{user_id}/{connection_id}")
async def websocket_endpoint(
    user_id: int,
    connection_id: str,
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Realtime socket. The bearer token in ``token`` must belong to ``user_id``."""
    claims = decode_token(token) if token else None
    if not claims or claims.get("user_id") != user_id or claims.get("type", "access") != "access":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    service = WebSocketService(db)

    try:
        await service.register_connection(
            user_id=user_id,
            connection_id=connection_id,
            subscriptions=["all"],
        )

        while True:
            data = await websocket.receive_json()

            if data.get("type") == "heartbeat":
                await service.heartbeat(connection_id)
                await websocket.send_json({"type": "heartbeat_ack"})
            elif data.get("type") == "subscribe":
                await websocket.send_json({"type": "subscribed"})

    except WebSocketDisconnect:
        await service.unregister_connection(connection_id)


PRESENCE_IDLE_AFTER = timedelta(minutes=5)


@websocket_router.get("/events")
async def list_realtime_events(
    limit: int = Query(50, ge=1, le=200),
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Recent realtime events, newest first (platform administrators only)"""
    events = await WebSocketService(db).list_recent_events(limit)
    return [
        {
            "id": event.id,
            "event_type": event.event_type,
            "event_source": event.event_source,
            "payload": event.payload,
            "priority": event.priority or 0,
            "status": event.status,
            "created_at": event.created_at.isoformat() if event.created_at else None,
        }
        for event in events
    ]


@websocket_router.get("/presence")
async def get_presence(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """How many sockets are connected, and how many of them have gone idle"""
    return await WebSocketService(db).presence(_utcnow(), PRESENCE_IDLE_AFTER)


@websocket_router.post("/broadcast", response_model=RealtimeEventResponse)
async def broadcast_event(
    req: RealtimeEventRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Publish a realtime event to the given users (platform administrators only)"""
    return await WebSocketService(db).broadcast_event(
        req.event_type,
        req.event_source,
        req.user_ids,
        req.payload,
        req.priority,
    )


# Background Job Endpoints
@jobs_router.post("/create", response_model=BackgroundJobResponse, status_code=201)
async def create_job(
    req: BackgroundJobRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Queue a job. Users queue jobs for themselves; administrators may queue for any user."""
    user_id = req.user_id if await _is_platform_admin(db, current_user) and req.user_id is not None else current_user.id
    return await BackgroundJobService(db).create_job(req.job_type, req.payload, user_id, req.priority)


@jobs_router.get("/pending", response_model=List[BackgroundJobResponse])
async def get_pending_jobs(
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Jobs ready to run. Users see their own; administrators see every user's."""
    scope = None if await _is_platform_admin(db, current_user) else current_user.id
    return await BackgroundJobService(db).get_pending_jobs(limit, scope)


@jobs_router.post("/{job_id}/start")
async def start_job(
    job_id: int,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Mark a job as running (platform administrators only)"""
    job = await BackgroundJobService(db).start_job(job_id)
    if not job:
        raise NotFoundError("Job")
    return {"status": "started", "job_id": job_id}


@jobs_router.post("/{job_id}/complete")
async def complete_job(
    job_id: int,
    result: Optional[dict] = None,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Mark a job as completed with its result (platform administrators only)"""
    job = await BackgroundJobService(db).complete_job(job_id, result)
    if not job:
        raise NotFoundError("Job")
    return {"status": "completed", "job_id": job_id}


@jobs_router.post("/schedules", response_model=dict, status_code=201)
async def create_schedule(
    req: JobScheduleRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Schedule a recurring job (platform administrators only)"""
    schedule = await BackgroundJobService(db).create_schedule(
        req.job_type,
        req.cron_expression,
        req.payload,
        req.description,
    )
    return {"id": schedule.id, "job_type": schedule.job_type}


# Data Pipeline Endpoints
@pipeline_router.get("/")
async def list_pipelines(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Every data pipeline with its state and run history"""
    return [
        {
            "id": pipeline.id,
            "name": pipeline.name,
            "source_type": pipeline.source_type,
            "destination_type": pipeline.destination_type,
            "status": pipeline.status,
            "is_active": bool(pipeline.is_active),
            "failure_count": pipeline.failure_count or 0,
            "last_run": pipeline.last_run.isoformat() if pipeline.last_run else None,
            "last_success": pipeline.last_success.isoformat() if pipeline.last_success else None,
        }
        for pipeline in await DataPipelineService(db).list_pipelines()
    ]


@pipeline_router.post("/", response_model=PipelineResponse, status_code=201)
async def create_pipeline(
    req: PipelineRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a data pipeline (platform administrators only)"""
    return await DataPipelineService(db).create_pipeline(
        req.name,
        req.source_type,
        req.destination_type,
        req.config,
        req.transformation_rules,
        req.schedule,
        req.description,
    )


@pipeline_router.post("/{pipeline_id}/activate")
async def activate_pipeline(
    pipeline_id: int,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Activate a data pipeline (platform administrators only)"""
    pipeline = await DataPipelineService(db).activate_pipeline(pipeline_id)
    if not pipeline:
        raise NotFoundError("Pipeline")
    return {"activated": True, "pipeline_id": pipeline_id}


@pipeline_router.post("/{pipeline_id}/execute", response_model=PipelineExecutionResponse)
async def execute_pipeline(
    pipeline_id: int,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Start a run of a data pipeline (platform administrators only)"""
    return await DataPipelineService(db).execute_pipeline(pipeline_id)


@pipeline_router.post("/{pipeline_id}/stages", response_model=dict, status_code=201)
async def add_pipeline_stage(
    pipeline_id: int,
    stage_name: str,
    stage_order: int,
    stage_type: str,
    config: dict,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Add a stage to a data pipeline (platform administrators only)"""
    stage = await DataPipelineService(db).add_pipeline_stage(
        pipeline_id,
        stage_name,
        stage_order,
        stage_type,
        config,
    )
    return {"id": stage.id, "stage_name": stage.stage_name}


# Cache Endpoints
@cache_router.post("/set", response_model=CacheEntryResponse)
async def set_cache(
    req: CacheEntryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Store a cache entry"""
    return await CacheService(db).set_cache(
        req.cache_key,
        req.cache_value,
        req.ttl_seconds,
        req.strategy,
    )


@cache_router.get("/get/{cache_key}", response_model=Optional[dict])
async def get_cache(
    cache_key: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Read a cache entry"""
    return await CacheService(db).get_cache(cache_key)


@cache_router.delete("/invalidate/{cache_key}")
async def invalidate_cache(
    cache_key: str,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Remove a cache entry (platform administrators only)"""
    if not await CacheService(db).invalidate_cache(cache_key):
        raise NotFoundError("Cache entry")
    return {"invalidated": True}


# Its own prefix: analytics_reporting mounts GET /cache/{cache_key} ahead of this module, which would shadow /cache/summary.
cache_summary_router = APIRouter(prefix="/cache-summary", tags=["caching"])


@cache_summary_router.get("")
async def get_cache_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cached entries, the hits they have served, and the memory they occupy. Read-only."""
    return await CacheService(db).cache_summary()


# Its own prefix: analytics_reporting mounts GET /cache/{cache_key} ahead of this module, which would shadow /cache/metrics.
cache_metrics_router = APIRouter(prefix="/cache-metrics", tags=["caching"])


@cache_metrics_router.get("", response_model=CacheMetricsResponse)
async def get_cache_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Recorded cache hits, misses and latency"""
    return await CacheService(db).get_cache_metrics()


# API Documentation Endpoints
@api_docs_router.post("/", response_model=dict, status_code=201)
async def create_documentation(
    req: APIDocumentationRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Publish an API documentation set (platform administrators only)"""
    doc = await APIDocumentationService(db).create_documentation(
        req.name,
        req.format,
        req.spec,
        req.version,
        req.description,
        req.base_path,
        req.servers,
    )
    return {"id": doc.id, "name": doc.name, "format": doc.format}


@api_docs_router.post("/{doc_id}/endpoints", response_model=dict, status_code=201)
async def add_endpoint(
    doc_id: int,
    req: APIEndpointRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Add an endpoint to an API documentation set (platform administrators only)"""
    endpoint = await APIDocumentationService(db).add_endpoint(
        doc_id,
        req.path,
        req.method,
        req.summary,
        req.description,
        req.parameters,
        req.request_schema,
        req.response_schema,
    )
    return {"id": endpoint.id, "path": endpoint.path, "method": endpoint.method}


@api_docs_router.get("/usage")
async def list_api_usage(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Call counts, errors and response times for every endpoint that has been measured"""
    return [
        {
            "id": row.id,
            "endpoint": row.endpoint,
            "method": row.method,
            "call_count": row.call_count or 0,
            "error_count": row.error_count or 0,
            "average_response_time_ms": round(row.average_response_time_ms or 0.0, 2),
        }
        for row in await APIDocumentationService(db).list_usage()
    ]


@api_docs_router.get("/{doc_id}", response_model=dict)
async def get_documentation(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    doc = await APIDocumentationService(db).get_documentation(doc_id)
    if not doc:
        raise NotFoundError("Documentation")
    return {
        "id": doc.id,
        "name": doc.name,
        "format": doc.format,
        "version": doc.version,
    }


@api_docs_router.get("/{doc_id}/endpoints", response_model=List[dict])
async def get_endpoints(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    endpoints = await APIDocumentationService(db).get_endpoints(doc_id)
    return [
        {"path": e.path, "method": e.method, "summary": e.summary}
        for e in endpoints
    ]


@api_docs_router.post("/usage/record")
async def record_api_usage(
    endpoint: str,
    method: str,
    response_time_ms: float,
    is_error: bool = False,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record one call of an endpoint (platform administrators only)"""
    metrics = await APIDocumentationService(db).record_usage(endpoint, method, response_time_ms, is_error)
    return {"endpoint": endpoint, "call_count": metrics.call_count}


@api_docs_router.get("/usage/{endpoint}", response_model=List[APIUsageMetricsResponse])
async def get_usage_metrics(
    endpoint: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await APIDocumentationService(db).get_usage(endpoint)
