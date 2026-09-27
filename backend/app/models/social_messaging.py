"""Social, Messaging & Discovery models: Modules 51-55"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class ModerationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"


class NotificationType(str, enum.Enum):
    FOLLOW = "follow"
    MENTION = "mention"
    COMMENT = "comment"
    LIKE = "like"
    MESSAGE = "message"


class MessageType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"


class SearchType(str, enum.Enum):
    USER = "user"
    CONTENT = "content"
    TAG = "tag"
    KEYWORD = "keyword"


# ==================== MODULE 51: CONTENT MODERATION ====================

class ContentModerationRule(Base):
    __tablename__ = "content_moderation_rules"
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(255), nullable=False, unique=True)
    pattern = Column(Text, nullable=False)
    action = Column(String(50), default="flag")
    severity = Column(String(50), default="medium")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ModerationReport(Base):
    __tablename__ = "moderation_reports"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False, index=True)
    reported_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reason = Column(String(255), nullable=False)
    status = Column(SQLEnum(ModerationStatus), default=ModerationStatus.PENDING, index=True)
    notes = Column(Text)
    reported_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    content = relationship("Content", backref="moderation_reports")
    reporter = relationship("User", foreign_keys=[reported_by], backref="reports_made")


class ContentApproval(Base):
    __tablename__ = "content_approvals"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False, unique=True)
    status = Column(SQLEnum(ModerationStatus), default=ModerationStatus.PENDING)
    reviewer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(Text)

    content = relationship("Content", backref="approval")
    reviewer = relationship("User", foreign_keys=[reviewer_id], backref="approvals_given")


# ==================== MODULE 52: SOCIAL FEATURES ====================

class UserFollow(Base):
    __tablename__ = "user_follows"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    followed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="uq_user_follow"),)

    follower = relationship("User", foreign_keys=[follower_id], backref="following")
    followed_user = relationship("User", foreign_keys=[following_id], backref="followers")


class Mention(Base):
    __tablename__ = "mentions"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    mentioned_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    mentioned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    content = relationship("Content", backref="mentions")
    mentioned_user = relationship("User", foreign_keys=[mentioned_user_id], backref="mentions_received")
    mentioner = relationship("User", foreign_keys=[mentioned_by], backref="mentions_made")


class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(255), nullable=False, unique=True, index=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ContentHashtag(Base):
    __tablename__ = "content_hashtags"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    hashtag_id = Column(Integer, ForeignKey("hashtags.id", ondelete="CASCADE"), nullable=False)

    content = relationship("Content", backref="hashtags")
    hashtag = relationship("Hashtag", backref="content_links")


# ==================== MODULE 53: MESSAGING ====================

class DirectMessage(Base):
    __tablename__ = "direct_messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(SQLEnum(MessageType), default=MessageType.TEXT)
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)

    sender = relationship("User", foreign_keys=[sender_id], backref="messages_sent")
    recipient = relationship("User", foreign_keys=[recipient_id], backref="messages_received")


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    participant_ids = Column(JSON)
    last_message_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ==================== MODULE 54: NOTIFICATIONS ====================

class UserNotification(Base):
    __tablename__ = "user_notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    read_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", foreign_keys=[user_id], backref="notifications")
    actor = relationship("User", foreign_keys=[actor_id], backref="notifications_caused")
    content = relationship("Content", backref="notifications")


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    notify_follows = Column(Boolean, default=True)
    notify_mentions = Column(Boolean, default=True)
    notify_comments = Column(Boolean, default=True)
    notify_messages = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=False)

    user = relationship("User", backref="notification_preferences")


# ==================== MODULE 55: SEARCH & DISCOVERY ====================

class SearchQuery(Base):
    __tablename__ = "search_queries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    query = Column(String(500), nullable=False)
    search_type = Column(SQLEnum(SearchType), default=SearchType.KEYWORD)
    results_count = Column(Integer, default=0)
    searched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="search_queries")


class DiscoveryRecommendation(Base):
    __tablename__ = "discovery_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    recommendation_score = Column(Float, default=0.0)
    reason = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="recommendations")
    content = relationship("Content", backref="recommended_to")


class TrendingTopic(Base):
    __tablename__ = "trending_topics"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False, unique=True, index=True)
    mention_count = Column(Integer, default=0)
    trend_score = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
