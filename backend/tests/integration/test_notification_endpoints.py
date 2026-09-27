"""Integration tests for notification endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, create_access_token


@pytest.fixture
async def auth_user(async_client: AsyncClient, test_session: AsyncSession):
    """Create authenticated user"""
    user = User(
        email="notif_api_test@example.com",
        password_hash=hash_password("pass123"),
        first_name="Notif",
        last_name="Test",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"user": user, "token": token}


class TestNotificationAPI:
    async def test_get_my_notifications(self, async_client: AsyncClient, auth_user):
        """Test getting user notifications"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/notifications/me",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_unread_count(self, async_client: AsyncClient, auth_user):
        """Test getting unread count"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/notifications/me/unread-count",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "unread_count" in data

    async def test_mark_all_read(self, async_client: AsyncClient, auth_user):
        """Test marking all as read"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.post(
            "/api/v1/notifications/me/read-all",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "marked_count" in data

    async def test_get_notification_logs(self, async_client: AsyncClient, auth_user):
        """Test getting notification logs"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/notifications/me/logs",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert "count" in data

    async def test_get_pending_emails(self, async_client: AsyncClient, auth_user):
        """Test getting pending emails"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/notifications/emails/pending",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_pending_pushes(self, async_client: AsyncClient, auth_user):
        """Test getting pending pushes"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/notifications/push/pending",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "notifications" in data
