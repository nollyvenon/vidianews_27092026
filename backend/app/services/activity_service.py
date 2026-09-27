"""Activity and audit logging service"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from app.models.activity_logs import (
    ActivityLog, AuditLog, ActivityFeed, RetentionPolicy,
    ActionType, EntityType
)
from app.models.user import User
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.logger import logger


class ActivityService:
    """Service for activity logging and audit trails"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Activity logging
    async def log_activity(
        self,
        user_id: int,
        action: ActionType,
        entity_type: EntityType,
        entity_id: int,
        description: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        extra_data: Optional[Dict] = None,
    ) -> ActivityLog:
        """Log a user activity"""
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            status=status,
            error_message=error_message,
            ip_address=ip_address,
            user_agent=user_agent,
            extra_data=extra_data or {},
        )
        self.session.add(activity)
        await self.session.flush()
        return activity

    async def get_user_activities(
        self,
        user_id: int,
        action: Optional[ActionType] = None,
        entity_type: Optional[EntityType] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ActivityLog]:
        """Get user activities with optional filters"""
        stmt = select(ActivityLog).where(ActivityLog.user_id == user_id)

        if action:
            stmt = stmt.where(ActivityLog.action == action)
        if entity_type:
            stmt = stmt.where(ActivityLog.entity_type == entity_type)

        stmt = stmt.order_by(ActivityLog.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_entity_activities(
        self,
        entity_type: EntityType,
        entity_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ActivityLog]:
        """Get all activities for a specific entity"""
        stmt = (
            select(ActivityLog)
            .where(
                and_(
                    ActivityLog.entity_type == entity_type,
                    ActivityLog.entity_id == entity_id,
                )
            )
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_activity_count(
        self,
        user_id: int,
        days: int = 7,
    ) -> int:
        """Get count of user activities in last N days"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(ActivityLog).where(
            and_(
                ActivityLog.user_id == user_id,
                ActivityLog.created_at >= cutoff,
            )
        )
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    # Audit logging
    async def log_change(
        self,
        user_id: int,
        entity_type: EntityType,
        entity_id: int,
        action: ActionType,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        reason: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> AuditLog:
        """Log a change to an entity"""
        # Calculate changed fields
        changed_fields = []
        if old_values and new_values:
            all_keys = set(old_values.keys()) | set(new_values.keys())
            changed_fields = [
                k for k in all_keys
                if old_values.get(k) != new_values.get(k)
            ]

        audit = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            old_values=old_values,
            new_values=new_values,
            changed_fields=changed_fields,
            reason=reason,
            request_id=request_id,
        )
        self.session.add(audit)
        await self.session.flush()
        return audit

    async def get_entity_audit_trail(
        self,
        entity_type: EntityType,
        entity_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AuditLog]:
        """Get complete audit trail for an entity"""
        stmt = (
            select(AuditLog)
            .where(
                and_(
                    AuditLog.entity_type == entity_type,
                    AuditLog.entity_id == entity_id,
                )
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_audit_logs(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AuditLog]:
        """Get all changes made by a user"""
        stmt = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Activity feed
    async def create_feed_item(
        self,
        user_id: int,
        actor_user_id: int,
        action: ActionType,
        entity_type: EntityType,
        entity_id: int,
        title: str,
        description: Optional[str] = None,
        activity_log_id: Optional[int] = None,
    ) -> ActivityFeed:
        """Create a feed item for user"""
        feed = ActivityFeed(
            user_id=user_id,
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            title=title,
            description=description,
            activity_log_id=activity_log_id,
        )
        self.session.add(feed)
        await self.session.flush()
        return feed

    async def get_user_feed(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ActivityFeed]:
        """Get user activity feed"""
        stmt = select(ActivityFeed).where(ActivityFeed.user_id == user_id)

        if unread_only:
            stmt = stmt.where(ActivityFeed.is_read == False)

        stmt = stmt.order_by(ActivityFeed.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_feed_item_read(self, feed_id: int, user_id: int) -> ActivityFeed:
        """Mark feed item as read"""
        feed = await self.session.get(ActivityFeed, feed_id)
        if not feed or feed.user_id != user_id:
            raise NotFoundError(f"Feed item {feed_id} not found")

        feed.is_read = True
        await self.session.flush()
        return feed

    async def mark_all_feed_read(self, user_id: int) -> int:
        """Mark all feed items as read for user"""
        stmt = (
            update(ActivityFeed)
            .where(
                and_(
                    ActivityFeed.user_id == user_id,
                    ActivityFeed.is_read == False,
                )
            )
            .values(is_read=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def archive_feed_item(self, feed_id: int, user_id: int) -> ActivityFeed:
        """Archive a feed item"""
        feed = await self.session.get(ActivityFeed, feed_id)
        if not feed or feed.user_id != user_id:
            raise NotFoundError(f"Feed item {feed_id} not found")

        feed.is_archived = True
        await self.session.flush()
        return feed

    async def get_unread_feed_count(self, user_id: int) -> int:
        """Get count of unread feed items"""
        stmt = select(ActivityFeed).where(
            and_(
                ActivityFeed.user_id == user_id,
                ActivityFeed.is_read == False,
                ActivityFeed.is_archived == False,
            )
        )
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    # Retention policies
    async def create_retention_policy(
        self,
        entity_type: EntityType,
        retention_days: int = 90,
        archive_days: int = 30,
        delete_after_archive: bool = True,
    ) -> RetentionPolicy:
        """Create data retention policy"""
        policy = RetentionPolicy(
            entity_type=entity_type,
            retention_days=retention_days,
            archive_days=archive_days,
            delete_after_archive=delete_after_archive,
        )
        self.session.add(policy)
        await self.session.flush()
        return policy

    async def get_retention_policy(
        self,
        entity_type: EntityType,
    ) -> Optional[RetentionPolicy]:
        """Get retention policy for entity type"""
        stmt = select(RetentionPolicy).where(RetentionPolicy.entity_type == entity_type)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def cleanup_old_logs(self, days: int = 90) -> int:
        """Delete logs older than retention period"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(ActivityLog).where(ActivityLog.created_at < cutoff)
        result = await self.session.execute(stmt)
        logs = result.scalars().all()

        for log in logs:
            await self.session.delete(log)

        await self.session.flush()
        return len(logs)

    async def cleanup_old_audit_logs(self, days: int = 365) -> int:
        """Delete audit logs older than retention period"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(AuditLog).where(AuditLog.created_at < cutoff)
        result = await self.session.execute(stmt)
        logs = result.scalars().all()

        for log in logs:
            await self.session.delete(log)

        await self.session.flush()
        return len(logs)

    async def get_activity_summary(
        self,
        user_id: int,
        days: int = 7,
    ) -> Dict[str, Any]:
        """Get summary of user activities"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = select(ActivityLog).where(
            and_(
                ActivityLog.user_id == user_id,
                ActivityLog.created_at >= cutoff,
            )
        )
        result = await self.session.execute(stmt)
        activities = result.scalars().all()

        # Count by action
        action_counts = {}
        entity_counts = {}

        for activity in activities:
            action_counts[activity.action.value] = action_counts.get(activity.action.value, 0) + 1
            entity_counts[activity.entity_type.value] = entity_counts.get(activity.entity_type.value, 0) + 1

        return {
            "total_activities": len(activities),
            "by_action": action_counts,
            "by_entity": entity_counts,
            "period_days": days,
        }
