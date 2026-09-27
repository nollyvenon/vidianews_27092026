"""Settings API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.settings_service import SettingsService
from app.utils.exceptions import NotFoundError
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/settings", tags=["settings"])


# Schemas
class NotificationPreferencesUpdate(BaseModel):
    email_on_activity: Optional[bool] = None
    email_on_mention: Optional[bool] = None
    email_on_message: Optional[bool] = None
    email_digest: Optional[str] = None
    push_enabled: Optional[bool] = None
    inapp_enabled: Optional[bool] = None


class PrivacySettingsUpdate(BaseModel):
    profile_visibility: Optional[str] = None
    show_email: Optional[bool] = None
    show_phone: Optional[bool] = None
    show_activity: Optional[bool] = None
    allow_messages: Optional[str] = None
    allow_analytics: Optional[bool] = None


class DisplaySettingsUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None


class AllSettingsUpdate(BaseModel):
    notifications: Optional[NotificationPreferencesUpdate] = None
    privacy: Optional[PrivacySettingsUpdate] = None
    display: Optional[DisplaySettingsUpdate] = None


# User settings endpoints
@router.get("/me", response_model=dict)
async def get_all_settings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get all user settings"""
    try:
        service = SettingsService(session)
        return await service.get_all_user_settings(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/me", response_model=dict)
async def update_all_settings(
    updates: AllSettingsUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update all user settings"""
    try:
        service = SettingsService(session)
        updates_dict = updates.dict(exclude_unset=True)
        return await service.update_all_user_settings(current_user.id, updates_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Notification settings
@router.get("/me/notifications", response_model=dict)
async def get_notification_settings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get notification preferences"""
    service = SettingsService(session)
    prefs = await service.get_notification_preferences(current_user.id)
    return {
        "email_on_activity": prefs.email_on_activity,
        "email_on_mention": prefs.email_on_mention,
        "email_on_message": prefs.email_on_message,
        "email_digest": prefs.email_digest,
        "push_enabled": prefs.push_enabled,
        "inapp_enabled": prefs.inapp_enabled,
        "dnd_enabled": prefs.dnd_enabled,
    }


@router.put("/me/notifications", response_model=dict)
async def update_notification_settings(
    updates: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update notification preferences"""
    try:
        service = SettingsService(session)
        prefs = await service.update_notification_preferences(
            current_user.id,
            **updates.dict(exclude_unset=True)
        )
        return {
            "email_on_activity": prefs.email_on_activity,
            "email_on_mention": prefs.email_on_mention,
            "push_enabled": prefs.push_enabled,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Privacy settings
@router.get("/me/privacy", response_model=dict)
async def get_privacy_settings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get privacy settings"""
    service = SettingsService(session)
    prefs = await service.get_privacy_settings(current_user.id)
    return {
        "profile_visibility": prefs.profile_visibility,
        "show_email": prefs.show_email,
        "show_phone": prefs.show_phone,
        "show_activity": prefs.show_activity,
        "allow_messages": prefs.allow_messages,
        "allow_analytics": prefs.allow_analytics,
    }


@router.put("/me/privacy", response_model=dict)
async def update_privacy_settings(
    updates: PrivacySettingsUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update privacy settings"""
    try:
        service = SettingsService(session)
        prefs = await service.update_privacy_settings(
            current_user.id,
            **updates.dict(exclude_unset=True)
        )
        return {
            "profile_visibility": prefs.profile_visibility,
            "allow_messages": prefs.allow_messages,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Display settings
@router.get("/me/display", response_model=dict)
async def get_display_settings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get display preferences"""
    service = SettingsService(session)
    prefs = await service.get_display_settings(current_user.id)
    return {
        "theme": prefs.theme,
        "language": prefs.language,
        "timezone": prefs.timezone,
        "font_size": prefs.font_size,
    }


@router.put("/me/display", response_model=dict)
async def update_display_settings(
    updates: DisplaySettingsUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update display preferences"""
    try:
        service = SettingsService(session)
        prefs = await service.update_display_settings(
            current_user.id,
            **updates.dict(exclude_unset=True)
        )
        return {
            "theme": prefs.theme,
            "language": prefs.language,
            "timezone": prefs.timezone,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# System settings (admin only - simplified)
@router.get("/system/{key}", response_model=dict)
async def get_system_setting(
    key: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get system setting (public settings only)"""
    try:
        service = SettingsService(session)
        return await service.get_system_setting(key)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
