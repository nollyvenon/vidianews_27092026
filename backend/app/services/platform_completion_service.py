"""Social, search, push notification, admin and system services (async).

Timestamps are naive UTC to match the naive ``DateTime`` columns in ``app.models.platform_completion``.
Each static method takes an ``AsyncSession`` as its first argument.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from sqlalchemy import and_, delete, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_completion import (
    AdminActionLog, AdminActionType, AdminUser, ContentComment, InteractionType, PlatformStatistics,
    PushNotificationConfig, PushNotificationLog, PushNotificationType, SavedSearch, SearchIndex,
    SearchIndexType, SystemNotification, UserFollow, UserInteraction, UserMessage,
)


def _utcnow() -> datetime:
    """Naive UTC, matching the naive DateTime columns"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class SocialService:
    @staticmethod
    async def create_interaction(
        db: AsyncSession,
        user_id: int,
        content_id: int,
        interaction_type: InteractionType,
        metadata: Optional[Dict] = None
    ) -> UserInteraction:
        existing = (await db.execute(select(UserInteraction).where(and_(
            UserInteraction.user_id == user_id,
            UserInteraction.content_id == content_id,
            UserInteraction.interaction_type == interaction_type
        )))).scalars().first()

        if existing:
            existing.updated_at = _utcnow()
            await db.commit()
            await db.refresh(existing)
            return existing

        interaction = UserInteraction(
            user_id=user_id,
            content_id=content_id,
            interaction_type=interaction_type,
            extra_metadata=metadata or {}
        )
        db.add(interaction)
        await db.commit()
        await db.refresh(interaction)
        return interaction

    @staticmethod
    async def remove_interaction(
        db: AsyncSession,
        user_id: int,
        content_id: int,
        interaction_type: InteractionType
    ) -> bool:
        result = await db.execute(delete(UserInteraction).where(and_(
            UserInteraction.user_id == user_id,
            UserInteraction.content_id == content_id,
            UserInteraction.interaction_type == interaction_type
        )))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_user_interactions(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserInteraction]:
        result = await db.execute(
            select(UserInteraction).where(UserInteraction.user_id == user_id)
            .order_by(desc(UserInteraction.created_at)).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_content_interactions(
        db: AsyncSession,
        content_id: int,
        interaction_type: Optional[InteractionType] = None
    ) -> List[UserInteraction]:
        stmt = select(UserInteraction).where(UserInteraction.content_id == content_id)
        if interaction_type:
            stmt = stmt.where(UserInteraction.interaction_type == interaction_type)
        return list((await db.execute(stmt)).scalars().all())

    @staticmethod
    async def follow_user(
        db: AsyncSession,
        follower_id: int,
        following_id: int
    ) -> UserFollow:
        if follower_id == following_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")

        existing = (await db.execute(select(UserFollow).where(and_(
            UserFollow.follower_id == follower_id,
            UserFollow.following_id == following_id
        )))).scalars().first()

        if existing:
            return existing

        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        db.add(follow)
        await db.commit()
        await db.refresh(follow)
        return follow

    @staticmethod
    async def unfollow_user(
        db: AsyncSession,
        follower_id: int,
        following_id: int
    ) -> bool:
        result = await db.execute(delete(UserFollow).where(and_(
            UserFollow.follower_id == follower_id,
            UserFollow.following_id == following_id
        )))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_followers(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserFollow]:
        result = await db.execute(
            select(UserFollow).where(UserFollow.following_id == user_id).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_following(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserFollow]:
        result = await db.execute(
            select(UserFollow).where(UserFollow.follower_id == user_id).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def create_comment(
        db: AsyncSession,
        user_id: int,
        content_id: int,
        text: str,
        parent_comment_id: Optional[int] = None
    ) -> ContentComment:
        comment = ContentComment(
            user_id=user_id,
            content_id=content_id,
            text=text,
            parent_comment_id=parent_comment_id
        )
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_comments(
        db: AsyncSession,
        content_id: int,
        parent_comment_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ContentComment]:
        stmt = select(ContentComment).where(ContentComment.content_id == content_id)
        if parent_comment_id:
            stmt = stmt.where(ContentComment.parent_comment_id == parent_comment_id)
        result = await db.execute(stmt.order_by(desc(ContentComment.created_at)).offset(offset).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def delete_comment(
        db: AsyncSession,
        comment_id: int,
        user_id: int
    ) -> bool:
        comment = await db.get(ContentComment, comment_id)

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Cannot delete others' comments")

        await db.delete(comment)
        await db.commit()
        return True

    @staticmethod
    async def send_message(
        db: AsyncSession,
        sender_id: int,
        recipient_id: int,
        text: str
    ) -> UserMessage:
        if sender_id == recipient_id:
            raise HTTPException(status_code=400, detail="Cannot message yourself")

        message = UserMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            body=text
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def get_conversation(
        db: AsyncSession,
        user_id: int,
        other_user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserMessage]:
        result = await db.execute(select(UserMessage).where(or_(
            and_(
                UserMessage.sender_id == user_id,
                UserMessage.recipient_id == other_user_id
            ),
            and_(
                UserMessage.sender_id == other_user_id,
                UserMessage.recipient_id == user_id
            )
        )).order_by(desc(UserMessage.created_at)).offset(offset).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def mark_message_read(
        db: AsyncSession,
        message_id: int,
        user_id: int
    ) -> bool:
        message = await db.get(UserMessage, message_id)

        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        if message.recipient_id != user_id:
            raise HTTPException(status_code=403, detail="Cannot mark as read")

        message.read = True
        message.read_at = _utcnow()
        await db.commit()
        return True


class SearchService:
    @staticmethod
    async def create_search_index(
        db: AsyncSession,
        content_id: int,
        index_type: SearchIndexType,
        title: str,
        content: str,
        metadata: Optional[Dict] = None,
        embeddings: Optional[List[float]] = None
    ) -> SearchIndex:
        search_index = SearchIndex(
            content_id=content_id,
            index_type=index_type,
            title=title,
            description=content,
            extra_metadata=metadata or {},
            embedding_vector=embeddings or []
        )
        db.add(search_index)
        await db.commit()
        await db.refresh(search_index)
        return search_index

    @staticmethod
    async def search_content(
        db: AsyncSession,
        query: str,
        index_type: Optional[SearchIndexType] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[SearchIndex]:
        stmt = select(SearchIndex).where(or_(
            SearchIndex.title.ilike(f"%{query}%"),
            SearchIndex.description.ilike(f"%{query}%")
        ))
        if index_type:
            stmt = stmt.where(SearchIndex.index_type == index_type)

        return list((await db.execute(stmt.offset(offset).limit(limit))).scalars().all())

    @staticmethod
    async def save_search(
        db: AsyncSession,
        user_id: int,
        query: str,
        filters: Optional[Dict] = None,
        result_count: int = 0
    ) -> SavedSearch:
        saved_search = SavedSearch(
            user_id=user_id,
            name=query[:255],
            query=query,
            filters=filters or {},
            result_count=result_count
        )
        db.add(saved_search)
        await db.commit()
        await db.refresh(saved_search)
        return saved_search

    @staticmethod
    async def get_saved_searches(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[SavedSearch]:
        result = await db.execute(
            select(SavedSearch).where(SavedSearch.user_id == user_id)
            .order_by(desc(SavedSearch.created_at)).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def delete_saved_search(
        db: AsyncSession,
        search_id: int,
        user_id: int
    ) -> bool:
        result = await db.execute(delete(SavedSearch).where(and_(
            SavedSearch.id == search_id,
            SavedSearch.user_id == user_id
        )))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def update_search_index(
        db: AsyncSession,
        search_index_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> SearchIndex:
        search_index = await db.get(SearchIndex, search_index_id)

        if not search_index:
            raise HTTPException(status_code=404, detail="Search index not found")

        if title:
            search_index.title = title
        if content:
            search_index.description = content
        if metadata:
            search_index.extra_metadata = metadata

        search_index.updated_at = _utcnow()
        await db.commit()
        await db.refresh(search_index)
        return search_index


class PushNotificationService:
    @staticmethod
    async def register_device(
        db: AsyncSession,
        user_id: int,
        device_token: str,
        platform: str,
        device_name: Optional[str] = None
    ) -> PushNotificationConfig:
        existing = (await db.execute(select(PushNotificationConfig).where(and_(
            PushNotificationConfig.user_id == user_id,
            PushNotificationConfig.device_token == device_token
        )))).scalars().first()

        if existing:
            existing.last_sync = _utcnow()
            await db.commit()
            await db.refresh(existing)
            return existing

        config = PushNotificationConfig(
            user_id=user_id,
            device_token=device_token,
            platform=platform,
            device_name=device_name,
            last_sync=_utcnow(),
        )
        db.add(config)
        await db.commit()
        await db.refresh(config)
        return config

    @staticmethod
    async def unregister_device(
        db: AsyncSession,
        device_id: int,
        user_id: int
    ) -> bool:
        result = await db.execute(delete(PushNotificationConfig).where(and_(
            PushNotificationConfig.id == device_id,
            PushNotificationConfig.user_id == user_id
        )))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_user_devices(
        db: AsyncSession,
        user_id: int
    ) -> List[PushNotificationConfig]:
        result = await db.execute(select(PushNotificationConfig).where(PushNotificationConfig.user_id == user_id))
        return list(result.scalars().all())

    @staticmethod
    async def log_notification(
        db: AsyncSession,
        user_id: int,
        notification_type: PushNotificationType,
        title: str,
        body: str,
        device_id: Optional[int] = None,
        status: str = "pending"
    ) -> PushNotificationLog:
        log = PushNotificationLog(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            body=body,
            device_id=device_id,
            status=status
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    @staticmethod
    async def update_notification_status(
        db: AsyncSession,
        log_id: int,
        status: str,
        delivered_at: Optional[datetime] = None,
        opened_at: Optional[datetime] = None
    ) -> PushNotificationLog:
        log = await db.get(PushNotificationLog, log_id)

        if not log:
            raise HTTPException(status_code=404, detail="Notification log not found")

        log.status = status
        if delivered_at:
            log.delivered_at = delivered_at
        if opened_at:
            log.opened_at = opened_at

        await db.commit()
        await db.refresh(log)
        return log

    @staticmethod
    async def get_notification_logs(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[PushNotificationLog]:
        result = await db.execute(
            select(PushNotificationLog).where(PushNotificationLog.user_id == user_id)
            .order_by(desc(PushNotificationLog.created_at)).offset(offset).limit(limit)
        )
        return list(result.scalars().all())


class AdminService:
    @staticmethod
    async def create_admin_user(
        db: AsyncSession,
        user_id: int,
        role: str,
        permissions: Optional[List[str]] = None
    ) -> AdminUser:
        existing = await AdminService.get_admin_user(db, user_id)

        if existing:
            raise HTTPException(status_code=400, detail="User is already an admin")

        admin = AdminUser(
            user_id=user_id,
            role=role,
            permissions=permissions or []
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return admin

    @staticmethod
    async def remove_admin_user(
        db: AsyncSession,
        user_id: int
    ) -> bool:
        result = await db.execute(delete(AdminUser).where(AdminUser.user_id == user_id))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_admin_user(
        db: AsyncSession,
        user_id: int
    ) -> Optional[AdminUser]:
        return (await db.execute(select(AdminUser).where(AdminUser.user_id == user_id))).scalars().first()

    @staticmethod
    async def log_admin_action(
        db: AsyncSession,
        admin_user_id: int,
        action_type: AdminActionType,
        resource_type: str,
        resource_id: int,
        details: Optional[Dict] = None,
        status: str = "completed"
    ) -> AdminActionLog:
        log = AdminActionLog(
            admin_id=admin_user_id,
            action_type=action_type,
            target_type=resource_type,
            target_id=resource_id,
            details=details or {},
            status=status
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    @staticmethod
    async def get_admin_logs(
        db: AsyncSession,
        admin_user_id: Optional[int] = None,
        action_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AdminActionLog]:
        stmt = select(AdminActionLog)
        if admin_user_id:
            stmt = stmt.where(AdminActionLog.admin_id == admin_user_id)
        if action_type:
            stmt = stmt.where(AdminActionLog.action_type == action_type)

        result = await db.execute(stmt.order_by(desc(AdminActionLog.created_at)).offset(offset).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def update_admin_permissions(
        db: AsyncSession,
        user_id: int,
        permissions: List[str]
    ) -> AdminUser:
        admin = await AdminService.get_admin_user(db, user_id)

        if not admin:
            raise HTTPException(status_code=404, detail="Admin user not found")

        admin.permissions = permissions
        await db.commit()
        await db.refresh(admin)
        return admin


class SystemService:
    @staticmethod
    async def create_system_notification(
        db: AsyncSession,
        title: str,
        message: str,
        notification_type: str,
        target_users: Optional[List[int]] = None,
        metadata: Optional[Dict] = None
    ) -> SystemNotification:
        notification = SystemNotification(
            title=title,
            message=message,
            notification_type=notification_type,
            target_users=target_users or [],
            extra_metadata=metadata or {}
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    @staticmethod
    async def get_system_notifications(
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0
    ) -> List[SystemNotification]:
        result = await db.execute(
            select(SystemNotification).order_by(desc(SystemNotification.created_at)).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def record_platform_statistic(
        db: AsyncSession,
        metric_name: str,
        metric_value: float,
        metric_type: str = "count",
        breakdown: Optional[Dict] = None
    ) -> PlatformStatistics:
        stat = PlatformStatistics(
            metric_name=metric_name,
            metric_value=metric_value,
            metric_type=metric_type,
            breakdown=breakdown or {}
        )
        db.add(stat)
        await db.commit()
        await db.refresh(stat)
        return stat

    @staticmethod
    async def get_platform_statistics(
        db: AsyncSession,
        metric_name: Optional[str] = None,
        days: int = 7,
        limit: int = 100
    ) -> List[PlatformStatistics]:
        cutoff_date = _utcnow() - timedelta(days=days)
        stmt = select(PlatformStatistics).where(PlatformStatistics.created_at >= cutoff_date)
        if metric_name:
            stmt = stmt.where(PlatformStatistics.metric_name == metric_name)

        result = await db.execute(stmt.order_by(desc(PlatformStatistics.created_at)).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def get_aggregated_statistics(
        db: AsyncSession,
        metric_name: str,
        days: int = 30
    ) -> Dict[str, Any]:
        cutoff_date = _utcnow() - timedelta(days=days)
        stats = (await db.execute(select(PlatformStatistics).where(and_(
            PlatformStatistics.metric_name == metric_name,
            PlatformStatistics.created_at >= cutoff_date
        )))).scalars().all()

        if not stats:
            return {
                "metric_name": metric_name,
                "count": 0,
                "sum": 0,
                "average": 0,
                "min": 0,
                "max": 0
            }

        values = [s.metric_value for s in stats]
        return {
            "metric_name": metric_name,
            "count": len(values),
            "sum": sum(values),
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "period_days": days
        }

    @staticmethod
    async def get_dashboard_summary(
        db: AsyncSession
    ) -> Dict[str, Any]:
        async def count(column) -> int:
            return (await db.execute(select(func.count(column)))).scalar() or 0

        return {
            "total_interactions": await count(UserInteraction.id),
            "total_follows": await count(UserFollow.id),
            "total_comments": await count(ContentComment.id),
            "total_messages": await count(UserMessage.id),
            "total_notifications": await count(PushNotificationLog.id),
            "timestamp": _utcnow().isoformat()
        }
