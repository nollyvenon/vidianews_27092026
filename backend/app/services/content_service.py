"""Content management service"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, desc, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.models.content import (
    Content, Video, MediaFile, ContentEngagement, ContentCategory, ContentTag,
    ContentType, ContentStatus, ContentAccessLevel, content_tags
)
from app.models.user import User
from app.models.activity_logs import ActivityLog, ActionType, EntityType
import math


class ContentService:
    """Service for content management"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Category Management
    async def create_category(self, name: str, slug: str, description: Optional[str] = None,
                             icon_url: Optional[str] = None, sort_order: int = 0) -> ContentCategory:
        """Create new content category"""
        category = ContentCategory(
            name=name,
            slug=slug,
            description=description,
            icon_url=icon_url,
            sort_order=sort_order
        )
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_category(self, category_id: int) -> Optional[ContentCategory]:
        """Get category by ID"""
        stmt = select(ContentCategory).where(ContentCategory.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_categories(self, is_active: bool = True, limit: int = 100) -> List[ContentCategory]:
        """Get all active categories"""
        stmt = select(ContentCategory).where(ContentCategory.is_active == is_active).order_by(ContentCategory.sort_order)
        if limit:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_category(self, category_id: int, **kwargs) -> Optional[ContentCategory]:
        """Update category"""
        stmt = update(ContentCategory).where(ContentCategory.id == category_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_category(category_id)

    async def delete_category(self, category_id: int) -> bool:
        """Delete category"""
        stmt = delete(ContentCategory).where(ContentCategory.id == category_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Tag Management
    async def create_tag(self, name: str, slug: str, description: Optional[str] = None) -> ContentTag:
        """Create new content tag"""
        tag = ContentTag(name=name, slug=slug, description=description)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def get_tag(self, tag_id: int) -> Optional[ContentTag]:
        """Get tag by ID"""
        stmt = select(ContentTag).where(ContentTag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_tags(self, is_active: bool = True) -> List[ContentTag]:
        """Get all active tags"""
        stmt = select(ContentTag).where(ContentTag.is_active == is_active).order_by(ContentTag.usage_count.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_tag(self, tag_id: int, **kwargs) -> Optional[ContentTag]:
        """Update tag"""
        stmt = update(ContentTag).where(ContentTag.id == tag_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_tag(tag_id)

    # Content CRUD Operations
    async def create_content(self, title: str, slug: str, content_type: ContentType,
                           creator_user_id: int, description: Optional[str] = None,
                           body: Optional[str] = None, category_id: Optional[int] = None,
                           thumbnail_url: Optional[str] = None, **kwargs) -> Content:
        """Create new content"""
        content = Content(
            title=title,
            slug=slug,
            content_type=content_type,
            creator_user_id=creator_user_id,
            description=description,
            body=body,
            category_id=category_id,
            thumbnail_url=thumbnail_url,
            **kwargs
        )
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)

        # Log activity
        await self._log_activity(creator_user_id, ActionType.CREATE, EntityType.DOCUMENT, content.id)

        return content

    async def get_content(self, content_id: int, include_engagement: bool = False) -> Optional[Content]:
        """Get content by ID"""
        stmt = select(Content).where(Content.id == content_id)
        stmt = stmt.options(
            selectinload(Content.category),
            selectinload(Content.tags),
            selectinload(Content.videos),
            selectinload(Content.media_files)
        )
        if include_engagement:
            stmt = stmt.options(selectinload(Content.engagement))

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_content_by_slug(self, slug: str) -> Optional[Content]:
        """Get content by slug"""
        stmt = select(Content).where(Content.slug == slug).options(
            selectinload(Content.category),
            selectinload(Content.tags),
            selectinload(Content.videos)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_content(self, content_id: int, user_id: int, **kwargs) -> Optional[Content]:
        """Update content"""
        stmt = update(Content).where(Content.id == content_id).values(
            updated_by_user_id=user_id,
            **kwargs
        )
        await self.session.execute(stmt)
        await self.session.commit()

        # Log activity
        await self._log_activity(user_id, ActionType.UPDATE, EntityType.DOCUMENT, content_id)

        return await self.get_content(content_id)

    async def delete_content(self, content_id: int, user_id: int) -> bool:
        """Delete content"""
        stmt = delete(Content).where(Content.id == content_id)
        result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount > 0:
            await self._log_activity(user_id, ActionType.DELETE, EntityType.DOCUMENT, content_id)
            return True
        return False

    # Content Querying
    async def list_content(self, content_type: Optional[ContentType] = None,
                          status: Optional[ContentStatus] = None,
                          category_id: Optional[int] = None,
                          is_featured: Optional[bool] = None,
                          access_level: Optional[ContentAccessLevel] = None,
                          limit: int = 50, offset: int = 0,
                          order_by: str = "created_at", order: str = "desc") -> List[Content]:
        """List content with filters"""
        conditions = []

        if content_type:
            conditions.append(Content.content_type == content_type)
        if status:
            conditions.append(Content.status == status)
        if category_id:
            conditions.append(Content.category_id == category_id)
        if is_featured is not None:
            conditions.append(Content.is_featured == is_featured)
        if access_level:
            conditions.append(Content.access_level == access_level)

        stmt = select(Content).options(
            selectinload(Content.category),
            selectinload(Content.tags)
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        if order.lower() == "desc":
            stmt = stmt.order_by(desc(getattr(Content, order_by)))
        else:
            stmt = stmt.order_by(getattr(Content, order_by))

        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search_content(self, query: str, content_type: Optional[ContentType] = None,
                            limit: int = 50, offset: int = 0) -> List[Content]:
        """Search content by title/description"""
        conditions = [
            or_(
                Content.title.ilike(f"%{query}%"),
                Content.description.ilike(f"%{query}%"),
                Content.body.ilike(f"%{query}%")
            )
        ]

        if content_type:
            conditions.append(Content.content_type == content_type)

        stmt = select(Content).where(and_(*conditions)).order_by(desc(Content.created_at))
        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_featured_content(self, content_type: Optional[ContentType] = None,
                                  limit: int = 10) -> List[Content]:
        """Get featured content"""
        stmt = select(Content).where(
            and_(
                Content.is_featured == True,
                Content.status == ContentStatus.PUBLISHED
            )
        ).order_by(desc(Content.published_at)).limit(limit)

        if content_type:
            stmt = stmt.where(Content.content_type == content_type)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_trending_content(self, days: int = 7, limit: int = 10) -> List[Content]:
        """Get trending content based on engagement"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = select(Content).where(
            and_(
                Content.status == ContentStatus.PUBLISHED,
                Content.created_at >= cutoff_date
            )
        ).order_by(desc(Content.views_count)).limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Video Management
    async def create_video(self, content_id: int, source_url: str,
                          duration_seconds: Optional[int] = None,
                          **kwargs) -> Video:
        """Create video for content"""
        video = Video(content_id=content_id, source_url=source_url,
                     duration_seconds=duration_seconds, **kwargs)
        self.session.add(video)
        await self.session.commit()
        await self.session.refresh(video)
        return video

    async def get_video(self, video_id: int) -> Optional[Video]:
        """Get video by ID"""
        stmt = select(Video).where(Video.id == video_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_video(self, video_id: int, **kwargs) -> Optional[Video]:
        """Update video"""
        stmt = update(Video).where(Video.id == video_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_video(video_id)

    async def get_content_video(self, content_id: int) -> Optional[Video]:
        """Get video for specific content"""
        stmt = select(Video).where(Video.content_id == content_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # Media File Management
    async def add_media_file(self, content_id: int, file_name: str, file_type: str,
                            mime_type: str, file_url: str, **kwargs) -> MediaFile:
        """Add media file to content"""
        media = MediaFile(
            content_id=content_id, file_name=file_name, file_type=file_type,
            mime_type=mime_type, file_url=file_url, **kwargs
        )
        self.session.add(media)
        await self.session.commit()
        await self.session.refresh(media)
        return media

    async def get_media_file(self, media_id: int) -> Optional[MediaFile]:
        """Get media file by ID"""
        stmt = select(MediaFile).where(MediaFile.id == media_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_content_media_files(self, content_id: int) -> List[MediaFile]:
        """Get all media files for content"""
        stmt = select(MediaFile).where(MediaFile.content_id == content_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_media_file(self, media_id: int) -> bool:
        """Delete media file"""
        stmt = delete(MediaFile).where(MediaFile.id == media_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Tags Association
    async def add_tags_to_content(self, content_id: int, tag_ids: List[int]) -> None:
        """Add tags to content"""
        content = await self.get_content(content_id)
        if content:
            tags = []
            for tag_id in tag_ids:
                tag = await self.get_tag(tag_id)
                if tag:
                    tags.append(tag)
                    # Update tag usage count
                    await self.update_tag(tag_id, usage_count=tag.usage_count + 1)

            content.tags = tags
            await self.session.commit()

    async def remove_tags_from_content(self, content_id: int, tag_ids: List[int]) -> None:
        """Remove tags from content"""
        content = await self.get_content(content_id)
        if content:
            tags_to_remove = [tag for tag in content.tags if tag.id in tag_ids]
            for tag in tags_to_remove:
                content.tags.remove(tag)
                # Update tag usage count
                await self.update_tag(tag.id, usage_count=max(0, tag.usage_count - 1))

            await self.session.commit()

    # Engagement Tracking
    async def record_engagement(self, content_id: int, engagement_type: str,
                               user_id: Optional[int] = None,
                               watch_seconds: int = 0,
                               watch_percentage: float = 0.0) -> ContentEngagement:
        """Record user engagement with content"""
        engagement = ContentEngagement(
            content_id=content_id,
            user_id=user_id,
            engagement_type=engagement_type,
            watch_seconds=watch_seconds,
            watch_percentage=watch_percentage
        )
        self.session.add(engagement)

        # Update content metrics
        content = await self.get_content(content_id)
        if content:
            if engagement_type == "view":
                content.views_count += 1
            elif engagement_type == "like":
                content.likes_count += 1
            elif engagement_type == "comment":
                content.comments_count += 1
            elif engagement_type == "share":
                content.shares_count += 1

        await self.session.commit()
        await self.session.refresh(engagement)
        return engagement

    async def get_content_engagement(self, content_id: int, engagement_type: Optional[str] = None,
                                    limit: int = 100) -> List[ContentEngagement]:
        """Get engagement for content"""
        conditions = [ContentEngagement.content_id == content_id]

        if engagement_type:
            conditions.append(ContentEngagement.engagement_type == engagement_type)

        stmt = select(ContentEngagement).where(and_(*conditions)).order_by(
            desc(ContentEngagement.created_at)).limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Publishing Workflow
    async def publish_content(self, content_id: int, user_id: int,
                             access_level: ContentAccessLevel = ContentAccessLevel.PUBLIC) -> Optional[Content]:
        """Publish content"""
        return await self.update_content(
            content_id, user_id,
            status=ContentStatus.PUBLISHED,
            published_at=datetime.now(timezone.utc),
            access_level=access_level
        )

    async def schedule_content(self, content_id: int, scheduled_at: datetime) -> Optional[Content]:
        """Schedule content for future publication"""
        return await self.update_content(
            content_id, user_id=None,
            status=ContentStatus.SCHEDULED,
            scheduled_at=scheduled_at
        )

    async def archive_content(self, content_id: int, user_id: int) -> Optional[Content]:
        """Archive content"""
        return await self.update_content(content_id, user_id, status=ContentStatus.ARCHIVED)

    async def get_scheduled_content(self) -> List[Content]:
        """Get scheduled content ready for publishing"""
        now = datetime.now(timezone.utc)
        stmt = select(Content).where(
            and_(
                Content.status == ContentStatus.SCHEDULED,
                Content.scheduled_at <= now
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Statistics and Analytics
    async def get_content_stats(self, content_id: int) -> Dict[str, Any]:
        """Get statistics for content"""
        content = await self.get_content(content_id)
        if not content:
            return {}

        engagement_counts = await self.session.execute(
            select(
                ContentEngagement.engagement_type,
                func.count(ContentEngagement.id).label("count")
            ).where(ContentEngagement.content_id == content_id).group_by(ContentEngagement.engagement_type)
        )

        return {
            "content_id": content.id,
            "title": content.title,
            "views": content.views_count,
            "likes": content.likes_count,
            "comments": content.comments_count,
            "shares": content.shares_count,
            "created_at": content.created_at,
            "published_at": content.published_at,
            "engagement_breakdown": {row[0]: row[1] for row in engagement_counts}
        }

    async def get_category_stats(self, category_id: int) -> Dict[str, Any]:
        """Get statistics for category"""
        category = await self.get_category(category_id)
        if not category:
            return {}

        stmt = select(func.count(Content.id)).where(Content.category_id == category_id)
        content_count = await self.session.scalar(stmt)

        return {
            "category_id": category.id,
            "category_name": category.name,
            "content_count": content_count,
            "is_active": category.is_active
        }

    # Bulk Operations
    async def bulk_update_content(self, content_ids: List[int], **kwargs) -> int:
        """Bulk update multiple content items"""
        stmt = update(Content).where(Content.id.in_(content_ids)).values(**kwargs)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def bulk_delete_content(self, content_ids: List[int]) -> int:
        """Bulk delete multiple content items"""
        stmt = delete(Content).where(Content.id.in_(content_ids))
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    # Helper Methods
    async def _log_activity(self, user_id: int, action: ActionType, entity_type: EntityType,
                           entity_id: int) -> None:
        """Log user activity"""
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=f"{action.value} {entity_type.value} {entity_id}"
        )
        self.session.add(activity)
        await self.session.commit()

    async def count_total_content(self, status: Optional[ContentStatus] = None) -> int:
        """Count total content"""
        stmt = select(func.count(Content.id))

        if status:
            stmt = stmt.where(Content.status == status)

        return await self.session.scalar(stmt)
