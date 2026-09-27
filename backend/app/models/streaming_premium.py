"""Streaming, Analytics & Premium models: Modules 56-60"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class StreamStatus(str, enum.Enum):
    LIVE = "live"
    ENDED = "ended"
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class AnalyticsMetric(str, enum.Enum):
    VIEWS = "views"
    WATCH_TIME = "watch_time"
    ENGAGEMENT = "engagement"
    REVENUE = "revenue"


class PartnershipType(str, enum.Enum):
    BRAND_DEAL = "brand_deal"
    AFFILIATE = "affiliate"
    COLLABORATION = "collaboration"
    SPONSORSHIP = "sponsorship"


class PremiumFeature(str, enum.Enum):
    HD_STREAMING = "hd_streaming"
    AD_FREE = "ad_free"
    EARLY_ACCESS = "early_access"
    EXCLUSIVE_CONTENT = "exclusive_content"


# ==================== MODULE 56: LIVESTREAMING ====================

class LiveStream(Base):
    __tablename__ = "live_streams"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(StreamStatus), default=StreamStatus.SCHEDULED, index=True)
    stream_key = Column(String(255), unique=True)
    rtmp_url = Column(String(500))
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    viewer_count = Column(Integer, default=0)
    category = Column(String(100))

    creator = relationship("User", backref="live_streams")


class StreamViewer(Base):
    __tablename__ = "stream_viewers"
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("live_streams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    left_at = Column(DateTime(timezone=True), nullable=True)
    watch_duration_seconds = Column(Integer, default=0)

    stream = relationship("LiveStream", backref="viewers")
    viewer = relationship("User", backref="stream_views")


class StreamChat(Base):
    __tablename__ = "stream_chats"
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("live_streams.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    stream = relationship("LiveStream", backref="chat_messages")
    user = relationship("User", backref="stream_messages")


# ==================== MODULE 57: EXTENDED SUBSCRIPTIONS ====================

class SubscriptionTier(Base):
    __tablename__ = "subscription_tiers"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price_usd = Column(Float, nullable=False)
    features = Column(JSON, default=[])
    max_subscribers = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    creator = relationship("User", backref="subscription_tiers")


class SubscriberRecord(Base):
    __tablename__ = "subscriber_records"
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tier_id = Column(Integer, ForeignKey("subscription_tiers.id", ondelete="CASCADE"), nullable=False)
    subscribed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))
    auto_renew = Column(Boolean, default=True)

    subscriber = relationship("User", foreign_keys=[subscriber_id], backref="subscriptions")
    tier = relationship("SubscriptionTier", backref="subscribers")


# ==================== MODULE 58: CREATOR ANALYTICS ====================

class CreatorAnalytics(Base):
    __tablename__ = "creator_analytics"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    total_views = Column(Integer, default=0)
    total_watch_hours = Column(Float, default=0.0)
    average_engagement_rate = Column(Float, default=0.0)
    subscriber_count = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    creator = relationship("User", backref="analytics")


class DailyAnalytic(Base):
    __tablename__ = "daily_analytics"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(DateTime(timezone=True), index=True)
    views = Column(Integer, default=0)
    watch_hours = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)

    creator = relationship("User", backref="daily_analytics")


# ==================== MODULE 59: PARTNERSHIPS ====================

class Partnership(Base):
    __tablename__ = "partnerships"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    partnership_type = Column(SQLEnum(PartnershipType), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="active")
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)

    creator = relationship("User", foreign_keys=[creator_id], backref="partnerships_created")
    partner = relationship("User", foreign_keys=[partner_id], backref="partnerships_received")


class Collaboration(Base):
    __tablename__ = "collaborations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    participant_ids = Column(JSON)
    content_ids = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    views = Column(Integer, default=0)
    revenue_split = Column(JSON)


# ==================== MODULE 60: PREMIUM FEATURES ====================

class PremiumSubscription(Base):
    __tablename__ = "premium_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    enabled_features = Column(JSON, default=[])
    subscribed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))
    price_per_month = Column(Float, default=9.99)

    user = relationship("User", backref="premium_subscription")


class PaywallContent(Base):
    __tablename__ = "paywall_content"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(Text)
    is_premium_only = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    content = relationship("Content", backref="paywall")


class PremiumAccess(Base):
    __tablename__ = "premium_access"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    purchased_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=True)
    price_paid = Column(Float)

    user = relationship("User", backref="premium_access")
    content = relationship("Content", backref="premium_purchasers")
