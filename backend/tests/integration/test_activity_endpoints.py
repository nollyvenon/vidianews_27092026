"""Integration tests for activity endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, create_access_token


@pytest.fixture
async def auth_user(async_client: AsyncClient, test_session: AsyncSession):
    """Create authenticated user"""
    user = User(
        email="activity_api_test@example.com",
        password_hash=hash_password("pass123"),
        first_name="Activity",
        last_name="Test",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"user": user, "token": token}


class TestActivityAPI:
    async def test_get_my_activities(self, async_client: AsyncClient, auth_user):
        """Test getting user activities"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/me",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_activity_count(self, async_client: AsyncClient, auth_user):
        """Test getting activity count"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/me/count",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "period_days" in data

    async def test_get_activity_summary(self, async_client: AsyncClient, auth_user):
        """Test getting activity summary"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/me/summary",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_activities" in data
        assert "by_action" in data
        assert "by_entity" in data

    async def test_get_audit_trail(self, async_client: AsyncClient, auth_user):
        """Test getting audit trail"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/audit/document/1",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_my_audit_logs(self, async_client: AsyncClient, auth_user):
        """Test getting user's audit logs"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/me/audit",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_activity_feed(self, async_client: AsyncClient, auth_user):
        """Test getting activity feed"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/feed",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_unread_feed_count(self, async_client: AsyncClient, auth_user):
        """Test getting unread feed count"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/activity/feed/unread-count",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "unread_count" in data

    async def test_mark_all_feed_read(self, async_client: AsyncClient, auth_user):
        """Test marking all feed as read"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.post(
            "/api/v1/activity/feed/read-all",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "marked_count" in data
