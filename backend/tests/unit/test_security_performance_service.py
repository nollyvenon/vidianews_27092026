"""Tests for Security & Performance services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.security_performance import *
from app.services.security_performance_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestRateLimitService:
    @pytest.mark.asyncio
    async def test_check_rate_limit(self, db):
        service = RateLimitService(db)
        result1 = await service.check_rate_limit(1, "/api/test", limit=2)
        result2 = await service.check_rate_limit(1, "/api/test", limit=2)
        result3 = await service.check_rate_limit(1, "/api/test", limit=2)

        assert result1 == True
        assert result2 == True
        assert result3 == False

    @pytest.mark.asyncio
    async def test_get_quota_usage(self, db):
        quota = QuotaUsage(user_id=1, api_calls=500, storage_gb=2.5)
        db.add(quota)
        await db.commit()

        service = RateLimitService(db)
        result = await service.get_quota_usage(1)

        assert result is not None
        assert result.api_calls == 500


class TestAuthService:
    @pytest.mark.asyncio
    async def test_connect_oauth(self, db):
        service = AuthService(db)
        oauth = await service.connect_oauth(1, "google", "user123", "token_abc")

        assert oauth.user_id == 1
        assert oauth.provider == "google"

    @pytest.mark.asyncio
    async def test_setup_mfa(self, db):
        service = AuthService(db)
        mfa = await service.setup_mfa(1, "totp", "secret_key_123")

        assert mfa.user_id == 1
        assert mfa.mfa_method == "totp"
        assert mfa.is_verified == False

    @pytest.mark.asyncio
    async def test_get_mfa(self, db):
        mfa_setup = MFASetup(user_id=1, mfa_method="sms", secret="secret_456")
        db.add(mfa_setup)
        await db.commit()

        service = AuthService(db)
        result = await service.get_mfa(1)

        assert result is not None
        assert result.mfa_method == "sms"


class TestPrivacyService:
    @pytest.mark.asyncio
    async def test_get_privacy_settings(self, db):
        settings = PrivacySettings(user_id=1, profile_visibility="public")
        db.add(settings)
        await db.commit()

        service = PrivacyService(db)
        result = await service.get_privacy_settings(1)

        assert result is not None
        assert result.profile_visibility == "public"

    @pytest.mark.asyncio
    async def test_update_privacy_settings(self, db):
        settings = PrivacySettings(user_id=1, profile_visibility="public")
        db.add(settings)
        await db.commit()

        service = PrivacyService(db)
        updated = await service.update_privacy_settings(1, profile_visibility="private")

        assert updated.profile_visibility == "private"

    @pytest.mark.asyncio
    async def test_request_data_deletion(self, db):
        service = PrivacyService(db)
        request = await service.request_data_deletion(1)

        assert request.user_id == 1
        assert request.status == "pending"

    @pytest.mark.asyncio
    async def test_log_consent(self, db):
        service = PrivacyService(db)
        log = await service.log_consent(1, "marketing", True)

        assert log.user_id == 1
        assert log.consent_type == "marketing"
        assert log.granted == True


class TestCacheService:
    @pytest.mark.asyncio
    async def test_get_cache_policy(self, db):
        policy = CachePolicy(resource_type="content", cache_type="redis", ttl_seconds=3600)
        db.add(policy)
        await db.commit()

        service = CacheService(db)
        result = await service.get_cache_policy("content")

        assert result is not None
        assert result.ttl_seconds == 3600

    @pytest.mark.asyncio
    async def test_record_cache_metric(self, db):
        service = CacheService(db)
        await service.record_cache_metric("content", True)

        metric = await service.session.execute(select(CacheMetric).where(CacheMetric.resource_type == "content"))
        result = metric.scalar_one()

        assert result.hits == 1


class TestPushNotificationService:
    @pytest.mark.asyncio
    async def test_register_device(self, db):
        service = PushNotificationService(db)
        device = await service.register_device(1, "device_1", "token_xyz", "ios")

        assert device.user_id == 1
        assert device.platform == "ios"

    @pytest.mark.asyncio
    async def test_get_user_devices(self, db):
        device = DeviceToken(user_id=1, device_id="device_1", token="token_123", platform="android")
        db.add(device)
        await db.commit()

        service = PushNotificationService(db)
        devices = await service.get_user_devices(1)

        assert len(devices) == 1
        assert devices[0].platform == "android"

    @pytest.mark.asyncio
    async def test_send_notification(self, db):
        service = PushNotificationService(db)
        notif = await service.send_notification(1, "Test Title", "Test Body")

        assert notif.user_id == 1
        assert notif.title == "Test Title"

    @pytest.mark.asyncio
    async def test_get_notifications(self, db):
        notif = PushNotification(user_id=1, title="Alert", body="Test notification")
        db.add(notif)
        await db.commit()

        service = PushNotificationService(db)
        notifications = await service.get_notifications(1)

        assert len(notifications) == 1
        assert notifications[0].title == "Alert"
