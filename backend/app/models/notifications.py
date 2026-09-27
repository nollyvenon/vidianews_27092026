"""Notification models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class NotificationType(str, enum.Enum):
    """Notification type enumeration"""
    ACTIVITY = "activity"
    MESSAGE = "message"
    MENTION = "mention"
    SYSTEM = "system"
    ALERT = "alert"
    REMINDER = "reminder"


class NotificationChannel(str, enum.Enum):
    """Notification delivery channel"""
    EMAIL = "email"
    PUSH = "push"
    INAPP = "in_app"


class Notification(Base):
    """In-app notification"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Notification content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(SQLEnum(NotificationType), default=NotificationType.SYSTEM, index=True)

    # Related resource
    resource_type = Column(String(50))  # user, organization, project, etc.
    resource_id = Column(Integer)
    action_url = Column(String(500))  # URL to navigate to when clicked

    # Status
    is_read = Column(Boolean, default=False, index=True)
    is_archived = Column(Boolean, default=False, index=True)

    # Extra data (metadata)
    extra_data = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_notif_user_read", "user_id", "is_read"),
        Index("idx_notif_user_created", "user_id", "created_at"),
        Index("idx_notif_type", "notification_type"),
    )


class EmailNotification(Base):
    """Email notification record"""
    __tablename__ = "email_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_email = Column(String(255), nullable=False)

    # Email content
    subject = Column(String(255), nullable=False)
    template = Column(String(100), nullable=False)  # email_verification, password_reset, etc.

    # Status
    status = Column(String(50), default="pending", index=True)  # pending, sent, bounced, failed

    # Tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)

    # Error info
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # Related notification
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_email_notif_user", "user_id"),
        Index("idx_email_notif_status", "status"),
        Index("idx_email_notif_recipient", "recipient_email"),
    )


class PushNotification(Base):
    """Push notification record"""
    __tablename__ = "push_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_token = Column(String(500), nullable=False)

    # Push content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    # Status
    status = Column(String(50), default="pending", index=True)  # pending, sent, failed

    # Platform
    platform = Column(String(50), default="mobile")  # mobile, web

    # Tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Error info
    error_message = Column(Text)

    # Related notification
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_push_notif_user", "user_id"),
        Index("idx_push_notif_status", "status"),
        Index("idx_push_notif_device", "device_token"),
    )


class NotificationTemplate(Base):
    """Email/push notification templates"""
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # Template content
    subject = Column(String(255))  # For emails
    title_template = Column(String(255), nullable=False)
    body_template = Column(Text, nullable=False)

    # Template variables (JSON)
    variables = Column(JSON, default=[])  # ["user_name", "action_url", ...]

    # Channel
    channel = Column(SQLEnum(NotificationChannel), default=NotificationChannel.EMAIL)

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class NotificationLog(Base):
    """Audit log for notification delivery"""
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Related records
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="SET NULL"), nullable=True)

    # Log details
    action = Column(String(50), nullable=False)  # created, sent, opened, clicked, failed
    channel = Column(SQLEnum(NotificationChannel))
    status = Column(String(50))
    message = Column(Text)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_notif_log_user", "user_id"),
        Index("idx_notif_log_action", "action"),
    )
