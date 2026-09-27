from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class AccessLevel(str, enum.Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    ADMIN = "admin"


class PermissionType(str, enum.Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    MANAGE = "manage"


class ModerationStatus(str, enum.Enum):
    APPROVED = "approved"
    PENDING = "pending"
    FLAGGED = "flagged"
    REJECTED = "rejected"
    APPEALED = "appealed"


class NotificationType(str, enum.Enum):
    ALERT = "alert"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"


class ReportFormat(str, enum.Enum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"


class SecurityAuditLog(Base):
    __tablename__ = "security_audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(Integer)
    status = Column(String(50))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    changes = Column(JSON, default={})
    severity = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_action", "action"),
        Index("idx_created_at", "created_at"),
        Index("idx_severity", "severity"),
    )


class AccessControl(Base):
    __tablename__ = "access_controls"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer, nullable=False)
    access_level = Column(Enum(AccessLevel), default=AccessLevel.PROTECTED)
    permissions = Column(ARRAY(String), default=[])
    granted_by = Column(Integer)
    granted_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "resource_type", "resource_id", name="uq_access"),
        Index("idx_user_id", "user_id"),
        Index("idx_resource", "resource_type", "resource_id"),
    )


class RoleBasedAccess(Base):
    __tablename__ = "role_based_access"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    role = Column(String(100), nullable=False)
    permissions = Column(ARRAY(String), default=[])
    can_edit_content = Column(Boolean, default=False)
    can_delete_content = Column(Boolean, default=False)
    can_manage_users = Column(Boolean, default=False)
    can_access_analytics = Column(Boolean, default=False)
    can_access_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_role", "role"),
    )


class ModerationQueue(Base):
    __tablename__ = "moderation_queues"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    status = Column(Enum(ModerationStatus), default=ModerationStatus.PENDING)
    reason = Column(Text)
    flags = Column(ARRAY(String), default=[])
    confidence_score = Column(Float, default=0.0)
    assigned_to = Column(Integer)
    reviewed_by = Column(Integer)
    reviewed_at = Column(DateTime)
    decision = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_status", "status"),
        Index("idx_content_id", "content_id"),
        Index("idx_assigned_to", "assigned_to"),
        Index("idx_confidence_score", "confidence_score"),
    )


class ComplianceRule(Base):
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    rule_type = Column(String(100), nullable=False)
    keywords = Column(ARRAY(String), default=[])
    patterns = Column(ARRAY(String), default=[])
    severity = Column(String(50))
    auto_action = Column(String(100))
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_enabled", "enabled"),
    )


class RateLimitConfig(Base):
    __tablename__ = "rate_limit_configs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ip_address = Column(String(45))
    endpoint = Column(String(255), nullable=False)
    requests_per_minute = Column(Integer, default=60)
    requests_per_hour = Column(Integer, default=1000)
    requests_per_day = Column(Integer, default=10000)
    burst_limit = Column(Integer, default=100)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_ip_address", "ip_address"),
        Index("idx_endpoint", "endpoint"),
    )


class ThrottleLog(Base):
    __tablename__ = "throttle_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ip_address = Column(String(45))
    endpoint = Column(String(255))
    requests_count = Column(Integer)
    limit_type = Column(String(50))
    throttled_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_ip_address", "ip_address"),
        Index("idx_throttled_at", "throttled_at"),
    )


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    in_app_enabled = Column(Boolean, default=True)
    frequency = Column(String(50), default="immediate")
    do_not_disturb_start = Column(String(5))
    do_not_disturb_end = Column(String(5))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
    )


class RealTimeNotification(Base):
    __tablename__ = "real_time_notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, default={})
    read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    action_url = Column(String(500))
    source = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_notification_type", "notification_type"),
        Index("idx_read", "read"),
        Index("idx_created_at", "created_at"),
    )


class AlertConfiguration(Base):
    __tablename__ = "alert_configurations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    alert_type = Column(String(100), nullable=False)
    condition = Column(String(255))
    threshold = Column(Float)
    enabled = Column(Boolean, default=True)
    notification_channels = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_alert_type", "alert_type"),
    )


class AdvancedReport(Base):
    __tablename__ = "advanced_reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    report_type = Column(String(100), nullable=False)
    format = Column(Enum(ReportFormat), default=ReportFormat.PDF)
    query = Column(JSON)
    filters = Column(JSON, default={})
    data = Column(JSON)
    file_path = Column(String(500))
    status = Column(String(50), default="pending")
    generated_at = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_report_type", "report_type"),
        Index("idx_status", "status"),
    )


class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    report_type = Column(String(100), nullable=False)
    sections = Column(ARRAY(String), default=[])
    format = Column(Enum(ReportFormat), default=ReportFormat.PDF)
    schedule = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_report_type", "report_type"),
    )


class ReportSchedule(Base):
    __tablename__ = "report_schedules"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    template_id = Column(Integer, ForeignKey("report_templates.id"))
    name = Column(String(255), nullable=False)
    cron_expression = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    recipient_emails = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_enabled", "enabled"),
    )


class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    export_type = Column(String(100), nullable=False)
    format = Column(Enum(ReportFormat), nullable=False)
    filters = Column(JSON)
    status = Column(String(50), default="pending")
    progress = Column(Integer, default=0)
    file_path = Column(String(500))
    record_count = Column(BigInteger, default=0)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_status", "status"),
        Index("idx_export_type", "export_type"),
    )
