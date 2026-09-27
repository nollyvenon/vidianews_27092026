"""Social, Messaging & Discovery endpoints: Modules 51-55"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.social_messaging import *
from app.services.social_messaging_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["social-messaging"])


# ==================== MODULE 51: CONTENT MODERATION ====================

@router.post("/moderation/rule")
async def create_moderation_rule(name: str, pattern: str, db: AsyncSession = Depends(get_db)):
    service = ModerationService(db)
    rule = await service.create_moderation_rule(name, pattern)
    return {"id": rule.id, "name": rule.rule_name}


@router.post("/moderation/report")
async def report_content(content_id: int, reason: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ModerationService(db)
    report = await service.report_content(content_id, user["id"], reason)
    return {"id": report.id, "status": report.status}


@router.get("/moderation/pending")
async def get_pending_reports(db: AsyncSession = Depends(get_db)):
    service = ModerationService(db)
    reports = await service.get_pending_reports()
    return [{"id": r.id, "content_id": r.content_id, "reason": r.reason} for r in reports]


# ==================== MODULE 52: SOCIAL FEATURES ====================

@router.post("/social/follow/{user_id}")
async def follow_user(user_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = SocialService(db)
    follow = await service.follow_user(user["id"], user_id)
    return {"id": follow.id, "follower_id": follow.follower_id}


@router.delete("/social/follow/{user_id}")
async def unfollow_user(user_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = SocialService(db)
    await service.unfollow_user(user["id"], user_id)
    return {"unfollowed": True}


@router.get("/social/followers/{user_id}")
async def get_followers(user_id: int, db: AsyncSession = Depends(get_db)):
    service = SocialService(db)
    followers = await service.get_followers(user_id)
    return [{"id": f.id, "follower_id": f.follower_id} for f in followers]


@router.post("/social/mention")
async def create_mention(content_id: int, mentioned_user_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = SocialService(db)
    mention = await service.create_mention(content_id, mentioned_user_id, user["id"])
    return {"id": mention.id, "mentioned_user_id": mention.mentioned_user_id}


@router.post("/social/hashtag")
async def add_hashtag(content_id: int, tag: str, db: AsyncSession = Depends(get_db)):
    service = SocialService(db)
    hashtag = await service.add_hashtag(content_id, tag)
    return {"id": hashtag.id, "tag": tag}


# ==================== MODULE 53: MESSAGING ====================

@router.post("/messages/send")
async def send_message(recipient_id: int, content: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = MessagingService(db)
    message = await service.send_message(user["id"], recipient_id, content)
    return {"id": message.id, "sent_at": message.sent_at}


@router.get("/messages/{user_id}")
async def get_conversation(user_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = MessagingService(db)
    messages = await service.get_conversation(user["id"], user_id)
    return [{"id": m.id, "sender_id": m.sender_id, "content": m.content, "is_read": m.is_read} for m in messages]


@router.put("/messages/{message_id}/read")
async def mark_message_read(message_id: int, db: AsyncSession = Depends(get_db)):
    service = MessagingService(db)
    await service.mark_as_read(message_id)
    return {"read": True}


@router.get("/messages/unread/count")
async def get_unread_count(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = MessagingService(db)
    count = await service.get_unread_count(user["id"])
    return {"unread_count": count}


# ==================== MODULE 54: NOTIFICATIONS ====================

@router.post("/notifications")
async def create_notification(notification_type: str, message: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = NotificationService(db)
    notif = await service.create_notification(user["id"], notification_type, message)
    return {"id": notif.id, "type": notif.notification_type}


@router.get("/notifications")
async def get_notifications(unread_only: bool = False, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = NotificationService(db)
    notifications = await service.get_notifications(user["id"], unread_only)
    return [{"id": n.id, "type": n.notification_type, "message": n.message, "is_read": n.is_read} for n in notifications]


@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int, db: AsyncSession = Depends(get_db)):
    service = NotificationService(db)
    await service.mark_as_read(notification_id)
    return {"read": True}


# ==================== MODULE 55: SEARCH & DISCOVERY ====================

@router.post("/search")
async def search(query: str, search_type: str = "keyword", db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = DiscoveryService(db)
    search = await service.log_search(query, user["id"], search_type)
    return {"id": search.id, "query": search.query}


@router.get("/recommendations")
async def get_recommendations(limit: int = 10, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = DiscoveryService(db)
    recs = await service.get_recommendations(user["id"], limit)
    return [{"id": r.id, "content_id": r.content_id, "score": r.recommendation_score} for r in recs]


@router.get("/trending")
async def get_trending_topics(limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = DiscoveryService(db)
    trends = await service.get_trending_topics(limit)
    return [{"id": t.id, "topic": t.topic, "score": t.trend_score} for t in trends]
