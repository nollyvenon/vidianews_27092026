"""Streaming, Analytics & Premium endpoints: Modules 56-60"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.streaming_premium import *
from app.services.streaming_premium_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["streaming-premium"])


# ==================== MODULE 56: LIVESTREAMING ====================

@router.post("/livestream")
async def create_livestream(title: str, description: str = None, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = LivestreamService(db)
    stream = await service.create_livestream(user["id"], title, description)
    return {"id": stream.id, "stream_key": stream.stream_key, "status": stream.status}


@router.put("/livestream/{stream_id}/start")
async def start_livestream(stream_id: int, db: AsyncSession = Depends(get_db)):
    service = LivestreamService(db)
    await service.start_livestream(stream_id)
    return {"started": True}


@router.put("/livestream/{stream_id}/end")
async def end_livestream(stream_id: int, db: AsyncSession = Depends(get_db)):
    service = LivestreamService(db)
    await service.end_livestream(stream_id)
    return {"ended": True}


@router.get("/livestream/active")
async def get_active_streams(db: AsyncSession = Depends(get_db)):
    service = LivestreamService(db)
    streams = await service.get_active_streams()
    return [{"id": s.id, "title": s.title, "viewers": s.viewer_count} for s in streams]


@router.post("/livestream/{stream_id}/chat")
async def send_chat(stream_id: int, message: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = LivestreamService(db)
    chat = await service.add_chat_message(stream_id, user["id"], message)
    return {"id": chat.id, "sent_at": chat.sent_at}


# ==================== MODULE 57: EXTENDED SUBSCRIPTIONS ====================

@router.post("/subscriptions/tier")
async def create_subscription_tier(name: str, price: float, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = SubscriptionService(db)
    tier = await service.create_subscription_tier(user["id"], name, price)
    return {"id": tier.id, "name": tier.name, "price": tier.price_usd}


@router.get("/subscriptions/tiers/{creator_id}")
async def get_creator_tiers(creator_id: int, db: AsyncSession = Depends(get_db)):
    service = SubscriptionService(db)
    tiers = await service.get_creator_tiers(creator_id)
    return [{"id": t.id, "name": t.name, "price": t.price_usd} for t in tiers]


@router.post("/subscriptions/tier/{tier_id}/subscribe")
async def subscribe_to_tier(tier_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = SubscriptionService(db)
    record = await service.subscribe_to_tier(user["id"], tier_id)
    return {"id": record.id, "tier_id": tier_id, "subscribed": True}


# ==================== MODULE 58: CREATOR ANALYTICS ====================

@router.get("/analytics/creator")
async def get_creator_analytics(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AnalyticsService(db)
    analytics = await service.get_creator_analytics(user["id"])
    if not analytics:
        return {"error": "No analytics found"}
    return {"total_views": analytics.total_views, "watch_hours": analytics.total_watch_hours, "subscribers": analytics.subscriber_count}


@router.post("/analytics/daily")
async def record_daily_analytics(views: int, watch_hours: float, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AnalyticsService(db)
    daily = await service.record_daily_analytics(user["id"], views, watch_hours)
    return {"id": daily.id, "date": daily.date}


@router.get("/analytics/daily")
async def get_daily_analytics(days: int = 7, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AnalyticsService(db)
    analytics = await service.get_daily_analytics(user["id"], days)
    return [{"date": a.date, "views": a.views, "watch_hours": a.watch_hours} for a in analytics]


# ==================== MODULE 59: PARTNERSHIPS ====================

@router.post("/partnerships")
async def create_partnership(partner_id: int, partnership_type: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PartnershipService(db)
    partnership = await service.create_partnership(user["id"], partner_id, partnership_type)
    return {"id": partnership.id, "type": partnership.partnership_type}


@router.get("/partnerships")
async def get_creator_partnerships(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PartnershipService(db)
    partnerships = await service.get_creator_partnerships(user["id"])
    return [{"id": p.id, "type": p.partnership_type, "status": p.status} for p in partnerships]


@router.post("/collaborations")
async def create_collaboration(name: str, participants: list, db: AsyncSession = Depends(get_db)):
    service = PartnershipService(db)
    collab = await service.create_collaboration(name, participants)
    return {"id": collab.id, "name": collab.name}


# ==================== MODULE 60: PREMIUM FEATURES ====================

@router.post("/premium/subscribe")
async def create_premium_subscription(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PremiumService(db)
    premium = await service.create_premium_subscription(user["id"], ["hd_streaming", "ad_free"])
    return {"id": premium.id, "is_active": premium.is_active}


@router.get("/premium/status")
async def get_premium_status(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PremiumService(db)
    premium = await service.get_premium_subscription(user["id"])
    if not premium:
        return {"is_premium": False}
    return {"is_premium": premium.is_active, "features": premium.enabled_features}


@router.post("/content/{content_id}/paywall")
async def add_paywall(content_id: int, price: float, db: AsyncSession = Depends(get_db)):
    service = PremiumService(db)
    paywall = await service.add_paywall_content(content_id, price)
    return {"id": paywall.id, "price": paywall.price}


@router.post("/content/{content_id}/purchase")
async def purchase_premium_access(content_id: int, price: float, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PremiumService(db)
    access = await service.grant_premium_access(user["id"], content_id, price)
    return {"id": access.id, "access_granted": True}


@router.get("/content/{content_id}/access")
async def check_premium_access(content_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = PremiumService(db)
    has_access = await service.check_premium_access(user["id"], content_id)
    return {"has_access": has_access}
