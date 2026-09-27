"""Security & Performance API endpoints: Modules 36-40"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.security_performance import *
from app.services.security_performance_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["security"])


# ==================== MODULE 36: RATE LIMITING ====================

@router.post("/rate-limit/check")
async def check_rate_limit(endpoint: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = RateLimitService(db)
    allowed = await service.check_rate_limit(user["id"], endpoint)
    return {"allowed": allowed}


@router.get("/quota/usage")
async def get_quota(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = RateLimitService(db)
    usage = await service.get_quota_usage(user["id"])
    if not usage:
        return {"error": "Quota not found"}
    return {"api_calls": usage.api_calls, "storage_gb": usage.storage_gb, "bandwidth_gb": usage.bandwidth_gb}


# ==================== MODULE 37: ADVANCED AUTH ====================

@router.post("/oauth/connect")
async def connect_oauth(provider: str, provider_user_id: str, token: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AuthService(db)
    oauth = await service.connect_oauth(user["id"], provider, provider_user_id, token)
    return {"id": oauth.id, "provider": oauth.provider}


@router.post("/mfa/setup")
async def setup_mfa(method: str, secret: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AuthService(db)
    mfa = await service.setup_mfa(user["id"], method, secret)
    return {"id": mfa.id, "method": mfa.mfa_method, "is_verified": mfa.is_verified}


@router.get("/mfa")
async def get_mfa(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AuthService(db)
    mfa = await service.get_mfa(user["id"])
    if not mfa:
        return {"error": "MFA not setup"}
    return {"method": mfa.mfa_method, "is_verified": mfa.is_verified}


# ==================== MODULE 38: GDPR & PRIVACY ====================

@router.get("/privacy/settings")
async def get_privacy_settings(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PrivacyService(db)
    settings = await service.get_privacy_settings(user["id"])
    if not settings:
        return {"error": "Privacy settings not found"}
    return {
        "profile_visibility": settings.profile_visibility,
        "content_visibility": settings.content_visibility,
        "allow_analytics": settings.allow_analytics,
        "allow_marketing": settings.allow_marketing
    }


@router.put("/privacy/settings")
async def update_privacy_settings(profile_visibility: str = None, content_visibility: str = None, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PrivacyService(db)
    kwargs = {}
    if profile_visibility:
        kwargs["profile_visibility"] = profile_visibility
    if content_visibility:
        kwargs["content_visibility"] = content_visibility
    settings = await service.update_privacy_settings(user["id"], **kwargs)
    return {"updated": True}


@router.post("/privacy/request-deletion")
async def request_data_deletion(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PrivacyService(db)
    request = await service.request_data_deletion(user["id"])
    return {"id": request.id, "status": request.status, "scheduled_for": request.scheduled_for}


@router.post("/privacy/consent-log")
async def log_consent(consent_type: str, granted: bool, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PrivacyService(db)
    log = await service.log_consent(user["id"], consent_type, granted)
    return {"id": log.id, "consent_type": log.consent_type, "granted": log.granted}


# ==================== MODULE 39: CACHING ====================

@router.get("/cache/policy/{resource_type}")
async def get_cache_policy(resource_type: str, db: AsyncSession = Depends(get_db)):
    service = CacheService(db)
    policy = await service.get_cache_policy(resource_type)
    if not policy:
        return {"error": "Cache policy not found"}
    return {"cache_type": policy.cache_type, "ttl_seconds": policy.ttl_seconds}


@router.post("/cache/metric")
async def record_cache_metric(resource_type: str, hit: bool, db: AsyncSession = Depends(get_db)):
    service = CacheService(db)
    await service.record_cache_metric(resource_type, hit)
    return {"recorded": True}


# ==================== MODULE 40: PUSH NOTIFICATIONS ====================

@router.post("/notifications/register-device")
async def register_device(device_id: str, token: str, platform: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PushNotificationService(db)
    device = await service.register_device(user["id"], device_id, token, platform)
    return {"id": device.id, "platform": device.platform}


@router.get("/notifications/devices")
async def get_user_devices(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PushNotificationService(db)
    devices = await service.get_user_devices(user["id"])
    return [{"id": d.id, "platform": d.platform, "is_active": d.is_active} for d in devices]


@router.post("/notifications/send")
async def send_notification(title: str, body: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PushNotificationService(db)
    notif = await service.send_notification(user["id"], title, body)
    return {"id": notif.id, "title": notif.title}


@router.get("/notifications")
async def get_notifications(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PushNotificationService(db)
    notifications = await service.get_notifications(user["id"])
    return [{"id": n.id, "title": n.title, "sent_at": n.sent_at, "read_at": n.read_at} for n in notifications]
