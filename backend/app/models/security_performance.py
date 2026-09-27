"""Security & Performance models: Modules 36-40"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class AuthProvider(str, enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"
    MICROSOFT = "microsoft"


class MFAMethod(str, enum.Enum):
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"


class PrivacyLevel(str, enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    FRIENDS_ONLY = "friends_only"


class CacheType(str, enum.Enum):
    REDIS = "redis"
    CLOUDFLARE = "cloudflare"
    LOCAL = "local"


# ==================== MODULE 36: RATE LIMITING ====================

class RateLimitBucket(Base):
    __tablename__ = "rate_limit_buckets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    endpoint = Column(String(255), nullable=False, index=True)
    requests_count = Column(Integer, default=0)
    reset_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="rate_limit_buckets")


class QuotaUsage(Base):
    __tablename__ = "quota_usage"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_calls = Column(Integer, default=0)
    storage_gb = Column(Float, default=0.0)
    bandwidth_gb = Column(Float, default=0.0)
    monthly_limit = Column(Integer, default=10000)
    reset_date = Column(DateTime(timezone=True))

    user = relationship("User", backref="quota_usage")


# ==================== MODULE 37: ADVANCED AUTH ====================

class OAuthProvider(Base):
    __tablename__ = "oauth_providers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(SQLEnum(AuthProvider), nullable=False, index=True)
    provider_user_id = Column(String(255), nullable=False)
    access_token = Column(String(500))
    refresh_token = Column(String(500))
    expires_at = Column(DateTime(timezone=True))
    connected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="oauth_providers")


class MFASetup(Base):
    __tablename__ = "mfa_setup"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    mfa_method = Column(SQLEnum(MFAMethod), nullable=False)
    secret = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    backup_codes = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="mfa_setup")


# ==================== MODULE 38: GDPR & PRIVACY ====================

class PrivacySettings(Base):
    __tablename__ = "privacy_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    profile_visibility = Column(SQLEnum(PrivacyLevel), default=PrivacyLevel.PUBLIC)
    content_visibility = Column(SQLEnum(PrivacyLevel), default=PrivacyLevel.PUBLIC)
    allow_analytics = Column(Boolean, default=True)
    allow_marketing = Column(Boolean, default=False)
    data_retention_days = Column(Integer, default=2555)

    user = relationship("User", backref="privacy_settings")


class DataDeletionRequest(Base):
    __tablename__ = "data_deletion_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending")
    requested_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    scheduled_for = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="deletion_requests")


class ConsentLog(Base):
    __tablename__ = "consent_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    consent_type = Column(String(100), nullable=False)
    version = Column(String(50))
    granted = Column(Boolean, default=False)
    ip_address = Column(String(45))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="consent_logs")


# ==================== MODULE 39: CACHING ====================

class CachePolicy(Base):
    __tablename__ = "cache_policies"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(100), nullable=False, unique=True)
    cache_type = Column(SQLEnum(CacheType), default=CacheType.REDIS)
    ttl_seconds = Column(Integer, default=3600)
    max_size_mb = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)

    __table_args__ = (Index("ix_cache_type", "cache_type"),)


class CacheMetric(Base):
    __tablename__ = "cache_metrics"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    hits = Column(Integer, default=0)
    misses = Column(Integer, default=0)
    evictions = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0.0)
    measured_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ==================== MODULE 40: PUSH NOTIFICATIONS ====================

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_id = Column(String(255), nullable=False)
    token = Column(String(500), nullable=False, unique=True)
    platform = Column(String(50))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="device_tokens")


class PushNotification(Base):
    __tablename__ = "push_notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    data = Column(JSON, default={})
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    read_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="push_notifications")
