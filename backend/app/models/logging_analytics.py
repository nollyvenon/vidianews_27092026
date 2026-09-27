"""Logging, Analytics & Documentation models: Modules 46-50"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class LogLevel(str, enum.Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeatureFlagStatus(str, enum.Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"


class AnalyticsEventType(str, enum.Enum):
    PAGE_VIEW = "page_view"
    CLICK = "click"
    VIDEO_PLAY = "video_play"
    CONTENT_SHARE = "content_share"
    SIGNUP = "signup"


class DocType(str, enum.Enum):
    API = "api"
    GUIDE = "guide"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"


# ==================== MODULE 46: LOGGING ====================

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(SQLEnum(LogLevel), nullable=False, index=True)
    service = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", backref="log_entries")


class LogAggregation(Base):
    __tablename__ = "log_aggregations"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(255), nullable=False, unique=True, index=True)
    total_logs = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    last_aggregated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ==================== MODULE 47: ERROR TRACKING ====================

class ErrorReport(Base):
    __tablename__ = "error_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    error_type = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    severity = Column(SQLEnum(ErrorSeverity), default=ErrorSeverity.MEDIUM)
    resolved = Column(Boolean, default=False)
    occurrence_count = Column(Integer, default=1)
    first_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="error_reports")


class ErrorSession(Base):
    __tablename__ = "error_sessions"
    id = Column(Integer, primary_key=True, index=True)
    error_report_id = Column(Integer, ForeignKey("error_reports.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(255), nullable=False, index=True)
    device_info = Column(JSON)
    browser_info = Column(JSON)
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    error_report = relationship("ErrorReport", backref="sessions")


# ==================== MODULE 48: FEATURE FLAGS ====================

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    status = Column(SQLEnum(FeatureFlagStatus), default=FeatureFlagStatus.DISABLED)
    rollout_percentage = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ABTest(Base):
    __tablename__ = "ab_tests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    feature_flag_id = Column(Integer, ForeignKey("feature_flags.id", ondelete="CASCADE"), nullable=False)
    variant_a = Column(String(255), nullable=False)
    variant_b = Column(String(255), nullable=False)
    traffic_split = Column(Integer, default=50)
    conversions_a = Column(Integer, default=0)
    conversions_b = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)

    feature_flag = relationship("FeatureFlag", backref="ab_tests")


# ==================== MODULE 49: ANALYTICS ====================

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    event_type = Column(SQLEnum(AnalyticsEventType), nullable=False, index=True)
    event_data = Column(JSON, default={})
    session_id = Column(String(255), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="analytics_events")


class UserSession(Base):
    __tablename__ = "user_sessions_analytics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(String(255), nullable=False, unique=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, default=0)
    page_views = Column(Integer, default=0)

    user = relationship("User", backref="user_sessions_analytics")


# ==================== MODULE 50: DOCUMENTATION ====================

class Documentation(Base):
    __tablename__ = "documentation"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    doc_type = Column(SQLEnum(DocType), nullable=False)
    version = Column(String(50), default="1.0.0")
    author = Column(String(255))
    published = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class APIDocumentation(Base):
    __tablename__ = "api_documentation"
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), nullable=False, unique=True, index=True)
    method = Column(String(10), nullable=False)
    description = Column(Text)
    request_schema = Column(JSON)
    response_schema = Column(JSON)
    examples = Column(JSON)
    auth_required = Column(Boolean, default=True)
    rate_limit = Column(Integer, nullable=True)
