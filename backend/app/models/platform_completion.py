from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class InteractionType(str, enum.Enum):
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    FOLLOW = "follow"
    BOOKMARK = "bookmark"


class SearchIndexType(str, enum.Enum):
    CONTENT = "content"
    USER = "user"
    TOPIC = "topic"
    AUTHOR = "author"


class PushNotificationType(str, enum.Enum):
    ENGAGEMENT = "engagement"
    CONTENT = "content"
    SOCIAL = "social"
    SYSTEM = "system"
    PROMOTIONAL = "promotional"


class AdminActionType(str, enum.Enum):
    USER_MANAGE = "user_manage"
    CONTENT_MANAGE = "content_manage"
    SYSTEM_CONFIG = "system_config"
    AUDIT = "audit"
    SECURITY = "security"


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    interaction_type = Column(Enum(InteractionType), nullable=False)
    target_id = Column(Integer, nullable=False)
    target_type = Column(String(50), nullable=False)
    content = Column(Text)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_interaction_type", "interaction_type"),
        Index("idx_target_id", "target_id"),
        Index("idx_created_at", "created_at"),
    )


class UserFollow(Base):
    __tablename__ = "user_follows"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, nullable=False)
    following_id = Column(Integer, nullable=False)
    followed_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_follow"),
        Index("idx_follower_id", "follower_id"),
        Index("idx_following_id", "following_id"),
    )


class ContentComment(Base):
    __tablename__ = "content_comments"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    parent_comment_id = Column(Integer)
    text = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    edited_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_content_id", "content_id"),
        Index("idx_user_id", "user_id"),
        Index("idx_parent_comment_id", "parent_comment_id"),
    )


class UserMessage(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    subject = Column(String(255))
    body = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_sender_id", "sender_id"),
        Index("idx_recipient_id", "recipient_id"),
        Index("idx_read", "read"),
    )


class SearchIndex(Base):
    __tablename__ = "search_indexes"

    id = Column(Integer, primary_key=True)
    index_type = Column(Enum(SearchIndexType), nullable=False)
    target_id = Column(Integer, nullable=False)
    title = Column(String(500))
    description = Column(Text)
    keywords = Column(ARRAY(String), default=[])
    embedding_vector = Column(ARRAY(Float))
    metadata = Column(JSON, default={})
    indexed_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_index_type", "index_type"),
        Index("idx_target_id", "target_id"),
        Index("idx_keywords", "keywords"),
    )


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    query = Column(String(500), nullable=False)
    filters = Column(JSON, default={})
    result_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
    )


class PushNotificationConfig(Base):
    __tablename__ = "push_notification_configs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    device_token = Column(String(500))
    platform = Column(String(50))
    enabled = Column(Boolean, default=True)
    notification_types = Column(ARRAY(String), default=[])
    quiet_hours_start = Column(String(5))
    quiet_hours_end = Column(String(5))
    last_sync = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_device_token", "device_token"),
    )


class PushNotificationLog(Base):
    __tablename__ = "push_notification_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    notification_type = Column(Enum(PushNotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text)
    deep_link = Column(String(500))
    sent_at = Column(DateTime, server_default=func.now())
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    status = Column(String(50), default="sent")

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_notification_type", "notification_type"),
        Index("idx_status", "status"),
    )


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    permissions = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_role", "role"),
    )


class AdminActionLog(Base):
    __tablename__ = "admin_action_logs"

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, nullable=False)
    action_type = Column(Enum(AdminActionType), nullable=False)
    target_id = Column(Integer)
    target_type = Column(String(100))
    details = Column(JSON, default={})
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_admin_id", "admin_id"),
        Index("idx_action_type", "action_type"),
        Index("idx_created_at", "created_at"),
    )


class SystemNotification(Base):
    __tablename__ = "system_notifications"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(50), default="info")
    category = Column(String(100))
    target_users = Column(ARRAY(Integer), default=[])
    broadcast = Column(Boolean, default=False)
    acknowledged_by = Column(ARRAY(Integer), default=[])
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)

    __table_args__ = (
        Index("idx_severity", "severity"),
        Index("idx_created_at", "created_at"),
    )


class PlatformStatistics(Base):
    __tablename__ = "platform_statistics"

    id = Column(Integer, primary_key=True)
    total_users = Column(BigInteger, default=0)
    active_users = Column(BigInteger, default=0)
    total_content = Column(BigInteger, default=0)
    total_interactions = Column(BigInteger, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    server_health = Column(Float, default=100.0)
    measured_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_measured_at", "measured_at"),
    )
