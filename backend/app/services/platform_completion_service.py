from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
from fastapi import HTTPException
from app.models.platform_completion import (
    UserInteraction, UserFollow, ContentComment, UserMessage,
    SearchIndex, SavedSearch, PushNotificationConfig, PushNotificationLog,
    AdminUser, AdminActionLog, SystemNotification, PlatformStatistics,
    InteractionType, ModerationStatus, PushNotificationType, AdminActionType
)


class SocialService:
    @staticmethod
    async def create_interaction(
        db: Session,
        user_id: int,
        content_id: int,
        interaction_type: str,
        metadata: Optional[Dict] = None
    ) -> UserInteraction:
        existing = db.query(UserInteraction).filter(
            and_(
                UserInteraction.user_id == user_id,
                UserInteraction.content_id == content_id,
                UserInteraction.interaction_type == interaction_type
            )
        ).first()

        if existing:
            existing.updated_at = datetime.utcnow()
            db.commit()
            return existing

        interaction = UserInteraction(
            user_id=user_id,
            content_id=content_id,
            interaction_type=interaction_type,
            metadata=metadata or {}
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction

    @staticmethod
    async def remove_interaction(
        db: Session,
        user_id: int,
        content_id: int,
        interaction_type: str
    ) -> bool:
        result = db.query(UserInteraction).filter(
            and_(
                UserInteraction.user_id == user_id,
                UserInteraction.content_id == content_id,
                UserInteraction.interaction_type == interaction_type
            )
        ).delete()
        db.commit()
        return result > 0

    @staticmethod
    async def get_user_interactions(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserInteraction]:
        return db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).order_by(desc(UserInteraction.created_at)).offset(offset).limit(limit).all()

    @staticmethod
    async def get_content_interactions(
        db: Session,
        content_id: int,
        interaction_type: Optional[str] = None
    ) -> List[UserInteraction]:
        query = db.query(UserInteraction).filter(
            UserInteraction.content_id == content_id
        )
        if interaction_type:
            query = query.filter(UserInteraction.interaction_type == interaction_type)
        return query.all()

    @staticmethod
    async def follow_user(
        db: Session,
        follower_id: int,
        following_id: int
    ) -> UserFollow:
        if follower_id == following_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")

        existing = db.query(UserFollow).filter(
            and_(
                UserFollow.follower_id == follower_id,
                UserFollow.following_id == following_id
            )
        ).first()

        if existing:
            return existing

        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        db.add(follow)
        db.commit()
        db.refresh(follow)
        return follow

    @staticmethod
    async def unfollow_user(
        db: Session,
        follower_id: int,
        following_id: int
    ) -> bool:
        result = db.query(UserFollow).filter(
            and_(
                UserFollow.follower_id == follower_id,
                UserFollow.following_id == following_id
            )
        ).delete()
        db.commit()
        return result > 0

    @staticmethod
    async def get_followers(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserFollow]:
        return db.query(UserFollow).filter(
            UserFollow.following_id == user_id
        ).offset(offset).limit(limit).all()

    @staticmethod
    async def get_following(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserFollow]:
        return db.query(UserFollow).filter(
            UserFollow.follower_id == user_id
        ).offset(offset).limit(limit).all()

    @staticmethod
    async def create_comment(
        db: Session,
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
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    async def get_comments(
        db: Session,
        content_id: int,
        parent_comment_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ContentComment]:
        query = db.query(ContentComment).filter(
            ContentComment.content_id == content_id
        )
        if parent_comment_id:
            query = query.filter(ContentComment.parent_comment_id == parent_comment_id)
        return query.order_by(desc(ContentComment.created_at)).offset(offset).limit(limit).all()

    @staticmethod
    async def delete_comment(
        db: Session,
        comment_id: int,
        user_id: int
    ) -> bool:
        comment = db.query(ContentComment).filter(
            ContentComment.id == comment_id
        ).first()

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Cannot delete others' comments")

        db.delete(comment)
        db.commit()
        return True

    @staticmethod
    async def send_message(
        db: Session,
        sender_id: int,
        recipient_id: int,
        text: str
    ) -> UserMessage:
        if sender_id == recipient_id:
            raise HTTPException(status_code=400, detail="Cannot message yourself")

        message = UserMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    async def get_conversation(
        db: Session,
        user_id: int,
        other_user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserMessage]:
        return db.query(UserMessage).filter(
            or_(
                and_(
                    UserMessage.sender_id == user_id,
                    UserMessage.recipient_id == other_user_id
                ),
                and_(
                    UserMessage.sender_id == other_user_id,
                    UserMessage.recipient_id == user_id
                )
            )
        ).order_by(desc(UserMessage.created_at)).offset(offset).limit(limit).all()

    @staticmethod
    async def mark_message_read(
        db: Session,
        message_id: int,
        user_id: int
    ) -> bool:
        message = db.query(UserMessage).filter(
            UserMessage.id == message_id
        ).first()

        if not message or message.recipient_id != user_id:
            raise HTTPException(status_code=403, detail="Cannot mark as read")

        message.read = True
        message.read_at = datetime.utcnow()
        db.commit()
        return True


class SearchService:
    @staticmethod
    async def create_search_index(
        db: Session,
        content_id: int,
        index_type: str,
        title: str,
        content: str,
        metadata: Optional[Dict] = None,
        embeddings: Optional[List[float]] = None
    ) -> SearchIndex:
        search_index = SearchIndex(
            content_id=content_id,
            index_type=index_type,
            title=title,
            content=content,
            metadata=metadata or {},
            embeddings=embeddings or []
        )
        db.add(search_index)
        db.commit()
        db.refresh(search_index)
        return search_index

    @staticmethod
    async def search_content(
        db: Session,
        query: str,
        index_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[SearchIndex]:
        search_query = db.query(SearchIndex).filter(
            or_(
                SearchIndex.title.ilike(f"%{query}%"),
                SearchIndex.content.ilike(f"%{query}%")
            )
        )
        if index_type:
            search_query = search_query.filter(SearchIndex.index_type == index_type)

        return search_query.offset(offset).limit(limit).all()

    @staticmethod
    async def save_search(
        db: Session,
        user_id: int,
        query: str,
        filters: Optional[Dict] = None,
        result_count: int = 0
    ) -> SavedSearch:
        saved_search = SavedSearch(
            user_id=user_id,
            query=query,
            filters=filters or {},
            result_count=result_count
        )
        db.add(saved_search)
        db.commit()
        db.refresh(saved_search)
        return saved_search

    @staticmethod
    async def get_saved_searches(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[SavedSearch]:
        return db.query(SavedSearch).filter(
            SavedSearch.user_id == user_id
        ).order_by(desc(SavedSearch.created_at)).offset(offset).limit(limit).all()

    @staticmethod
    async def delete_saved_search(
        db: Session,
        search_id: int,
        user_id: int
    ) -> bool:
        result = db.query(SavedSearch).filter(
            and_(
                SavedSearch.id == search_id,
                SavedSearch.user_id == user_id
            )
        ).delete()
        db.commit()
        return result > 0

    @staticmethod
    async def update_search_index(
        db: Session,
        search_index_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> SearchIndex:
        search_index = db.query(SearchIndex).filter(
            SearchIndex.id == search_index_id
        ).first()

        if not search_index:
            raise HTTPException(status_code=404, detail="Search index not found")

        if title:
            search_index.title = title
        if content:
            search_index.content = content
        if metadata:
            search_index.metadata = metadata

        search_index.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(search_index)
        return search_index


class PushNotificationService:
    @staticmethod
    async def register_device(
        db: Session,
        user_id: int,
        device_token: str,
        platform: str,
        device_name: Optional[str] = None
    ) -> PushNotificationConfig:
        existing = db.query(PushNotificationConfig).filter(
            and_(
                PushNotificationConfig.user_id == user_id,
                PushNotificationConfig.device_token == device_token
            )
        ).first()

        if existing:
            existing.last_active = datetime.utcnow()
            db.commit()
            return existing

        config = PushNotificationConfig(
            user_id=user_id,
            device_token=device_token,
            platform=platform,
            device_name=device_name
        )
        db.add(config)
        db.commit()
        db.refresh(config)
        return config

    @staticmethod
    async def unregister_device(
        db: Session,
        device_id: int,
        user_id: int
    ) -> bool:
        result = db.query(PushNotificationConfig).filter(
            and_(
                PushNotificationConfig.id == device_id,
                PushNotificationConfig.user_id == user_id
            )
        ).delete()
        db.commit()
        return result > 0

    @staticmethod
    async def get_user_devices(
        db: Session,
        user_id: int
    ) -> List[PushNotificationConfig]:
        return db.query(PushNotificationConfig).filter(
            PushNotificationConfig.user_id == user_id
        ).all()

    @staticmethod
    async def log_notification(
        db: Session,
        user_id: int,
        notification_type: str,
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
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    async def update_notification_status(
        db: Session,
        log_id: int,
        status: str,
        delivered_at: Optional[datetime] = None,
        opened_at: Optional[datetime] = None
    ) -> PushNotificationLog:
        log = db.query(PushNotificationLog).filter(
            PushNotificationLog.id == log_id
        ).first()

        if not log:
            raise HTTPException(status_code=404, detail="Notification log not found")

        log.status = status
        if delivered_at:
            log.delivered_at = delivered_at
        if opened_at:
            log.opened_at = opened_at

        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    async def get_notification_logs(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[PushNotificationLog]:
        return db.query(PushNotificationLog).filter(
            PushNotificationLog.user_id == user_id
        ).order_by(desc(PushNotificationLog.created_at)).offset(offset).limit(limit).all()


class AdminService:
    @staticmethod
    async def create_admin_user(
        db: Session,
        user_id: int,
        role: str,
        permissions: Optional[List[str]] = None
    ) -> AdminUser:
        existing = db.query(AdminUser).filter(
            AdminUser.user_id == user_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="User is already an admin")

        admin = AdminUser(
            user_id=user_id,
            role=role,
            permissions=permissions or []
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    @staticmethod
    async def remove_admin_user(
        db: Session,
        user_id: int
    ) -> bool:
        result = db.query(AdminUser).filter(
            AdminUser.user_id == user_id
        ).delete()
        db.commit()
        return result > 0

    @staticmethod
    async def get_admin_user(
        db: Session,
        user_id: int
    ) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(
            AdminUser.user_id == user_id
        ).first()

    @staticmethod
    async def log_admin_action(
        db: Session,
        admin_user_id: int,
        action_type: str,
        resource_type: str,
        resource_id: int,
        details: Optional[Dict] = None,
        status: str = "completed"
    ) -> AdminActionLog:
        log = AdminActionLog(
            admin_user_id=admin_user_id,
            action_type=action_type,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            status=status
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    async def get_admin_logs(
        db: Session,
        admin_user_id: Optional[int] = None,
        action_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AdminActionLog]:
        query = db.query(AdminActionLog)
        if admin_user_id:
            query = query.filter(AdminActionLog.admin_user_id == admin_user_id)
        if action_type:
            query = query.filter(AdminActionLog.action_type == action_type)

        return query.order_by(desc(AdminActionLog.created_at)).offset(offset).limit(limit).all()

    @staticmethod
    async def update_admin_permissions(
        db: Session,
        user_id: int,
        permissions: List[str]
    ) -> AdminUser:
        admin = db.query(AdminUser).filter(
            AdminUser.user_id == user_id
        ).first()

        if not admin:
            raise HTTPException(status_code=404, detail="Admin user not found")

        admin.permissions = permissions
        admin.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(admin)
        return admin


class SystemService:
    @staticmethod
    async def create_system_notification(
        db: Session,
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
            metadata=metadata or {}
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    async def get_system_notifications(
        db: Session,
        limit: int = 50,
        offset: int = 0
    ) -> List[SystemNotification]:
        return db.query(SystemNotification).order_by(
            desc(SystemNotification.created_at)
        ).offset(offset).limit(limit).all()

    @staticmethod
    async def record_platform_statistic(
        db: Session,
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
        db.commit()
        db.refresh(stat)
        return stat

    @staticmethod
    async def get_platform_statistics(
        db: Session,
        metric_name: Optional[str] = None,
        days: int = 7,
        limit: int = 100
    ) -> List[PlatformStatistics]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(PlatformStatistics).filter(
            PlatformStatistics.created_at >= cutoff_date
        )
        if metric_name:
            query = query.filter(PlatformStatistics.metric_name == metric_name)

        return query.order_by(desc(PlatformStatistics.created_at)).limit(limit).all()

    @staticmethod
    async def get_aggregated_statistics(
        db: Session,
        metric_name: str,
        days: int = 30
    ) -> Dict[str, Any]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        stats = db.query(PlatformStatistics).filter(
            and_(
                PlatformStatistics.metric_name == metric_name,
                PlatformStatistics.created_at >= cutoff_date
            )
        ).all()

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
        db: Session
    ) -> Dict[str, Any]:
        total_interactions = db.query(func.count(UserInteraction.id)).scalar() or 0
        total_follows = db.query(func.count(UserFollow.id)).scalar() or 0
        total_comments = db.query(func.count(ContentComment.id)).scalar() or 0
        total_messages = db.query(func.count(UserMessage.id)).scalar() or 0
        total_notifications = db.query(func.count(PushNotificationLog.id)).scalar() or 0

        return {
            "total_interactions": total_interactions,
            "total_follows": total_follows,
            "total_comments": total_comments,
            "total_messages": total_messages,
            "total_notifications": total_notifications,
            "timestamp": datetime.utcnow().isoformat()
        }
