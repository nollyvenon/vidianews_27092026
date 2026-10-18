"""Security & Performance API endpoints: Modules 36-40"""

from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Literal
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from app.core.admin_access import require_admin
from app.db.session import get_db
from app.models.security_performance import *
from app.services.security_performance_service import *
from app.core.security import get_current_user
from app.services.mfa_service import generate_secret, provisioning_uri
from fastapi import HTTPException

router = APIRouter(tags=["security"])


# ==================== MODULE 36: RATE LIMITING ====================

@router.post("/rate-limit/check")
async def check_rate_limit(endpoint: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = RateLimitService(db)
    allowed = await service.check_rate_limit(user.id, endpoint)
    return {"allowed": allowed}


DEFAULT_MONTHLY_API_LIMIT = 10000


@router.get("/quota/usage")
async def get_quota(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Usage since the account was created: API calls and response bandwidth as recorded per request,
    and the size of the media files the user has uploaded to their content."""
    from app.models.content import Content, MediaFile
    from app.services.api_usage_recorder import BYTES_PER_GB

    usage = (await db.execute(select(QuotaUsage).where(QuotaUsage.user_id == user.id))).scalar_one_or_none()
    stored_bytes = (await db.execute(
        select(func.coalesce(func.sum(MediaFile.file_size), 0))
        .join(Content, Content.id == MediaFile.content_id)
        .where(Content.creator_user_id == user.id)
    )).scalar_one()
    return {
        "api_calls": int(usage.api_calls or 0) if usage else 0,
        "api_call_limit": int(usage.monthly_limit or DEFAULT_MONTHLY_API_LIMIT) if usage else DEFAULT_MONTHLY_API_LIMIT,
        "storage_gb": round(int(stored_bytes) / BYTES_PER_GB, 9),
        "bandwidth_gb": round(float(usage.bandwidth_gb or 0.0), 9) if usage else 0.0,
    }


# ==================== MODULE 37: ADVANCED AUTH ====================

@router.post("/oauth/connect")
async def connect_oauth(provider: str, provider_user_id: str, token: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        AuthProvider(provider)
    except ValueError:
        raise HTTPException(status_code=422, detail="Unsupported sign-in provider")
    service = AuthService(db)
    oauth = await service.connect_oauth(user.id, provider, provider_user_id, token)
    return {"id": oauth.id, "provider": oauth.provider.value}


@router.post("/mfa/setup")
async def setup_mfa(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Start two-factor setup: a server-generated TOTP secret. Confirm it with POST /api/v1/auth/mfa/enable."""
    if user.mfa_enabled:
        raise HTTPException(status_code=409, detail="Two-factor authentication is already enabled")
    user.mfa_secret = generate_secret()
    await db.commit()
    return {"method": "totp", "secret": user.mfa_secret, "otpauth_uri": provisioning_uri(user.mfa_secret, user.email)}


@router.get("/mfa")
async def get_mfa(user: User = Depends(get_current_user)):
    """Two-factor status of the signed-in user"""
    return {"enabled": bool(user.mfa_enabled), "method": "totp" if user.mfa_enabled else None}


# ==================== MODULE 38: GDPR & PRIVACY ====================

@router.get("/privacy/settings")
async def get_privacy_settings(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PrivacyService(db)
    settings = await service.get_privacy_settings(user.id)
    if not settings:
        settings = PrivacySettings(user_id=user.id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    return {
        "profile_visibility": settings.profile_visibility,
        "content_visibility": settings.content_visibility,
        "allow_analytics": settings.allow_analytics,
        "allow_marketing": settings.allow_marketing
    }


@router.put("/privacy/settings")
async def update_privacy_settings(
    profile_visibility: str = None,
    content_visibility: str = None,
    allow_analytics: bool = None,
    allow_marketing: bool = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = PrivacyService(db)
    if await service.get_privacy_settings(user.id) is None:
        db.add(PrivacySettings(user_id=user.id))
        await db.commit()
    kwargs = {}
    if allow_analytics is not None:
        kwargs["allow_analytics"] = allow_analytics
    if allow_marketing is not None:
        kwargs["allow_marketing"] = allow_marketing
    try:
        if profile_visibility:
            kwargs["profile_visibility"] = PrivacyLevel(profile_visibility)
        if content_visibility:
            kwargs["content_visibility"] = PrivacyLevel(content_visibility)
    except ValueError:
        raise HTTPException(status_code=422, detail="Visibility must be public, private or friends_only")
    settings = await service.update_privacy_settings(user.id, **kwargs)
    return {
        "profile_visibility": settings.profile_visibility.value,
        "content_visibility": settings.content_visibility.value,
        "allow_analytics": settings.allow_analytics,
        "allow_marketing": settings.allow_marketing,
    }


@router.post("/privacy/request-deletion")
async def request_data_deletion(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PrivacyService(db)
    request = await service.request_data_deletion(user.id)
    return {"id": request.id, "status": request.status, "scheduled_for": request.scheduled_for}


@router.get("/privacy/consents")
async def list_consents(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Every consent decision recorded for the signed-in user, newest first"""
    rows = (await db.execute(
        select(ConsentLog).where(ConsentLog.user_id == user.id).order_by(ConsentLog.id.desc())
    )).scalars().all()
    return [
        {"id": row.id, "consent_type": row.consent_type, "granted": bool(row.granted), "version": row.version}
        for row in rows
    ]


@router.get("/privacy/export")
async def export_personal_data(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """A copy of the personal data held for the signed-in user, as JSON"""
    privacy = (await db.execute(select(PrivacySettings).where(PrivacySettings.user_id == user.id))).scalar_one_or_none()
    consents = (await db.execute(select(ConsentLog).where(ConsentLog.user_id == user.id))).scalars().all()
    deletions = (await db.execute(select(DataDeletionRequest).where(DataDeletionRequest.user_id == user.id))).scalars().all()
    return {
        "account": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "privacy_settings": None if privacy is None else {
            "profile_visibility": privacy.profile_visibility.value,
            "content_visibility": privacy.content_visibility.value,
            "allow_analytics": privacy.allow_analytics,
            "allow_marketing": privacy.allow_marketing,
        },
        "consents": [
            {"consent_type": row.consent_type, "granted": bool(row.granted), "version": row.version}
            for row in consents
        ],
        "deletion_requests": [
            {"status": row.status, "requested_at": row.requested_at.isoformat() if row.requested_at else None,
             "scheduled_for": row.scheduled_for.isoformat() if row.scheduled_for else None}
            for row in deletions
        ],
    }


@router.post("/privacy/consent-log")
async def log_consent(consent_type: str, granted: bool, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PrivacyService(db)
    log = await service.log_consent(user.id, consent_type, granted)
    return {"id": log.id, "consent_type": log.consent_type, "granted": log.granted}


# ==================== MODULE 39: CACHING ====================

class CachePolicyUpdate(BaseModel):
    cache_type: Literal["redis", "cloudflare", "local"]
    ttl_seconds: int = Field(..., ge=1, le=604800)
    max_size_mb: int = Field(100, ge=1, le=102400)
    is_active: bool = True


async def _hit_totals(db: AsyncSession, resource_type: str):
    row = (await db.execute(
        select(func.coalesce(func.sum(CacheMetric.hits), 0), func.coalesce(func.sum(CacheMetric.misses), 0))
        .where(CacheMetric.resource_type == resource_type)
    )).one()
    return int(row[0]), int(row[1])


def _policy_payload(policy: CachePolicy, hits: int, misses: int) -> dict:
    total = hits + misses
    return {
        "resource_type": policy.resource_type,
        "cache_type": policy.cache_type.value,
        "ttl_seconds": policy.ttl_seconds,
        "max_size_mb": policy.max_size_mb,
        "is_active": policy.is_active,
        "hits": hits,
        "misses": misses,
        "hit_rate": round(hits / total * 100, 2) if total else 0.0,
    }


@router.get("/cache/policies")
async def list_cache_policies(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Cache policies with the hit and miss totals recorded for each resource"""
    policies = (await db.execute(select(CachePolicy).order_by(CachePolicy.resource_type))).scalars().all()
    return [_policy_payload(policy, *(await _hit_totals(db, policy.resource_type))) for policy in policies]


@router.put("/cache/policies/{resource_type}")
async def save_cache_policy(
    resource_type: str,
    body: CachePolicyUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin("cache")),
):
    """Create or change the policy for a resource (administrators only)"""
    policy = (await db.execute(select(CachePolicy).where(CachePolicy.resource_type == resource_type))).scalar_one_or_none()
    if policy is None:
        policy = CachePolicy(resource_type=resource_type)
        db.add(policy)
    policy.cache_type = CacheType(body.cache_type)
    policy.ttl_seconds = body.ttl_seconds
    policy.max_size_mb = body.max_size_mb
    policy.is_active = body.is_active
    await db.commit()
    await db.refresh(policy)
    return _policy_payload(policy, *(await _hit_totals(db, resource_type)))


@router.get("/cache/policy/{resource_type}")
async def get_cache_policy(resource_type: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    policy = (await db.execute(select(CachePolicy).where(CachePolicy.resource_type == resource_type))).scalar_one_or_none()
    if policy is None:
        raise HTTPException(status_code=404, detail="Cache policy not found")
    return _policy_payload(policy, *(await _hit_totals(db, resource_type)))


@router.post("/cache/metric")
async def record_cache_metric(resource_type: str, hit: bool, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CacheService(db)
    await service.record_cache_metric(resource_type, hit)
    return {"recorded": True}


# ==================== MODULE 40: PUSH NOTIFICATIONS ====================

@router.post("/notifications/register-device")
async def register_device(device_id: str, token: str, platform: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PushNotificationService(db)
    device = await service.register_device(user.id, device_id, token, platform)
    return {"id": device.id, "platform": device.platform}


@router.get("/notifications/devices")
async def get_user_devices(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PushNotificationService(db)
    devices = await service.get_user_devices(user.id)
    return [{"id": d.id, "platform": d.platform, "is_active": d.is_active} for d in devices]


@router.post("/notifications/send")
async def send_notification(title: str, body: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PushNotificationService(db)
    notif = await service.send_notification(user.id, title, body)
    return {"id": notif.id, "title": notif.title}


@router.get("/notifications")
async def get_notifications(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = PushNotificationService(db)
    notifications = await service.get_notifications(user.id)
    return [{"id": n.id, "title": n.title, "sent_at": n.sent_at, "read_at": n.read_at} for n in notifications]
