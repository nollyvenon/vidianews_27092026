"""Unit tests for SettingsService"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.settings_service import SettingsService
from app.models.user import User
from app.core.security import hash_password


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        email="settings_test@example.com",
        password_hash=hash_password("pass"),
        first_name="Test",
        last_name="User",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()
    return user


class TestNotificationSettings:
    async def test_get_notification_preferences(self, test_session: AsyncSession, test_user: User):
        """Test getting notification preferences"""
        service = SettingsService(test_session)
        prefs = await service.get_notification_preferences(test_user.id)

        assert prefs.user_id == test_user.id
        assert prefs.email_on_activity is True

    async def test_update_notification_preferences(self, test_session: AsyncSession, test_user: User):
        """Test updating notification preferences"""
        service = SettingsService(test_session)

        updated = await service.update_notification_preferences(
            test_user.id,
            email_on_activity=False,
            push_enabled=False
        )

        assert updated.email_on_activity is False
        assert updated.push_enabled is False


class TestPrivacySettings:
    async def test_get_privacy_settings(self, test_session: AsyncSession, test_user: User):
        """Test getting privacy settings"""
        service = SettingsService(test_session)
        prefs = await service.get_privacy_settings(test_user.id)

        assert prefs.user_id == test_user.id
        assert prefs.profile_visibility == "private"

    async def test_update_privacy_settings(self, test_session: AsyncSession, test_user: User):
        """Test updating privacy settings"""
        service = SettingsService(test_session)

        updated = await service.update_privacy_settings(
            test_user.id,
            profile_visibility="public",
            show_email=True
        )

        assert updated.profile_visibility == "public"
        assert updated.show_email is True


class TestDisplaySettings:
    async def test_get_display_settings(self, test_session: AsyncSession, test_user: User):
        """Test getting display settings"""
        service = SettingsService(test_session)
        prefs = await service.get_display_settings(test_user.id)

        assert prefs.user_id == test_user.id
        assert prefs.theme == "light"

    async def test_update_display_settings(self, test_session: AsyncSession, test_user: User):
        """Test updating display settings"""
        service = SettingsService(test_session)

        updated = await service.update_display_settings(
            test_user.id,
            theme="dark",
            language="es"
        )

        assert updated.theme == "dark"
        assert updated.language == "es"


class TestAllSettings:
    async def test_get_all_user_settings(self, test_session: AsyncSession, test_user: User):
        """Test getting all user settings"""
        service = SettingsService(test_session)
        all_settings = await service.get_all_user_settings(test_user.id)

        assert "notifications" in all_settings
        assert "privacy" in all_settings
        assert "display" in all_settings

    async def test_update_all_user_settings(self, test_session: AsyncSession, test_user: User):
        """Test updating all user settings at once"""
        service = SettingsService(test_session)

        updates = {
            "notifications": {"email_on_activity": False},
            "privacy": {"profile_visibility": "public"},
            "display": {"theme": "dark"}
        }

        result = await service.update_all_user_settings(test_user.id, updates)

        assert result["notifications"]["email_on_activity"] is False
        assert result["privacy"]["profile_visibility"] == "public"
        assert result["display"]["theme"] == "dark"


class TestUserSettings:
    async def test_set_user_setting(self, test_session: AsyncSession, test_user: User):
        """Test setting user setting"""
        service = SettingsService(test_session)

        setting = await service.set_user_setting(
            test_user.id,
            "custom_key",
            {"value": "custom_value"},
            category="custom"
        )

        assert setting.key == "custom_key"
        assert setting.category == "custom"

    async def test_get_user_settings_by_category(self, test_session: AsyncSession, test_user: User):
        """Test getting settings by category"""
        service = SettingsService(test_session)

        await service.set_user_setting(test_user.id, "setting1", {"val": 1}, category="test")
        await service.set_user_setting(test_user.id, "setting2", {"val": 2}, category="test")

        settings = await service.get_user_settings_by_category(test_user.id, "test")

        assert len(settings) == 2
