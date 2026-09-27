from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
import secrets
import hmac
import hashlib
from app.models.user_management import (
    EmailTemplate, EmailCampaign, CampaignRecipient, UserSegment,
    UserSegmentMembership, UserPreferenceProfile, NotificationLog,
    SubscriberProfile, SubscriberActivity, SubscriberAnalytics,
    WebhookEndpoint, WebhookLog, APIKey, PersonalizationProfile,
    CampaignStatus, NotificationChannel, UserSegmentType
)


class EmailTemplateService:
    async def create_email_template(
        self,
        db: AsyncSession,
        name: str,
        subject: str,
        body: str,
        template_variables: Dict = None,
    ) -> Dict[str, Any]:
        template = EmailTemplate(
            name=name,
            subject=subject,
            body=body,
            template_variables=template_variables or {},
        )
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return {
            "id": template.id,
            "name": template.name,
            "subject": template.subject,
            "body": template.body,
            "template_variables": template.template_variables,
        }

    async def get_email_template(self, db: AsyncSession, template_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(EmailTemplate).where(EmailTemplate.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            raise ValueError(f"Template {template_id} not found")
        return {
            "id": template.id,
            "name": template.name,
            "subject": template.subject,
            "body": template.body,
        }


class EmailCampaignService:
    async def create_email_campaign(
        self,
        db: AsyncSession,
        name: str,
        template_id: int,
        subject: str,
        from_email: str,
        scheduled_at: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        campaign = EmailCampaign(
            name=name,
            template_id=template_id,
            subject=subject,
            from_email=from_email,
            status=CampaignStatus.DRAFT,
            scheduled_at=scheduled_at,
        )
        db.add(campaign)
        await db.commit()
        await db.refresh(campaign)
        return {
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status.value,
            "scheduled_at": campaign.scheduled_at,
        }

    async def add_campaign_recipients(
        self,
        db: AsyncSession,
        campaign_id: int,
        recipients: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(EmailCampaign).where(EmailCampaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        for recipient in recipients:
            recipient_obj = CampaignRecipient(
                campaign_id=campaign_id,
                user_id=recipient["user_id"],
                email=recipient["email"],
                status="pending",
            )
            db.add(recipient_obj)

        campaign.recipient_count = len(recipients)
        await db.commit()

        return {
            "campaign_id": campaign_id,
            "recipient_count": len(recipients),
        }

    async def update_campaign_metrics(
        self,
        db: AsyncSession,
        campaign_id: int,
        sent_count: int = 0,
        open_count: int = 0,
        click_count: int = 0,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(EmailCampaign).where(EmailCampaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        campaign.sent_count = sent_count
        campaign.open_count = open_count
        campaign.click_count = click_count

        if campaign.recipient_count > 0:
            campaign.open_rate = (open_count / campaign.recipient_count) * 100
            campaign.click_rate = (click_count / campaign.recipient_count) * 100

        await db.commit()
        await db.refresh(campaign)

        return {
            "campaign_id": campaign_id,
            "open_rate": campaign.open_rate,
            "click_rate": campaign.click_rate,
        }

    async def send_campaign(self, db: AsyncSession, campaign_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(EmailCampaign).where(EmailCampaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        campaign.status = CampaignStatus.SENDING
        campaign.sent_at = datetime.utcnow()
        await db.commit()

        return {
            "campaign_id": campaign_id,
            "status": campaign.status.value,
            "sent_at": campaign.sent_at,
        }


class UserSegmentService:
    async def create_user_segment(
        self,
        db: AsyncSession,
        name: str,
        segment_type: UserSegmentType,
        description: Optional[str] = None,
        filter_criteria: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        segment = UserSegment(
            name=name,
            segment_type=segment_type,
            description=description,
            filter_criteria=filter_criteria or {},
        )
        db.add(segment)
        await db.commit()
        await db.refresh(segment)
        return {
            "id": segment.id,
            "name": segment.name,
            "segment_type": segment.segment_type.value,
            "user_count": segment.user_count,
        }

    async def add_users_to_segment(
        self,
        db: AsyncSession,
        segment_id: int,
        user_ids: List[int],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(UserSegment).where(UserSegment.id == segment_id)
        )
        segment = result.scalar_one_or_none()
        if not segment:
            raise ValueError(f"Segment {segment_id} not found")

        for user_id in user_ids:
            membership = UserSegmentMembership(
                segment_id=segment_id,
                user_id=user_id,
            )
            db.add(membership)

        segment.user_count = len(user_ids)
        await db.commit()

        return {
            "segment_id": segment_id,
            "user_count": len(user_ids),
        }

    async def get_segment_users(
        self,
        db: AsyncSession,
        segment_id: int,
    ) -> List[int]:
        result = await db.execute(
            select(UserSegmentMembership.user_id).where(
                UserSegmentMembership.segment_id == segment_id
            )
        )
        return [row[0] for row in result.all()]


class SubscriberService:
    async def create_or_update_subscriber(
        self,
        db: AsyncSession,
        user_id: int,
        subscription_tier: str = "free",
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(SubscriberProfile).where(SubscriberProfile.user_id == user_id)
        )
        subscriber = result.scalar_one_or_none()

        if subscriber:
            subscriber.subscription_tier = subscription_tier
            subscriber.updated_at = datetime.utcnow()
        else:
            subscriber = SubscriberProfile(
                user_id=user_id,
                subscription_tier=subscription_tier,
            )
            db.add(subscriber)

        await db.commit()
        await db.refresh(subscriber)

        return {
            "id": subscriber.id,
            "user_id": subscriber.user_id,
            "subscription_tier": subscriber.subscription_tier,
            "engagement_score": subscriber.engagement_score,
            "churn_risk_score": subscriber.churn_risk_score,
        }

    async def record_subscriber_activity(
        self,
        db: AsyncSession,
        subscriber_id: int,
        activity_type: str,
        content_id: Optional[int] = None,
        metadata: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        activity = SubscriberActivity(
            subscriber_id=subscriber_id,
            activity_type=activity_type,
            content_id=content_id,
            metadata=metadata or {},
        )
        db.add(activity)

        # Update subscriber last activity
        result = await db.execute(
            select(SubscriberProfile).where(SubscriberProfile.id == subscriber_id)
        )
        subscriber = result.scalar_one_or_none()
        if subscriber:
            subscriber.last_activity_at = datetime.utcnow()
            if activity_type == "read":
                subscriber.articles_read += 1

        await db.commit()

        return {
            "activity_id": activity.id,
            "activity_type": activity_type,
            "recorded_at": activity.created_at,
        }

    async def calculate_engagement_score(self, db: AsyncSession, subscriber_id: int) -> float:
        result = await db.execute(
            select(SubscriberActivity).where(
                SubscriberActivity.subscriber_id == subscriber_id
            )
        )
        activities = result.scalars().all()

        score = 0.0
        activity_weights = {
            "login": 5.0,
            "read": 20.0,
            "share": 30.0,
            "comment": 25.0,
            "subscribe": 50.0,
        }

        for activity in activities:
            score += activity_weights.get(activity.activity_type, 0)

        # Decay score based on activity age
        now = datetime.utcnow()
        for activity in activities:
            days_old = (now - activity.created_at).days
            decay_factor = 0.95 ** days_old
            score *= decay_factor

        return min(score, 100.0)

    async def calculate_churn_risk(self, db: AsyncSession, subscriber_id: int) -> float:
        result = await db.execute(
            select(SubscriberProfile).where(SubscriberProfile.id == subscriber_id)
        )
        subscriber = result.scalar_one_or_none()
        if not subscriber:
            return 0.0

        now = datetime.utcnow()
        days_since_activity = (now - subscriber.last_activity_at).days

        # Base churn risk
        churn_risk = 0.0

        # Increase risk for inactivity
        if days_since_activity > 30:
            churn_risk += 0.3
        elif days_since_activity > 14:
            churn_risk += 0.15

        # Decrease risk for high engagement
        if subscriber.engagement_score > 70:
            churn_risk -= 0.2
        elif subscriber.engagement_score < 30:
            churn_risk += 0.2

        # Premium subscribers have lower churn risk
        if subscriber.subscription_tier == "premium":
            churn_risk -= 0.1

        return max(0.0, min(churn_risk, 1.0))

    async def update_daily_analytics(
        self,
        db: AsyncSession,
        subscriber_id: int,
        date: datetime,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(SubscriberActivity).where(
                and_(
                    SubscriberActivity.subscriber_id == subscriber_id,
                    func.date(SubscriberActivity.created_at) == date.date(),
                )
            )
        )
        activities = result.scalars().all()

        articles_read = sum(1 for a in activities if a.activity_type == "read")
        session_count = len(set(a.created_at for a in activities))

        engagement_score = await self.calculate_engagement_score(db, subscriber_id)

        analytics = SubscriberAnalytics(
            subscriber_id=subscriber_id,
            date=date,
            daily_active=len(activities) > 0,
            articles_read=articles_read,
            session_count=session_count,
            engagement_score=engagement_score,
        )
        db.add(analytics)
        await db.commit()

        return {
            "subscriber_id": subscriber_id,
            "date": date,
            "articles_read": articles_read,
            "engagement_score": engagement_score,
        }


class NotificationService:
    async def send_notification(
        self,
        db: AsyncSession,
        user_id: int,
        channel: NotificationChannel,
        title: str,
        message: str,
    ) -> Dict[str, Any]:
        notification = NotificationLog(
            user_id=user_id,
            channel=channel,
            title=title,
            message=message,
            status="pending",
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        return {
            "id": notification.id,
            "user_id": user_id,
            "channel": notification.channel.value,
            "status": notification.status,
        }

    async def mark_as_sent(self, db: AsyncSession, notification_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(NotificationLog).where(NotificationLog.id == notification_id)
        )
        notification = result.scalar_one_or_none()
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")

        notification.status = "sent"
        notification.sent_at = datetime.utcnow()
        await db.commit()

        return {
            "notification_id": notification_id,
            "status": "sent",
        }

    async def mark_as_read(self, db: AsyncSession, notification_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(NotificationLog).where(NotificationLog.id == notification_id)
        )
        notification = result.scalar_one_or_none()
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")

        notification.status = "read"
        notification.read_at = datetime.utcnow()
        await db.commit()

        return {
            "notification_id": notification_id,
            "status": "read",
        }


class WebhookService:
    async def create_webhook_endpoint(
        self,
        db: AsyncSession,
        name: str,
        url: str,
        events: List[str],
    ) -> Dict[str, Any]:
        secret_key = secrets.token_urlsafe(32)

        webhook = WebhookEndpoint(
            name=name,
            url=url,
            events=events,
            secret_key=secret_key,
        )
        db.add(webhook)
        await db.commit()
        await db.refresh(webhook)

        return {
            "id": webhook.id,
            "name": webhook.name,
            "url": webhook.url,
            "events": webhook.events,
            "secret_key": secret_key,
        }

    async def trigger_webhook(
        self,
        db: AsyncSession,
        webhook_id: int,
        event_type: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(WebhookEndpoint).where(WebhookEndpoint.id == webhook_id)
        )
        webhook = result.scalar_one_or_none()
        if not webhook:
            raise ValueError(f"Webhook {webhook_id} not found")

        webhook.last_triggered_at = datetime.utcnow()

        log = WebhookLog(
            webhook_id=webhook_id,
            event_type=event_type,
            payload=payload,
        )
        db.add(log)
        await db.commit()

        return {
            "log_id": log.id,
            "webhook_id": webhook_id,
            "event_type": event_type,
        }

    @staticmethod
    def generate_signature(payload: str, secret_key: str) -> str:
        return hmac.new(
            secret_key.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def verify_webhook_signature(payload: str, signature: str, secret_key: str) -> bool:
        expected_signature = WebhookService.generate_signature(payload, secret_key)
        return hmac.compare_digest(signature, expected_signature)


class APIKeyService:
    async def create_api_key(
        self,
        db: AsyncSession,
        user_id: int,
        name: str,
        permissions: List[str],
    ) -> Dict[str, Any]:
        key = secrets.token_urlsafe(32)

        api_key = APIKey(
            user_id=user_id,
            key=key,
            name=name,
            permissions=permissions,
        )
        db.add(api_key)
        await db.commit()

        return {
            "key_id": api_key.id,
            "key": key,
            "name": name,
            "permissions": permissions,
        }

    async def validate_api_key(self, db: AsyncSession, key: str) -> Optional[Dict[str, Any]]:
        result = await db.execute(
            select(APIKey).where(and_(APIKey.key == key, APIKey.is_active == True))
        )
        api_key = result.scalar_one_or_none()
        if not api_key:
            return None

        api_key.last_used_at = datetime.utcnow()
        await db.commit()

        return {
            "key_id": api_key.id,
            "user_id": api_key.user_id,
            "permissions": api_key.permissions,
        }

    async def revoke_api_key(self, db: AsyncSession, key_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(APIKey).where(APIKey.id == key_id)
        )
        api_key = result.scalar_one_or_none()
        if not api_key:
            raise ValueError(f"API Key {key_id} not found")

        api_key.is_active = False
        await db.commit()

        return {
            "key_id": key_id,
            "status": "revoked",
        }


class PersonalizationService:
    async def create_personalization_profile(
        self,
        db: AsyncSession,
        user_id: int,
        reading_level: str = "intermediate",
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if profile:
            profile.reading_level = reading_level
            profile.timezone = timezone
        else:
            profile = PersonalizationProfile(
                user_id=user_id,
                reading_level=reading_level,
                timezone=timezone,
            )
            db.add(profile)

        await db.commit()
        await db.refresh(profile)

        return {
            "user_id": profile.user_id,
            "reading_level": profile.reading_level,
            "timezone": profile.timezone,
        }

    async def update_user_interests(
        self,
        db: AsyncSession,
        user_id: int,
        keywords: List[str],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            raise ValueError(f"Profile for user {user_id} not found")

        profile.keyword_interests = keywords
        profile.last_personalization_update = datetime.utcnow()
        await db.commit()

        return {
            "user_id": user_id,
            "keyword_interests": keywords,
        }

    async def calculate_personalization_score(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> float:
        result = await db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            return 0.0

        score = 50.0  # Base score

        # Increase score for profile completeness
        if profile.reading_level:
            score += 10.0
        if profile.keyword_interests:
            score += 15.0
        if profile.author_preferences:
            score += 10.0
        if profile.content_type_preferences:
            score += 10.0
        if profile.timezone:
            score += 5.0

        profile.personalization_score = min(score, 100.0)
        await db.commit()

        return profile.personalization_score
