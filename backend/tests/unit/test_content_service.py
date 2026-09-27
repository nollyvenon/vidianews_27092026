"""Unit tests for content service"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.content import (
    Content, Video, MediaFile, ContentEngagement, ContentCategory, ContentTag,
    ContentType, ContentStatus, ContentAccessLevel
)
from app.models.user import User, Role
from app.models.activity_logs import ActivityLog
from app.services.content_service import ContentService
from app.db.base import Base


@pytest.fixture
async def db_session():
    """Create test database session"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        # Create test user
        user = User(
            email="test@example.com",
            hashed_password="hashedpass",
            is_active=True,
            is_verified=True
        )
        session.add(user)
        await session.commit()

        yield session

    await engine.dispose()


@pytest.fixture
async def service(db_session):
    """Create content service"""
    return ContentService(db_session)


@pytest.fixture
async def test_user(db_session):
    """Get test user"""
    result = await db_session.execute("SELECT * FROM users LIMIT 1")
    return result.scalar_one_or_none()


class TestContentCategoryService:
    """Test category operations"""

    async def test_create_category(self, service):
        """Test creating category"""
        category = await service.create_category(
            name="Tech News",
            slug="tech-news",
            description="Technology news"
        )
        assert category.id is not None
        assert category.name == "Tech News"
        assert category.slug == "tech-news"

    async def test_get_category(self, service):
        """Test getting category"""
        created = await service.create_category("News", "news")
        fetched = await service.get_category(created.id)
        assert fetched.id == created.id
        assert fetched.name == "News"

    async def test_get_categories(self, service):
        """Test listing categories"""
        await service.create_category("News", "news")
        await service.create_category("Video", "video")

        categories = await service.get_categories()
        assert len(categories) >= 2

    async def test_update_category(self, service):
        """Test updating category"""
        created = await service.create_category("News", "news")
        updated = await service.update_category(created.id, name="Breaking News")
        assert updated.name == "Breaking News"

    async def test_delete_category(self, service):
        """Test deleting category"""
        created = await service.create_category("News", "news")
        deleted = await service.delete_category(created.id)
        assert deleted is True

        fetched = await service.get_category(created.id)
        assert fetched is None


class TestContentTagService:
    """Test tag operations"""

    async def test_create_tag(self, service):
        """Test creating tag"""
        tag = await service.create_tag(name="Breaking", slug="breaking")
        assert tag.id is not None
        assert tag.name == "Breaking"

    async def test_get_tag(self, service):
        """Test getting tag"""
        created = await service.create_tag("News", "news")
        fetched = await service.get_tag(created.id)
        assert fetched.id == created.id

    async def test_get_tags(self, service):
        """Test listing tags"""
        await service.create_tag("News", "news")
        await service.create_tag("Breaking", "breaking")

        tags = await service.get_tags()
        assert len(tags) >= 2

    async def test_update_tag(self, service):
        """Test updating tag"""
        created = await service.create_tag("News", "news")
        updated = await service.update_tag(created.id, name="Breaking News")
        assert updated.name == "Breaking News"


class TestContentOperations:
    """Test content CRUD operations"""

    async def test_create_content(self, service):
        """Test creating content"""
        content = await service.create_content(
            title="Test Article",
            slug="test-article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1,
            description="Test description"
        )
        assert content.id is not None
        assert content.title == "Test Article"
        assert content.status == ContentStatus.DRAFT

    async def test_get_content(self, service):
        """Test getting content"""
        created = await service.create_content(
            title="Test", slug="test",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        fetched = await service.get_content(created.id)
        assert fetched.id == created.id

    async def test_get_content_by_slug(self, service):
        """Test getting content by slug"""
        created = await service.create_content(
            title="Test", slug="test-slug",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        fetched = await service.get_content_by_slug("test-slug")
        assert fetched.id == created.id

    async def test_update_content(self, service):
        """Test updating content"""
        created = await service.create_content(
            title="Test", slug="test",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        updated = await service.update_content(created.id, 1, title="Updated")
        assert updated.title == "Updated"

    async def test_delete_content(self, service):
        """Test deleting content"""
        created = await service.create_content(
            title="Test", slug="test",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        deleted = await service.delete_content(created.id, 1)
        assert deleted is True

    async def test_list_content(self, service):
        """Test listing content"""
        await service.create_content(
            title="Article 1", slug="article-1",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        await service.create_content(
            title="Video 1", slug="video-1",
            content_type=ContentType.VIDEO,
            creator_user_id=1
        )

        articles = await service.list_content(content_type=ContentType.ARTICLE)
        assert len(articles) >= 1

    async def test_search_content(self, service):
        """Test searching content"""
        await service.create_content(
            title="Python Tutorial", slug="python-tutorial",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        results = await service.search_content("Python")
        assert len(results) >= 1

    async def test_get_featured_content(self, service):
        """Test getting featured content"""
        await service.create_content(
            title="Featured Article", slug="featured",
            content_type=ContentType.ARTICLE,
            creator_user_id=1,
            is_featured=True,
            status=ContentStatus.PUBLISHED
        )

        featured = await service.get_featured_content()
        assert len(featured) >= 1


class TestVideoManagement:
    """Test video operations"""

    async def test_create_video(self, service):
        """Test creating video"""
        content = await service.create_content(
            title="Video", slug="video",
            content_type=ContentType.VIDEO,
            creator_user_id=1
        )

        video = await service.create_video(
            content_id=content.id,
            source_url="https://example.com/video.mp4",
            duration_seconds=120
        )
        assert video.id is not None
        assert video.content_id == content.id

    async def test_get_video(self, service):
        """Test getting video"""
        content = await service.create_content(
            title="Video", slug="video",
            content_type=ContentType.VIDEO,
            creator_user_id=1
        )

        created = await service.create_video(
            content_id=content.id,
            source_url="https://example.com/video.mp4"
        )

        fetched = await service.get_video(created.id)
        assert fetched.id == created.id

    async def test_get_content_video(self, service):
        """Test getting content video"""
        content = await service.create_content(
            title="Video", slug="video",
            content_type=ContentType.VIDEO,
            creator_user_id=1
        )

        await service.create_video(
            content_id=content.id,
            source_url="https://example.com/video.mp4"
        )

        video = await service.get_content_video(content.id)
        assert video is not None


class TestMediaFiles:
    """Test media file operations"""

    async def test_add_media_file(self, service):
        """Test adding media file"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        media = await service.add_media_file(
            content_id=content.id,
            file_name="image.jpg",
            file_type="image",
            mime_type="image/jpeg",
            file_url="https://example.com/image.jpg"
        )
        assert media.id is not None

    async def test_get_media_file(self, service):
        """Test getting media file"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        created = await service.add_media_file(
            content_id=content.id,
            file_name="image.jpg",
            file_type="image",
            mime_type="image/jpeg",
            file_url="https://example.com/image.jpg"
        )

        fetched = await service.get_media_file(created.id)
        assert fetched.id == created.id

    async def test_get_content_media_files(self, service):
        """Test getting content media files"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        await service.add_media_file(
            content_id=content.id,
            file_name="image.jpg",
            file_type="image",
            mime_type="image/jpeg",
            file_url="https://example.com/image.jpg"
        )

        files = await service.get_content_media_files(content.id)
        assert len(files) >= 1

    async def test_delete_media_file(self, service):
        """Test deleting media file"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        media = await service.add_media_file(
            content_id=content.id,
            file_name="image.jpg",
            file_type="image",
            mime_type="image/jpeg",
            file_url="https://example.com/image.jpg"
        )

        deleted = await service.delete_media_file(media.id)
        assert deleted is True


class TestEngagement:
    """Test engagement tracking"""

    async def test_record_engagement(self, service):
        """Test recording engagement"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        engagement = await service.record_engagement(
            content_id=content.id,
            engagement_type="view",
            user_id=1
        )
        assert engagement.id is not None

        # Verify content view count updated
        updated_content = await service.get_content(content.id)
        assert updated_content.views_count == 1

    async def test_record_like_engagement(self, service):
        """Test recording like engagement"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        await service.record_engagement(
            content_id=content.id,
            engagement_type="like"
        )

        updated = await service.get_content(content.id)
        assert updated.likes_count == 1

    async def test_get_content_engagement(self, service):
        """Test getting engagement"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        await service.record_engagement(
            content_id=content.id,
            engagement_type="view"
        )

        engagement = await service.get_content_engagement(content.id)
        assert len(engagement) >= 1


class TestPublishingWorkflow:
    """Test publishing workflow"""

    async def test_publish_content(self, service):
        """Test publishing content"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        published = await service.publish_content(content.id, 1)
        assert published.status == ContentStatus.PUBLISHED
        assert published.published_at is not None

    async def test_schedule_content(self, service):
        """Test scheduling content"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        scheduled_time = datetime.now(timezone.utc) + timedelta(hours=1)
        scheduled = await service.schedule_content(content.id, scheduled_time)
        assert scheduled.status == ContentStatus.SCHEDULED

    async def test_archive_content(self, service):
        """Test archiving content"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        archived = await service.archive_content(content.id, 1)
        assert archived.status == ContentStatus.ARCHIVED


class TestStats:
    """Test statistics"""

    async def test_get_content_stats(self, service):
        """Test getting content stats"""
        content = await service.create_content(
            title="Article", slug="article",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        await service.record_engagement(content.id, "view")

        stats = await service.get_content_stats(content.id)
        assert stats["content_id"] == content.id
        assert stats["views"] == 1

    async def test_count_total_content(self, service):
        """Test counting total content"""
        await service.create_content(
            title="Article", slug="article-1",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        await service.create_content(
            title="Article", slug="article-2",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        count = await service.count_total_content()
        assert count >= 2


class TestBulkOperations:
    """Test bulk operations"""

    async def test_bulk_update_content(self, service):
        """Test bulk updating content"""
        content1 = await service.create_content(
            title="Article 1", slug="article-1",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        content2 = await service.create_content(
            title="Article 2", slug="article-2",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        count = await service.bulk_update_content(
            [content1.id, content2.id],
            is_featured=True
        )
        assert count == 2

    async def test_bulk_delete_content(self, service):
        """Test bulk deleting content"""
        content1 = await service.create_content(
            title="Article 1", slug="article-1",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )
        content2 = await service.create_content(
            title="Article 2", slug="article-2",
            content_type=ContentType.ARTICLE,
            creator_user_id=1
        )

        count = await service.bulk_delete_content([content1.id, content2.id])
        assert count == 2
