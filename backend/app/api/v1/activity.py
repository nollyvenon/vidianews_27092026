"""Activity log and audit trail API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.activity_service import ActivityService
from app.models.activity_logs import ActionType, EntityType
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


# Schemas
class ActivityLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
    description: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
    changed_fields: List[str]
    created_at: str

    class Config:
        from_attributes = True


class FeedItemResponse(BaseModel):
    id: int
    action: str
    title: str
    description: Optional[str]
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True


# User activity endpoints
@router.get("/me", response_model=List[ActivityLogResponse])
async def get_my_activities(
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get current user's activities"""
    service = ActivityService(session)

    action_enum = ActionType(action) if action else None
    entity_enum = EntityType(entity_type) if entity_type else None

    activities = await service.get_user_activities(
        current_user.id,
        action=action_enum,
        entity_type=entity_enum,
        limit=limit,
        offset=offset,
    )
    return activities


@router.get("/me/count", response_model=dict)
async def get_activity_count(
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get count of user activities"""
    service = ActivityService(session)
    count = await service.get_user_activity_count(current_user.id, days=days)
    return {"count": count, "period_days": days}


@router.get("/me/summary", response_model=dict)
async def get_activity_summary(
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get activity summary for user"""
    service = ActivityService(session)
    summary = await service.get_activity_summary(current_user.id, days=days)
    return summary


# Audit trail endpoints
@router.get("/audit/{entity_type}/{entity_id}", response_model=List[AuditLogResponse])
async def get_audit_trail(
    entity_type: str,
    entity_id: int,
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get audit trail for an entity"""
    try:
        entity_enum = EntityType(entity_type)
        service = ActivityService(session)
        logs = await service.get_entity_audit_trail(
            entity_enum,
            entity_id,
            limit=limit,
            offset=offset,
        )
        return logs
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid entity type")


@router.get("/me/audit", response_model=List[AuditLogResponse])
async def get_my_audit_logs(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get all changes made by current user"""
    service = ActivityService(session)
    logs = await service.get_user_audit_logs(
        current_user.id,
        limit=limit,
        offset=offset,
    )
    return logs


# Activity feed endpoints
@router.get("/feed", response_model=List[FeedItemResponse])
async def get_activity_feed(
    unread_only: bool = Query(False),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user's activity feed"""
    service = ActivityService(session)
    feed = await service.get_user_feed(
        current_user.id,
        unread_only=unread_only,
        limit=limit,
        offset=offset,
    )
    return feed


@router.get("/feed/unread-count", response_model=dict)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get count of unread feed items"""
    service = ActivityService(session)
    count = await service.get_unread_feed_count(current_user.id)
    return {"unread_count": count}


@router.post("/feed/{feed_id}/read", response_model=FeedItemResponse)
async def mark_feed_read(
    feed_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark feed item as read"""
    try:
        service = ActivityService(session)
        feed = await service.mark_feed_item_read(feed_id, current_user.id)
        await session.commit()
        return feed
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/feed/read-all", response_model=dict)
async def mark_all_feed_read(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark all feed items as read"""
    try:
        service = ActivityService(session)
        count = await service.mark_all_feed_read(current_user.id)
        await session.commit()
        return {"marked_count": count}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/feed/{feed_id}/archive", response_model=FeedItemResponse)
async def archive_feed_item(
    feed_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Archive a feed item"""
    try:
        service = ActivityService(session)
        feed = await service.archive_feed_item(feed_id, current_user.id)
        await session.commit()
        return feed
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
