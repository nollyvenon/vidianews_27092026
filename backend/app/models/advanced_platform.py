from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class WebSocketConnectionStatus(str, enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PipelineStageStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class CacheStrategy(str, enum.Enum):
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    FIFO = "fifo"


class DocumentationFormat(str, enum.Enum):
    OPENAPI3 = "openapi3"
    SWAGGER2 = "swagger2"
    GRAPHQL = "graphql"
    ASYNCAPI = "asyncapi"


class WebSocketConnection(Base):
    __tablename__ = "websocket_connections"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    connection_id = Column(String(255), nullable=False, unique=True)
    status = Column(Enum(WebSocketConnectionStatus), default=WebSocketConnectionStatus.CONNECTED)
    event_subscriptions = Column(ARRAY(String), default=[])
    ip_address = Column(String(45))
    user_agent = Column(Text)
    connected_at = Column(DateTime, server_default=func.now())
    last_heartbeat = Column(DateTime, server_default=func.now(), onupdate=func.now())
    disconnected_at = Column(DateTime)

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_connection_id", "connection_id"),
        Index("idx_status", "status"),
    )


class RealtimeEvent(Base):
    __tablename__ = "realtime_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)
    event_source = Column(String(100), nullable=False)
    user_ids = Column(ARRAY(Integer), default=[])
    payload = Column(JSON, nullable=False)
    priority = Column(Integer, default=0)
    retry_count = Column(Integer, default=0)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    published_at = Column(DateTime)
    expires_at = Column(DateTime)

    __table_args__ = (
        Index("idx_event_type", "event_type"),
        Index("idx_status", "status"),
        Index("idx_created_at", "created_at"),
    )


class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id = Column(Integer, primary_key=True)
    job_type = Column(String(100), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    user_id = Column(Integer)
    priority = Column(Integer, default=0)
    payload = Column(JSON, nullable=False)
    result = Column(JSON)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_job_type", "job_type"),
        Index("idx_status", "status"),
        Index("idx_user_id", "user_id"),
        Index("idx_priority", "priority"),
        Index("idx_scheduled_at", "scheduled_at"),
    )


class JobSchedule(Base):
    __tablename__ = "job_schedules"

    id = Column(Integer, primary_key=True)
    job_type = Column(String(100), nullable=False)
    cron_expression = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    description = Column(Text)
    payload = Column(JSON, default={})
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_job_type", "job_type"),
        Index("idx_enabled", "enabled"),
    )


class DataPipeline(Base):
    __tablename__ = "data_pipelines"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    source_type = Column(String(100), nullable=False)
    destination_type = Column(String(100), nullable=False)
    status = Column(String(50), default="draft")
    is_active = Column(Boolean, default=False)
    schedule = Column(String(100))
    config = Column(JSON, default={})
    transformation_rules = Column(JSON, default={})
    last_run = Column(DateTime)
    last_success = Column(DateTime)
    failure_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_status", "status"),
        Index("idx_is_active", "is_active"),
    )


class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey("data_pipelines.id"), nullable=False)
    status = Column(String(50), default="pending")
    records_processed = Column(BigInteger, default=0)
    records_failed = Column(BigInteger, default=0)
    execution_time_ms = Column(BigInteger)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    error_message = Column(Text)

    __table_args__ = (
        Index("idx_pipeline_id", "pipeline_id"),
        Index("idx_status", "status"),
        Index("idx_started_at", "started_at"),
    )


class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey("data_pipelines.id"), nullable=False)
    stage_name = Column(String(100), nullable=False)
    stage_order = Column(Integer, nullable=False)
    stage_type = Column(String(50), nullable=False)
    config = Column(JSON, default={})
    status = Column(Enum(PipelineStageStatus), default=PipelineStageStatus.PENDING)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_pipeline_id", "pipeline_id"),
        Index("idx_stage_order", "stage_order"),
    )


class CacheEntry(Base):
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True)
    cache_key = Column(String(500), nullable=False, unique=True)
    cache_value = Column(JSON, nullable=False)
    strategy = Column(Enum(CacheStrategy), default=CacheStrategy.TTL)
    ttl_seconds = Column(Integer)
    hit_count = Column(Integer, default=0)
    size_bytes = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    expires_at = Column(DateTime)

    __table_args__ = (
        Index("idx_cache_key", "cache_key"),
        Index("idx_strategy", "strategy"),
        Index("idx_expires_at", "expires_at"),
    )


class CacheMetrics(Base):
    __tablename__ = "cache_metrics"

    id = Column(Integer, primary_key=True)
    total_requests = Column(BigInteger, default=0)
    total_hits = Column(BigInteger, default=0)
    total_misses = Column(BigInteger, default=0)
    average_response_time_ms = Column(Float, default=0.0)
    memory_usage_mb = Column(Float, default=0.0)
    eviction_count = Column(BigInteger, default=0)
    measured_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_measured_at", "measured_at"),
    )


class APIDocumentation(Base):
    __tablename__ = "api_documentations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    format = Column(Enum(DocumentationFormat), default=DocumentationFormat.OPENAPI3)
    version = Column(String(50), default="1.0.0")
    spec = Column(JSON, nullable=False)
    base_path = Column(String(255))
    servers = Column(ARRAY(String), default=[])
    authentication_schemes = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_format", "format"),
    )


class APIEndpoint(Base):
    __tablename__ = "api_endpoints"

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey("api_documentations.id"), nullable=False)
    path = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)
    summary = Column(String(500))
    description = Column(Text)
    parameters = Column(JSON, default={})
    request_schema = Column(JSON)
    response_schema = Column(JSON)
    status_codes = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_doc_id", "doc_id"),
        Index("idx_path", "path"),
        Index("idx_method", "method"),
    )


class APIUsageMetrics(Base):
    __tablename__ = "api_usage_metrics"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)
    call_count = Column(BigInteger, default=0)
    error_count = Column(BigInteger, default=0)
    average_response_time_ms = Column(Float, default=0.0)
    max_response_time_ms = Column(Float, default=0.0)
    min_response_time_ms = Column(Float, default=0.0)
    measured_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_endpoint", "endpoint"),
        Index("idx_measured_at", "measured_at"),
    )
