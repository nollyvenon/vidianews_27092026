"""Services for Modules 31-35"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.models.monetization import *


class RealtimeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_connection(self, user_id: int, connection_id: str, channels: List[str]) -> WebSocketConnection:
        conn = WebSocketConnection(user_id=user_id, connection_id=connection_id, channels=channels)
        self.session.add(conn)
        await self.session.commit()
        await self.session.refresh(conn)
        return conn

    async def get_connection(self, connection_id: str) -> Optional[WebSocketConnection]:
        stmt = select(WebSocketConnection).where(WebSocketConnection.connection_id == connection_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def log_event(self, event_type: str, channel: str, data: Dict) -> RealtimeEvent:
        event = RealtimeEvent(event_type=event_type, channel=channel, data=data)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event


class BillingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscription(self, user_id: int, org_id: int, tier: str) -> Subscription:
        sub = Subscription(user_id=user_id, organization_id=org_id, tier=tier)
        self.session.add(sub)
        await self.session.commit()
        await self.session.refresh(sub)
        return sub

    async def get_subscription(self, user_id: int) -> Optional[Subscription]:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_invoice(self, sub_id: int, amount: float) -> Invoice:
        invoice = Invoice(subscription_id=sub_id, amount=amount, due_date=datetime.now(timezone.utc) + timedelta(days=30))
        self.session.add(invoice)
        await self.session.commit()
        await self.session.refresh(invoice)
        return invoice

    async def get_invoices(self, sub_id: int) -> List[Invoice]:
        stmt = select(Invoice).where(Invoice.subscription_id == sub_id).order_by(desc(Invoice.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_payment(self, user_id: int, invoice_id: int, amount: float) -> Payment:
        payment = Payment(user_id=user_id, invoice_id=invoice_id, amount=amount, status=PaymentStatus.COMPLETED)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment


class MarketplaceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_creator_profile(self, user_id: int, bio: str = "") -> CreatorProfile:
        profile = CreatorProfile(user_id=user_id, bio=bio)
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def get_creator_profile(self, user_id: int) -> Optional[CreatorProfile]:
        stmt = select(CreatorProfile).where(CreatorProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_creators(self, verified_only: bool = False) -> List[CreatorProfile]:
        stmt = select(CreatorProfile)
        if verified_only:
            stmt = stmt.where(CreatorProfile.is_verified == True)
        stmt = stmt.order_by(desc(CreatorProfile.followers))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_earnings(self, creator_id: int, amount: float) -> bool:
        stmt = update(CreatorProfile).where(CreatorProfile.id == creator_id).values(
            earnings=CreatorProfile.earnings + amount
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dashboard(self, user_id: int, name: str, widgets: List = []) -> CustomDashboard:
        dashboard = CustomDashboard(user_id=user_id, name=name, widgets=widgets)
        self.session.add(dashboard)
        await self.session.commit()
        await self.session.refresh(dashboard)
        return dashboard

    async def get_dashboard(self, dashboard_id: int) -> Optional[CustomDashboard]:
        stmt = select(CustomDashboard).where(CustomDashboard.id == dashboard_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_dashboards(self, user_id: int) -> List[CustomDashboard]:
        stmt = select(CustomDashboard).where(CustomDashboard.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_export(self, user_id: int, export_type: str, format: str = "csv") -> DataExport:
        export = DataExport(user_id=user_id, export_type=export_type, format=format)
        self.session.add(export)
        await self.session.commit()
        await self.session.refresh(export)
        return export


class CampaignService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_campaign(self, user_id: int, name: str, subject: str, body: str) -> EmailCampaign:
        campaign = EmailCampaign(creator_id=user_id, name=name, subject=subject, body=body)
        self.session.add(campaign)
        await self.session.commit()
        await self.session.refresh(campaign)
        return campaign

    async def get_campaign(self, campaign_id: int) -> Optional[EmailCampaign]:
        stmt = select(EmailCampaign).where(EmailCampaign.id == campaign_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_campaigns(self, user_id: int) -> List[EmailCampaign]:
        stmt = select(EmailCampaign).where(EmailCampaign.creator_id == user_id).order_by(desc(EmailCampaign.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def send_campaign(self, campaign_id: int) -> bool:
        stmt = update(EmailCampaign).where(EmailCampaign.id == campaign_id).values(status="sent", sent_at=datetime.now(timezone.utc))
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
