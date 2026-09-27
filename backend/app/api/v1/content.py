"""Content management API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.content import ContentType, ContentStatus, ContentAccessLevel
from app.services.content_service import ContentService
from app.schemas.content import (
    ContentCategoryCreate, ContentCategoryUpdate, ContentCategoryResponse,
    ContentTagCreate, ContentTagUpdate, ContentTagResponse,
    ContentCreate, ContentUpdate, ContentResponse, ContentDetailResponse, ContentListResponse,
    VideoCreate, VideoUpdate, VideoResponse,
    MediaFileCreate, MediaFileResponse,
    ContentEngagementCreate, ContentEngagementResponse,
    PublishContentRequest, ScheduleContentRequest, ArchiveContentRequest,
    ContentSearchRequest, ContentBulkUpdateRequest, ContentBulkDeleteRequest
)

router = APIRouter(prefix="/content", tags=["content"])


# Category Endpoints
@router.post("/categories", response_model=ContentCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    req: ContentCategoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new content category"""
    service = ContentService(session)
    return await service.create_category(
        name=req.name,
        slug=req.slug,
        description=req.description,
        icon_url=req.icon_url,
        sort_order=req.sort_order
    )


@router.get("/categories", response_model=List[ContentCategoryResponse])
async def list_categories(
    is_active: bool = Query(True),
    limit: int = Query(100, le=1000),
    session: AsyncSession = Depends(get_db),
):
    """List content categories"""
    service = ContentService(session)
    return await service.get_categories(is_active=is_active, limit=limit)


@router.get("/categories/{category_id}", response_model=ContentCategoryResponse)
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get category by ID"""
    service = ContentService(session)
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=ContentCategoryResponse)
async def update_category(
    category_id: int,
    req: ContentCategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update category"""
    service = ContentService(session)
    category = await service.update_category(category_id, **req.model_dump(exclude_unset=True))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete category"""
    service = ContentService(session)
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


# Tag Endpoints
@router.post("/tags", response_model=ContentTagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    req: ContentTagCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new tag"""
    service = ContentService(session)
    return await service.create_tag(name=req.name, slug=req.slug, description=req.description)


@router.get("/tags", response_model=List[ContentTagResponse])
async def list_tags(
    is_active: bool = Query(True),
    session: AsyncSession = Depends(get_db),
):
    """List tags"""
    service = ContentService(session)
    return await service.get_tags(is_active=is_active)


@router.get("/tags/{tag_id}", response_model=ContentTagResponse)
async def get_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get tag by ID"""
    service = ContentService(session)
    tag = await service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.put("/tags/{tag_id}", response_model=ContentTagResponse)
async def update_tag(
    tag_id: int,
    req: ContentTagUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update tag"""
    service = ContentService(session)
    tag = await service.update_tag(tag_id, **req.model_dump(exclude_unset=True))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


# Content Endpoints
@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    req: ContentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new content"""
    service = ContentService(session)

    content = await service.create_content(
        title=req.title,
        slug=req.slug,
        content_type=req.content_type,
        creator_user_id=current_user.id,
        description=req.description,
        body=req.body,
        category_id=req.category_id,
        thumbnail_url=req.thumbnail_url,
        featured_image_url=req.featured_image_url,
        status=req.status,
        access_level=req.access_level,
        published_at=req.published_at,
        scheduled_at=req.scheduled_at,
        is_featured=req.is_featured,
        is_commentable=req.is_commentable,
        is_shareable=req.is_shareable,
        allow_embedding=req.allow_embedding,
        seo_title=req.seo_title,
        seo_description=req.seo_description,
        seo_keywords=req.seo_keywords,
    )

    # Add tags
    if req.tag_ids:
        await service.add_tags_to_content(content.id, req.tag_ids)

    # Create video if provided
    if req.video:
        await service.create_video(
            content_id=content.id,
            source_url=req.video.source_url,
            duration_seconds=req.video.duration_seconds,
            mime_type=req.video.mime_type,
            hls_manifest_url=req.video.hls_manifest_url,
            dash_manifest_url=req.video.dash_manifest_url,
        )

    return await service.get_content(content.id)


@router.get("/", response_model=ContentListResponse)
async def list_content(
    content_type: Optional[ContentType] = Query(None),
    status_filter: Optional[ContentStatus] = Query(None, alias="status"),
    category_id: Optional[int] = Query(None),
    is_featured: Optional[bool] = Query(None),
    access_level: Optional[ContentAccessLevel] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("created_at"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    session: AsyncSession = Depends(get_db),
):
    """List content with filters"""
    service = ContentService(session)

    offset = (page - 1) * page_size
    items = await service.list_content(
        content_type=content_type,
        status=status_filter,
        category_id=category_id,
        is_featured=is_featured,
        access_level=access_level,
        limit=page_size,
        offset=offset,
        order_by=order_by,
        order=order
    )

    total = await service.count_total_content(status=status_filter)
    total_pages = (total + page_size - 1) // page_size

    return ContentListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/search", response_model=List[ContentResponse])
async def search_content(
    query: str = Query(..., min_length=1),
    content_type: Optional[ContentType] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    session: AsyncSession = Depends(get_db),
):
    """Search content"""
    service = ContentService(session)
    return await service.search_content(query, content_type, limit=limit, offset=offset)


@router.get("/featured", response_model=List[ContentResponse])
async def get_featured_content(
    content_type: Optional[ContentType] = Query(None),
    limit: int = Query(10, le=50),
    session: AsyncSession = Depends(get_db),
):
    """Get featured content"""
    service = ContentService(session)
    return await service.get_featured_content(content_type=content_type, limit=limit)


@router.get("/trending", response_model=List[ContentResponse])
async def get_trending_content(
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(10, le=50),
    session: AsyncSession = Depends(get_db),
):
    """Get trending content"""
    service = ContentService(session)
    return await service.get_trending_content(days=days, limit=limit)


@router.get("/{content_id}", response_model=ContentDetailResponse)
async def get_content(
    content_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get content by ID"""
    service = ContentService(session)
    content = await service.get_content(content_id, include_engagement=True)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.get("/by-slug/{slug}", response_model=ContentDetailResponse)
async def get_content_by_slug(
    slug: str,
    session: AsyncSession = Depends(get_db),
):
    """Get content by slug"""
    service = ContentService(session)
    content = await service.get_content_by_slug(slug)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    req: ContentUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update content"""
    service = ContentService(session)

    # Update tags if provided
    if req.tag_ids is not None:
        content = await service.get_content(content_id)
        if content:
            current_tag_ids = [t.id for t in content.tags]
            tags_to_remove = set(current_tag_ids) - set(req.tag_ids)
            tags_to_add = set(req.tag_ids) - set(current_tag_ids)

            if tags_to_remove:
                await service.remove_tags_from_content(content_id, list(tags_to_remove))
            if tags_to_add:
                await service.add_tags_to_content(content_id, list(tags_to_add))

    content = await service.update_content(
        content_id,
        current_user.id,
        **req.model_dump(exclude_unset=True, exclude={"tag_ids"})
    )

    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete content"""
    service = ContentService(session)
    deleted = await service.delete_content(content_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")


# Publishing Endpoints
@router.post("/{content_id}/publish", response_model=ContentResponse)
async def publish_content(
    content_id: int,
    req: PublishContentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Publish content"""
    service = ContentService(session)
    content = await service.publish_content(
        content_id,
        current_user.id,
        access_level=req.access_level
    )
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.post("/{content_id}/schedule", response_model=ContentResponse)
async def schedule_content(
    content_id: int,
    req: ScheduleContentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Schedule content"""
    service = ContentService(session)
    content = await service.schedule_content(content_id, req.scheduled_at)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.post("/{content_id}/archive", response_model=ContentResponse)
async def archive_content(
    content_id: int,
    req: ArchiveContentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Archive content"""
    service = ContentService(session)
    content = await service.archive_content(content_id, current_user.id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


# Video Management
@router.post("/{content_id}/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def add_video(
    content_id: int,
    req: VideoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add video to content"""
    service = ContentService(session)
    content = await service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")

    return await service.create_video(
        content_id=content_id,
        source_url=req.source_url,
        duration_seconds=req.duration_seconds,
        mime_type=req.mime_type,
        hls_manifest_url=req.hls_manifest_url,
        dash_manifest_url=req.dash_manifest_url,
    )


@router.get("/{content_id}/videos", response_model=Optional[VideoResponse])
async def get_content_video(
    content_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get video for content"""
    service = ContentService(session)
    return await service.get_content_video(content_id)


@router.put("/{content_id}/videos/{video_id}", response_model=VideoResponse)
async def update_video(
    content_id: int,
    video_id: int,
    req: VideoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update video"""
    service = ContentService(session)
    video = await service.update_video(video_id, **req.model_dump(exclude_unset=True))
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return video


# Media Files
@router.post("/{content_id}/media", response_model=MediaFileResponse, status_code=status.HTTP_201_CREATED)
async def add_media_file(
    content_id: int,
    req: MediaFileCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add media file to content"""
    service = ContentService(session)
    return await service.add_media_file(
        content_id=content_id,
        file_name=req.file_name,
        file_type=req.file_type,
        mime_type=req.mime_type,
        file_url=req.file_url,
        file_size=req.file_size,
        thumbnail_url=req.thumbnail_url,
        alt_text=req.alt_text,
        caption=req.caption,
        width=req.width,
        height=req.height,
    )


@router.get("/{content_id}/media", response_model=List[MediaFileResponse])
async def get_media_files(
    content_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get media files for content"""
    service = ContentService(session)
    return await service.get_content_media_files(content_id)


@router.delete("/{content_id}/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media_file(
    content_id: int,
    media_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete media file"""
    service = ContentService(session)
    deleted = await service.delete_media_file(media_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found")


# Engagement
@router.post("/{content_id}/engage", response_model=ContentEngagementResponse, status_code=status.HTTP_201_CREATED)
async def record_engagement(
    content_id: int,
    req: ContentEngagementCreate,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Record user engagement"""
    service = ContentService(session)
    return await service.record_engagement(
        content_id=content_id,
        engagement_type=req.engagement_type,
        user_id=current_user.id if current_user else None,
        watch_seconds=req.watch_seconds,
        watch_percentage=req.watch_percentage,
    )


@router.get("/{content_id}/engagement", response_model=List[ContentEngagementResponse])
async def get_engagement(
    content_id: int,
    engagement_type: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    session: AsyncSession = Depends(get_db),
):
    """Get engagement for content"""
    service = ContentService(session)
    return await service.get_content_engagement(content_id, engagement_type, limit=limit)


# Statistics
@router.get("/{content_id}/stats", response_model=dict)
async def get_content_stats(
    content_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get content statistics"""
    service = ContentService(session)
    stats = await service.get_content_stats(content_id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return stats


# Bulk Operations
@router.post("/bulk/update", response_model=dict)
async def bulk_update_content(
    req: ContentBulkUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Bulk update content"""
    service = ContentService(session)
    update_data = {}

    if req.status:
        update_data["status"] = req.status
    if req.category_id:
        update_data["category_id"] = req.category_id
    if req.is_featured is not None:
        update_data["is_featured"] = req.is_featured

    count = await service.bulk_update_content(req.content_ids, **update_data)
    return {"updated": count, "total": len(req.content_ids)}


@router.post("/bulk/delete", response_model=dict)
async def bulk_delete_content(
    req: ContentBulkDeleteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Bulk delete content"""
    service = ContentService(session)
    count = await service.bulk_delete_content(req.content_ids)
    return {"deleted": count, "total": len(req.content_ids)}
