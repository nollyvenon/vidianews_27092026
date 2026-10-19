from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, BigInteger
)
import enum

from app.db.base import Base


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
        Index("idx_user_id_security_audit_logs", "user_id"),
        Index("idx_action", "action"),
        Index("idx_created_at_security_audit_logs", "created_at"),
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
        Index("idx_user_id_access_controls", "user_id"),
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
        Index("idx_user_id_role_based_access", "user_id"),
        Index("idx_role", "role"),
    )


class ModerationQueue(Base):
    __tablename__ = "moderation_queues"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    status = Column(Enum(ModerationStatus, name="enterprise_features_moderation_status"), default=ModerationStatus.PENDING)
    reason = Column(Text)
    flags = Column(ARRAY(String), default=[])
    confidence_score = Column(Float, default=0.0)
    assigned_to = Column(Integer)
    reviewed_by = Column(Integer)
    reviewed_at = Column(DateTime)
    decision = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_status_moderation_queues", "status"),
        Index("idx_content_id_moderation_queues", "content_id"),
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
        Index("idx_name_compliance_rules", "name"),
        Index("idx_enabled_compliance_rules", "enabled"),
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
        Index("idx_user_id_rate_limit_configs", "user_id"),
        Index("idx_ip_address", "ip_address"),
        Index("idx_endpoint_rate_limit_configs", "endpoint"),
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
        Index("idx_user_id_throttle_logs", "user_id"),
        Index("idx_ip_address_throttle_logs", "ip_address"),
        Index("idx_throttled_at", "throttled_at"),
    )


class NotificationPreference(Base):
    __tablename__ = "enterprise_notification_preferences"

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
        Index("idx_user_id_enterprise_notification_preferences", "user_id"),
    )


class RealTimeNotification(Base):
    __tablename__ = "real_time_notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    notification_type = Column(Enum(NotificationType, name="enterprise_features_notification_type"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, default={})
    read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    action_url = Column(String(500))
    source = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id_real_time_notifications", "user_id"),
        Index("idx_notification_type", "notification_type"),
        Index("idx_read", "read"),
        Index("idx_created_at_real_time_notifications", "created_at"),
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
        Index("idx_user_id_alert_configurations", "user_id"),
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
        Index("idx_user_id_advanced_reports", "user_id"),
        Index("idx_report_type", "report_type"),
        Index("idx_status_advanced_reports", "status"),
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
        Index("idx_name_report_templates", "name"),
        Index("idx_report_type_report_templates", "report_type"),
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
        Index("idx_user_id_report_schedules", "user_id"),
        Index("idx_enabled_report_schedules", "enabled"),
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
        Index("idx_user_id_export_jobs", "user_id"),
        Index("idx_status_export_jobs", "status"),
        Index("idx_export_type", "export_type"),
    )


# ==================== SECURITY, MODERATION & RATE LIMITS ====================


class SecurityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ModerationAction(str, enum.Enum):
    WARN = "warn"
    HIDE = "hide"
    REMOVE = "remove"
    SUSPEND = "suspend"
    BAN = "ban"


class SecurityPolicy(Base):
    """Named security policy with its configuration"""
    __tablename__ = "security_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    level = Column(Enum(SecurityLevel, native_enum=False, length=20), nullable=False, default=SecurityLevel.MEDIUM)
    policy_config = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ModerationRule(Base):
    """Pattern-based moderation rule and the action it triggers"""
    __tablename__ = "moderation_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    pattern = Column(Text, nullable=False)
    action = Column(Enum(ModerationAction, native_enum=False, length=20), nullable=False, default=ModerationAction.WARN)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class RateLimiterConfig(Base):
    """Per-endpoint rate limit"""
    __tablename__ = "rate_limiter_configs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), unique=True, nullable=False, index=True)
    requests_per_window = Column(Integer, nullable=False)
    window_seconds = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class NotificationConfig(Base):
    """Configuration for a notification channel"""
    __tablename__ = "notification_configs"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(50), unique=True, nullable=False, index=True)
    config = Column(JSON, default=dict)
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
