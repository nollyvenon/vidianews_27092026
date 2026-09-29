"""Analytics and admin models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum
from app.db.base import Base


class AnalyticsEventType(str, Enum):
    PAGE_VIEW = "page_view"
    USER_SIGNUP = "user_signup"
    COURSE_ENROLLMENT = "course_enrollment"
    COURSE_COMPLETION = "course_completion"
    PURCHASE = "purchase"
    CONTENT_VIEW = "content_view"
    SEARCH = "search"
    LOGOUT = "logout"


class ReportType(str, Enum):
    REVENUE = "revenue"
    USERS = "users"
    ENGAGEMENT = "engagement"
    COURSES = "courses"
    MEMBERSHIPS = "memberships"
    CUSTOM = "custom"


class AdminAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SUSPEND = "suspend"
    RESTORE = "restore"
    EXPORT = "export"


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    event_type = Column(SQLEnum(AnalyticsEventType), nullable=False)
    event_data = Column(JSON, default={})
    session_id = Column(String(255), index=True)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    referrer = Column(String(500))
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    user = relationship("User")


class AnalyticsDashboard(Base):
    __tablename__ = "analytics_dashboards"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    widgets = Column(JSON, default=[])
    is_public = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class UserMetric(Base):
    __tablename__ = "user_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    total_logins = Column(Integer, default=0)
    last_login = Column(DateTime)
    total_session_time = Column(Integer, default=0)
    courses_enrolled = Column(Integer, default=0)
    courses_completed = Column(Integer, default=0)
    total_spend = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User")


class RevenueMetric(Base):
    __tablename__ = "revenue_metrics"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    date = Column(DateTime, nullable=False, index=True)
    total_revenue = Column(Float, default=0.0)
    course_revenue = Column(Float, default=0.0)
    membership_revenue = Column(Float, default=0.0)
    transaction_count = Column(Integer, default=0)
    average_transaction = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


class EngagementMetric(Base):
    __tablename__ = "engagement_metrics"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    date = Column(DateTime, nullable=False, index=True)
    active_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    daily_active_users = Column(Integer, default=0)
    average_session_duration = Column(Integer, default=0)
    bounce_rate = Column(Float, default=0.0)
    pages_per_session = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    report_data = Column(JSON, default={})
    filters = Column(JSON, default={})
    is_scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(String(50))
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    generated_at = Column(DateTime)


class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    admin_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    action = Column(SQLEnum(AdminAction), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    changes = Column(JSON, default={})
    reason = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)


class SystemHealth(Base):
    __tablename__ = "system_health"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    api_response_time = Column(Float)
    error_rate = Column(Float)
    uptime_percentage = Column(Float)
    active_connections = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)


class UserBehavior(Base):
    __tablename__ = "user_behavior"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    page_visited = Column(String(255))
    time_spent = Column(Integer)
    actions_taken = Column(JSON, default=[])
    device_type = Column(String(50))
    browser = Column(String(100))
    operating_system = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    user = relationship("User")


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=True)
    course_updates = Column(Boolean, default=True)
    order_updates = Column(Boolean, default=True)
    weekly_digest = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User")


class ContentModeration(Base):
    __tablename__ = "content_moderation"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    reported_by = Column(Integer, ForeignKey("user.id"))
    reason = Column(String(255))
    status = Column(String(50), default="pending")
    moderator_id = Column(Integer, ForeignKey("user.id"))
    action_taken = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    resolved_at = Column(DateTime)


class PermissionPolicy(Base):
    __tablename__ = "permission_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    permissions = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    role_name = Column(String(100), nullable=False)
    permission_policy_id = Column(Integer, ForeignKey("permission_policies.id"))
    assigned_by = Column(Integer, ForeignKey("user.id"))
    assigned_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)


class SystemAlert(Base):
    __tablename__ = "system_alerts"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    alert_type = Column(String(100), nullable=False)
    severity = Column(String(50), default="warning")
    message = Column(Text, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    resolved_at = Column(DateTime)
