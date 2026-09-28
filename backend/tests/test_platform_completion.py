import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base
from app.main import app
from app.models.platform_completion import (
    UserInteraction, UserFollow, ContentComment, UserMessage,
    SearchIndex, SavedSearch, PushNotificationConfig, PushNotificationLog,
    AdminUser, AdminActionLog, SystemNotification, PlatformStatistics
)
from app.services.platform_completion_service import (
    SocialService, SearchService, PushNotificationService,
    AdminService, SystemService
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        return db_session

    from app.database import get_db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


class TestSocialService:
    @pytest.mark.asyncio
    async def test_create_interaction(self, db_session):
        interaction = await SocialService.create_interaction(
            db_session, 1, 1, "like", {"sentiment": "positive"}
        )
        assert interaction.user_id == 1
        assert interaction.content_id == 1
        assert interaction.interaction_type == "like"

    @pytest.mark.asyncio
    async def test_create_duplicate_interaction(self, db_session):
        await SocialService.create_interaction(db_session, 1, 1, "like")
        interaction = await SocialService.create_interaction(
            db_session, 1, 1, "like"
        )
        assert interaction.user_id == 1

    @pytest.mark.asyncio
    async def test_remove_interaction(self, db_session):
        await SocialService.create_interaction(db_session, 1, 1, "like")
        success = await SocialService.remove_interaction(db_session, 1, 1, "like")
        assert success is True

    @pytest.mark.asyncio
    async def test_get_user_interactions(self, db_session):
        await SocialService.create_interaction(db_session, 1, 1, "like")
        await SocialService.create_interaction(db_session, 1, 2, "comment")
        interactions = await SocialService.get_user_interactions(db_session, 1)
        assert len(interactions) == 2

    @pytest.mark.asyncio
    async def test_get_content_interactions(self, db_session):
        await SocialService.create_interaction(db_session, 1, 1, "like")
        await SocialService.create_interaction(db_session, 2, 1, "like")
        interactions = await SocialService.get_content_interactions(db_session, 1)
        assert len(interactions) == 2

    @pytest.mark.asyncio
    async def test_follow_user(self, db_session):
        follow = await SocialService.follow_user(db_session, 1, 2)
        assert follow.follower_id == 1
        assert follow.following_id == 2

    @pytest.mark.asyncio
    async def test_follow_self_error(self, db_session):
        with pytest.raises(Exception):
            await SocialService.follow_user(db_session, 1, 1)

    @pytest.mark.asyncio
    async def test_unfollow_user(self, db_session):
        await SocialService.follow_user(db_session, 1, 2)
        success = await SocialService.unfollow_user(db_session, 1, 2)
        assert success is True

    @pytest.mark.asyncio
    async def test_get_followers(self, db_session):
        await SocialService.follow_user(db_session, 1, 2)
        await SocialService.follow_user(db_session, 3, 2)
        followers = await SocialService.get_followers(db_session, 2)
        assert len(followers) == 2

    @pytest.mark.asyncio
    async def test_get_following(self, db_session):
        await SocialService.follow_user(db_session, 1, 2)
        await SocialService.follow_user(db_session, 1, 3)
        following = await SocialService.get_following(db_session, 1)
        assert len(following) == 2

    @pytest.mark.asyncio
    async def test_create_comment(self, db_session):
        comment = await SocialService.create_comment(
            db_session, 1, 1, "Great content!"
        )
        assert comment.user_id == 1
        assert comment.content_id == 1
        assert comment.text == "Great content!"

    @pytest.mark.asyncio
    async def test_create_nested_comment(self, db_session):
        parent = await SocialService.create_comment(db_session, 1, 1, "Parent")
        child = await SocialService.create_comment(
            db_session, 2, 1, "Reply", parent.id
        )
        assert child.parent_comment_id == parent.id

    @pytest.mark.asyncio
    async def test_get_comments(self, db_session):
        await SocialService.create_comment(db_session, 1, 1, "Comment 1")
        await SocialService.create_comment(db_session, 2, 1, "Comment 2")
        comments = await SocialService.get_comments(db_session, 1)
        assert len(comments) == 2

    @pytest.mark.asyncio
    async def test_delete_comment(self, db_session):
        comment = await SocialService.create_comment(db_session, 1, 1, "Test")
        success = await SocialService.delete_comment(db_session, comment.id, 1)
        assert success is True

    @pytest.mark.asyncio
    async def test_send_message(self, db_session):
        message = await SocialService.send_message(
            db_session, 1, 2, "Hello!"
        )
        assert message.sender_id == 1
        assert message.recipient_id == 2

    @pytest.mark.asyncio
    async def test_send_self_message_error(self, db_session):
        with pytest.raises(Exception):
            await SocialService.send_message(db_session, 1, 1, "Self")

    @pytest.mark.asyncio
    async def test_get_conversation(self, db_session):
        await SocialService.send_message(db_session, 1, 2, "Hi")
        await SocialService.send_message(db_session, 2, 1, "Hello")
        messages = await SocialService.get_conversation(db_session, 1, 2)
        assert len(messages) == 2

    @pytest.mark.asyncio
    async def test_mark_message_read(self, db_session):
        message = await SocialService.send_message(db_session, 1, 2, "Hi")
        success = await SocialService.mark_message_read(db_session, message.id, 2)
        assert success is True


class TestSearchService:
    @pytest.mark.asyncio
    async def test_create_search_index(self, db_session):
        index = await SearchService.create_search_index(
            db_session, 1, "content", "Title", "Body content"
        )
        assert index.content_id == 1
        assert index.index_type == "content"

    @pytest.mark.asyncio
    async def test_search_content(self, db_session):
        await SearchService.create_search_index(
            db_session, 1, "content", "Python Tutorial", "Learn Python"
        )
        await SearchService.create_search_index(
            db_session, 2, "content", "Java Guide", "Learn Java"
        )
        results = await SearchService.search_content(db_session, "Python")
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_save_search(self, db_session):
        saved = await SearchService.save_search(
            db_session, 1, "python tutorials", {"category": "tech"}
        )
        assert saved.user_id == 1
        assert saved.query == "python tutorials"

    @pytest.mark.asyncio
    async def test_get_saved_searches(self, db_session):
        await SearchService.save_search(db_session, 1, "query1")
        await SearchService.save_search(db_session, 1, "query2")
        searches = await SearchService.get_saved_searches(db_session, 1)
        assert len(searches) == 2

    @pytest.mark.asyncio
    async def test_delete_saved_search(self, db_session):
        saved = await SearchService.save_search(db_session, 1, "query")
        success = await SearchService.delete_saved_search(db_session, saved.id, 1)
        assert success is True

    @pytest.mark.asyncio
    async def test_update_search_index(self, db_session):
        index = await SearchService.create_search_index(
            db_session, 1, "content", "Old Title", "Old content"
        )
        updated = await SearchService.update_search_index(
            db_session, index.id, "New Title"
        )
        assert updated.title == "New Title"


class TestPushNotificationService:
    @pytest.mark.asyncio
    async def test_register_device(self, db_session):
        device = await PushNotificationService.register_device(
            db_session, 1, "token123", "ios", "iPhone 12"
        )
        assert device.user_id == 1
        assert device.device_token == "token123"

    @pytest.mark.asyncio
    async def test_register_duplicate_device(self, db_session):
        await PushNotificationService.register_device(
            db_session, 1, "token123", "ios"
        )
        device = await PushNotificationService.register_device(
            db_session, 1, "token123", "ios"
        )
        assert device.user_id == 1

    @pytest.mark.asyncio
    async def test_unregister_device(self, db_session):
        device = await PushNotificationService.register_device(
            db_session, 1, "token123", "ios"
        )
        success = await PushNotificationService.unregister_device(db_session, device.id, 1)
        assert success is True

    @pytest.mark.asyncio
    async def test_get_user_devices(self, db_session):
        await PushNotificationService.register_device(db_session, 1, "token1", "ios")
        await PushNotificationService.register_device(db_session, 1, "token2", "android")
        devices = await PushNotificationService.get_user_devices(db_session, 1)
        assert len(devices) == 2

    @pytest.mark.asyncio
    async def test_log_notification(self, db_session):
        log = await PushNotificationService.log_notification(
            db_session, 1, "engagement", "New Like", "Someone liked your post"
        )
        assert log.user_id == 1
        assert log.notification_type == "engagement"

    @pytest.mark.asyncio
    async def test_update_notification_status(self, db_session):
        log = await PushNotificationService.log_notification(
            db_session, 1, "engagement", "Test", "Body"
        )
        updated = await PushNotificationService.update_notification_status(
            db_session, log.id, "delivered"
        )
        assert updated.status == "delivered"

    @pytest.mark.asyncio
    async def test_get_notification_logs(self, db_session):
        await PushNotificationService.log_notification(
            db_session, 1, "engagement", "Test 1", "Body 1"
        )
        await PushNotificationService.log_notification(
            db_session, 1, "content", "Test 2", "Body 2"
        )
        logs = await PushNotificationService.get_notification_logs(db_session, 1)
        assert len(logs) == 2


class TestAdminService:
    @pytest.mark.asyncio
    async def test_create_admin_user(self, db_session):
        admin = await AdminService.create_admin_user(
            db_session, 1, "moderator", ["delete_content", "block_user"]
        )
        assert admin.user_id == 1
        assert admin.role == "moderator"

    @pytest.mark.asyncio
    async def test_create_duplicate_admin_error(self, db_session):
        await AdminService.create_admin_user(db_session, 1, "moderator")
        with pytest.raises(Exception):
            await AdminService.create_admin_user(db_session, 1, "admin")

    @pytest.mark.asyncio
    async def test_remove_admin_user(self, db_session):
        await AdminService.create_admin_user(db_session, 1, "moderator")
        success = await AdminService.remove_admin_user(db_session, 1)
        assert success is True

    @pytest.mark.asyncio
    async def test_get_admin_user(self, db_session):
        created = await AdminService.create_admin_user(db_session, 1, "moderator")
        fetched = await AdminService.get_admin_user(db_session, 1)
        assert fetched.user_id == created.user_id

    @pytest.mark.asyncio
    async def test_log_admin_action(self, db_session):
        await AdminService.create_admin_user(db_session, 1, "moderator")
        log = await AdminService.log_admin_action(
            db_session, 1, "delete_content", "post", 123, {"reason": "spam"}
        )
        assert log.admin_user_id == 1
        assert log.action_type == "delete_content"

    @pytest.mark.asyncio
    async def test_get_admin_logs(self, db_session):
        await AdminService.create_admin_user(db_session, 1, "moderator")
        await AdminService.log_admin_action(
            db_session, 1, "delete_content", "post", 123
        )
        await AdminService.log_admin_action(
            db_session, 1, "block_user", "user", 456
        )
        logs = await AdminService.get_admin_logs(db_session)
        assert len(logs) == 2

    @pytest.mark.asyncio
    async def test_update_admin_permissions(self, db_session):
        await AdminService.create_admin_user(
            db_session, 1, "moderator", ["delete_content"]
        )
        updated = await AdminService.update_admin_permissions(
            db_session, 1, ["delete_content", "block_user", "view_analytics"]
        )
        assert len(updated.permissions) == 3


class TestSystemService:
    @pytest.mark.asyncio
    async def test_create_system_notification(self, db_session):
        notif = await SystemService.create_system_notification(
            db_session, "Maintenance", "System will be down", "system"
        )
        assert notif.title == "Maintenance"

    @pytest.mark.asyncio
    async def test_get_system_notifications(self, db_session):
        await SystemService.create_system_notification(
            db_session, "Alert 1", "Message 1", "alert"
        )
        await SystemService.create_system_notification(
            db_session, "Alert 2", "Message 2", "alert"
        )
        notifs = await SystemService.get_system_notifications(db_session)
        assert len(notifs) == 2

    @pytest.mark.asyncio
    async def test_record_platform_statistic(self, db_session):
        stat = await SystemService.record_platform_statistic(
            db_session, "active_users", 1500.0, "count"
        )
        assert stat.metric_name == "active_users"
        assert stat.metric_value == 1500.0

    @pytest.mark.asyncio
    async def test_get_platform_statistics(self, db_session):
        await SystemService.record_platform_statistic(
            db_session, "active_users", 1000
        )
        await SystemService.record_platform_statistic(
            db_session, "active_users", 1100
        )
        stats = await SystemService.get_platform_statistics(
            db_session, "active_users"
        )
        assert len(stats) >= 1

    @pytest.mark.asyncio
    async def test_get_aggregated_statistics(self, db_session):
        await SystemService.record_platform_statistic(db_session, "metric1", 100)
        await SystemService.record_platform_statistic(db_session, "metric1", 200)
        await SystemService.record_platform_statistic(db_session, "metric1", 300)
        agg = await SystemService.get_aggregated_statistics(db_session, "metric1")
        assert agg["count"] == 3
        assert agg["average"] == 200.0

    @pytest.mark.asyncio
    async def test_get_dashboard_summary(self, db_session):
        await SocialService.create_interaction(db_session, 1, 1, "like")
        await SocialService.follow_user(db_session, 1, 2)
        summary = await SystemService.get_dashboard_summary(db_session)
        assert "total_interactions" in summary
        assert "total_follows" in summary
