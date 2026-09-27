"""Tests for Streaming, Analytics & Premium services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.streaming_premium import *
from app.services.streaming_premium_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestLivestreamService:
    @pytest.mark.asyncio
    async def test_create_livestream(self, db):
        service = LivestreamService(db)
        stream = await service.create_livestream(1, "My Live Stream", "Come watch!")

        assert stream.creator_id == 1
        assert stream.title == "My Live Stream"
        assert stream.status == "scheduled"

    @pytest.mark.asyncio
    async def test_start_livestream(self, db):
        stream = LiveStream(creator_id=1, title="Test Stream", status="scheduled")
        db.add(stream)
        await db.commit()

        service = LivestreamService(db)
        await service.start_livestream(stream.id)

        updated = await db.get(LiveStream, stream.id)
        assert updated.status == "live"

    @pytest.mark.asyncio
    async def test_add_chat_message(self, db):
        stream = LiveStream(creator_id=1, title="Test", status="live")
        db.add(stream)
        await db.commit()

        service = LivestreamService(db)
        chat = await service.add_chat_message(stream.id, 2, "Great stream!")

        assert chat.message == "Great stream!"


class TestSubscriptionService:
    @pytest.mark.asyncio
    async def test_create_subscription_tier(self, db):
        service = SubscriptionService(db)
        tier = await service.create_subscription_tier(1, "Gold", 9.99, ["exclusive_content"])

        assert tier.name == "Gold"
        assert tier.price_usd == 9.99

    @pytest.mark.asyncio
    async def test_get_creator_tiers(self, db):
        tier = SubscriptionTier(creator_id=1, name="Silver", price_usd=4.99)
        db.add(tier)
        await db.commit()

        service = SubscriptionService(db)
        tiers = await service.get_creator_tiers(1)

        assert len(tiers) == 1
        assert tiers[0].name == "Silver"

    @pytest.mark.asyncio
    async def test_subscribe_to_tier(self, db):
        tier = SubscriptionTier(creator_id=1, name="Platinum", price_usd=19.99)
        db.add(tier)
        await db.commit()

        service = SubscriptionService(db)
        record = await service.subscribe_to_tier(2, tier.id)

        assert record.subscriber_id == 2
        assert record.tier_id == tier.id


class TestAnalyticsService:
    @pytest.mark.asyncio
    async def test_record_daily_analytics(self, db):
        service = AnalyticsService(db)
        daily = await service.record_daily_analytics(1, 1000, 50.5, 25.0)

        assert daily.creator_id == 1
        assert daily.views == 1000
        assert daily.watch_hours == 50.5

    @pytest.mark.asyncio
    async def test_get_daily_analytics(self, db):
        daily = DailyAnalytic(creator_id=1, views=500, watch_hours=25.0)
        db.add(daily)
        await db.commit()

        service = AnalyticsService(db)
        analytics = await service.get_daily_analytics(1, 7)

        assert len(analytics) >= 1


class TestPartnershipService:
    @pytest.mark.asyncio
    async def test_create_partnership(self, db):
        service = PartnershipService(db)
        partnership = await service.create_partnership(1, 2, "brand_deal", "Collab with XYZ brand")

        assert partnership.creator_id == 1
        assert partnership.partner_id == 2

    @pytest.mark.asyncio
    async def test_get_creator_partnerships(self, db):
        partnership = Partnership(creator_id=1, partner_id=3, partnership_type="sponsorship")
        db.add(partnership)
        await db.commit()

        service = PartnershipService(db)
        partnerships = await service.get_creator_partnerships(1)

        assert len(partnerships) == 1

    @pytest.mark.asyncio
    async def test_create_collaboration(self, db):
        service = PartnershipService(db)
        collab = await service.create_collaboration("Joint Project", [1, 2, 3])

        assert collab.name == "Joint Project"


class TestPremiumService:
    @pytest.mark.asyncio
    async def test_create_premium_subscription(self, db):
        service = PremiumService(db)
        premium = await service.create_premium_subscription(1, ["hd_streaming", "ad_free"])

        assert premium.user_id == 1
        assert premium.is_active == True

    @pytest.mark.asyncio
    async def test_get_premium_subscription(self, db):
        premium = PremiumSubscription(user_id=1, is_active=True)
        db.add(premium)
        await db.commit()

        service = PremiumService(db)
        result = await service.get_premium_subscription(1)

        assert result is not None
        assert result.user_id == 1

    @pytest.mark.asyncio
    async def test_add_paywall_content(self, db):
        service = PremiumService(db)
        paywall = await service.add_paywall_content(1, 2.99)

        assert paywall.content_id == 1
        assert paywall.price == 2.99

    @pytest.mark.asyncio
    async def test_grant_premium_access(self, db):
        service = PremiumService(db)
        access = await service.grant_premium_access(1, 5, 2.99)

        assert access.user_id == 1
        assert access.content_id == 5

    @pytest.mark.asyncio
    async def test_check_premium_access(self, db):
        access = PremiumAccess(user_id=1, content_id=10, price_paid=3.99)
        db.add(access)
        await db.commit()

        service = PremiumService(db)
        has_access = await service.check_premium_access(1, 10)

        assert has_access == True
