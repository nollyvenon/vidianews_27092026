"""Services for Social, Messaging & Discovery: Modules 51-55"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc, func, or_
from typing import Optional, List
from datetime import datetime, timezone
from app.models.social_messaging import *


class ModerationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_moderation_rule(self, rule_name: str, pattern: str, action: str = "flag") -> ContentModerationRule:
        rule = ContentModerationRule(rule_name=rule_name, pattern=pattern, action=action)
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def report_content(self, content_id: int, reported_by: int, reason: str) -> ModerationReport:
        report = ModerationReport(content_id=content_id, reported_by=reported_by, reason=reason)
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def approve_content(self, content_id: int, reviewer_id: int) -> ContentApproval:
        approval = ContentApproval(content_id=content_id, reviewer_id=reviewer_id, status="approved", reviewed_at=datetime.now(timezone.utc))
        self.session.add(approval)
        await self.session.commit()
        await self.session.refresh(approval)
        return approval

    async def get_pending_reports(self) -> List[ModerationReport]:
        stmt = select(ModerationReport).where(ModerationReport.status == "pending").order_by(desc(ModerationReport.reported_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()


class SocialService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def follow_user(self, follower_id: int, following_id: int) -> UserFollow:
        follow = UserFollow(follower_id=follower_id, following_id=following_id)
        self.session.add(follow)
        await self.session.commit()
        await self.session.refresh(follow)
        return follow

    async def unfollow_user(self, follower_id: int, following_id: int) -> None:
        stmt = delete(UserFollow).where(and_(UserFollow.follower_id == follower_id, UserFollow.following_id == following_id))
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_followers(self, user_id: int) -> List[UserFollow]:
        stmt = select(UserFollow).where(UserFollow.following_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_mention(self, content_id: int, mentioned_user_id: int, mentioned_by: int) -> Mention:
        mention = Mention(content_id=content_id, mentioned_user_id=mentioned_user_id, mentioned_by=mentioned_by)
        self.session.add(mention)
        await self.session.commit()
        await self.session.refresh(mention)
        return mention

    async def add_hashtag(self, content_id: int, tag: str) -> ContentHashtag:
        hashtag = await self.session.execute(select(Hashtag).where(Hashtag.tag == tag))
        ht = hashtag.scalar_one_or_none()
        if not ht:
            ht = Hashtag(tag=tag)
            self.session.add(ht)
            await self.session.flush()

        content_tag = ContentHashtag(content_id=content_id, hashtag_id=ht.id)
        self.session.add(content_tag)
        ht.usage_count += 1
        await self.session.commit()
        await self.session.refresh(content_tag)
        return content_tag


class MessagingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_message(self, sender_id: int, recipient_id: int, content: str, msg_type: str = "text") -> DirectMessage:
        message = DirectMessage(sender_id=sender_id, recipient_id=recipient_id, content=content, message_type=msg_type)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_conversation(self, user1_id: int, user2_id: int) -> List[DirectMessage]:
        stmt = select(DirectMessage).where(
            or_(
                and_(DirectMessage.sender_id == user1_id, DirectMessage.recipient_id == user2_id),
                and_(DirectMessage.sender_id == user2_id, DirectMessage.recipient_id == user1_id)
            )
        ).order_by(DirectMessage.sent_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, message_id: int) -> None:
        stmt = update(DirectMessage).where(DirectMessage.id == message_id).values(
            is_read=True, read_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_unread_count(self, user_id: int) -> int:
        count = await self.session.execute(
            select(func.count(DirectMessage.id)).where(
                and_(DirectMessage.recipient_id == user_id, DirectMessage.is_read == False)
            )
        )
        return count.scalar() or 0


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(self, user_id: int, notification_type: str, message: str, actor_id: int = None) -> UserNotification:
        notif = UserNotification(user_id=user_id, notification_type=notification_type, message=message, actor_id=actor_id)
        self.session.add(notif)
        await self.session.commit()
        await self.session.refresh(notif)
        return notif

    async def get_notifications(self, user_id: int, unread_only: bool = False) -> List[UserNotification]:
        stmt = select(UserNotification).where(UserNotification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(UserNotification.is_read == False)
        stmt = stmt.order_by(desc(UserNotification.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int) -> None:
        stmt = update(UserNotification).where(UserNotification.id == notification_id).values(
            is_read=True, read_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_notification_preferences(self, user_id: int) -> Optional[NotificationPreference]:
        stmt = select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class DiscoveryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_search(self, query: str, user_id: int = None, search_type: str = "keyword") -> SearchQuery:
        search = SearchQuery(query=query, user_id=user_id, search_type=search_type)
        self.session.add(search)
        await self.session.commit()
        await self.session.refresh(search)
        return search

    async def create_recommendation(self, user_id: int, content_id: int, score: float, reason: str = None) -> DiscoveryRecommendation:
        rec = DiscoveryRecommendation(user_id=user_id, content_id=content_id, recommendation_score=score, reason=reason)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def get_recommendations(self, user_id: int, limit: int = 10) -> List[DiscoveryRecommendation]:
        stmt = select(DiscoveryRecommendation).where(
            DiscoveryRecommendation.user_id == user_id
        ).order_by(desc(DiscoveryRecommendation.recommendation_score)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_trending_topics(self, limit: int = 10) -> List[TrendingTopic]:
        stmt = select(TrendingTopic).order_by(desc(TrendingTopic.trend_score)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
