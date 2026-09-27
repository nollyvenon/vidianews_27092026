"""Settings models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class SystemSetting(Base):
    """Application-wide system settings"""
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    data_type = Column(String(50))  # string, boolean, integer, json
    description = Column(Text)
    is_public = Column(Boolean, default=False)  # Can be read by any user
    is_secret = Column(Boolean, default=False)  # Hidden value (encrypted)

    category = Column(String(100))  # mail, storage, features, etc.

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_key", "key"),
        Index("idx_category", "category"),
    )


class UserSetting(Base):
    """User-specific settings"""
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)
    data_type = Column(String(50))  # string, boolean, integer, json

    category = Column(String(100))  # notifications, privacy, display, etc.

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_user_key", "user_id", "key"),
        Index("idx_user_category", "user_id", "category"),
    )


class TenantSetting(Base):
    """Tenant-specific settings"""
    __tablename__ = "tenant_settings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)

    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)
    data_type = Column(String(50))
    description = Column(Text)

    category = Column(String(100))  # billing, features, branding, etc.

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_tenant_key", "tenant_id", "key"),
        Index("idx_tenant_category", "tenant_id", "category"),
    )


class NotificationPreference(Base):
    """User notification preferences"""
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Email notifications
    email_on_activity = Column(Boolean, default=True)
    email_on_mention = Column(Boolean, default=True)
    email_on_message = Column(Boolean, default=True)
    email_digest = Column(String(50), default="daily")  # never, daily, weekly, realtime

    # Push notifications
    push_enabled = Column(Boolean, default=True)
    push_on_activity = Column(Boolean, default=True)
    push_on_message = Column(Boolean, default=True)

    # In-app notifications
    inapp_enabled = Column(Boolean, default=True)
    inapp_sound = Column(Boolean, default=False)

    # Do not disturb
    dnd_enabled = Column(Boolean, default=False)
    dnd_start_time = Column(String(10))  # HH:MM format
    dnd_end_time = Column(String(10))    # HH:MM format

    # Unsubscribe tokens
    unsubscribe_token = Column(String(255), unique=True, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PrivacySetting(Base):
    """User privacy settings"""
    __tablename__ = "privacy_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    profile_visibility = Column(String(50), default="private")  # public, friends_only, private
    show_email = Column(Boolean, default=False)
    show_phone = Column(Boolean, default=False)
    show_activity = Column(Boolean, default=False)
    show_last_seen = Column(Boolean, default=True)
    allow_messages = Column(String(50), default="everyone")  # everyone, friends_only, nobody
    allow_search = Column(Boolean, default=True)

    # Data sharing
    allow_analytics = Column(Boolean, default=True)
    allow_marketing_emails = Column(Boolean, default=True)
    allow_third_party_sharing = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class DisplaySetting(Base):
    """User display/UI preferences"""
    __tablename__ = "display_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    theme = Column(String(50), default="light")  # light, dark, auto
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    date_format = Column(String(50), default="YYYY-MM-DD")
    time_format = Column(String(50), default="24h")  # 24h, 12h

    # UI preferences
    sidebar_collapsed = Column(Boolean, default=False)
    compact_mode = Column(Boolean, default=False)
    animations_enabled = Column(Boolean, default=True)

    # Font and size
    font_size = Column(String(50), default="medium")  # small, medium, large

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
