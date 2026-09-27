"""Integration tests for settings endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, create_access_token


@pytest.fixture
async def auth_user(async_client: AsyncClient, test_session: AsyncSession):
    """Create authenticated user"""
    user = User(
        email="settings_api_test@example.com",
        password_hash=hash_password("pass123"),
        first_name="Settings",
        last_name="Test",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"user": user, "token": token}


class TestSettingsAPI:
    async def test_get_all_settings(self, async_client: AsyncClient, auth_user):
        """Test getting all settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/settings/me",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "notifications" in data
        assert "privacy" in data
        assert "display" in data

    async def test_update_all_settings(self, async_client: AsyncClient, auth_user):
        """Test updating all settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.put(
            "/api/v1/settings/me",
            json={
                "notifications": {"email_on_activity": False},
                "privacy": {"profile_visibility": "public"},
                "display": {"theme": "dark"}
            },
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["notifications"]["email_on_activity"] is False

    async def test_get_notification_settings(self, async_client: AsyncClient, auth_user):
        """Test getting notification settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/settings/me/notifications",
            headers=headers,
        )

        assert response.status_code == 200
        assert "email_on_activity" in response.json()

    async def test_update_notification_settings(self, async_client: AsyncClient, auth_user):
        """Test updating notification settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.put(
            "/api/v1/settings/me/notifications",
            json={"push_enabled": False, "inapp_enabled": False},
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json()["push_enabled"] is False

    async def test_get_privacy_settings(self, async_client: AsyncClient, auth_user):
        """Test getting privacy settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/settings/me/privacy",
            headers=headers,
        )

        assert response.status_code == 200
        assert "profile_visibility" in response.json()

    async def test_update_privacy_settings(self, async_client: AsyncClient, auth_user):
        """Test updating privacy settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.put(
            "/api/v1/settings/me/privacy",
            json={"profile_visibility": "public", "show_email": True},
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json()["profile_visibility"] == "public"

    async def test_get_display_settings(self, async_client: AsyncClient, auth_user):
        """Test getting display settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            "/api/v1/settings/me/display",
            headers=headers,
        )

        assert response.status_code == 200
        assert "theme" in response.json()

    async def test_update_display_settings(self, async_client: AsyncClient, auth_user):
        """Test updating display settings"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.put(
            "/api/v1/settings/me/display",
            json={"theme": "dark", "language": "es"},
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json()["theme"] == "dark"
