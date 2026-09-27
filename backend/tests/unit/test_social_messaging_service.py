"""Tests for Social, Messaging & Discovery services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.social_messaging import *
from app.services.social_messaging_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestModerationService:
    @pytest.mark.asyncio
    async def test_create_moderation_rule(self, db):
        service = ModerationService(db)
        rule = await service.create_moderation_rule("spam", "viagra|casino", "reject")

        assert rule.rule_name == "spam"
        assert rule.action == "reject"

    @pytest.mark.asyncio
    async def test_report_content(self, db):
        service = ModerationService(db)
        report = await service.report_content(1, 2, "Offensive content")

        assert report.content_id == 1
        assert report.status == "pending"


class TestSocialService:
    @pytest.mark.asyncio
    async def test_follow_user(self, db):
        service = SocialService(db)
        follow = await service.follow_user(1, 2)

        assert follow.follower_id == 1
        assert follow.following_id == 2

    @pytest.mark.asyncio
    async def test_get_followers(self, db):
        follow = UserFollow(follower_id=1, following_id=2)
        db.add(follow)
        await db.commit()

        service = SocialService(db)
        followers = await service.get_followers(2)

        assert len(followers) == 1

    @pytest.mark.asyncio
    async def test_create_mention(self, db):
        service = SocialService(db)
        mention = await service.create_mention(1, 2, 3)

        assert mention.mentioned_user_id == 2
        assert mention.mentioned_by == 3

    @pytest.mark.asyncio
    async def test_add_hashtag(self, db):
        service = SocialService(db)
        hashtag = await service.add_hashtag(1, "trending")

        assert hashtag.hashtag_id is not None


class TestMessagingService:
    @pytest.mark.asyncio
    async def test_send_message(self, db):
        service = MessagingService(db)
        message = await service.send_message(1, 2, "Hello there")

        assert message.sender_id == 1
        assert message.recipient_id == 2
        assert message.content == "Hello there"

    @pytest.mark.asyncio
    async def test_get_conversation(self, db):
        msg = DirectMessage(sender_id=1, recipient_id=2, content="Hi", message_type="text")
        db.add(msg)
        await db.commit()

        service = MessagingService(db)
        conversation = await service.get_conversation(1, 2)

        assert len(conversation) == 1

    @pytest.mark.asyncio
    async def test_mark_as_read(self, db):
        msg = DirectMessage(sender_id=1, recipient_id=2, content="Test", is_read=False)
        db.add(msg)
        await db.commit()

        service = MessagingService(db)
        await service.mark_as_read(msg.id)

        updated = await db.get(DirectMessage, msg.id)
        assert updated.is_read == True

    @pytest.mark.asyncio
    async def test_get_unread_count(self, db):
        msg1 = DirectMessage(sender_id=1, recipient_id=2, content="Test1", is_read=False)
        msg2 = DirectMessage(sender_id=1, recipient_id=2, content="Test2", is_read=False)
        db.add_all([msg1, msg2])
        await db.commit()

        service = MessagingService(db)
        count = await service.get_unread_count(2)

        assert count == 2


class TestNotificationService:
    @pytest.mark.asyncio
    async def test_create_notification(self, db):
        service = NotificationService(db)
        notif = await service.create_notification(1, "follow", "User followed you")

        assert notif.notification_type == "follow"
        assert notif.is_read == False

    @pytest.mark.asyncio
    async def test_get_notifications(self, db):
        notif = UserNotification(user_id=1, notification_type="like", message="Someone liked your post")
        db.add(notif)
        await db.commit()

        service = NotificationService(db)
        notifications = await service.get_notifications(1)

        assert len(notifications) == 1

    @pytest.mark.asyncio
    async def test_mark_notification_as_read(self, db):
        notif = UserNotification(user_id=1, notification_type="mention", message="You were mentioned")
        db.add(notif)
        await db.commit()

        service = NotificationService(db)
        await service.mark_as_read(notif.id)

        updated = await db.get(UserNotification, notif.id)
        assert updated.is_read == True


class TestDiscoveryService:
    @pytest.mark.asyncio
    async def test_log_search(self, db):
        service = DiscoveryService(db)
        search = await service.log_search("python", 1, "keyword")

        assert search.query == "python"
        assert search.user_id == 1

    @pytest.mark.asyncio
    async def test_create_recommendation(self, db):
        service = DiscoveryService(db)
        rec = await service.create_recommendation(1, 5, 0.95, "Similar to your views")

        assert rec.user_id == 1
        assert rec.recommendation_score == 0.95

    @pytest.mark.asyncio
    async def test_get_trending_topics(self, db):
        topic = TrendingTopic(topic="python", mention_count=1000, trend_score=0.95)
        db.add(topic)
        await db.commit()

        service = DiscoveryService(db)
        trends = await service.get_trending_topics(10)

        assert len(trends) == 1
        assert trends[0].topic == "python"
