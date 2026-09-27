"""Unit tests for ActivityService"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.activity_service import ActivityService
from app.models.user import User
from app.models.activity_logs import ActionType, EntityType
from app.core.security import hash_password


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        email="activity_test@example.com",
        password_hash=hash_password("pass"),
        first_name="Activity",
        last_name="Test",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()
    return user


class TestActivityLogging:
    async def test_log_activity(self, test_session: AsyncSession, test_user: User):
        """Test logging an activity"""
        service = ActivityService(test_session)

        activity = await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            description="Created a document",
        )

        assert activity.user_id == test_user.id
        assert activity.action == ActionType.CREATE
        assert activity.status == "success"

    async def test_get_user_activities(self, test_session: AsyncSession, test_user: User):
        """Test getting user activities"""
        service = ActivityService(test_session)

        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )
        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.UPDATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )

        activities = await service.get_user_activities(test_user.id)

        assert len(activities) == 2

    async def test_get_user_activities_with_filter(self, test_session: AsyncSession, test_user: User):
        """Test getting user activities with action filter"""
        service = ActivityService(test_session)

        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )
        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.DELETE,
            entity_type=EntityType.DOCUMENT,
            entity_id=2,
        )

        creates = await service.get_user_activities(
            test_user.id,
            action=ActionType.CREATE,
        )

        assert len(creates) == 1
        assert creates[0].action == ActionType.CREATE

    async def test_get_entity_activities(self, test_session: AsyncSession, test_user: User):
        """Test getting activities for an entity"""
        service = ActivityService(test_session)

        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )
        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.UPDATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )

        activities = await service.get_entity_activities(
            EntityType.DOCUMENT,
            1,
        )

        assert len(activities) == 2

    async def test_get_user_activity_count(self, test_session: AsyncSession, test_user: User):
        """Test getting activity count"""
        service = ActivityService(test_session)

        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.LOGIN,
            entity_type=EntityType.USER,
            entity_id=test_user.id,
        )

        count = await service.get_user_activity_count(test_user.id, days=7)

        assert count >= 1


class TestAuditLogging:
    async def test_log_change(self, test_session: AsyncSession, test_user: User):
        """Test logging a change"""
        service = ActivityService(test_session)

        audit = await service.log_change(
            user_id=test_user.id,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            action=ActionType.UPDATE,
            old_values={"title": "Old Title"},
            new_values={"title": "New Title"},
            reason="Updated title",
        )

        assert audit.user_id == test_user.id
        assert audit.action == ActionType.UPDATE
        assert "title" in audit.changed_fields

    async def test_get_entity_audit_trail(self, test_session: AsyncSession, test_user: User):
        """Test getting audit trail for entity"""
        service = ActivityService(test_session)

        await service.log_change(
            user_id=test_user.id,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            action=ActionType.CREATE,
            new_values={"title": "Doc 1"},
        )
        await service.log_change(
            user_id=test_user.id,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            action=ActionType.UPDATE,
            old_values={"title": "Doc 1"},
            new_values={"title": "Doc Updated"},
        )

        trail = await service.get_entity_audit_trail(EntityType.DOCUMENT, 1)

        assert len(trail) == 2

    async def test_get_user_audit_logs(self, test_session: AsyncSession, test_user: User):
        """Test getting user's audit logs"""
        service = ActivityService(test_session)

        await service.log_change(
            user_id=test_user.id,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            action=ActionType.UPDATE,
            old_values={"name": "Old"},
            new_values={"name": "New"},
        )

        logs = await service.get_user_audit_logs(test_user.id)

        assert len(logs) >= 1


class TestActivityFeed:
    async def test_create_feed_item(self, test_session: AsyncSession, test_user: User):
        """Test creating feed item"""
        service = ActivityService(test_session)

        feed = await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            title="New document created",
        )

        assert feed.user_id == test_user.id
        assert feed.action == ActionType.CREATE
        assert feed.is_read is False

    async def test_get_user_feed(self, test_session: AsyncSession, test_user: User):
        """Test getting user feed"""
        service = ActivityService(test_session)

        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            title="Item 1",
        )
        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.UPDATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=2,
            title="Item 2",
        )

        feed = await service.get_user_feed(test_user.id)

        assert len(feed) == 2

    async def test_mark_feed_item_read(self, test_session: AsyncSession, test_user: User):
        """Test marking feed item as read"""
        service = ActivityService(test_session)

        feed = await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            title="Test",
        )

        marked = await service.mark_feed_item_read(feed.id, test_user.id)

        assert marked.is_read is True

    async def test_get_unread_feed_count(self, test_session: AsyncSession, test_user: User):
        """Test getting unread feed count"""
        service = ActivityService(test_session)

        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            title="Item 1",
        )
        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=2,
            title="Item 2",
        )

        count = await service.get_unread_feed_count(test_user.id)

        assert count == 2

    async def test_mark_all_feed_read(self, test_session: AsyncSession, test_user: User):
        """Test marking all feed as read"""
        service = ActivityService(test_session)

        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
            title="Item 1",
        )
        await service.create_feed_item(
            user_id=test_user.id,
            actor_user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=2,
            title="Item 2",
        )

        count = await service.mark_all_feed_read(test_user.id)

        assert count == 2


class TestRetentionPolicies:
    async def test_create_retention_policy(self, test_session: AsyncSession):
        """Test creating retention policy"""
        service = ActivityService(test_session)

        policy = await service.create_retention_policy(
            entity_type=EntityType.DOCUMENT,
            retention_days=90,
            archive_days=30,
        )

        assert policy.entity_type == EntityType.DOCUMENT
        assert policy.retention_days == 90

    async def test_get_retention_policy(self, test_session: AsyncSession):
        """Test getting retention policy"""
        service = ActivityService(test_session)

        created = await service.create_retention_policy(
            entity_type=EntityType.USER,
            retention_days=180,
        )

        retrieved = await service.get_retention_policy(EntityType.USER)

        assert retrieved.retention_days == 180


class TestActivitySummary:
    async def test_get_activity_summary(self, test_session: AsyncSession, test_user: User):
        """Test getting activity summary"""
        service = ActivityService(test_session)

        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=1,
        )
        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.CREATE,
            entity_type=EntityType.PROJECT,
            entity_id=2,
        )
        await service.log_activity(
            user_id=test_user.id,
            action=ActionType.UPDATE,
            entity_type=EntityType.DOCUMENT,
            entity_id=3,
        )

        summary = await service.get_activity_summary(test_user.id, days=7)

        assert summary["total_activities"] >= 3
        assert "by_action" in summary
        assert "by_entity" in summary
