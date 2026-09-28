from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class UserSegmentType(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    VIP = "vip"
    TRIAL = "trial"
    CHURNED = "churned"
    ENGAGED = "engaged"
    LOW_ENGAGEMENT = "low_engagement"


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    FAILED = "failed"


class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    template_variables = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_email_template_name", "name"),
    )


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    from_email = Column(String(255), nullable=False)
    recipient_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    bounce_count = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_email_campaign_status", "status"),
        Index("idx_email_campaign_created_at", "created_at"),
    )


class CampaignRecipient(Base):
    __tablename__ = "campaign_recipients"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")  # pending, sent, opened, clicked, bounced
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    bounced_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_campaign_recipient_campaign", "campaign_id"),
        Index("idx_campaign_recipient_user", "user_id"),
        Index("idx_campaign_recipient_status", "status"),
    )


class UserSegment(Base):
    __tablename__ = "user_segments"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    segment_type = Column(Enum(UserSegmentType), nullable=False)
    filter_criteria = Column(JSON, default={})
    user_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_segment_type", "segment_type"),
        Index("idx_user_segment_created_at", "created_at"),
    )


class UserSegmentMembership(Base):
    __tablename__ = "user_segment_memberships"

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey("user_segments.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    joined_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("segment_id", "user_id", name="uq_segment_user"),
        Index("idx_segment_membership_segment", "segment_id"),
        Index("idx_segment_membership_user", "user_id"),
    )


class UserPreferenceProfile(Base):
    __tablename__ = "user_preference_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    preferred_categories = Column(ARRAY(String), default=[])
    preferred_languages = Column(ARRAY(String), default=["en"])
    notification_channels = Column(ARRAY(String), default=["email"])
    email_frequency = Column(String(50), default="daily")  # daily, weekly, instant, never
    digest_enabled = Column(Boolean, default=True)
    personalization_enabled = Column(Boolean, default=True)
    opted_in_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_preference_user_id", "user_id"),
    )


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, sent, failed, read
    read_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    sent_at = Column(DateTime)

    __table_args__ = (
        Index("idx_notification_user_id", "user_id"),
        Index("idx_notification_channel", "channel"),
        Index("idx_notification_status", "status"),
        Index("idx_notification_created_at", "created_at"),
    )


class SubscriberProfile(Base):
    __tablename__ = "subscriber_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    subscription_tier = Column(String(50), default="free")  # free, premium, enterprise
    subscription_status = Column(String(50), default="active")  # active, paused, cancelled
    subscription_start_date = Column(DateTime, server_default=func.now())
    subscription_end_date = Column(DateTime)
    articles_read = Column(Integer, default=0)
    total_session_time = Column(Float, default=0.0)  # in minutes
    engagement_score = Column(Float, default=0.0)
    churn_risk_score = Column(Float, default=0.0)
    last_activity_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_subscriber_user_id", "user_id"),
        Index("idx_subscriber_tier", "subscription_tier"),
        Index("idx_subscriber_status", "subscription_status"),
        Index("idx_subscriber_churn_risk", "churn_risk_score"),
    )


class SubscriberActivity(Base):
    __tablename__ = "subscriber_activity"

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey("subscriber_profiles.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # login, read, share, comment, subscribe
    content_id = Column(Integer)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_subscriber_activity_subscriber", "subscriber_id"),
        Index("idx_subscriber_activity_type", "activity_type"),
        Index("idx_subscriber_activity_created_at", "created_at"),
    )


class SubscriberAnalytics(Base):
    __tablename__ = "subscriber_analytics"

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey("subscriber_profiles.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    daily_active = Column(Boolean, default=False)
    articles_read = Column(Integer, default=0)
    session_count = Column(Integer, default=0)
    avg_session_time = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    retention_score = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("subscriber_id", "date", name="uq_subscriber_daily_analytics"),
        Index("idx_subscriber_analytics_subscriber", "subscriber_id"),
        Index("idx_subscriber_analytics_date", "date"),
    )


class WebhookEndpoint(Base):
    __tablename__ = "webhook_endpoints"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    events = Column(ARRAY(String), default=[])
    is_active = Column(Boolean, default=True)
    secret_key = Column(String(255), nullable=False, unique=True)
    retry_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_webhook_active", "is_active"),
        Index("idx_webhook_created_at", "created_at"),
    )


class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True)
    webhook_id = Column(Integer, ForeignKey("webhook_endpoints.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    status_code = Column(Integer)
    response = Column(Text)
    error = Column(Text)
    retry_attempt = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_webhook_log_webhook", "webhook_id"),
        Index("idx_webhook_log_event_type", "event_type"),
        Index("idx_webhook_log_created_at", "created_at"),
    )


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    key = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    permissions = Column(ARRAY(String), default=[])
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_api_key_user", "user_id"),
        Index("idx_api_key_active", "is_active"),
    )


class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    reading_level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    content_type_preferences = Column(JSON, default={})
    author_preferences = Column(ARRAY(Integer), default=[])
    keyword_interests = Column(ARRAY(String), default=[])
    reading_time_pref = Column(Integer, default=0)  # in minutes
    timezone = Column(String(50), default="UTC")
    last_personalization_update = Column(DateTime, server_default=func.now())
    personalization_score = Column(Float, default=0.0)

    __table_args__ = (
        Index("idx_personalization_user_id", "user_id"),
    )
