"""Content management schemas"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.content import ContentType, ContentStatus, ContentAccessLevel, VideoQuality


# Category Schemas
class ContentCategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class ContentCategoryCreate(ContentCategoryBase):
    """Create category"""
    pass


class ContentCategoryUpdate(BaseModel):
    """Update category"""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class ContentCategoryResponse(ContentCategoryBase):
    """Category response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Tag Schemas
class ContentTagBase(BaseModel):
    """Base tag schema"""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class ContentTagCreate(ContentTagBase):
    """Create tag"""
    pass


class ContentTagUpdate(BaseModel):
    """Update tag"""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ContentTagResponse(ContentTagBase):
    """Tag response"""
    id: int
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Media File Schemas
class MediaFileBase(BaseModel):
    """Base media file schema"""
    file_name: str
    file_type: str
    mime_type: str
    file_url: str
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class MediaFileCreate(MediaFileBase):
    """Create media file"""
    file_size: Optional[int] = None
    thumbnail_url: Optional[str] = None


class MediaFileUpdate(BaseModel):
    """Update media file"""
    alt_text: Optional[str] = None
    caption: Optional[str] = None


class MediaFileResponse(MediaFileBase):
    """Media file response"""
    id: int
    file_size: Optional[int]
    thumbnail_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Video Schemas
class VideoBase(BaseModel):
    """Base video schema"""
    source_url: str
    duration_seconds: Optional[int] = None
    mime_type: Optional[str] = "video/mp4"
    has_transcription: bool = False
    has_captions: bool = False
    is_live: bool = False
    allow_download: bool = False


class VideoCreate(VideoBase):
    """Create video"""
    hls_manifest_url: Optional[str] = None
    dash_manifest_url: Optional[str] = None


class VideoUpdate(BaseModel):
    """Update video"""
    source_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    hls_manifest_url: Optional[str] = None
    dash_manifest_url: Optional[str] = None
    has_transcription: Optional[bool] = None
    has_captions: Optional[bool] = None
    allow_download: Optional[bool] = None


class VideoResponse(VideoBase):
    """Video response"""
    id: int
    content_id: int
    encoding_status: str
    encoding_progress: float
    available_qualities: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Main Content Schemas
class ContentBase(BaseModel):
    """Base content schema"""
    title: str = Field(..., min_length=1, max_length=500)
    slug: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    body: Optional[str] = None
    content_type: ContentType
    category_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    featured_image_url: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None


class ContentCreate(ContentBase):
    """Create content"""
    status: ContentStatus = ContentStatus.DRAFT
    access_level: ContentAccessLevel = ContentAccessLevel.PUBLIC
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    is_featured: bool = False
    is_commentable: bool = True
    is_shareable: bool = True
    allow_embedding: bool = True
    tag_ids: List[int] = []
    video: Optional[VideoCreate] = None


class ContentUpdate(BaseModel):
    """Update content"""
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    category_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    featured_image_url: Optional[str] = None
    status: Optional[ContentStatus] = None
    access_level: Optional[ContentAccessLevel] = None
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    is_featured: Optional[bool] = None
    is_commentable: Optional[bool] = None
    is_shareable: Optional[bool] = None
    allow_embedding: Optional[bool] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class ContentResponse(ContentBase):
    """Content response"""
    id: int
    status: ContentStatus
    access_level: ContentAccessLevel
    creator_user_id: Optional[int]
    category_id: Optional[int]
    views_count: int
    likes_count: int
    comments_count: int
    shares_count: int
    is_featured: bool
    published_at: Optional[datetime]
    scheduled_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tags: List[ContentTagResponse] = []
    videos: List[VideoResponse] = []

    class Config:
        from_attributes = True


class ContentDetailResponse(ContentResponse):
    """Detailed content response with all relationships"""
    media_files: List[MediaFileResponse] = []
    category: Optional[ContentCategoryResponse] = None


class ContentListResponse(BaseModel):
    """Content list response with pagination"""
    items: List[ContentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Engagement Schemas
class ContentEngagementCreate(BaseModel):
    """Create engagement"""
    engagement_type: str = Field(..., min_length=1, max_length=50)
    watch_seconds: int = 0
    watch_percentage: float = 0.0


class ContentEngagementResponse(BaseModel):
    """Engagement response"""
    id: int
    content_id: int
    user_id: Optional[int]
    engagement_type: str
    watch_seconds: int
    watch_percentage: float
    created_at: datetime

    class Config:
        from_attributes = True


# Bulk Operations
class ContentBulkUpdateRequest(BaseModel):
    """Bulk update content"""
    content_ids: List[int]
    status: Optional[ContentStatus] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_featured: Optional[bool] = None


class ContentBulkDeleteRequest(BaseModel):
    """Bulk delete content"""
    content_ids: List[int]


# Search and Filter
class ContentSearchRequest(BaseModel):
    """Search content"""
    query: Optional[str] = None
    content_type: Optional[ContentType] = None
    status: Optional[ContentStatus] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    access_level: Optional[ContentAccessLevel] = None
    is_featured: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
    page: int = 1
    page_size: int = 20


# Publish Workflow
class PublishContentRequest(BaseModel):
    """Publish content"""
    published_at: Optional[datetime] = None
    access_level: ContentAccessLevel = ContentAccessLevel.PUBLIC


class ScheduleContentRequest(BaseModel):
    """Schedule content for publication"""
    scheduled_at: datetime


class ArchiveContentRequest(BaseModel):
    """Archive content"""
    reason: Optional[str] = None
