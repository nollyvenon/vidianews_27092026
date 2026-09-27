"""APIs for Modules 31-35"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.monetization_service import *
from pydantic import BaseModel

router = APIRouter(prefix="/monetization", tags=["monetization"])

# ==================== MODULE 31: REAL-TIME ====================

class ConnectionCreate(BaseModel):
    connection_id: str
    channels: List[str]

@router.post("/realtime/connect", status_code=status.HTTP_201_CREATED)
async def create_connection(req: ConnectionCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create WebSocket connection"""
    service = RealtimeService(session)
    return await service.create_connection(current_user.id, req.connection_id, req.channels)

# ==================== MODULE 32: BILLING ====================

class SubscriptionCreate(BaseModel):
    tier: str

@router.post("/subscriptions", status_code=status.HTTP_201_CREATED)
async def create_subscription(req: SubscriptionCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create subscription"""
    service = BillingService(session)
    return await service.create_subscription(current_user.id, current_user.organization_id, req.tier)

@router.get("/subscriptions/current")
async def get_subscription(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get current subscription"""
    service = BillingService(session)
    sub = await service.get_subscription(current_user.id)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sub

@router.get("/invoices")
async def list_invoices(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List invoices"""
    service = BillingService(session)
    sub = await service.get_subscription(current_user.id)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.get_invoices(sub.id)

# ==================== MODULE 33: MARKETPLACE ====================

@router.post("/creator-profile", status_code=status.HTTP_201_CREATED)
async def create_creator_profile(bio: Optional[str] = None, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create creator profile"""
    service = MarketplaceService(session)
    return await service.create_creator_profile(current_user.id, bio or "")

@router.get("/creator-profile")
async def get_creator_profile(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get creator profile"""
    service = MarketplaceService(session)
    profile = await service.get_creator_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return profile

@router.get("/creators")
async def list_creators(verified_only: bool = False, session: AsyncSession = Depends(get_db)):
    """List creators"""
    service = MarketplaceService(session)
    return await service.list_creators(verified_only)

# ==================== MODULE 34: ANALYTICS ====================

class DashboardCreate(BaseModel):
    name: str
    widgets: Optional[List] = []

@router.post("/dashboards", status_code=status.HTTP_201_CREATED)
async def create_dashboard(req: DashboardCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create custom dashboard"""
    service = AnalyticsService(session)
    return await service.create_dashboard(current_user.id, req.name, req.widgets)

@router.get("/dashboards")
async def list_dashboards(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List dashboards"""
    service = AnalyticsService(session)
    return await service.list_dashboards(current_user.id)

@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id: int, session: AsyncSession = Depends(get_db)):
    """Get dashboard"""
    service = AnalyticsService(session)
    dashboard = await service.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return dashboard

@router.post("/exports", status_code=status.HTTP_201_CREATED)
async def create_export(export_type: str, format: str = "csv", current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create data export"""
    service = AnalyticsService(session)
    return await service.create_export(current_user.id, export_type, format)

# ==================== MODULE 35: CAMPAIGNS ====================

class CampaignCreate(BaseModel):
    name: str
    subject: str
    body: str

@router.post("/campaigns", status_code=status.HTTP_201_CREATED)
async def create_campaign(req: CampaignCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create email campaign"""
    service = CampaignService(session)
    return await service.create_campaign(current_user.id, req.name, req.subject, req.body)

@router.get("/campaigns")
async def list_campaigns(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List campaigns"""
    service = CampaignService(session)
    return await service.list_campaigns(current_user.id)

@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: int, session: AsyncSession = Depends(get_db)):
    """Get campaign"""
    service = CampaignService(session)
    campaign = await service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return campaign

@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(campaign_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Send campaign"""
    service = CampaignService(session)
    success = await service.send_campaign(campaign_id)
    return {"sent": success}
