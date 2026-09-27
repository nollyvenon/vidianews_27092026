import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.user_management import (
    EmailTemplate, EmailCampaign, UserSegment, SubscriberProfile,
    SubscriberActivity, NotificationLog, WebhookEndpoint, APIKey,
    PersonalizationProfile, CampaignStatus, NotificationChannel,
    UserSegmentType
)
from app.services.user_management_service import (
    EmailTemplateService, EmailCampaignService, UserSegmentService,
    SubscriberService, NotificationService, WebhookService,
    APIKeyService, PersonalizationService
)


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: None)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


class TestEmailTemplateService:
    @pytest.mark.asyncio
    async def test_create_email_template(self, db):
        service = EmailTemplateService()
        result = await service.create_email_template(
            db,
            "Welcome Template",
            "Welcome to VidiaNews",
            "<h1>Welcome</h1>",
            {"name": "User Name"},
        )

        assert result["name"] == "Welcome Template"
        assert result["subject"] == "Welcome to VidiaNews"

    @pytest.mark.asyncio
    async def test_create_template_without_variables(self, db):
        service = EmailTemplateService()
        result = await service.create_email_template(
            db,
            "Simple Template",
            "Subject",
            "Body",
        )

        assert result["template_variables"] == {}


class TestEmailCampaignService:
    @pytest.mark.asyncio
    async def test_create_email_campaign(self, db):
        service = EmailCampaignService()
        result = await service.create_email_campaign(
            db,
            "Weekly Newsletter",
            1,
            "Your Weekly News",
            "newsletter@vidianews.com",
        )

        assert result["name"] == "Weekly Newsletter"
        assert result["status"] == CampaignStatus.DRAFT.value

    @pytest.mark.asyncio
    async def test_add_campaign_recipients(self, db):
        service = EmailCampaignService()

        # Create campaign first
        campaign_result = await service.create_email_campaign(
            db,
            "Test Campaign",
            1,
            "Subject",
            "from@example.com",
        )

        recipients = [
            {"user_id": 1, "email": "user1@example.com"},
            {"user_id": 2, "email": "user2@example.com"},
        ]

        result = await service.add_campaign_recipients(
            db,
            campaign_result["id"],
            recipients,
        )

        assert result["recipient_count"] == 2

    @pytest.mark.asyncio
    async def test_update_campaign_metrics(self, db):
        service = EmailCampaignService()

        campaign_result = await service.create_email_campaign(
            db,
            "Test Campaign",
            1,
            "Subject",
            "from@example.com",
        )

        result = await service.update_campaign_metrics(
            db,
            campaign_result["id"],
            sent_count=100,
            open_count=25,
            click_count=5,
        )

        assert result["open_rate"] == 0.0  # 0 recipients, no rate
        assert result["click_rate"] == 0.0

    @pytest.mark.asyncio
    async def test_send_campaign(self, db):
        service = EmailCampaignService()

        campaign_result = await service.create_email_campaign(
            db,
            "Test Campaign",
            1,
            "Subject",
            "from@example.com",
        )

        result = await service.send_campaign(db, campaign_result["id"])
        assert result["status"] == CampaignStatus.SENDING.value
        assert result["sent_at"] is not None


class TestUserSegmentService:
    @pytest.mark.asyncio
    async def test_create_user_segment(self, db):
        service = UserSegmentService()
        result = await service.create_user_segment(
            db,
            "Premium Users",
            UserSegmentType.VIP,
            "High-value subscribers",
        )

        assert result["name"] == "Premium Users"
        assert result["segment_type"] == UserSegmentType.VIP.value

    @pytest.mark.asyncio
    async def test_add_users_to_segment(self, db):
        service = UserSegmentService()

        segment_result = await service.create_user_segment(
            db,
            "Test Segment",
            UserSegmentType.ACTIVE,
        )

        user_ids = [1, 2, 3, 4, 5]
        result = await service.add_users_to_segment(db, segment_result["id"], user_ids)

        assert result["user_count"] == 5

    @pytest.mark.asyncio
    async def test_get_segment_users(self, db):
        service = UserSegmentService()

        segment_result = await service.create_user_segment(
            db,
            "Test Segment",
            UserSegmentType.ACTIVE,
        )

        user_ids = [1, 2, 3]
        await service.add_users_to_segment(db, segment_result["id"], user_ids)

        retrieved_users = await service.get_segment_users(db, segment_result["id"])
        assert len(retrieved_users) == 3


class TestSubscriberService:
    @pytest.mark.asyncio
    async def test_create_subscriber(self, db):
        service = SubscriberService()
        result = await service.create_or_update_subscriber(
            db,
            user_id=1,
            subscription_tier="premium",
        )

        assert result["user_id"] == 1
        assert result["subscription_tier"] == "premium"
        assert result["engagement_score"] == 0.0

    @pytest.mark.asyncio
    async def test_record_subscriber_activity(self, db):
        service = SubscriberService()

        subscriber = await service.create_or_update_subscriber(db, 1)

        result = await service.record_subscriber_activity(
            db,
            subscriber["id"],
            "read",
            content_id=123,
        )

        assert result["activity_type"] == "read"

    @pytest.mark.asyncio
    async def test_calculate_engagement_score(self, db):
        service = SubscriberService()

        subscriber = await service.create_or_update_subscriber(db, 1)

        # Record activities
        await service.record_subscriber_activity(db, subscriber["id"], "login")
        await service.record_subscriber_activity(db, subscriber["id"], "read")
        await service.record_subscriber_activity(db, subscriber["id"], "share")

        score = await service.calculate_engagement_score(db, subscriber["id"])
        assert score >= 0.0
        assert score <= 100.0

    @pytest.mark.asyncio
    async def test_calculate_churn_risk(self, db):
        service = SubscriberService()

        subscriber = await service.create_or_update_subscriber(db, 1, "premium")

        risk = await service.calculate_churn_risk(db, subscriber["id"])
        assert risk >= 0.0
        assert risk <= 1.0

    @pytest.mark.asyncio
    async def test_update_daily_analytics(self, db):
        service = SubscriberService()

        subscriber = await service.create_or_update_subscriber(db, 1)

        await service.record_subscriber_activity(db, subscriber["id"], "read")
        await service.record_subscriber_activity(db, subscriber["id"], "read")

        result = await service.update_daily_analytics(db, subscriber["id"], datetime.utcnow())
        assert result["articles_read"] >= 0


class TestNotificationService:
    @pytest.mark.asyncio
    async def test_send_notification(self, db):
        service = NotificationService()

        result = await service.send_notification(
            db,
            user_id=1,
            channel=NotificationChannel.EMAIL,
            title="Test Notification",
            message="This is a test",
        )

        assert result["user_id"] == 1
        assert result["channel"] == NotificationChannel.EMAIL.value
        assert result["status"] == "pending"

    @pytest.mark.asyncio
    async def test_mark_notification_sent(self, db):
        service = NotificationService()

        notification = await service.send_notification(
            db,
            1,
            NotificationChannel.EMAIL,
            "Test",
            "Message",
        )

        result = await service.mark_as_sent(db, notification["id"])
        assert result["status"] == "sent"

    @pytest.mark.asyncio
    async def test_mark_notification_read(self, db):
        service = NotificationService()

        notification = await service.send_notification(
            db,
            1,
            NotificationChannel.EMAIL,
            "Test",
            "Message",
        )

        result = await service.mark_as_read(db, notification["id"])
        assert result["status"] == "read"


class TestWebhookService:
    @pytest.mark.asyncio
    async def test_create_webhook_endpoint(self, db):
        service = WebhookService()

        result = await service.create_webhook_endpoint(
            db,
            "Test Webhook",
            "https://example.com/webhook",
            ["user.created", "content.published"],
        )

        assert result["name"] == "Test Webhook"
        assert len(result["events"]) == 2
        assert "secret_key" in result

    @pytest.mark.asyncio
    async def test_trigger_webhook(self, db):
        service = WebhookService()

        webhook = await service.create_webhook_endpoint(
            db,
            "Test Webhook",
            "https://example.com/webhook",
            ["user.created"],
        )

        result = await service.trigger_webhook(
            db,
            webhook["id"],
            "user.created",
            {"user_id": 1, "email": "user@example.com"},
        )

        assert result["event_type"] == "user.created"

    @pytest.mark.asyncio
    async def test_generate_signature(self):
        payload = '{"test": "data"}'
        secret = "test_secret"

        signature = WebhookService.generate_signature(payload, secret)
        assert isinstance(signature, str)
        assert len(signature) == 64  # SHA-256 hex is 64 chars

    @pytest.mark.asyncio
    async def test_verify_webhook_signature(self):
        payload = '{"test": "data"}'
        secret = "test_secret"

        signature = WebhookService.generate_signature(payload, secret)
        is_valid = WebhookService.verify_webhook_signature(payload, signature, secret)

        assert is_valid is True

    @pytest.mark.asyncio
    async def test_verify_invalid_signature(self):
        payload = '{"test": "data"}'
        secret = "test_secret"

        is_valid = WebhookService.verify_webhook_signature(payload, "invalid_sig", secret)
        assert is_valid is False


class TestAPIKeyService:
    @pytest.mark.asyncio
    async def test_create_api_key(self, db):
        service = APIKeyService()

        result = await service.create_api_key(
            db,
            user_id=1,
            name="Production API Key",
            permissions=["read:articles", "read:users"],
        )

        assert result["name"] == "Production API Key"
        assert len(result["permissions"]) == 2
        assert "key" in result

    @pytest.mark.asyncio
    async def test_validate_api_key(self, db):
        service = APIKeyService()

        key_result = await service.create_api_key(
            db,
            1,
            "Test Key",
            ["read:articles"],
        )

        result = await service.validate_api_key(db, key_result["key"])
        assert result is not None
        assert result["user_id"] == 1

    @pytest.mark.asyncio
    async def test_validate_invalid_key(self, db):
        service = APIKeyService()

        result = await service.validate_api_key(db, "invalid_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_revoke_api_key(self, db):
        service = APIKeyService()

        key_result = await service.create_api_key(db, 1, "Test Key", [])

        result = await service.revoke_api_key(db, key_result["key_id"])
        assert result["status"] == "revoked"


class TestPersonalizationService:
    @pytest.mark.asyncio
    async def test_create_personalization_profile(self, db):
        service = PersonalizationService()

        result = await service.create_personalization_profile(
            db,
            user_id=1,
            reading_level="advanced",
            timezone="America/New_York",
        )

        assert result["user_id"] == 1
        assert result["reading_level"] == "advanced"
        assert result["timezone"] == "America/New_York"

    @pytest.mark.asyncio
    async def test_update_user_interests(self, db):
        service = PersonalizationService()

        await service.create_personalization_profile(db, 1)

        result = await service.update_user_interests(
            db,
            1,
            ["technology", "artificial-intelligence", "blockchain"],
        )

        assert len(result["keyword_interests"]) == 3

    @pytest.mark.asyncio
    async def test_calculate_personalization_score(self, db):
        service = PersonalizationService()

        await service.create_personalization_profile(db, 1)
        await service.update_user_interests(db, 1, ["tech", "ai"])

        score = await service.calculate_personalization_score(db, 1)
        assert score >= 0.0
        assert score <= 100.0


class TestIntegrationScenarios:
    @pytest.mark.asyncio
    async def test_email_campaign_workflow(self, db):
        email_service = EmailCampaignService()
        segment_service = UserSegmentService()

        # Create segment
        segment = await segment_service.create_user_segment(
            db,
            "Newsletter Recipients",
            UserSegmentType.ACTIVE,
        )

        # Add users to segment
        await segment_service.add_users_to_segment(db, segment["id"], [1, 2, 3])

        # Create campaign
        campaign = await email_service.create_email_campaign(
            db,
            "Weekly Newsletter",
            1,
            "Your Weekly Update",
            "newsletter@example.com",
        )

        # Add recipients
        await email_service.add_campaign_recipients(
            db,
            campaign["id"],
            [
                {"user_id": 1, "email": "user1@example.com"},
                {"user_id": 2, "email": "user2@example.com"},
                {"user_id": 3, "email": "user3@example.com"},
            ],
        )

        # Send campaign
        result = await email_service.send_campaign(db, campaign["id"])
        assert result["status"] == CampaignStatus.SENDING.value

    @pytest.mark.asyncio
    async def test_subscriber_engagement_workflow(self, db):
        subscriber_service = SubscriberService()
        notification_service = NotificationService()

        # Create subscriber
        subscriber = await subscriber_service.create_or_update_subscriber(db, 1, "premium")

        # Record activities
        await subscriber_service.record_subscriber_activity(db, subscriber["id"], "login")
        await subscriber_service.record_subscriber_activity(db, subscriber["id"], "read", 101)
        await subscriber_service.record_subscriber_activity(db, subscriber["id"], "share")

        # Calculate metrics
        engagement = await subscriber_service.calculate_engagement_score(db, subscriber["id"])
        churn_risk = await subscriber_service.calculate_churn_risk(db, subscriber["id"])

        assert engagement > 0.0
        assert 0.0 <= churn_risk <= 1.0

        # Send notification
        notification = await notification_service.send_notification(
            db,
            subscriber["user_id"],
            NotificationChannel.EMAIL,
            "Check out new content",
            "We have new articles for you",
        )

        await notification_service.mark_as_sent(db, notification["id"])
        assert notification["status"] == "pending"

    @pytest.mark.asyncio
    async def test_webhook_integration_workflow(self, db):
        webhook_service = WebhookService()

        # Create webhook endpoint
        webhook = await webhook_service.create_webhook_endpoint(
            db,
            "User Events Webhook",
            "https://example.com/events",
            ["user.created", "user.updated"],
        )

        # Trigger webhook
        log = await webhook_service.trigger_webhook(
            db,
            webhook["id"],
            "user.created",
            {"user_id": 1, "email": "newuser@example.com"},
        )

        assert log["event_type"] == "user.created"
        assert log["webhook_id"] == webhook["id"]

    @pytest.mark.asyncio
    async def test_api_key_validation_workflow(self, db):
        api_key_service = APIKeyService()

        # Create API key
        key = await api_key_service.create_api_key(
            db,
            1,
            "App API Key",
            ["read:articles", "read:users"],
        )

        # Validate API key
        validated = await api_key_service.validate_api_key(db, key["key"])
        assert validated is not None
        assert validated["permissions"] == key["permissions"]

        # Revoke API key
        revoked = await api_key_service.revoke_api_key(db, key["key_id"])
        assert revoked["status"] == "revoked"

        # Try to validate revoked key
        invalid = await api_key_service.validate_api_key(db, key["key"])
        assert invalid is None


class TestEdgeCases:
    @pytest.mark.asyncio
    async def test_handle_nonexistent_campaign(self, db):
        service = EmailCampaignService()

        with pytest.raises(ValueError):
            await service.send_campaign(db, 9999)

    @pytest.mark.asyncio
    async def test_handle_nonexistent_segment(self, db):
        service = UserSegmentService()

        with pytest.raises(ValueError):
            await service.add_users_to_segment(db, 9999, [1, 2, 3])

    @pytest.mark.asyncio
    async def test_negative_subscriber_count(self, db):
        service = UserSegmentService()

        segment = await service.create_user_segment(
            db,
            "Test",
            UserSegmentType.ACTIVE,
        )

        # Adding zero users
        result = await service.add_users_to_segment(db, segment["id"], [])
        assert result["user_count"] == 0

    @pytest.mark.asyncio
    async def test_large_campaign_recipients(self, db):
        service = EmailCampaignService()

        campaign = await service.create_email_campaign(
            db,
            "Large Campaign",
            1,
            "Subject",
            "from@example.com",
        )

        # Add 1000 recipients
        recipients = [
            {"user_id": i, "email": f"user{i}@example.com"}
            for i in range(1000)
        ]

        result = await service.add_campaign_recipients(db, campaign["id"], recipients)
        assert result["recipient_count"] == 1000

    @pytest.mark.asyncio
    async def test_high_engagement_score(self, db):
        service = SubscriberService()

        subscriber = await service.create_or_update_subscriber(db, 1)

        # Record many high-value activities
        for i in range(10):
            await service.record_subscriber_activity(db, subscriber["id"], "subscribe")
            await service.record_subscriber_activity(db, subscriber["id"], "share")

        score = await service.calculate_engagement_score(db, subscriber["id"])
        assert 0.0 <= score <= 100.0

    @pytest.mark.asyncio
    async def test_timezone_support(self, db):
        service = PersonalizationService()

        timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "UTC"]

        for tz in timezones:
            result = await service.create_personalization_profile(db, 1, timezone=tz)
            assert result["timezone"] == tz
