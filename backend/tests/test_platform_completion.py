"""Platform completion services: social graph, messaging, search, devices, notification logs, admin and system (async)."""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.models.platform_completion import (
    AdminActionType,
    AdminUser,
    InteractionType,
    PlatformStatistics,
    PushNotificationConfig,
    PushNotificationLog,
    PushNotificationType,
    SavedSearch,
    SearchIndexType,
    SystemNotification,
    UserMessage,
)
from app.services.platform_completion_service import (
    AdminService,
    PushNotificationService,
    SearchService,
    SocialService,
    SystemService,
)


def _naive_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@pytest.fixture
async def users(reference_data):
    """Users 1 and 2 from the seeded reference data."""
    return (1, 2)


class TestSocialService:
    async def test_create_interaction(self, session, users):
        interaction = await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE, {"sentiment": "positive"})
        assert interaction.user_id == 1
        assert interaction.content_id == 1
        assert interaction.interaction_type == InteractionType.LIKE
        assert interaction.extra_metadata == {"sentiment": "positive"}

    async def test_create_duplicate_interaction(self, session, users):
        first = await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE)
        again = await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE)
        assert again.id == first.id
        assert again.updated_at is not None

    async def test_remove_interaction(self, session, users):
        await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE)
        assert await SocialService.remove_interaction(session, 1, 1, InteractionType.LIKE) is True
        assert await SocialService.remove_interaction(session, 1, 1, InteractionType.LIKE) is False

    async def test_get_user_interactions(self, session, users):
        await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE)
        await SocialService.create_interaction(session, 1, 2, InteractionType.COMMENT)
        interactions = await SocialService.get_user_interactions(session, 1)
        assert len(interactions) == 2

    async def test_get_content_interactions(self, session, users):
        await SocialService.create_interaction(session, 1, 7, InteractionType.LIKE)
        await SocialService.create_interaction(session, 2, 7, InteractionType.SHARE)
        everything = await SocialService.get_content_interactions(session, 7)
        shares = await SocialService.get_content_interactions(session, 7, InteractionType.SHARE)
        assert len(everything) == 2
        assert [i.user_id for i in shares] == [2]

    async def test_follow_user(self, session, users):
        follow = await SocialService.follow_user(session, 1, 2)
        assert follow.follower_id == 1
        assert follow.following_id == 2
        assert follow.followed_at is not None
        assert (await SocialService.follow_user(session, 1, 2)).id == follow.id

    async def test_follow_self_error(self, session, users):
        with pytest.raises(HTTPException) as info:
            await SocialService.follow_user(session, 1, 1)
        assert info.value.status_code == 400

    async def test_unfollow_user(self, session, users):
        await SocialService.follow_user(session, 1, 2)
        assert await SocialService.unfollow_user(session, 1, 2) is True
        assert await SocialService.unfollow_user(session, 1, 2) is False

    async def test_get_followers(self, session, users):
        await SocialService.follow_user(session, 1, 2)
        followers = await SocialService.get_followers(session, 2)
        assert [f.follower_id for f in followers] == [1]

    async def test_get_following(self, session, users):
        await SocialService.follow_user(session, 1, 2)
        following = await SocialService.get_following(session, 1)
        assert [f.following_id for f in following] == [2]

    async def test_create_comment(self, session, users):
        comment = await SocialService.create_comment(session, 1, 3, "Nice article")
        assert comment.text == "Nice article"
        assert comment.parent_comment_id is None
        assert comment.created_at is not None

    async def test_create_nested_comment(self, session, users):
        parent = await SocialService.create_comment(session, 1, 3, "Parent")
        child = await SocialService.create_comment(session, 2, 3, "Reply", parent.id)
        assert child.parent_comment_id == parent.id

    async def test_get_comments(self, session, users):
        parent = await SocialService.create_comment(session, 1, 3, "Parent")
        await SocialService.create_comment(session, 2, 3, "Reply", parent.id)
        top = await SocialService.get_comments(session, 3)
        replies = await SocialService.get_comments(session, 3, parent_comment_id=parent.id)
        assert len(top) == 2
        assert [c.text for c in replies] == ["Reply"]

    async def test_delete_comment(self, session, users):
        comment = await SocialService.create_comment(session, 1, 3, "Mine")
        with pytest.raises(HTTPException) as foreign:
            await SocialService.delete_comment(session, comment.id, 2)
        assert foreign.value.status_code == 403
        assert await SocialService.delete_comment(session, comment.id, 1) is True
        with pytest.raises(HTTPException) as missing:
            await SocialService.delete_comment(session, comment.id, 1)
        assert missing.value.status_code == 404

    async def test_send_message(self, session, users):
        message = await SocialService.send_message(session, 1, 2, "Hello")
        assert message.sender_id == 1
        assert message.recipient_id == 2
        assert message.read is False

    async def test_send_self_message_error(self, session, users):
        with pytest.raises(HTTPException) as info:
            await SocialService.send_message(session, 1, 1, "Hello me")
        assert info.value.status_code == 400

    async def test_get_conversation(self, session, users):
        await SocialService.send_message(session, 1, 2, "one")
        await SocialService.send_message(session, 2, 1, "two")
        await SocialService.send_message(session, 2, 1, "three")
        conversation = await SocialService.get_conversation(session, 1, 2)
        assert len(conversation) == 3

    async def test_mark_message_read(self, session, users):
        message = await SocialService.send_message(session, 1, 2, "read me")
        assert await SocialService.mark_message_read(session, message.id, 2) is True
        stored = await session.get(UserMessage, message.id)
        assert stored.read is True
        assert stored.read_at is not None

    async def test_only_the_recipient_marks_a_message_read(self, session, users):
        message = await SocialService.send_message(session, 1, 2, "private")
        with pytest.raises(HTTPException) as foreign:
            await SocialService.mark_message_read(session, message.id, 1)
        assert foreign.value.status_code == 403
        with pytest.raises(HTTPException) as missing:
            await SocialService.mark_message_read(session, 999999, 2)
        assert missing.value.status_code == 404


class TestSearchService:
    async def test_create_search_index(self, session, users):
        index = await SearchService.create_search_index(session, 1, SearchIndexType.CONTENT, "Title", "Body", {"lang": "en"}, [0.1, 0.2])
        assert index.title == "Title"
        assert index.extra_metadata == {"lang": "en"}
        assert index.embedding_vector == [0.1, 0.2]

    async def test_search_content(self, session, users):
        await SearchService.create_search_index(session, 1, SearchIndexType.CONTENT, "Python tips", "Body")
        await SearchService.create_search_index(session, 2, SearchIndexType.TOPIC, "Cooking", "pasta python")
        both = await SearchService.search_content(session, "python")
        articles = await SearchService.search_content(session, "python", index_type=SearchIndexType.CONTENT)
        assert len(both) == 2
        assert [i.title for i in articles] == ["Python tips"]

    async def test_save_search(self, session, users):
        saved = await SearchService.save_search(session, 1, "python tutorials", {"type": SearchIndexType.CONTENT}, result_count=4)
        assert saved.name == "python tutorials"
        assert saved.result_count == 4

    async def test_get_saved_searches(self, session, users):
        await SearchService.save_search(session, 1, "one")
        await SearchService.save_search(session, 1, "two")
        await SearchService.save_search(session, 2, "theirs")
        assert len(await SearchService.get_saved_searches(session, 1)) == 2

    async def test_delete_saved_search(self, session, users):
        saved = await SearchService.save_search(session, 1, "gone")
        assert await SearchService.delete_saved_search(session, saved.id, 2) is False
        assert await SearchService.delete_saved_search(session, saved.id, 1) is True
        assert await session.get(SavedSearch, saved.id) is None

    async def test_update_search_index(self, session, users):
        index = await SearchService.create_search_index(session, 1, SearchIndexType.CONTENT, "Old", "Old body")
        updated = await SearchService.update_search_index(session, index.id, title="New", metadata={"v": 2})
        assert updated.title == "New"
        assert updated.description == "Old body"
        assert updated.extra_metadata == {"v": 2}
        with pytest.raises(HTTPException) as info:
            await SearchService.update_search_index(session, 999999, title="x")
        assert info.value.status_code == 404


class TestPushNotificationService:
    async def test_register_device(self, session, users):
        device = await PushNotificationService.register_device(session, 1, "token-a", "ios", "iPhone")
        assert device.platform == "ios"
        assert device.device_name == "iPhone"
        assert device.last_sync is not None

    async def test_register_duplicate_device(self, session, users):
        first = await PushNotificationService.register_device(session, 1, "token-a", "ios")
        again = await PushNotificationService.register_device(session, 1, "token-a", "ios")
        assert again.id == first.id

    async def test_unregister_device(self, session, users):
        device = await PushNotificationService.register_device(session, 1, "token-b", "android")
        assert await PushNotificationService.unregister_device(session, device.id, 2) is False
        assert await PushNotificationService.unregister_device(session, device.id, 1) is True
        assert await session.get(PushNotificationConfig, device.id) is None

    async def test_get_user_devices(self, session, users):
        await PushNotificationService.register_device(session, 1, "token-c", "web")
        await PushNotificationService.register_device(session, 2, "token-d", "web")
        assert [d.device_token for d in await PushNotificationService.get_user_devices(session, 1)] == ["token-c"]

    async def test_log_notification(self, session, users):
        log = await PushNotificationService.log_notification(session, 1, PushNotificationType.SYSTEM, "Hi", "Body")
        assert log.status == "pending"
        assert log.created_at is not None

    async def test_update_notification_status(self, session, users):
        log = await PushNotificationService.log_notification(session, 1, PushNotificationType.SYSTEM, "Hi", "Body")
        delivered = _naive_utc()
        updated = await PushNotificationService.update_notification_status(session, log.id, "delivered", delivered_at=delivered)
        assert updated.status == "delivered"
        assert updated.delivered_at == delivered
        with pytest.raises(HTTPException) as info:
            await PushNotificationService.update_notification_status(session, 999999, "delivered")
        assert info.value.status_code == 404

    async def test_get_notification_logs(self, session, users):
        await PushNotificationService.log_notification(session, 1, PushNotificationType.SYSTEM, "A", "a")
        await PushNotificationService.log_notification(session, 1, PushNotificationType.SYSTEM, "B", "b")
        logs = await PushNotificationService.get_notification_logs(session, 1)
        assert {log.title for log in logs} == {"A", "B"}
        assert await session.get(PushNotificationLog, logs[0].id) is not None


class TestAdminService:
    async def test_create_admin_user(self, session, users):
        admin = await AdminService.create_admin_user(session, 1, "moderator", ["content:review"])
        assert admin.role == "moderator"
        assert admin.permissions == ["content:review"]

    async def test_create_duplicate_admin_error(self, session, users):
        await AdminService.create_admin_user(session, 1, "moderator")
        with pytest.raises(HTTPException) as info:
            await AdminService.create_admin_user(session, 1, "owner")
        assert info.value.status_code == 400

    async def test_remove_admin_user(self, session, users):
        await AdminService.create_admin_user(session, 1, "moderator")
        assert await AdminService.remove_admin_user(session, 1) is True
        assert await AdminService.remove_admin_user(session, 1) is False

    async def test_get_admin_user(self, session, users):
        admin = await AdminService.create_admin_user(session, 2, "support")
        assert (await AdminService.get_admin_user(session, 2)).id == admin.id
        assert await AdminService.get_admin_user(session, 1) is None

    async def test_log_admin_action(self, session, users):
        log = await AdminService.log_admin_action(session, 1, AdminActionType.CONTENT_MANAGE, "course", 5, {"field": "title"})
        assert log.details == {"field": "title"}
        assert log.status == "completed"
        assert log.created_at is not None

    async def test_get_admin_logs(self, session, users):
        await AdminService.log_admin_action(session, 1, AdminActionType.CONTENT_MANAGE, "course", 5)
        await AdminService.log_admin_action(session, 1, AdminActionType.DELETE_CONTENT, "course", 6)
        await AdminService.log_admin_action(session, 2, AdminActionType.CONTENT_MANAGE, "course", 7)
        assert len(await AdminService.get_admin_logs(session, admin_user_id=1)) == 2
        updates = await AdminService.get_admin_logs(session, action_type=AdminActionType.CONTENT_MANAGE)
        assert len(updates) == 2

    async def test_update_admin_permissions(self, session, users):
        await AdminService.create_admin_user(session, 1, "moderator", ["a"])
        updated = await AdminService.update_admin_permissions(session, 1, ["a", "b"])
        assert updated.permissions == ["a", "b"]
        with pytest.raises(HTTPException) as info:
            await AdminService.update_admin_permissions(session, 999999, [])
        assert info.value.status_code == 404
        assert await session.get(AdminUser, updated.id) is not None


class TestSystemService:
    async def test_create_system_notification(self, session, users):
        notice = await SystemService.create_system_notification(session, "Maintenance", "Tonight", "warning", [1, 2])
        assert notice.target_users == [1, 2]
        assert notice.created_at is not None

    async def test_get_system_notifications(self, session, users):
        await SystemService.create_system_notification(session, "First", "m", "info")
        await SystemService.create_system_notification(session, "Second", "m", "info")
        notices = await SystemService.get_system_notifications(session)
        assert [n.title for n in notices] == ["Second", "First"]
        assert await session.get(SystemNotification, notices[0].id) is not None

    async def test_record_platform_statistic(self, session, users):
        stat = await SystemService.record_platform_statistic(session, "signups", 12.0, breakdown={"web": 10})
        assert stat.metric_type == "count"
        assert stat.breakdown == {"web": 10}

    async def test_get_platform_statistics(self, session, users):
        recent = await SystemService.record_platform_statistic(session, "signups", 3.0)
        old = await SystemService.record_platform_statistic(session, "signups", 9.0)
        old.created_at = _naive_utc() - timedelta(days=30)
        await session.commit()
        stats = await SystemService.get_platform_statistics(session, metric_name="signups", days=7)
        assert [s.id for s in stats] == [recent.id]
        assert await session.get(PlatformStatistics, old.id) is not None

    async def test_get_aggregated_statistics(self, session, users):
        await SystemService.record_platform_statistic(session, "revenue", 10.0)
        await SystemService.record_platform_statistic(session, "revenue", 30.0)
        summary = await SystemService.get_aggregated_statistics(session, "revenue", days=30)
        assert summary["count"] == 2
        assert summary["sum"] == 40.0
        assert summary["average"] == 20.0
        assert summary["min"] == 10.0
        assert summary["max"] == 30.0
        empty = await SystemService.get_aggregated_statistics(session, "nothing", days=30)
        assert empty["count"] == 0

    async def test_get_dashboard_summary(self, session, users):
        await SocialService.create_interaction(session, 1, 1, InteractionType.LIKE)
        await SocialService.follow_user(session, 1, 2)
        await SocialService.create_comment(session, 1, 1, "hi")
        await SocialService.send_message(session, 1, 2, "hello")
        summary = await SystemService.get_dashboard_summary(session)
        assert summary["total_interactions"] == 1
        assert summary["total_follows"] == 1
        assert summary["total_comments"] == 1
        assert summary["total_messages"] == 1
        assert summary["total_notifications"] == 0
        assert datetime.fromisoformat(summary["timestamp"])
