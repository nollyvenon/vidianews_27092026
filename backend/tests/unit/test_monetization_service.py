"""Tests for monetization (Modules 31-35)"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.base import Base
from app.models.monetization import *
from app.services.monetization_service import *


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_connection(test_db):
    service = RealtimeService(test_db)
    conn = await service.create_connection(1, "conn_123", ["channel1"])
    assert conn.connection_id == "conn_123"

@pytest.mark.asyncio
async def test_create_subscription(test_db):
    service = BillingService(test_db)
    sub = await service.create_subscription(1, 1, "pro")
    assert sub.tier == "pro"

@pytest.mark.asyncio
async def test_create_invoice(test_db):
    service = BillingService(test_db)
    sub = await service.create_subscription(1, 1, "pro")
    invoice = await service.create_invoice(sub.id, 99.99)
    assert invoice.amount == 99.99

@pytest.mark.asyncio
async def test_create_creator_profile(test_db):
    service = MarketplaceService(test_db)
    profile = await service.create_creator_profile(1, "Amazing creator")
    assert profile.user_id == 1

@pytest.mark.asyncio
async def test_create_dashboard(test_db):
    service = AnalyticsService(test_db)
    dashboard = await service.create_dashboard(1, "Q3 Analytics")
    assert dashboard.name == "Q3 Analytics"

@pytest.mark.asyncio
async def test_create_campaign(test_db):
    service = CampaignService(test_db)
    campaign = await service.create_campaign(1, "Welcome", "Welcome!", "Thanks for joining")
    assert campaign.name == "Welcome"
