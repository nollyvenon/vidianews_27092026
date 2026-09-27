from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.services.advanced_platform_service import (
    WebSocketService, BackgroundJobService, DataPipelineService,
    CacheService, APIDocumentationService
)


# Pydantic Schemas
class WebSocketConnectionResponse(BaseModel):
    id: int
    user_id: int
    connection_id: str
    status: str
    event_subscriptions: List[str]
    connected_at: datetime

    class Config:
        from_attributes = True


class RealtimeEventRequest(BaseModel):
    event_type: str
    event_source: str
    user_ids: List[int]
    payload: dict
    priority: int = 0


class RealtimeEventResponse(BaseModel):
    id: int
    event_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class BackgroundJobRequest(BaseModel):
    job_type: str
    payload: dict
    user_id: Optional[int] = None
    priority: int = 0


class BackgroundJobResponse(BaseModel):
    id: int
    job_type: str
    status: str
    user_id: Optional[int]
    priority: int
    created_at: datetime

    class Config:
        from_attributes = True


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
    id: int
    name: str
    source_type: str
    destination_type: str
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PipelineExecutionResponse(BaseModel):
    id: int
    pipeline_id: int
    status: str
    records_processed: int
    records_failed: int
    started_at: datetime

    class Config:
        from_attributes = True


class CacheEntryRequest(BaseModel):
    cache_key: str
    cache_value: dict
    ttl_seconds: Optional[int] = None
    strategy: str = "ttl"


class CacheEntryResponse(BaseModel):
    cache_key: str
    hit_count: int
    size_bytes: int
    created_at: datetime

    class Config:
        from_attributes = True


class CacheMetricsResponse(BaseModel):
    total_requests: int
    total_hits: int
    total_misses: int
    average_response_time_ms: float
    memory_usage_mb: float

    class Config:
        from_attributes = True


class APIDocumentationRequest(BaseModel):
    name: str
    format: str
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
    endpoint: str
    method: str
    call_count: int
    error_count: int
    average_response_time_ms: float
    measured_at: datetime

    class Config:
        from_attributes = True


# Routers
websocket_router = APIRouter(prefix="/websocket", tags=["websocket"])
jobs_router = APIRouter(prefix="/jobs", tags=["background-jobs"])
pipeline_router = APIRouter(prefix="/pipelines", tags=["data-pipeline"])
cache_router = APIRouter(prefix="/cache", tags=["caching"])
api_docs_router = APIRouter(prefix="/api-docs", tags=["api-documentation"])


# WebSocket Endpoints
@websocket_router.websocket("/ws/{user_id}/{connection_id}")
async def websocket_endpoint(
    user_id: int,
    connection_id: str,
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
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


@websocket_router.post("/broadcast", response_model=RealtimeEventResponse)
async def broadcast_event(
    req: RealtimeEventRequest,
    db: Session = Depends(get_db),
):
    service = WebSocketService(db)
    event = await service.broadcast_event(
        req.event_type,
        req.event_source,
        req.user_ids,
        req.payload,
        req.priority,
    )
    return event


# Background Job Endpoints
@jobs_router.post("/create", response_model=BackgroundJobResponse)
async def create_job(
    req: BackgroundJobRequest,
    db: Session = Depends(get_db),
):
    service = BackgroundJobService(db)
    job = await service.create_job(
        req.job_type,
        req.payload,
        req.user_id,
        req.priority,
    )
    return job


@jobs_router.get("/pending", response_model=List[BackgroundJobResponse])
async def get_pending_jobs(
    limit: int = Query(50),
    db: Session = Depends(get_db),
):
    service = BackgroundJobService(db)
    jobs = await service.get_pending_jobs(limit)
    return jobs


@jobs_router.post("/{job_id}/start")
async def start_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    service = BackgroundJobService(db)
    job = await service.start_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "started", "job_id": job_id}


@jobs_router.post("/{job_id}/complete")
async def complete_job(
    job_id: int,
    result: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    service = BackgroundJobService(db)
    job = await service.complete_job(job_id, result)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "completed", "job_id": job_id}


@jobs_router.post("/schedules", response_model=dict)
async def create_schedule(
    req: JobScheduleRequest,
    db: Session = Depends(get_db),
):
    service = BackgroundJobService(db)
    schedule = await service.create_schedule(
        req.job_type,
        req.cron_expression,
        req.payload,
        req.description,
    )
    return {"id": schedule.id, "job_type": schedule.job_type}


# Data Pipeline Endpoints
@pipeline_router.post("/", response_model=PipelineResponse)
async def create_pipeline(
    req: PipelineRequest,
    db: Session = Depends(get_db),
):
    service = DataPipelineService(db)
    pipeline = await service.create_pipeline(
        req.name,
        req.source_type,
        req.destination_type,
        req.config,
        req.transformation_rules,
        req.schedule,
        req.description,
    )
    return pipeline


@pipeline_router.post("/{pipeline_id}/activate")
async def activate_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db),
):
    service = DataPipelineService(db)
    pipeline = await service.activate_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"activated": True, "pipeline_id": pipeline_id}


@pipeline_router.post("/{pipeline_id}/execute", response_model=PipelineExecutionResponse)
async def execute_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db),
):
    service = DataPipelineService(db)
    execution = await service.execute_pipeline(pipeline_id)
    return execution


@pipeline_router.post("/{pipeline_id}/stages", response_model=dict)
async def add_pipeline_stage(
    pipeline_id: int,
    stage_name: str,
    stage_order: int,
    stage_type: str,
    config: dict,
    db: Session = Depends(get_db),
):
    service = DataPipelineService(db)
    stage = await service.add_pipeline_stage(
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
    db: Session = Depends(get_db),
):
    service = CacheService(db)
    entry = await service.set_cache(
        req.cache_key,
        req.cache_value,
        req.ttl_seconds,
        req.strategy,
    )
    return entry


@cache_router.get("/get/{cache_key}", response_model=Optional[dict])
async def get_cache(
    cache_key: str,
    db: Session = Depends(get_db),
):
    service = CacheService(db)
    return await service.get_cache(cache_key)


@cache_router.delete("/invalidate/{cache_key}")
async def invalidate_cache(
    cache_key: str,
    db: Session = Depends(get_db),
):
    service = CacheService(db)
    success = await service.invalidate_cache(cache_key)
    if not success:
        raise HTTPException(status_code=404, detail="Cache entry not found")
    return {"invalidated": True}


@cache_router.get("/metrics", response_model=CacheMetricsResponse)
async def get_cache_metrics(
    db: Session = Depends(get_db),
):
    service = CacheService(db)
    return await service.get_cache_metrics()


# API Documentation Endpoints
@api_docs_router.post("/", response_model=dict)
async def create_documentation(
    req: APIDocumentationRequest,
    db: Session = Depends(get_db),
):
    service = APIDocumentationService(db)
    doc = await service.create_documentation(
        req.name,
        req.format,
        req.spec,
        req.version,
        req.description,
        req.base_path,
        req.servers,
    )
    return {"id": doc.id, "name": doc.name, "format": doc.format}


@api_docs_router.post("/{doc_id}/endpoints", response_model=dict)
async def add_endpoint(
    doc_id: int,
    req: APIEndpointRequest,
    db: Session = Depends(get_db),
):
    service = APIDocumentationService(db)
    endpoint = await service.add_endpoint(
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


@api_docs_router.get("/{doc_id}", response_model=dict)
async def get_documentation(
    doc_id: int,
    db: Session = Depends(get_db),
):
    service = APIDocumentationService(db)
    doc = await service.get_documentation(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documentation not found")
    return {
        "id": doc.id,
        "name": doc.name,
        "format": doc.format,
        "version": doc.version,
    }


@api_docs_router.get("/{doc_id}/endpoints", response_model=List[dict])
async def get_endpoints(
    doc_id: int,
    db: Session = Depends(get_db),
):
    service = APIDocumentationService(db)
    endpoints = await service.get_endpoints(doc_id)
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
    db: Session = Depends(get_db),
):
    service = APIDocumentationService(db)
    metrics = await service.record_usage(endpoint, method, response_time_ms, is_error)
    return {"endpoint": endpoint, "call_count": metrics.call_count}


@api_docs_router.get("/usage/{endpoint}", response_model=List[APIUsageMetricsResponse])
async def get_usage_metrics(
    endpoint: str,
    db: Session = Depends(get_db),
):
    from app.models.advanced_platform import APIUsageMetrics
    metrics = db.query(APIUsageMetrics).filter(
        APIUsageMetrics.endpoint == endpoint
    ).all()
    return metrics
