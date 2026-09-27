"""Integration models: Modules 21-25 (Analytics, Webhooks, Notifications, Audit, Search)"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class IntegrationType(str, enum.Enum):
    SLACK = "slack"
    WEBHOOK = "webhook"
    ZAPIER = "zapier"
    STRIPE = "stripe"
    SENDGRID = "sendgrid"
    TWILIO = "twilio"


class ReportType(str, enum.Enum):
    PERFORMANCE = "performance"
    ENGAGEMENT = "engagement"
    REVENUE = "revenue"
    COMPLIANCE = "compliance"
    USAGE = "usage"


class NotificationType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class AuditAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    EXPORT = "export"
    SHARE = "share"
    API_CALL = "api_call"


# ==================== MODULE 21: ADVANCED ANALYTICS ====================

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    filters = Column(JSON, default={})
    date_range = Column(JSON)
    is_scheduled = Column(Boolean, default=False, index=True)
    schedule_frequency = Column(String(50))
    recipients = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="analytics_reports")
    organization = relationship("Organization", backref="analytics_reports")
    __table_args__ = (Index("ix_reports_org_type", "organization_id", "report_type"),)


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    dimensions = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    organization = relationship("Organization", backref="metrics")


class Dashboard(Base):
    __tablename__ = "dashboards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    widgets = Column(JSON, default=[])
    layout = Column(JSON)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="dashboards")
    organization = relationship("Organization", backref="dashboards")


# ==================== MODULE 22: WEBHOOKS & INTEGRATIONS ====================

class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_type = Column(SQLEnum(IntegrationType), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    config = Column(JSON, nullable=False)
    api_key = Column(String(500))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", backref="integrations")


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    secret = Column(String(500))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", backref="webhooks")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String(50), default="pending", index=True)
    response = Column(JSON)
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    webhook = relationship("Webhook", backref="events")


# ==================== MODULE 23: NOTIFICATIONS ====================

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    digest_frequency = Column(String(50), default="daily")

    user = relationship("User", backref="notification_preferences")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="notifications")


# ==================== MODULE 24: AUDIT & COMPLIANCE ====================

class AuditTrail(Base):
    __tablename__ = "audit_trails"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(Integer, index=True)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="audit_trails")
    organization = relationship("Organization", backref="audit_trails")
    __table_args__ = (Index("ix_audit_org_action", "organization_id", "action", "created_at"),)


class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(String(100), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    findings = Column(JSON, default=[])
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", backref="compliance_reports")


# ==================== MODULE 25: SEARCH & DISCOVERY ====================

class SearchIndex(Base):
    __tablename__ = "search_indexes"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    tags = Column(JSON, default=[])
    embeddings = Column(JSON)
    last_indexed = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", backref="search_indexes")
    __table_args__ = (Index("ix_search_org_type", "organization_id", "resource_type"),)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_type = Column(String(100), nullable=False)
    recommended_resource_type = Column(String(100), nullable=False)
    recommended_resource_id = Column(Integer, nullable=False)
    score = Column(Float, default=0.0)
    reason = Column(Text)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="recommendations")
