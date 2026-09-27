from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.db import get_db
from app.services.user_management_service import (
    EmailTemplateService, EmailCampaignService, UserSegmentService,
    SubscriberService, NotificationService, WebhookService,
    APIKeyService, PersonalizationService
)

# Routers
email_router = APIRouter(prefix="/emails", tags=["Email Management"])
segment_router = APIRouter(prefix="/segments", tags=["User Segmentation"])
subscriber_router = APIRouter(prefix="/subscribers", tags=["Subscriber Management"])
notification_router = APIRouter(prefix="/notifications", tags=["Notifications"])
webhook_router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
api_key_router = APIRouter(prefix="/api-keys", tags=["API Keys"])
personalization_router = APIRouter(prefix="/personalization", tags=["Personalization"])


# Pydantic Models
class EmailTemplateRequest(BaseModel):
    name: str
    subject: str
    body: str
    template_variables: Optional[Dict] = None


class EmailCampaignRequest(BaseModel):
    name: str
    template_id: int
    subject: str
    from_email: str
    scheduled_at: Optional[datetime] = None


class CampaignRecipientRequest(BaseModel):
    campaign_id: int
    recipients: List[Dict[str, Any]]


class UserSegmentRequest(BaseModel):
    name: str
    segment_type: str
    description: Optional[str] = None
    filter_criteria: Optional[Dict] = None


class AddSegmentUsersRequest(BaseModel):
    user_ids: List[int]


class SubscriberRequest(BaseModel):
    user_id: int
    subscription_tier: str = "free"


class SubscriberActivityRequest(BaseModel):
    subscriber_id: int
    activity_type: str
    content_id: Optional[int] = None
    metadata: Optional[Dict] = None


class NotificationRequest(BaseModel):
    user_id: int
    channel: str
    title: str
    message: str


class WebhookEndpointRequest(BaseModel):
    name: str
    url: str
    events: List[str]


class WebhookTriggerRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]


class APIKeyRequest(BaseModel):
    name: str
    permissions: List[str]


class PersonalizationProfileRequest(BaseModel):
    user_id: int
    reading_level: str = "intermediate"
    timezone: str = "UTC"


class UserInterestsRequest(BaseModel):
    user_id: int
    keywords: List[str]


# Email Template Endpoints
@email_router.post("/templates", status_code=status.HTTP_201_CREATED)
async def create_email_template(
    request: EmailTemplateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = EmailTemplateService()
    result = await service.create_email_template(
        db,
        request.name,
        request.subject,
        request.body,
        request.template_variables,
    )
    return result


@email_router.get("/templates/{template_id}")
async def get_email_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = EmailTemplateService()
    try:
        result = await service.get_email_template(db, template_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Email Campaign Endpoints
@email_router.post("/campaigns", status_code=status.HTTP_201_CREATED)
async def create_email_campaign(
    request: EmailCampaignRequest,
    db: AsyncSession = Depends(get_db),
):
    service = EmailCampaignService()
    result = await service.create_email_campaign(
        db,
        request.name,
        request.template_id,
        request.subject,
        request.from_email,
        request.scheduled_at,
    )
    return result


@email_router.post("/campaigns/recipients")
async def add_campaign_recipients(
    request: CampaignRecipientRequest,
    db: AsyncSession = Depends(get_db),
):
    service = EmailCampaignService()
    try:
        result = await service.add_campaign_recipients(
            db,
            request.campaign_id,
            request.recipients,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@email_router.patch("/campaigns/{campaign_id}/metrics")
async def update_campaign_metrics(
    campaign_id: int,
    sent_count: int = 0,
    open_count: int = 0,
    click_count: int = 0,
    db: AsyncSession = Depends(get_db),
):
    service = EmailCampaignService()
    try:
        result = await service.update_campaign_metrics(
            db,
            campaign_id,
            sent_count,
            open_count,
            click_count,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@email_router.post("/campaigns/{campaign_id}/send")
async def send_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = EmailCampaignService()
    try:
        result = await service.send_campaign(db, campaign_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# User Segment Endpoints
@segment_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_segment(
    request: UserSegmentRequest,
    db: AsyncSession = Depends(get_db),
):
    service = UserSegmentService()
    result = await service.create_user_segment(
        db,
        request.name,
        request.segment_type,
        request.description,
        request.filter_criteria,
    )
    return result


@segment_router.post("/{segment_id}/users")
async def add_users_to_segment(
    segment_id: int,
    request: AddSegmentUsersRequest,
    db: AsyncSession = Depends(get_db),
):
    service = UserSegmentService()
    try:
        result = await service.add_users_to_segment(
            db,
            segment_id,
            request.user_ids,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@segment_router.get("/{segment_id}/users")
async def get_segment_users(
    segment_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = UserSegmentService()
    user_ids = await service.get_segment_users(db, segment_id)
    return {"segment_id": segment_id, "user_ids": user_ids}


# Subscriber Endpoints
@subscriber_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_subscriber(
    request: SubscriberRequest,
    db: AsyncSession = Depends(get_db),
):
    service = SubscriberService()
    result = await service.create_or_update_subscriber(
        db,
        request.user_id,
        request.subscription_tier,
    )
    return result


@subscriber_router.post("/activity")
async def record_subscriber_activity(
    request: SubscriberActivityRequest,
    db: AsyncSession = Depends(get_db),
):
    service = SubscriberService()
    result = await service.record_subscriber_activity(
        db,
        request.subscriber_id,
        request.activity_type,
        request.content_id,
        request.metadata,
    )
    return result


@subscriber_router.get("/{subscriber_id}/engagement-score")
async def get_engagement_score(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = SubscriberService()
    score = await service.calculate_engagement_score(db, subscriber_id)
    return {"subscriber_id": subscriber_id, "engagement_score": score}


@subscriber_router.get("/{subscriber_id}/churn-risk")
async def get_churn_risk(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = SubscriberService()
    risk = await service.calculate_churn_risk(db, subscriber_id)
    return {"subscriber_id": subscriber_id, "churn_risk_score": risk}


@subscriber_router.post("/{subscriber_id}/analytics/daily")
async def update_daily_analytics(
    subscriber_id: int,
    date: datetime,
    db: AsyncSession = Depends(get_db),
):
    service = SubscriberService()
    result = await service.update_daily_analytics(db, subscriber_id, date)
    return result


# Notification Endpoints
@notification_router.post("/", status_code=status.HTTP_201_CREATED)
async def send_notification(
    request: NotificationRequest,
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService()
    result = await service.send_notification(
        db,
        request.user_id,
        request.channel,
        request.title,
        request.message,
    )
    return result


@notification_router.patch("/{notification_id}/sent")
async def mark_notification_sent(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService()
    try:
        result = await service.mark_as_sent(db, notification_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@notification_router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService()
    try:
        result = await service.mark_as_read(db, notification_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Webhook Endpoints
@webhook_router.post("/endpoints", status_code=status.HTTP_201_CREATED)
async def create_webhook_endpoint(
    request: WebhookEndpointRequest,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService()
    result = await service.create_webhook_endpoint(
        db,
        request.name,
        request.url,
        request.events,
    )
    return result


@webhook_router.post("/{webhook_id}/trigger")
async def trigger_webhook(
    webhook_id: int,
    request: WebhookTriggerRequest,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService()
    try:
        result = await service.trigger_webhook(
            db,
            webhook_id,
            request.event_type,
            request.payload,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# API Key Endpoints
@api_key_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: APIKeyRequest,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = APIKeyService()
    result = await service.create_api_key(
        db,
        user_id,
        request.name,
        request.permissions,
    )
    return result


@api_key_router.get("/validate")
async def validate_api_key(
    key: str,
    db: AsyncSession = Depends(get_db),
):
    service = APIKeyService()
    result = await service.validate_api_key(db, key)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return result


@api_key_router.delete("/{key_id}")
async def revoke_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = APIKeyService()
    try:
        result = await service.revoke_api_key(db, key_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Personalization Endpoints
@personalization_router.post("/profiles", status_code=status.HTTP_201_CREATED)
async def create_personalization_profile(
    request: PersonalizationProfileRequest,
    db: AsyncSession = Depends(get_db),
):
    service = PersonalizationService()
    result = await service.create_personalization_profile(
        db,
        request.user_id,
        request.reading_level,
        request.timezone,
    )
    return result


@personalization_router.post("/interests")
async def update_user_interests(
    request: UserInterestsRequest,
    db: AsyncSession = Depends(get_db),
):
    service = PersonalizationService()
    try:
        result = await service.update_user_interests(
            db,
            request.user_id,
            request.keywords,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@personalization_router.get("/{user_id}/score")
async def get_personalization_score(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = PersonalizationService()
    score = await service.calculate_personalization_score(db, user_id)
    return {"user_id": user_id, "personalization_score": score}


# Include routers in main app (in main.py)
def include_user_management_routers(app):
    app.include_router(email_router, prefix="/api/v1")
    app.include_router(segment_router, prefix="/api/v1")
    app.include_router(subscriber_router, prefix="/api/v1")
    app.include_router(notification_router, prefix="/api/v1")
    app.include_router(webhook_router, prefix="/api/v1")
    app.include_router(api_key_router, prefix="/api/v1")
    app.include_router(personalization_router, prefix="/api/v1")
