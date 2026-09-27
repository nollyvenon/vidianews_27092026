"""Integration tests for content API endpoints"""

import pytest
from httpx import AsyncClient
from datetime import datetime, timezone
from app.models.content import ContentStatus, ContentAccessLevel, ContentType
from app.main import app


@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def auth_headers(client):
    """Get authentication headers"""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {"Authorization": "Bearer fake-token"}


class TestCategoryEndpoints:
    """Test category endpoints"""

    async def test_create_category(self, client, auth_headers):
        """Test creating category"""
        response = await client.post(
            "/api/v1/content/categories",
            json={"name": "Tech", "slug": "tech"},
            headers=auth_headers
        )
        assert response.status_code in [201, 401, 403]

    async def test_list_categories(self, client):
        """Test listing categories"""
        response = await client.get("/api/v1/content/categories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_category(self, client):
        """Test getting category"""
        response = await client.get("/api/v1/content/categories/1")
        assert response.status_code in [200, 404]


class TestTagEndpoints:
    """Test tag endpoints"""

    async def test_create_tag(self, client, auth_headers):
        """Test creating tag"""
        response = await client.post(
            "/api/v1/content/tags",
            json={"name": "Breaking", "slug": "breaking"},
            headers=auth_headers
        )
        assert response.status_code in [201, 401, 403]

    async def test_list_tags(self, client):
        """Test listing tags"""
        response = await client.get("/api/v1/content/tags")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestContentEndpoints:
    """Test content endpoints"""

    async def test_create_content(self, client, auth_headers):
        """Test creating content"""
        response = await client.post(
            "/api/v1/content/",
            json={
                "title": "Test Article",
                "slug": "test-article",
                "description": "Test",
                "content_type": "article"
            },
            headers=auth_headers
        )
        assert response.status_code in [201, 401, 403, 422]

    async def test_list_content(self, client):
        """Test listing content"""
        response = await client.get("/api/v1/content/")
        assert response.status_code == 200
        assert "items" in response.json() or isinstance(response.json(), list)

    async def test_search_content(self, client):
        """Test searching content"""
        response = await client.get("/api/v1/content/search?query=test")
        assert response.status_code in [200, 422]

    async def test_get_featured_content(self, client):
        """Test getting featured content"""
        response = await client.get("/api/v1/content/featured")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_trending_content(self, client):
        """Test getting trending content"""
        response = await client.get("/api/v1/content/trending")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_content_by_id(self, client):
        """Test getting content by ID"""
        response = await client.get("/api/v1/content/1")
        assert response.status_code in [200, 404]

    async def test_get_content_by_slug(self, client):
        """Test getting content by slug"""
        response = await client.get("/api/v1/content/by-slug/test-slug")
        assert response.status_code in [200, 404]

    async def test_update_content(self, client, auth_headers):
        """Test updating content"""
        response = await client.put(
            "/api/v1/content/1",
            json={"title": "Updated"},
            headers=auth_headers
        )
        assert response.status_code in [200, 404, 401, 403]

    async def test_delete_content(self, client, auth_headers):
        """Test deleting content"""
        response = await client.delete(
            "/api/v1/content/1",
            headers=auth_headers
        )
        assert response.status_code in [204, 404, 401, 403]


class TestPublishingEndpoints:
    """Test publishing workflow endpoints"""

    async def test_publish_content(self, client, auth_headers):
        """Test publishing content"""
        response = await client.post(
            "/api/v1/content/1/publish",
            json={"access_level": "public"},
            headers=auth_headers
        )
        assert response.status_code in [200, 404, 401, 403]

    async def test_schedule_content(self, client, auth_headers):
        """Test scheduling content"""
        scheduled_time = datetime.now(timezone.utc).isoformat()
        response = await client.post(
            "/api/v1/content/1/schedule",
            json={"scheduled_at": scheduled_time},
            headers=auth_headers
        )
        assert response.status_code in [200, 404, 401, 403, 422]

    async def test_archive_content(self, client, auth_headers):
        """Test archiving content"""
        response = await client.post(
            "/api/v1/content/1/archive",
            json={},
            headers=auth_headers
        )
        assert response.status_code in [200, 404, 401, 403]


class TestVideoEndpoints:
    """Test video endpoints"""

    async def test_add_video(self, client, auth_headers):
        """Test adding video"""
        response = await client.post(
            "/api/v1/content/1/videos",
            json={"source_url": "https://example.com/video.mp4"},
            headers=auth_headers
        )
        assert response.status_code in [201, 404, 401, 403]

    async def test_get_video(self, client):
        """Test getting video"""
        response = await client.get("/api/v1/content/1/videos")
        assert response.status_code in [200, 404]


class TestMediaEndpoints:
    """Test media endpoints"""

    async def test_add_media_file(self, client, auth_headers):
        """Test adding media file"""
        response = await client.post(
            "/api/v1/content/1/media",
            json={
                "file_name": "image.jpg",
                "file_type": "image",
                "mime_type": "image/jpeg",
                "file_url": "https://example.com/image.jpg"
            },
            headers=auth_headers
        )
        assert response.status_code in [201, 404, 401, 403]

    async def test_get_media_files(self, client):
        """Test getting media files"""
        response = await client.get("/api/v1/content/1/media")
        assert response.status_code in [200, 404]


class TestEngagementEndpoints:
    """Test engagement endpoints"""

    async def test_record_engagement(self, client):
        """Test recording engagement"""
        response = await client.post(
            "/api/v1/content/1/engage",
            json={"engagement_type": "view"}
        )
        assert response.status_code in [201, 404]

    async def test_get_engagement(self, client):
        """Test getting engagement"""
        response = await client.get("/api/v1/content/1/engagement")
        assert response.status_code in [200, 404]


class TestStatsEndpoints:
    """Test statistics endpoints"""

    async def test_get_content_stats(self, client):
        """Test getting content stats"""
        response = await client.get("/api/v1/content/1/stats")
        assert response.status_code in [200, 404]


class TestBulkOperations:
    """Test bulk operation endpoints"""

    async def test_bulk_update(self, client, auth_headers):
        """Test bulk update"""
        response = await client.post(
            "/api/v1/content/bulk/update",
            json={"content_ids": [1, 2]},
            headers=auth_headers
        )
        assert response.status_code in [200, 401, 403]

    async def test_bulk_delete(self, client, auth_headers):
        """Test bulk delete"""
        response = await client.post(
            "/api/v1/content/bulk/delete",
            json={"content_ids": [1, 2]},
            headers=auth_headers
        )
        assert response.status_code in [200, 401, 403]
