"""Activity logs and audit trail models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class ActionType(str, enum.Enum):
    """Activity action types"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    SHARE = "share"
    DOWNLOAD = "download"


class EntityType(str, enum.Enum):
    """Entity types for audit"""
    USER = "user"
    ORGANIZATION = "organization"
    PROJECT = "project"
    DOCUMENT = "document"
    SETTING = "setting"
    NOTIFICATION = "notification"
    PROFILE = "profile"
    TENANT = "tenant"
    ROLE = "role"
    PERMISSION = "permission"


class ActivityLog(Base):
    """Activity log - records all user actions"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Action details
    action = Column(SQLEnum(ActionType), nullable=False, index=True)
    entity_type = Column(SQLEnum(EntityType), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False)

    # Description and details
    description = Column(Text)
    status = Column(String(50), default="success")  # success, failure
    error_message = Column(Text)

    # IP and user agent
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))

    # Metadata
    extra_data = Column(JSON, default={})

    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_activity_user", "user_id"),
        Index("idx_activity_entity", "entity_type", "entity_id"),
        Index("idx_activity_action", "action"),
        Index("idx_activity_created", "created_at"),
        Index("idx_activity_user_created", "user_id", "created_at"),
    )

    # Relationships
    user = relationship("User", back_populates="activity_logs")


class AuditLog(Base):
    """Audit log - tracks changes to entities"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Entity info
    entity_type = Column(SQLEnum(EntityType), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False)

    # Change details
    action = Column(SQLEnum(ActionType), nullable=False)  # create, update, delete

    # Before and after values (for updates)
    old_values = Column(JSON)  # Previous values
    new_values = Column(JSON)  # Current values
    changed_fields = Column(JSON, default=[])  # List of changed field names

    # Metadata
    reason = Column(Text)  # Why was the change made?
    request_id = Column(String(100), index=True)  # Request ID for tracing

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_audit_user", "user_id"),
        Index("idx_audit_entity", "entity_type", "entity_id"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_created", "created_at"),
    )


class ActivityFeed(Base):
    """Activity feed - user-specific activity stream"""
    __tablename__ = "activity_feeds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Activity reference
    activity_log_id = Column(Integer, ForeignKey("activity_logs.id", ondelete="CASCADE"), nullable=True)

    # Feed metadata
    actor_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(SQLEnum(ActionType), nullable=False)

    # What changed
    entity_type = Column(SQLEnum(EntityType), nullable=False)
    entity_id = Column(Integer, nullable=False)

    # Display info
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Feed status
    is_read = Column(Boolean, default=False, index=True)
    is_archived = Column(Boolean, default=False)

    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_feed_user", "user_id"),
        Index("idx_feed_user_read", "user_id", "is_read"),
        Index("idx_feed_entity", "entity_type", "entity_id"),
        Index("idx_feed_created", "created_at"),
    )


class RetentionPolicy(Base):
    """Data retention policy for logs"""
    __tablename__ = "retention_policies"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(SQLEnum(EntityType), nullable=False, unique=True)

    # Retention settings
    retention_days = Column(Integer, default=90)  # Keep logs for this many days
    archive_days = Column(Integer, default=30)  # Archive after this many days
    delete_after_archive = Column(Boolean, default=True)  # Auto-delete archived logs

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
