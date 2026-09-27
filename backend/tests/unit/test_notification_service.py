"""Unit tests for NotificationService"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.notification_service import NotificationService
from app.models.user import User
from app.models.notifications import NotificationType, NotificationChannel
from app.core.security import hash_password


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        email="notif_test@example.com",
        password_hash=hash_password("pass"),
        first_name="Notif",
        last_name="Test",
        status="active",
    )
    test_session.add(user)
    await test_session.flush()
    return user


class TestInAppNotifications:
    async def test_create_notification(self, test_session: AsyncSession, test_user: User):
        """Test creating in-app notification"""
        service = NotificationService(test_session)

        notif = await service.create_notification(
            user_id=test_user.id,
            title="Test Notification",
            message="This is a test",
            notification_type=NotificationType.ACTIVITY,
        )

        assert notif.user_id == test_user.id
        assert notif.title == "Test Notification"
        assert notif.is_read is False

    async def test_get_user_notifications(self, test_session: AsyncSession, test_user: User):
        """Test getting user notifications"""
        service = NotificationService(test_session)

        await service.create_notification(
            user_id=test_user.id,
            title="Notif 1",
            message="Message 1",
        )
        await service.create_notification(
            user_id=test_user.id,
            title="Notif 2",
            message="Message 2",
        )

        notifications = await service.get_user_notifications(test_user.id)

        assert len(notifications) == 2
        assert notifications[0].title in ["Notif 1", "Notif 2"]

    async def test_mark_as_read(self, test_session: AsyncSession, test_user: User):
        """Test marking notification as read"""
        service = NotificationService(test_session)

        notif = await service.create_notification(
            user_id=test_user.id,
            title="Test",
            message="Test",
        )

        marked = await service.mark_as_read(notif.id, test_user.id)

        assert marked.is_read is True
        assert marked.read_at is not None

    async def test_get_unread_count(self, test_session: AsyncSession, test_user: User):
        """Test getting unread notification count"""
        service = NotificationService(test_session)

        await service.create_notification(
            user_id=test_user.id,
            title="Unread 1",
            message="Message",
        )
        await service.create_notification(
            user_id=test_user.id,
            title="Unread 2",
            message="Message",
        )

        count = await service.get_unread_count(test_user.id)

        assert count == 2

    async def test_mark_all_as_read(self, test_session: AsyncSession, test_user: User):
        """Test marking all as read"""
        service = NotificationService(test_session)

        await service.create_notification(
            user_id=test_user.id,
            title="Notif 1",
            message="Message 1",
        )
        await service.create_notification(
            user_id=test_user.id,
            title="Notif 2",
            message="Message 2",
        )

        count = await service.mark_all_as_read(test_user.id)

        assert count == 2

        unread_count = await service.get_unread_count(test_user.id)
        assert unread_count == 0

    async def test_archive_notification(self, test_session: AsyncSession, test_user: User):
        """Test archiving notification"""
        service = NotificationService(test_session)

        notif = await service.create_notification(
            user_id=test_user.id,
            title="Archive Me",
            message="Test",
        )

        archived = await service.archive_notification(notif.id, test_user.id)

        assert archived.is_archived is True

    async def test_delete_notification(self, test_session: AsyncSession, test_user: User):
        """Test deleting notification"""
        service = NotificationService(test_session)

        notif = await service.create_notification(
            user_id=test_user.id,
            title="Delete Me",
            message="Test",
        )

        result = await service.delete_notification(notif.id, test_user.id)

        assert result is True


class TestEmailNotifications:
    async def test_send_email(self, test_session: AsyncSession, test_user: User):
        """Test sending email notification"""
        service = NotificationService(test_session)

        email = await service.send_email(
            user_id=test_user.id,
            recipient_email="test@example.com",
            subject="Test Email",
            template="welcome",
        )

        assert email.user_id == test_user.id
        assert email.recipient_email == "test@example.com"
        assert email.status == "pending"

    async def test_mark_email_sent(self, test_session: AsyncSession, test_user: User):
        """Test marking email as sent"""
        service = NotificationService(test_session)

        email = await service.send_email(
            user_id=test_user.id,
            recipient_email="test@example.com",
            subject="Test",
            template="welcome",
        )

        sent = await service.mark_email_sent(email.id)

        assert sent.status == "sent"
        assert sent.sent_at is not None

    async def test_get_pending_emails(self, test_session: AsyncSession, test_user: User):
        """Test getting pending emails"""
        service = NotificationService(test_session)

        await service.send_email(
            user_id=test_user.id,
            recipient_email="test1@example.com",
            subject="Email 1",
            template="welcome",
        )
        await service.send_email(
            user_id=test_user.id,
            recipient_email="test2@example.com",
            subject="Email 2",
            template="notification",
        )

        pending = await service.get_pending_emails(limit=10)

        assert len(pending) == 2


class TestPushNotifications:
    async def test_send_push(self, test_session: AsyncSession, test_user: User):
        """Test sending push notification"""
        service = NotificationService(test_session)

        push = await service.send_push(
            user_id=test_user.id,
            device_token="device123",
            title="Push Title",
            message="Push Message",
        )

        assert push.user_id == test_user.id
        assert push.device_token == "device123"
        assert push.status == "pending"

    async def test_mark_push_sent(self, test_session: AsyncSession, test_user: User):
        """Test marking push as sent"""
        service = NotificationService(test_session)

        push = await service.send_push(
            user_id=test_user.id,
            device_token="device123",
            title="Push",
            message="Message",
        )

        sent = await service.mark_push_sent(push.id)

        assert sent.status == "sent"
        assert sent.sent_at is not None

    async def test_mark_push_delivered(self, test_session: AsyncSession, test_user: User):
        """Test marking push as delivered"""
        service = NotificationService(test_session)

        push = await service.send_push(
            user_id=test_user.id,
            device_token="device123",
            title="Push",
            message="Message",
        )

        delivered = await service.mark_push_delivered(push.id)

        assert delivered.delivered_at is not None

    async def test_get_pending_pushes(self, test_session: AsyncSession, test_user: User):
        """Test getting pending pushes"""
        service = NotificationService(test_session)

        await service.send_push(
            user_id=test_user.id,
            device_token="device1",
            title="Push 1",
            message="Message 1",
        )
        await service.send_push(
            user_id=test_user.id,
            device_token="device2",
            title="Push 2",
            message="Message 2",
        )

        pending = await service.get_pending_pushes(limit=10)

        assert len(pending) == 2


class TestNotificationTemplates:
    async def test_create_template(self, test_session: AsyncSession):
        """Test creating notification template"""
        service = NotificationService(test_session)

        template = await service.create_template(
            name="welcome_email",
            subject="Welcome!",
            title_template="Welcome {{user_name}}",
            body_template="Thanks for joining!",
            variables=["user_name"],
        )

        assert template.name == "welcome_email"
        assert template.subject == "Welcome!"

    async def test_get_template(self, test_session: AsyncSession):
        """Test getting template by name"""
        service = NotificationService(test_session)

        created = await service.create_template(
            name="test_template",
            subject="Test",
            title_template="Title",
            body_template="Body",
        )

        retrieved = await service.get_template("test_template")

        assert retrieved.name == "test_template"
        assert retrieved.subject == "Test"


class TestNotificationLogs:
    async def test_get_notification_logs(self, test_session: AsyncSession, test_user: User):
        """Test getting notification logs"""
        service = NotificationService(test_session)

        notif = await service.create_notification(
            user_id=test_user.id,
            title="Test",
            message="Test",
        )

        await service._log_notification(
            test_user.id,
            notif.id,
            "created",
            NotificationChannel.INAPP,
            "success",
        )

        logs = await service.get_notification_logs(test_user.id, limit=10)

        assert len(logs) >= 1
        assert logs[0].action == "created"
