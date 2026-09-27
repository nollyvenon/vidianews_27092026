"""Notification service for email, push, and in-app notifications"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from app.models.notifications import (
    Notification, EmailNotification, PushNotification,
    NotificationTemplate, NotificationLog,
    NotificationType, NotificationChannel
)
from app.models.user import User
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.logger import logger
import json


class NotificationService:
    """Service for managing all notification types"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # In-app notifications
    async def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.SYSTEM,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        action_url: Optional[str] = None,
        extra_data: Optional[Dict] = None,
    ) -> Notification:
        """Create an in-app notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            resource_type=resource_type,
            resource_id=resource_id,
            action_url=action_url,
            extra_data=extra_data or {},
        )
        self.session.add(notification)
        await self.session.flush()
        return notification

    async def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Notification]:
        """Get user notifications"""
        stmt = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
        stmt = stmt.order_by(Notification.created_at.desc()).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications"""
        stmt = select(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_archived == False,
            )
        )
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        """Mark notification as read"""
        stmt = select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notification = (await self.session.execute(stmt)).scalar_one_or_none()
        if not notification:
            raise NotFoundError(f"Notification {notification_id} not found")

        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        await self.session.flush()
        return notification

    async def mark_all_as_read(self, user_id: int) -> int:
        """Mark all unread notifications as read"""
        stmt = (
            update(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False,
                )
            )
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def archive_notification(self, notification_id: int, user_id: int) -> Notification:
        """Archive a notification"""
        stmt = select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notification = (await self.session.execute(stmt)).scalar_one_or_none()
        if not notification:
            raise NotFoundError(f"Notification {notification_id} not found")

        notification.is_archived = True
        await self.session.flush()
        return notification

    async def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete a notification"""
        stmt = select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notification = (await self.session.execute(stmt)).scalar_one_or_none()
        if not notification:
            raise NotFoundError(f"Notification {notification_id} not found")

        await self.session.delete(notification)
        await self.session.flush()
        return True

    # Email notifications
    async def send_email(
        self,
        user_id: int,
        recipient_email: str,
        subject: str,
        template: str,
        notification_id: Optional[int] = None,
    ) -> EmailNotification:
        """Create email notification record"""
        email_notif = EmailNotification(
            user_id=user_id,
            recipient_email=recipient_email,
            subject=subject,
            template=template,
            notification_id=notification_id,
        )
        self.session.add(email_notif)
        await self.session.flush()

        # Log the action
        await self._log_notification(user_id, notification_id, "created", NotificationChannel.EMAIL, "pending")

        return email_notif

    async def mark_email_sent(self, email_id: int) -> EmailNotification:
        """Mark email as sent"""
        email_notif = await self.session.get(EmailNotification, email_id)
        if not email_notif:
            raise NotFoundError(f"Email notification {email_id} not found")

        email_notif.status = "sent"
        email_notif.sent_at = datetime.now(timezone.utc)
        await self.session.flush()
        return email_notif

    async def mark_email_opened(self, email_id: int) -> EmailNotification:
        """Mark email as opened"""
        email_notif = await self.session.get(EmailNotification, email_id)
        if not email_notif:
            raise NotFoundError(f"Email notification {email_id} not found")

        email_notif.opened_at = datetime.now(timezone.utc)
        await self.session.flush()
        return email_notif

    async def get_pending_emails(self, limit: int = 100) -> List[EmailNotification]:
        """Get pending emails to send"""
        stmt = (
            select(EmailNotification)
            .where(EmailNotification.status == "pending")
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Push notifications
    async def send_push(
        self,
        user_id: int,
        device_token: str,
        title: str,
        message: str,
        platform: str = "mobile",
        notification_id: Optional[int] = None,
    ) -> PushNotification:
        """Create push notification record"""
        push_notif = PushNotification(
            user_id=user_id,
            device_token=device_token,
            title=title,
            message=message,
            platform=platform,
            notification_id=notification_id,
        )
        self.session.add(push_notif)
        await self.session.flush()

        # Log the action
        await self._log_notification(user_id, notification_id, "created", NotificationChannel.PUSH, "pending")

        return push_notif

    async def mark_push_sent(self, push_id: int) -> PushNotification:
        """Mark push as sent"""
        push_notif = await self.session.get(PushNotification, push_id)
        if not push_notif:
            raise NotFoundError(f"Push notification {push_id} not found")

        push_notif.status = "sent"
        push_notif.sent_at = datetime.now(timezone.utc)
        await self.session.flush()
        return push_notif

    async def mark_push_delivered(self, push_id: int) -> PushNotification:
        """Mark push as delivered"""
        push_notif = await self.session.get(PushNotification, push_id)
        if not push_notif:
            raise NotFoundError(f"Push notification {push_id} not found")

        push_notif.delivered_at = datetime.now(timezone.utc)
        await self.session.flush()
        return push_notif

    async def get_pending_pushes(self, limit: int = 100) -> List[PushNotification]:
        """Get pending pushes to send"""
        stmt = (
            select(PushNotification)
            .where(PushNotification.status == "pending")
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Templates
    async def create_template(
        self,
        name: str,
        title_template: str,
        body_template: str,
        subject: Optional[str] = None,
        channel: NotificationChannel = NotificationChannel.EMAIL,
        variables: Optional[List[str]] = None,
    ) -> NotificationTemplate:
        """Create notification template"""
        template = NotificationTemplate(
            name=name,
            title_template=title_template,
            body_template=body_template,
            subject=subject,
            channel=channel,
            variables=variables or [],
        )
        self.session.add(template)
        await self.session.flush()
        return template

    async def get_template(self, name: str) -> Optional[NotificationTemplate]:
        """Get template by name"""
        stmt = select(NotificationTemplate).where(NotificationTemplate.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # Logging
    async def _log_notification(
        self,
        user_id: int,
        notification_id: Optional[int],
        action: str,
        channel: NotificationChannel,
        status: str,
        message: Optional[str] = None,
    ) -> NotificationLog:
        """Log notification action"""
        log = NotificationLog(
            user_id=user_id,
            notification_id=notification_id,
            action=action,
            channel=channel,
            status=status,
            message=message,
        )
        self.session.add(log)
        await self.session.flush()
        return log

    async def get_notification_logs(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> List[NotificationLog]:
        """Get notification logs for user"""
        stmt = (
            select(NotificationLog)
            .where(NotificationLog.user_id == user_id)
            .order_by(NotificationLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Cleanup
    async def delete_old_notifications(self, days: int = 30) -> int:
        """Delete notifications older than specified days"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(Notification).where(Notification.created_at < cutoff_date)
        result = await self.session.execute(stmt)
        notifications = result.scalars().all()

        for notif in notifications:
            await self.session.delete(notif)

        await self.session.flush()
        return len(notifications)
