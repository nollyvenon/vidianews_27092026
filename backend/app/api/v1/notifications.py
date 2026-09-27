"""Notification API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService
from app.models.notifications import NotificationType
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


# Schemas
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True


class CreateNotificationRequest(BaseModel):
    title: str
    message: str
    notification_type: Optional[str] = "system"
    action_url: Optional[str] = None


class EmailNotificationResponse(BaseModel):
    id: int
    recipient_email: str
    subject: str
    status: str
    sent_at: Optional[str] = None

    class Config:
        from_attributes = True


# In-app notification endpoints
@router.get("/me", response_model=List[NotificationResponse])
async def get_my_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get current user's notifications"""
    service = NotificationService(session)
    notifications = await service.get_user_notifications(
        current_user.id,
        unread_only=unread_only,
        limit=limit,
        offset=offset,
    )
    return notifications


@router.get("/me/unread-count", response_model=dict)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get count of unread notifications"""
    service = NotificationService(session)
    count = await service.get_unread_count(current_user.id)
    return {"unread_count": count}


@router.post("/me/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark notification as read"""
    try:
        service = NotificationService(session)
        notification = await service.mark_as_read(notification_id, current_user.id)
        await session.commit()
        return notification
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/me/read-all", response_model=dict)
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark all notifications as read"""
    try:
        service = NotificationService(session)
        count = await service.mark_all_as_read(current_user.id)
        await session.commit()
        return {"marked_count": count}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/me/{notification_id}/archive", response_model=NotificationResponse)
async def archive_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Archive a notification"""
    try:
        service = NotificationService(session)
        notification = await service.archive_notification(notification_id, current_user.id)
        await session.commit()
        return notification
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/me/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete a notification"""
    try:
        service = NotificationService(session)
        await service.delete_notification(notification_id, current_user.id)
        await session.commit()
        return {"deleted": True}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Email notification endpoints
@router.get("/emails/pending", response_model=List[EmailNotificationResponse])
async def get_pending_emails(
    limit: int = Query(100, le=1000),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get pending emails (admin only)"""
    service = NotificationService(session)
    emails = await service.get_pending_emails(limit=limit)
    return emails


@router.post("/emails/{email_id}/mark-sent", response_model=EmailNotificationResponse)
async def mark_email_sent(
    email_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark email as sent"""
    try:
        service = NotificationService(session)
        email = await service.mark_email_sent(email_id)
        await session.commit()
        return email
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Push notification endpoints
@router.get("/push/pending", response_model=dict)
async def get_pending_pushes(
    limit: int = Query(100, le=1000),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get pending push notifications (admin only)"""
    service = NotificationService(session)
    pushes = await service.get_pending_pushes(limit=limit)
    return {"count": len(pushes), "notifications": pushes}


# Notification logs
@router.get("/me/logs", response_model=dict)
async def get_notification_logs(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get notification logs for current user"""
    service = NotificationService(session)
    logs = await service.get_notification_logs(current_user.id, limit=limit, offset=offset)
    return {"logs": logs, "count": len(logs)}
