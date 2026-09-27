"""Advanced feature models: Modules 26-30"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class PermissionLevel(str, enum.Enum):
    NONE = "none"
    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"
    MANAGE = "manage"
    ADMIN = "admin"


class StorageProvider(str, enum.Enum):
    S3 = "s3"
    AZURE = "azure"
    GCS = "gcs"
    LOCAL = "local"


class VideoQualityLevel(str, enum.Enum):
    HD = "hd"
    FULL_HD = "full_hd"
    FOUR_K = "four_k"
    AUDIO_ONLY = "audio_only"


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReactionType(str, enum.Enum):
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


# ==================== MODULE 26: ADVANCED PERMISSIONS ====================

class ResourcePermission(Base):
    __tablename__ = "resource_permissions"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=True, index=True)
    permission_level = Column(SQLEnum(PermissionLevel), nullable=False, index=True)
    granted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="resource_permissions")
    role = relationship("Role", backref="resource_permissions")
    __table_args__ = (Index("ix_resource_perm", "resource_type", "resource_id", "user_id"),)


class ShareLink(Base):
    __tablename__ = "share_links"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer, nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_level = Column(SQLEnum(PermissionLevel), default=PermissionLevel.VIEW)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    access_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    creator = relationship("User", backref="share_links")


# ==================== MODULE 27: FILE MANAGEMENT & STORAGE ====================

class StorageFile(Base):
    __tablename__ = "storage_files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    provider = Column(SQLEnum(StorageProvider), default=StorageProvider.S3)
    url = Column(String(500), nullable=False)
    versions = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="storage_files")
    organization = relationship("Organization", backref="storage_files")


class CDNUrl(Base):
    __tablename__ = "cdn_urls"
    id = Column(Integer, primary_key=True, index=True)
    storage_file_id = Column(Integer, ForeignKey("storage_files.id", ondelete="CASCADE"), nullable=False)
    cdn_url = Column(String(500), nullable=False)
    cdn_provider = Column(String(100))
    cache_control = Column(String(100))
    bandwidth_used = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    storage_file = relationship("StorageFile", backref="cdn_urls")


# ==================== MODULE 28: VIDEO PROCESSING ====================

class VideoProcess(Base):
    __tablename__ = "video_processes"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    quality_level = Column(SQLEnum(VideoQualityLevel), nullable=False)
    status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING, index=True)
    file_key = Column(String(500))
    duration = Column(Integer)
    bitrate = Column(Integer)
    resolution = Column(String(20))
    progress = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    video = relationship("Video", backref="processes")


class Thumbnail(Base):
    __tablename__ = "thumbnails"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    file_key = Column(String(500), nullable=False)
    url = Column(String(500), nullable=False)
    timestamp = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    video = relationship("Video", backref="thumbnails")


# ==================== MODULE 29: COMMENTS & COLLABORATION ====================

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, index=True)
    content = Column(Text, nullable=False)
    mentions = Column(JSON, default=[])
    is_edited = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="comments")
    replies = relationship("Comment", remote_side=[parent_comment_id], backref="parent")
    __table_args__ = (Index("ix_comment_resource", "resource_type", "resource_id"),)


class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reaction_type = Column(SQLEnum(ReactionType), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    comment = relationship("Comment", backref="reactions")
    user = relationship("User", backref="reactions")


class Mention(Base):
    __tablename__ = "mentions"
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    mentioned_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_notified = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    comment = relationship("Comment", backref="mention_records")
    user = relationship("User", backref="mentions")


# ==================== MODULE 30: RECOMMENDATIONS ENGINE ====================

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    preferred_categories = Column(JSON, default=[])
    preferred_creators = Column(JSON, default=[])
    watch_history = Column(JSON, default=[])
    engagement_score = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="preferences")


class Recommendation(Base):
    __tablename__ = "recommendations_engine"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, nullable=False, index=True)
    score = Column(Float, nullable=False)
    reason = Column(String(255))
    algorithm = Column(String(100))
    is_clicked = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="recommendations_engine")


class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    embedding = Column(JSON)
    cohort = Column(String(100))
    traits = Column(JSON, default={})
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="personalization_profile")
