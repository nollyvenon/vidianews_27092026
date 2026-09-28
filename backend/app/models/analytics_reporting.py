from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class ReportType(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class SearchIndexStatus(str, enum.Enum):
    PENDING = "pending"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"


class CacheLevel(str, enum.Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_pageviews = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    avg_session_duration = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    revenue = Column(Numeric(10, 2), default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_analytics_report_type", "report_type"),
        Index("idx_analytics_report_period", "period_start", "period_end"),
        Index("idx_analytics_report_created_at", "created_at"),
    )


class PageViewMetrics(Base):
    __tablename__ = "pageview_metrics"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    page_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    avg_time_on_page = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    scroll_depth = Column(Float, default=0.0)
    conversion_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("content_id", "date", name="uq_pageview_daily"),
        Index("idx_pageview_content", "content_id"),
        Index("idx_pageview_date", "date"),
    )


class UserBehaviorEvent(Base):
    __tablename__ = "user_behavior_events"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content_id = Column(Integer)
    event_type = Column(String(50), nullable=False)  # click, scroll, hover, exit, etc.
    event_data = Column(JSON, default={})
    page_url = Column(String(2048))
    referrer = Column(String(2048))
    device_type = Column(String(50))
    browser = Column(String(100))
    os = Column(String(100))
    timestamp = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_behavior_user", "user_id"),
        Index("idx_behavior_content", "content_id"),
        Index("idx_behavior_event_type", "event_type"),
        Index("idx_behavior_timestamp", "timestamp"),
    )


class HeatmapData(Base):
    __tablename__ = "heatmap_data"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False, unique=True)
    heatmap_json = Column(JSON, nullable=False)
    scroll_depth_percentiles = Column(JSON, default={})
    click_zones = Column(JSON, default={})
    exit_rate = Column(Float, default=0.0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_heatmap_content", "content_id"),
    )


class SearchIndex(Base):
    __tablename__ = "search_index"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    full_text = Column(Text)
    tags = Column(ARRAY(String), default=[])
    categories = Column(ARRAY(String), default=[])
    keywords = Column(ARRAY(String), default=[])
    search_vector = Column(String)  # Full-text search vector
    status = Column(Enum(SearchIndexStatus), default=SearchIndexStatus.PENDING)
    indexed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_search_status", "status"),
        Index("idx_search_indexed_at", "indexed_at"),
    )


class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query = Column(String(255), nullable=False)
    result_count = Column(Integer, default=0)
    clicked_result = Column(Integer)
    search_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_search_query_user", "user_id"),
        Index("idx_search_query_text", "query"),
        Index("idx_search_query_created_at", "created_at"),
    )


class CacheEntry(Base):
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True)
    key = Column(String(512), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    cache_level = Column(Enum(CacheLevel), default=CacheLevel.WARM)
    ttl_seconds = Column(Integer, default=3600)
    hits = Column(Integer, default=0)
    last_accessed = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_cache_key", "key"),
        Index("idx_cache_level", "cache_level"),
        Index("idx_cache_last_accessed", "last_accessed"),
    )


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, etc.
    response_time_ms = Column(Integer, default=0)
    status_code = Column(Integer, default=200)
    request_size = Column(Integer, default=0)
    response_size = Column(Integer, default=0)
    timestamp = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_perf_endpoint", "endpoint"),
        Index("idx_perf_method", "method"),
        Index("idx_perf_status", "status_code"),
        Index("idx_perf_timestamp", "timestamp"),
    )


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    component = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    timestamp = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_system_log_level", "level"),
        Index("idx_system_log_component", "component"),
        Index("idx_system_log_timestamp", "timestamp"),
    )


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer)
    changes = Column(JSON, default={})
    ip_address = Column(String(45))
    timestamp = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_audit_admin", "admin_id"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource_type", "resource_type"),
        Index("idx_audit_timestamp", "timestamp"),
    )


class SystemHealthCheck(Base):
    __tablename__ = "system_health_checks"

    id = Column(Integer, primary_key=True)
    service_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # healthy, degraded, unhealthy
    response_time_ms = Column(Integer)
    last_check = Column(DateTime, server_default=func.now())
    uptime_percentage = Column(Float, default=100.0)
    error_count = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_health_service", "service_name"),
        Index("idx_health_status", "status"),
        Index("idx_health_last_check", "last_check"),
    )


class ConfigurationSetting(Base):
    __tablename__ = "configuration_settings"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    setting_type = Column(String(50), default="string")  # string, number, boolean, json
    description = Column(Text)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_config_key", "key"),
    )


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    enabled = Column(Boolean, default=False)
    rollout_percentage = Column(Integer, default=0)  # 0-100
    target_segments = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_feature_flag_name", "name"),
        Index("idx_feature_flag_enabled", "enabled"),
    )
