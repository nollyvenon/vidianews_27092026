"""API, Monitoring & Testing models: Modules 41-45"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float, Float as SQLFloat
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class APIVersion(str, enum.Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class EventType(str, enum.Enum):
    USER_CREATED = "user.created"
    CONTENT_UPLOADED = "content.uploaded"
    PAYMENT_RECEIVED = "payment.received"
    SUBSCRIPTION_CHANGED = "subscription.changed"


class WebhookStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"


class MetricType(str, enum.Enum):
    REQUEST_COUNT = "request_count"
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ==================== MODULE 41: API VERSIONING ====================

class APIEndpointVersion(Base):
    __tablename__ = "api_endpoint_versions"
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), nullable=False, index=True)
    version = Column(SQLEnum(APIVersion), nullable=False)
    deprecated = Column(Boolean, default=False)
    sunset_date = Column(DateTime(timezone=True), nullable=True)
    schema = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class VersionMigration(Base):
    __tablename__ = "version_migrations"
    id = Column(Integer, primary_key=True, index=True)
    old_version = Column(SQLEnum(APIVersion), nullable=False)
    new_version = Column(SQLEnum(APIVersion), nullable=False)
    migration_script = Column(Text)
    status = Column(String(50), default="pending")
    executed_at = Column(DateTime(timezone=True), nullable=True)


# ==================== MODULE 42: GRAPHQL ====================

class GraphQLQuery(Base):
    __tablename__ = "graphql_queries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    query_string = Column(Text, nullable=False)
    response_schema = Column(JSON)
    execution_count = Column(Integer, default=0)
    avg_execution_time_ms = Column(Float, default=0.0)


class GraphQLMutation(Base):
    __tablename__ = "graphql_mutations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    mutation_string = Column(Text, nullable=False)
    input_schema = Column(JSON)
    return_schema = Column(JSON)
    execution_count = Column(Integer, default=0)


# ==================== MODULE 43: WEBHOOKS ====================

class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    secret = Column(String(255), nullable=False)
    status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.ACTIVE)
    retry_count = Column(Integer, default=3)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="webhooks")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(SQLEnum(EventType), nullable=False)
    payload = Column(JSON, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    response_status = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    webhook = relationship("Webhook", backref="events")


# ==================== MODULE 44: TESTING ====================

class TestSuite(Base):
    __tablename__ = "test_suites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    test_count = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    coverage_percentage = Column(Float, default=0.0)


class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    test_suite_id = Column(Integer, ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=False)
    test_name = Column(String(255), nullable=False)
    status = Column(String(50))
    duration_ms = Column(Float)
    error_message = Column(Text, nullable=True)
    run_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    test_suite = relationship("TestSuite", backref="results")


# ==================== MODULE 45: MONITORING ====================

class SystemMetric(Base):
    __tablename__ = "system_metrics"
    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(SQLEnum(MetricType), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


class PerformanceAlert(Base):
    __tablename__ = "performance_alerts"
    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(SQLEnum(MetricType), nullable=False)
    severity = Column(SQLEnum(AlertSeverity), nullable=False, index=True)
    threshold = Column(Float)
    current_value = Column(Float)
    message = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(255), nullable=False, index=True)
    status = Column(String(50))
    response_time_ms = Column(Float)
    last_checked = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    uptime_percentage = Column(Float, default=100.0)
