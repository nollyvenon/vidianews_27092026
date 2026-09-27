"""Monetization models: Modules 31-35"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class BillingCycle(str, enum.Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"
    ONE_TIME = "one_time"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


# ==================== MODULE 31: REAL-TIME UPDATES ====================

class WebSocketConnection(Base):
    __tablename__ = "websocket_connections"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    connection_id = Column(String(255), nullable=False, unique=True)
    channels = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_heartbeat = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="websocket_connections")


class RealtimeEvent(Base):
    __tablename__ = "realtime_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    channel = Column(String(100), nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (Index("ix_event_channel", "channel", "created_at"),)


# ==================== MODULE 32: BILLING & PAYMENTS ====================

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, index=True)
    billing_cycle = Column(SQLEnum(BillingCycle), default=BillingCycle.MONTHLY)
    stripe_subscription_id = Column(String(255), unique=True)
    amount = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True, index=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    renews_at = Column(DateTime(timezone=True))
    canceled_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="subscription")
    organization = relationship("Organization", backref="subscription")


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    stripe_invoice_id = Column(String(255), unique=True)
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    due_date = Column(DateTime(timezone=True))
    paid_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    subscription = relationship("Subscription", backref="invoices")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    stripe_payment_id = Column(String(255), unique=True)
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_method = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="payments")
    invoice = relationship("Invoice", backref="payments")


# ==================== MODULE 33: MARKETPLACE ====================

class CreatorProfile(Base):
    __tablename__ = "creator_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    bio = Column(Text)
    profile_url = Column(String(255))
    banner_url = Column(String(255))
    followers = Column(Integer, default=0)
    earnings = Column(Float, default=0.0)
    stripe_account_id = Column(String(255))
    is_verified = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="creator_profile")


class Monetization(Base):
    __tablename__ = "monetizations"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id", ondelete="CASCADE"), nullable=False)
    monthly_revenue = Column(Float, default=0.0)
    total_earnings = Column(Float, default=0.0)
    payouts = Column(JSON, default=[])
    is_enabled = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator = relationship("CreatorProfile", backref="monetization")


# ==================== MODULE 34: ADVANCED ANALYTICS ====================

class CustomDashboard(Base):
    __tablename__ = "custom_dashboards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    widgets = Column(JSON, default=[])
    filters = Column(JSON, default={})
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="custom_dashboards")


class DataExport(Base):
    __tablename__ = "data_exports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    export_type = Column(String(50), nullable=False)
    format = Column(String(20), default="csv")
    file_url = Column(String(500))
    status = Column(String(50), default="processing")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="data_exports")


# ==================== MODULE 35: EMAIL CAMPAIGNS ====================

class EmailCampaign(Base):
    __tablename__ = "email_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    recipient_count = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    status = Column(String(50), default="draft")
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    creator = relationship("User", backref="email_campaigns")


class CampaignMetric(Base):
    __tablename__ = "campaign_metrics"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id", ondelete="CASCADE"), nullable=False)
    sent = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    unsubscribed = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    campaign = relationship("EmailCampaign", backref="metrics")
