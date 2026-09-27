"""Services for Streaming, Analytics & Premium: Modules 56-60"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc, func
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from app.models.streaming_premium import *
import secrets


class LivestreamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_livestream(self, creator_id: int, title: str, description: str = None, scheduled_at: datetime = None) -> LiveStream:
        stream = LiveStream(creator_id=creator_id, title=title, description=description, scheduled_at=scheduled_at, stream_key=secrets.token_urlsafe(32))
        self.session.add(stream)
        await self.session.commit()
        await self.session.refresh(stream)
        return stream

    async def start_livestream(self, stream_id: int) -> None:
        stmt = update(LiveStream).where(LiveStream.id == stream_id).values(
            status="live", started_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def end_livestream(self, stream_id: int) -> None:
        stmt = update(LiveStream).where(LiveStream.id == stream_id).values(
            status="ended", ended_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_active_streams(self) -> List[LiveStream]:
        stmt = select(LiveStream).where(LiveStream.status == "live").order_by(desc(LiveStream.viewer_count))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_viewer(self, stream_id: int, user_id: int = None) -> StreamViewer:
        viewer = StreamViewer(stream_id=stream_id, user_id=user_id)
        self.session.add(viewer)
        await self.session.commit()
        await self.session.refresh(viewer)
        return viewer

    async def add_chat_message(self, stream_id: int, user_id: int, message: str) -> StreamChat:
        chat = StreamChat(stream_id=stream_id, user_id=user_id, message=message)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat


class SubscriptionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscription_tier(self, creator_id: int, name: str, price: float, features: list = []) -> SubscriptionTier:
        tier = SubscriptionTier(creator_id=creator_id, name=name, price_usd=price, features=features)
        self.session.add(tier)
        await self.session.commit()
        await self.session.refresh(tier)
        return tier

    async def get_creator_tiers(self, creator_id: int) -> List[SubscriptionTier]:
        stmt = select(SubscriptionTier).where(SubscriptionTier.creator_id == creator_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def subscribe_to_tier(self, subscriber_id: int, tier_id: int) -> SubscriberRecord:
        record = SubscriberRecord(subscriber_id=subscriber_id, tier_id=tier_id, expires_at=datetime.now(timezone.utc) + timedelta(days=30))
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_subscriber_count(self, tier_id: int) -> int:
        count = await self.session.execute(select(func.count(SubscriberRecord.id)).where(SubscriberRecord.tier_id == tier_id))
        return count.scalar() or 0


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_creator_analytics(self, creator_id: int, views: int = 0, watch_hours: float = 0.0) -> None:
        stmt = update(CreatorAnalytics).where(CreatorAnalytics.creator_id == creator_id).values(
            total_views=CreatorAnalytics.total_views + views,
            total_watch_hours=CreatorAnalytics.total_watch_hours + watch_hours,
            updated_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_creator_analytics(self, creator_id: int) -> Optional[CreatorAnalytics]:
        stmt = select(CreatorAnalytics).where(CreatorAnalytics.creator_id == creator_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def record_daily_analytics(self, creator_id: int, views: int, watch_hours: float, revenue: float = 0.0) -> DailyAnalytic:
        daily = DailyAnalytic(creator_id=creator_id, date=datetime.now(timezone.utc), views=views, watch_hours=watch_hours, revenue=revenue)
        self.session.add(daily)
        await self.session.commit()
        await self.session.refresh(daily)
        return daily

    async def get_daily_analytics(self, creator_id: int, days: int = 7) -> List[DailyAnalytic]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(DailyAnalytic).where(
            and_(DailyAnalytic.creator_id == creator_id, DailyAnalytic.date >= since)
        ).order_by(DailyAnalytic.date)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class PartnershipService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_partnership(self, creator_id: int, partner_id: int, partnership_type: str, description: str = None) -> Partnership:
        partnership = Partnership(creator_id=creator_id, partner_id=partner_id, partnership_type=partnership_type, description=description)
        self.session.add(partnership)
        await self.session.commit()
        await self.session.refresh(partnership)
        return partnership

    async def get_creator_partnerships(self, creator_id: int) -> List[Partnership]:
        stmt = select(Partnership).where(Partnership.creator_id == creator_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_collaboration(self, name: str, participants: list, description: str = None) -> Collaboration:
        collab = Collaboration(name=name, participant_ids=participants, description=description)
        self.session.add(collab)
        await self.session.commit()
        await self.session.refresh(collab)
        return collab


class PremiumService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_premium_subscription(self, user_id: int, features: list = []) -> PremiumSubscription:
        premium = PremiumSubscription(user_id=user_id, enabled_features=features, expires_at=datetime.now(timezone.utc) + timedelta(days=365))
        self.session.add(premium)
        await self.session.commit()
        await self.session.refresh(premium)
        return premium

    async def get_premium_subscription(self, user_id: int) -> Optional[PremiumSubscription]:
        stmt = select(PremiumSubscription).where(PremiumSubscription.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_paywall_content(self, content_id: int, price: float, is_premium_only: bool = False) -> PaywallContent:
        paywall = PaywallContent(content_id=content_id, price=price, is_premium_only=is_premium_only)
        self.session.add(paywall)
        await self.session.commit()
        await self.session.refresh(paywall)
        return paywall

    async def grant_premium_access(self, user_id: int, content_id: int, price: float) -> PremiumAccess:
        access = PremiumAccess(user_id=user_id, content_id=content_id, price_paid=price, expires_at=datetime.now(timezone.utc) + timedelta(days=365))
        self.session.add(access)
        await self.session.commit()
        await self.session.refresh(access)
        return access

    async def check_premium_access(self, user_id: int, content_id: int) -> bool:
        access = await self.session.execute(
            select(PremiumAccess).where(and_(PremiumAccess.user_id == user_id, PremiumAccess.content_id == content_id))
        )
        return access.scalar_one_or_none() is not None
