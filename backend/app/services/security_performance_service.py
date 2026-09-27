"""Services for Modules 36-40"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.models.security_performance import *


class RateLimitService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_rate_limit(self, user_id: int, endpoint: str, limit: int = 100) -> bool:
        now = datetime.now(timezone.utc)
        stmt = select(RateLimitBucket).where(
            and_(RateLimitBucket.user_id == user_id, RateLimitBucket.endpoint == endpoint, RateLimitBucket.reset_at > now)
        )
        result = await self.session.execute(stmt)
        bucket = result.scalar_one_or_none()

        if not bucket:
            bucket = RateLimitBucket(user_id=user_id, endpoint=endpoint, reset_at=now + timedelta(hours=1))
            self.session.add(bucket)

        if bucket.requests_count >= limit:
            return False

        bucket.requests_count += 1
        await self.session.commit()
        return True

    async def get_quota_usage(self, user_id: int) -> Optional[QuotaUsage]:
        stmt = select(QuotaUsage).where(QuotaUsage.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def connect_oauth(self, user_id: int, provider: str, provider_user_id: str, token: str) -> OAuthProvider:
        oauth = OAuthProvider(user_id=user_id, provider=provider, provider_user_id=provider_user_id, access_token=token)
        self.session.add(oauth)
        await self.session.commit()
        await self.session.refresh(oauth)
        return oauth

    async def setup_mfa(self, user_id: int, method: str, secret: str) -> MFASetup:
        mfa = MFASetup(user_id=user_id, mfa_method=method, secret=secret)
        self.session.add(mfa)
        await self.session.commit()
        await self.session.refresh(mfa)
        return mfa

    async def get_mfa(self, user_id: int) -> Optional[MFASetup]:
        stmt = select(MFASetup).where(MFASetup.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class PrivacyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_privacy_settings(self, user_id: int) -> Optional[PrivacySettings]:
        stmt = select(PrivacySettings).where(PrivacySettings.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_privacy_settings(self, user_id: int, **kwargs) -> PrivacySettings:
        stmt = update(PrivacySettings).where(PrivacySettings.user_id == user_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_privacy_settings(user_id)

    async def request_data_deletion(self, user_id: int) -> DataDeletionRequest:
        request = DataDeletionRequest(user_id=user_id, scheduled_for=datetime.now(timezone.utc) + timedelta(days=30))
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request

    async def log_consent(self, user_id: int, consent_type: str, granted: bool) -> ConsentLog:
        log = ConsentLog(user_id=user_id, consent_type=consent_type, granted=granted)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log


class CacheService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cache_policy(self, resource_type: str) -> Optional[CachePolicy]:
        stmt = select(CachePolicy).where(CachePolicy.resource_type == resource_type)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def record_cache_metric(self, resource_type: str, hit: bool) -> None:
        stmt = select(CacheMetric).where(CacheMetric.resource_type == resource_type)
        result = await self.session.execute(stmt)
        metric = result.scalar_one_or_none()

        if not metric:
            metric = CacheMetric(resource_type=resource_type)
            self.session.add(metric)

        if hit:
            metric.hits += 1
        else:
            metric.misses += 1

        await self.session.commit()


class PushNotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_device(self, user_id: int, device_id: str, token: str, platform: str) -> DeviceToken:
        device = DeviceToken(user_id=user_id, device_id=device_id, token=token, platform=platform)
        self.session.add(device)
        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def get_user_devices(self, user_id: int) -> List[DeviceToken]:
        stmt = select(DeviceToken).where(and_(DeviceToken.user_id == user_id, DeviceToken.is_active == True))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def send_notification(self, user_id: int, title: str, body: str, data: Dict = {}) -> PushNotification:
        notif = PushNotification(user_id=user_id, title=title, body=body, data=data)
        self.session.add(notif)
        await self.session.commit()
        await self.session.refresh(notif)
        return notif

    async def get_notifications(self, user_id: int) -> List[PushNotification]:
        stmt = select(PushNotification).where(PushNotification.user_id == user_id).order_by(desc(PushNotification.sent_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()
