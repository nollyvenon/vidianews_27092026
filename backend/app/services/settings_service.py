"""Settings service for managing system, user, and tenant settings"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.settings import (
    SystemSetting, UserSetting, TenantSetting,
    NotificationPreference, PrivacySetting, DisplaySetting
)
from app.models.user import User
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.logger import logger


class SettingsService:
    """Service for managing all types of settings"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # System settings
    async def get_system_setting(self, key: str) -> dict:
        """Get system setting by key"""
        stmt = select(SystemSetting).where(SystemSetting.key == key)
        setting = (await self.session.execute(stmt)).scalar_one_or_none()
        if not setting:
            raise NotFoundError(f"System setting '{key}' not found")
        return {"key": setting.key, "value": setting.value, "type": setting.data_type}

    async def set_system_setting(self, key: str, value: dict, **kwargs) -> SystemSetting:
        """Set or update system setting"""
        stmt = select(SystemSetting).where(SystemSetting.key == key)
        setting = (await self.session.execute(stmt)).scalar_one_or_none()

        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = SystemSetting(key=key, value=value, **{
                k: v for k, v in kwargs.items()
                if k in {"data_type", "description", "is_public", "is_secret", "category"}
            })
            self.session.add(setting)

        await self.session.commit()
        logger.info(f"System setting updated: {key}")
        return setting

    async def get_system_settings_by_category(self, category: str) -> list[dict]:
        """Get all system settings in a category"""
        stmt = select(SystemSetting).where(SystemSetting.category == category)
        settings = (await self.session.execute(stmt)).scalars().all()
        return [{"key": s.key, "value": s.value} for s in settings]

    # User settings
    async def get_user_setting(self, user_id: int, key: str) -> dict:
        """Get user setting"""
        stmt = select(UserSetting).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()
        if not setting:
            raise NotFoundError(f"User setting '{key}' not found")
        return {"key": setting.key, "value": setting.value}

    async def set_user_setting(self, user_id: int, key: str, value: dict, **kwargs) -> UserSetting:
        """Set or update user setting"""
        stmt = select(UserSetting).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()

        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = UserSetting(user_id=user_id, key=key, value=value, **{
                k: v for k, v in kwargs.items() if k in {"data_type", "category"}
            })
            self.session.add(setting)

        await self.session.commit()
        return setting

    async def get_user_settings_by_category(self, user_id: int, category: str) -> list[dict]:
        """Get all user settings in a category"""
        stmt = select(UserSetting).where(
            and_(UserSetting.user_id == user_id, UserSetting.category == category)
        )
        settings = (await self.session.execute(stmt)).scalars().all()
        return [{"key": s.key, "value": s.value} for s in settings]

    # Tenant settings
    async def get_tenant_setting(self, tenant_id: int, key: str) -> dict:
        """Get tenant setting"""
        stmt = select(TenantSetting).where(
            and_(TenantSetting.tenant_id == tenant_id, TenantSetting.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()
        if not setting:
            raise NotFoundError(f"Tenant setting '{key}' not found")
        return {"key": setting.key, "value": setting.value}

    async def set_tenant_setting(self, tenant_id: int, key: str, value: dict, **kwargs) -> TenantSetting:
        """Set or update tenant setting"""
        stmt = select(TenantSetting).where(
            and_(TenantSetting.tenant_id == tenant_id, TenantSetting.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()

        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = TenantSetting(tenant_id=tenant_id, key=key, value=value, **{
                k: v for k, v in kwargs.items() if k in {"data_type", "description", "category"}
            })
            self.session.add(setting)

        await self.session.commit()
        logger.info(f"Tenant setting updated: {tenant_id} - {key}")
        return setting

    # Notification preferences
    async def get_notification_preferences(self, user_id: int) -> NotificationPreference:
        """Get user notification preferences"""
        stmt = select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        prefs = (await self.session.execute(stmt)).scalar_one_or_none()

        if not prefs:
            prefs = NotificationPreference(user_id=user_id)
            self.session.add(prefs)
            await self.session.commit()

        return prefs

    async def update_notification_preferences(self, user_id: int, **kwargs) -> NotificationPreference:
        """Update notification preferences"""
        prefs = await self.get_notification_preferences(user_id)

        allowed = {
            "email_on_activity", "email_on_mention", "email_on_message", "email_digest",
            "push_enabled", "push_on_activity", "push_on_message",
            "inapp_enabled", "inapp_sound",
            "dnd_enabled", "dnd_start_time", "dnd_end_time"
        }

        for key, value in kwargs.items():
            if key in allowed and hasattr(prefs, key):
                setattr(prefs, key, value)

        prefs.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return prefs

    # Privacy settings
    async def get_privacy_settings(self, user_id: int) -> PrivacySetting:
        """Get user privacy settings"""
        stmt = select(PrivacySetting).where(PrivacySetting.user_id == user_id)
        prefs = (await self.session.execute(stmt)).scalar_one_or_none()

        if not prefs:
            prefs = PrivacySetting(user_id=user_id)
            self.session.add(prefs)
            await self.session.commit()

        return prefs

    async def update_privacy_settings(self, user_id: int, **kwargs) -> PrivacySetting:
        """Update privacy settings"""
        prefs = await self.get_privacy_settings(user_id)

        allowed = {
            "profile_visibility", "show_email", "show_phone", "show_activity", "show_last_seen",
            "allow_messages", "allow_search", "allow_analytics", "allow_marketing_emails",
            "allow_third_party_sharing"
        }

        for key, value in kwargs.items():
            if key in allowed and hasattr(prefs, key):
                setattr(prefs, key, value)

        prefs.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return prefs

    # Display settings
    async def get_display_settings(self, user_id: int) -> DisplaySetting:
        """Get user display settings"""
        stmt = select(DisplaySetting).where(DisplaySetting.user_id == user_id)
        prefs = (await self.session.execute(stmt)).scalar_one_or_none()

        if not prefs:
            prefs = DisplaySetting(user_id=user_id)
            self.session.add(prefs)
            await self.session.commit()

        return prefs

    async def update_display_settings(self, user_id: int, **kwargs) -> DisplaySetting:
        """Update display settings"""
        prefs = await self.get_display_settings(user_id)

        allowed = {
            "theme", "language", "timezone", "date_format", "time_format",
            "sidebar_collapsed", "compact_mode", "animations_enabled", "font_size"
        }

        for key, value in kwargs.items():
            if key in allowed and hasattr(prefs, key):
                setattr(prefs, key, value)

        prefs.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return prefs

    # All user preferences
    async def get_all_user_settings(self, user_id: int) -> dict:
        """Get all user settings at once"""
        notifications = await self.get_notification_preferences(user_id)
        privacy = await self.get_privacy_settings(user_id)
        display = await self.get_display_settings(user_id)

        return {
            "notifications": self._to_dict(notifications),
            "privacy": self._to_dict(privacy),
            "display": self._to_dict(display),
        }

    async def update_all_user_settings(self, user_id: int, settings: dict) -> dict:
        """Update multiple setting categories at once"""
        if "notifications" in settings:
            await self.update_notification_preferences(user_id, **settings["notifications"])

        if "privacy" in settings:
            await self.update_privacy_settings(user_id, **settings["privacy"])

        if "display" in settings:
            await self.update_display_settings(user_id, **settings["display"])

        return await self.get_all_user_settings(user_id)

    def _to_dict(self, obj) -> dict:
        """Convert settings object to dict"""
        return {
            key: getattr(obj, key)
            for key in dir(obj)
            if not key.startswith("_") and key not in {"metadata", "sa_instance_state"}
            and not callable(getattr(obj, key))
        }
