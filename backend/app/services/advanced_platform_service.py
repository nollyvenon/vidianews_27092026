from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, timedelta
import json
import asyncio

from app.models.advanced_platform import (
    WebSocketConnection, RealtimeEvent, BackgroundJob, JobSchedule,
    DataPipeline, PipelineExecution, PipelineStage, CacheEntry, CacheMetrics,
    APIDocumentation, APIEndpoint, APIUsageMetrics,
    WebSocketConnectionStatus, JobStatus, PipelineStageStatus,
    CacheStrategy, DocumentationFormat
)


class WebSocketService:
    def __init__(self, db: Session):
        self.db = db
        self.active_connections: Dict[str, Set[str]] = {}

    async def register_connection(
        self,
        user_id: int,
        connection_id: str,
        subscriptions: List[str],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> WebSocketConnection:
        connection = WebSocketConnection(
            user_id=user_id,
            connection_id=connection_id,
            event_subscriptions=subscriptions,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(connection)
        self.db.commit()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(connection_id)

        return connection

    async def unregister_connection(self, connection_id: str) -> bool:
        connection = self.db.query(WebSocketConnection).filter(
            WebSocketConnection.connection_id == connection_id
        ).first()

        if connection:
            connection.status = WebSocketConnectionStatus.DISCONNECTED
            connection.disconnected_at = datetime.utcnow()
            self.db.commit()

            if connection.user_id in self.active_connections:
                self.active_connections[connection.user_id].discard(connection_id)

            return True
        return False

    async def heartbeat(self, connection_id: str) -> bool:
        connection = self.db.query(WebSocketConnection).filter(
            WebSocketConnection.connection_id == connection_id
        ).first()

        if connection:
            connection.last_heartbeat = datetime.utcnow()
            connection.status = WebSocketConnectionStatus.CONNECTED
            self.db.commit()
            return True
        return False

    async def get_connections_for_user(self, user_id: int) -> List[WebSocketConnection]:
        return self.db.query(WebSocketConnection).filter(
            WebSocketConnection.user_id == user_id,
            WebSocketConnection.status == WebSocketConnectionStatus.CONNECTED,
        ).all()

    async def broadcast_event(
        self,
        event_type: str,
        event_source: str,
        user_ids: List[int],
        payload: Dict[str, Any],
        priority: int = 0,
    ) -> RealtimeEvent:
        event = RealtimeEvent(
            event_type=event_type,
            event_source=event_source,
            user_ids=user_ids,
            payload=payload,
            priority=priority,
        )
        self.db.add(event)
        self.db.commit()
        return event

    async def publish_event(self, event_id: int) -> Optional[RealtimeEvent]:
        event = self.db.query(RealtimeEvent).filter(
            RealtimeEvent.id == event_id
        ).first()

        if event:
            event.status = "published"
            event.published_at = datetime.utcnow()
            self.db.commit()

        return event


class BackgroundJobService:
    def __init__(self, db: Session):
        self.db = db

    async def create_job(
        self,
        job_type: str,
        payload: Dict[str, Any],
        user_id: Optional[int] = None,
        priority: int = 0,
        scheduled_at: Optional[datetime] = None,
    ) -> BackgroundJob:
        job = BackgroundJob(
            job_type=job_type,
            payload=payload,
            user_id=user_id,
            priority=priority,
            scheduled_at=scheduled_at,
        )
        self.db.add(job)
        self.db.commit()
        return job

    async def get_pending_jobs(self, limit: int = 50) -> List[BackgroundJob]:
        now = datetime.utcnow()
        return self.db.query(BackgroundJob).filter(
            BackgroundJob.status == JobStatus.PENDING,
            (BackgroundJob.scheduled_at.is_(None)) |
            (BackgroundJob.scheduled_at <= now),
        ).order_by(BackgroundJob.priority.desc()).limit(limit).all()

    async def start_job(self, job_id: int) -> Optional[BackgroundJob]:
        job = self.db.query(BackgroundJob).filter(
            BackgroundJob.id == job_id
        ).first()

        if job:
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            self.db.commit()

        return job

    async def complete_job(
        self,
        job_id: int,
        result: Optional[Dict[str, Any]] = None,
    ) -> Optional[BackgroundJob]:
        job = self.db.query(BackgroundJob).filter(
            BackgroundJob.id == job_id
        ).first()

        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.result = result
            self.db.commit()

        return job

    async def fail_job(
        self,
        job_id: int,
        error_message: str,
    ) -> Optional[BackgroundJob]:
        job = self.db.query(BackgroundJob).filter(
            BackgroundJob.id == job_id
        ).first()

        if job:
            job.retry_count += 1
            if job.retry_count >= job.max_retries:
                job.status = JobStatus.FAILED
                job.completed_at = datetime.utcnow()
            else:
                job.status = JobStatus.PENDING
                job.scheduled_at = datetime.utcnow() + timedelta(minutes=5 * job.retry_count)

            job.error_message = error_message
            self.db.commit()

        return job

    async def create_schedule(
        self,
        job_type: str,
        cron_expression: str,
        payload: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> JobSchedule:
        schedule = JobSchedule(
            job_type=job_type,
            cron_expression=cron_expression,
            payload=payload or {},
            description=description,
        )
        self.db.add(schedule)
        self.db.commit()
        return schedule


class DataPipelineService:
    def __init__(self, db: Session):
        self.db = db

    async def create_pipeline(
        self,
        name: str,
        source_type: str,
        destination_type: str,
        config: Dict[str, Any],
        transformation_rules: Optional[Dict[str, Any]] = None,
        schedule: Optional[str] = None,
        description: Optional[str] = None,
    ) -> DataPipeline:
        pipeline = DataPipeline(
            name=name,
            source_type=source_type,
            destination_type=destination_type,
            config=config,
            transformation_rules=transformation_rules or {},
            schedule=schedule,
            description=description,
        )
        self.db.add(pipeline)
        self.db.commit()
        return pipeline

    async def activate_pipeline(self, pipeline_id: int) -> Optional[DataPipeline]:
        pipeline = self.db.query(DataPipeline).filter(
            DataPipeline.id == pipeline_id
        ).first()

        if pipeline:
            pipeline.is_active = True
            pipeline.status = "active"
            self.db.commit()

        return pipeline

    async def execute_pipeline(self, pipeline_id: int) -> PipelineExecution:
        pipeline = self.db.query(DataPipeline).filter(
            DataPipeline.id == pipeline_id
        ).first()

        execution = PipelineExecution(
            pipeline_id=pipeline_id,
            status="running",
        )
        self.db.add(execution)
        self.db.commit()

        return execution

    async def complete_execution(
        self,
        execution_id: int,
        records_processed: int,
        records_failed: int = 0,
        execution_time_ms: int = 0,
    ) -> Optional[PipelineExecution]:
        execution = self.db.query(PipelineExecution).filter(
            PipelineExecution.id == execution_id
        ).first()

        if execution:
            execution.status = "success"
            execution.completed_at = datetime.utcnow()
            execution.records_processed = records_processed
            execution.records_failed = records_failed
            execution.execution_time_ms = execution_time_ms
            self.db.commit()

        return execution

    async def add_pipeline_stage(
        self,
        pipeline_id: int,
        stage_name: str,
        stage_order: int,
        stage_type: str,
        config: Dict[str, Any],
    ) -> PipelineStage:
        stage = PipelineStage(
            pipeline_id=pipeline_id,
            stage_name=stage_name,
            stage_order=stage_order,
            stage_type=stage_type,
            config=config,
        )
        self.db.add(stage)
        self.db.commit()
        return stage

    async def get_pipeline_stages(self, pipeline_id: int) -> List[PipelineStage]:
        return self.db.query(PipelineStage).filter(
            PipelineStage.pipeline_id == pipeline_id
        ).order_by(PipelineStage.stage_order).all()


class CacheService:
    def __init__(self, db: Session):
        self.db = db
        self.local_cache: Dict[str, Any] = {}

    async def set_cache(
        self,
        cache_key: str,
        cache_value: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
        strategy: CacheStrategy = CacheStrategy.TTL,
    ) -> CacheEntry:
        expires_at = None
        if ttl_seconds:
            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

        entry = CacheEntry(
            cache_key=cache_key,
            cache_value=cache_value,
            ttl_seconds=ttl_seconds,
            strategy=strategy,
            expires_at=expires_at,
            size_bytes=len(json.dumps(cache_value).encode()),
        )
        self.db.add(entry)
        self.db.commit()

        self.local_cache[cache_key] = cache_value

        return entry

    async def get_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        if cache_key in self.local_cache:
            entry = self.db.query(CacheEntry).filter(
                CacheEntry.cache_key == cache_key
            ).first()
            if entry:
                entry.hit_count += 1
                self.db.commit()
            return self.local_cache[cache_key]

        entry = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key == cache_key
        ).first()

        if entry:
            if entry.expires_at and entry.expires_at < datetime.utcnow():
                self.db.delete(entry)
                self.db.commit()
                return None

            entry.hit_count += 1
            self.db.commit()
            self.local_cache[cache_key] = entry.cache_value
            return entry.cache_value

        return None

    async def invalidate_cache(self, cache_key: str) -> bool:
        self.local_cache.pop(cache_key, None)
        entry = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key == cache_key
        ).first()

        if entry:
            self.db.delete(entry)
            self.db.commit()
            return True

        return False

    async def get_cache_metrics(self) -> CacheMetrics:
        entries = self.db.query(CacheEntry).all()
        total_hits = sum(e.hit_count for e in entries)
        total_size = sum(e.size_bytes or 0 for e in entries)

        metrics = CacheMetrics(
            total_requests=len(entries),
            total_hits=total_hits,
            total_misses=len(entries) - total_hits,
            memory_usage_mb=total_size / (1024 * 1024),
        )
        self.db.add(metrics)
        self.db.commit()

        return metrics


class APIDocumentationService:
    def __init__(self, db: Session):
        self.db = db

    async def create_documentation(
        self,
        name: str,
        format: DocumentationFormat,
        spec: Dict[str, Any],
        version: str = "1.0.0",
        description: Optional[str] = None,
        base_path: Optional[str] = None,
        servers: Optional[List[str]] = None,
    ) -> APIDocumentation:
        doc = APIDocumentation(
            name=name,
            format=format,
            spec=spec,
            version=version,
            description=description,
            base_path=base_path,
            servers=servers or [],
        )
        self.db.add(doc)
        self.db.commit()
        return doc

    async def add_endpoint(
        self,
        doc_id: int,
        path: str,
        method: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict] = None,
        request_schema: Optional[Dict] = None,
        response_schema: Optional[Dict] = None,
        status_codes: Optional[Dict] = None,
    ) -> APIEndpoint:
        endpoint = APIEndpoint(
            doc_id=doc_id,
            path=path,
            method=method,
            summary=summary,
            description=description,
            parameters=parameters or {},
            request_schema=request_schema,
            response_schema=response_schema,
            status_codes=status_codes or {},
        )
        self.db.add(endpoint)
        self.db.commit()
        return endpoint

    async def get_documentation(self, doc_id: int) -> Optional[APIDocumentation]:
        return self.db.query(APIDocumentation).filter(
            APIDocumentation.id == doc_id
        ).first()

    async def get_endpoints(self, doc_id: int) -> List[APIEndpoint]:
        return self.db.query(APIEndpoint).filter(
            APIEndpoint.doc_id == doc_id
        ).all()

    async def record_usage(
        self,
        endpoint: str,
        method: str,
        response_time_ms: float,
        is_error: bool = False,
    ) -> APIUsageMetrics:
        metrics = self.db.query(APIUsageMetrics).filter(
            APIUsageMetrics.endpoint == endpoint,
            APIUsageMetrics.method == method,
        ).first()

        if not metrics:
            metrics = APIUsageMetrics(
                endpoint=endpoint,
                method=method,
            )
            self.db.add(metrics)

        metrics.call_count += 1
        if is_error:
            metrics.error_count += 1

        metrics.average_response_time_ms = (
            (metrics.average_response_time_ms * (metrics.call_count - 1) + response_time_ms)
            / metrics.call_count
        )

        if response_time_ms > (metrics.max_response_time_ms or 0):
            metrics.max_response_time_ms = response_time_ms

        if response_time_ms < (metrics.min_response_time_ms or float('inf')):
            metrics.min_response_time_ms = response_time_ms

        self.db.commit()
        return metrics
