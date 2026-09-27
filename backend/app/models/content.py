"""Content management models for videos and articles"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Float, Index, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class ContentType(str, enum.Enum):
    """Content types"""
    VIDEO = "video"
    ARTICLE = "article"
    BLOG_POST = "blog_post"
    NEWSLETTER = "newsletter"


class ContentStatus(str, enum.Enum):
    """Content publication status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ContentAccessLevel(str, enum.Enum):
    """Content access levels"""
    PUBLIC = "public"
    MEMBERS_ONLY = "members_only"
    PREMIUM = "premium"
    PRIVATE = "private"


class VideoQuality(str, enum.Enum):
    """Video quality tiers"""
    PREVIEW = "preview"
    SD = "sd"
    HD = "hd"
    FULL_HD = "full_hd"
    UHD_4K = "uhd_4k"


# Association table for content tags
content_tags = Table(
    "content_tags_association",
    Base.metadata,
    Column("content_id", Integer, ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("content_tags.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_content_tags_content", "content_id"),
    Index("idx_content_tags_tag", "tag_id"),
)


class ContentCategory(Base):
    """Content categories for organizing content"""
    __tablename__ = "content_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    icon_url = Column(String(500))

    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    contents = relationship("Content", back_populates="category")

    __table_args__ = (
        Index("idx_category_active", "is_active"),
        Index("idx_category_slug", "slug"),
    )


class ContentTag(Base):
    """Tags for organizing and discovering content"""
    __tablename__ = "content_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)

    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    usage_count = Column(Integer, default=0)  # Denormalized for performance

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_tag_active", "is_active"),
        Index("idx_tag_slug", "slug"),
    )


class Content(Base):
    """Main content table for videos and articles"""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)

    # Core metadata
    title = Column(String(500), nullable=False, index=True)
    slug = Column(String(500), nullable=False, unique=True, index=True)
    description = Column(Text)
    body = Column(Text)  # Full content for articles

    # Author and ownership
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Classification
    content_type = Column(SQLEnum(ContentType), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("content_categories.id", ondelete="SET NULL"), nullable=True, index=True)

    # Media
    thumbnail_url = Column(String(500))
    featured_image_url = Column(String(500))

    # Publication workflow
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT, nullable=False, index=True)
    access_level = Column(SQLEnum(ContentAccessLevel), default=ContentAccessLevel.PUBLIC, nullable=False)

    # Publication dates
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # SEO metadata
    seo_title = Column(String(255))
    seo_description = Column(String(500))
    seo_keywords = Column(String(500))

    # Engagement metrics
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)

    # Visibility and settings
    is_featured = Column(Boolean, default=False, index=True)
    is_commentable = Column(Boolean, default=True)
    is_shareable = Column(Boolean, default=True)
    allow_embedding = Column(Boolean, default=True)

    # Additional metadata
    extra_data = Column(JSON, default={})
    custom_metadata = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_content_type", "content_type"),
        Index("idx_content_status", "status"),
        Index("idx_content_creator", "creator_user_id"),
        Index("idx_content_category", "category_id"),
        Index("idx_content_featured", "is_featured"),
        Index("idx_content_published", "published_at"),
        Index("idx_content_created", "created_at"),
        UniqueConstraint("slug", name="uq_content_slug"),
    )

    # Relationships
    creator = relationship("User", foreign_keys=[creator_user_id], backref="created_contents")
    updated_by = relationship("User", foreign_keys=[updated_by_user_id])
    category = relationship("ContentCategory", back_populates="contents")
    videos = relationship("Video", back_populates="content", cascade="all, delete-orphan")
    media_files = relationship("MediaFile", back_populates="content", cascade="all, delete-orphan")
    tags = relationship("ContentTag", secondary=content_tags, backref="contents")
    engagement = relationship("ContentEngagement", back_populates="content", cascade="all, delete-orphan")


class Video(Base):
    """Video-specific metadata and processing"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Video properties
    duration_seconds = Column(Integer)  # Video duration
    mime_type = Column(String(50))  # video/mp4, etc.

    # Transcoding and quality
    source_url = Column(String(500), nullable=False)
    hls_manifest_url = Column(String(500))  # For adaptive streaming
    dash_manifest_url = Column(String(500))  # For DASH streaming

    # Encoding status
    encoding_status = Column(String(50), default="pending")  # pending, in_progress, completed, failed
    encoding_progress = Column(Float, default=0.0)  # 0-100
    encoding_error = Column(Text)

    # Transcription and captions
    has_transcription = Column(Boolean, default=False)
    transcription_url = Column(String(500))
    has_captions = Column(Boolean, default=False)
    caption_url = Column(String(500))

    # Video quality available
    available_qualities = Column(JSON, default=[])  # List of available quality versions

    # Streaming configuration
    is_live = Column(Boolean, default=False)
    live_stream_url = Column(String(500))
    allow_download = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_video_content", "content_id"),
        Index("idx_video_encoding_status", "encoding_status"),
    )

    # Relationships
    content = relationship("Content", back_populates="videos")


class MediaFile(Base):
    """Media files associated with content (images, documents, etc.)"""
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)

    # File information
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # image, video, document, etc.
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer)  # Size in bytes

    # URLs
    file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))

    # For images
    width = Column(Integer)
    height = Column(Integer)

    # Metadata
    alt_text = Column(String(255))
    caption = Column(Text)
    extra_data = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_media_content", "content_id"),
        Index("idx_media_type", "file_type"),
    )

    # Relationships
    content = relationship("Content", back_populates="media_files")


class ContentEngagement(Base):
    """User engagement with content"""
    __tablename__ = "content_engagement"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    # Engagement type
    engagement_type = Column(String(50), nullable=False)  # view, like, comment, share, bookmark

    # Engagement data
    session_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(String(500))

    # Watch time (for videos)
    watch_seconds = Column(Integer, default=0)
    watch_percentage = Column(Float, default=0.0)

    # Metadata
    extra_data = Column(JSON, default={})

    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_engagement_content", "content_id"),
        Index("idx_engagement_user", "user_id"),
        Index("idx_engagement_type", "engagement_type"),
        Index("idx_engagement_created", "created_at"),
    )

    # Relationships
    content = relationship("Content", back_populates="engagement")
    user = relationship("User", backref="content_engagement")
