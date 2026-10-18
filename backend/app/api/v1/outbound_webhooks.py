"""Outbound webhook endpoints for the signed-in user's endpoints."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.outbound_webhook_service import (
    EVENT_CATALOG,
    MAX_EVENTS_PER_ENDPOINT,
    OutboundWebhookService,
    WebhookError,
    delivery_view,
    webhook_view,
)

router = APIRouter(prefix="/outbound-webhooks", tags=["outbound-webhooks"])


class WebhookCreate(BaseModel):
    url: str = Field(..., max_length=500)
    description: Optional[str] = Field(None, max_length=255)
    events: List[str] = Field(..., min_length=1, max_length=MAX_EVENTS_PER_ENDPOINT)


class WebhookUpdate(BaseModel):
    url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, max_length=255)
    events: Optional[List[str]] = Field(None, min_length=1, max_length=MAX_EVENTS_PER_ENDPOINT)
    is_active: Optional[bool] = None


class WebhookOut(BaseModel):
    id: int
    url: str
    description: Optional[str]
    events: List[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class WebhookCreated(WebhookOut):
    """Returned once, on creation. The signing secret is never shown again."""

    secret: str


class SecretOut(BaseModel):
    """Returned once, on rotation."""

    secret: str


class DeliveryOut(BaseModel):
    id: int
    webhook_id: int
    event: str
    status: str
    response_status: Optional[int]
    error: Optional[str]
    created_at: Optional[datetime]


class EventOut(BaseModel):
    event: str
    description: str


def _raise(error: WebhookError) -> None:
    raise HTTPException(status_code=error.status_code, detail=error.message)


@router.get("/events", response_model=List[EventOut])
async def list_events(_user: User = Depends(get_current_user)):
    """Events an endpoint can subscribe to."""
    return [{"event": name, "description": text} for name, text in EVENT_CATALOG.items()]


@router.post("", response_model=WebhookCreated, status_code=status.HTTP_201_CREATED)
async def create_webhook(
    payload: WebhookCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    try:
        webhook, secret = await OutboundWebhookService(session, user.id).create(
            payload.url, payload.description, payload.events,
        )
    except WebhookError as error:
        _raise(error)
    return {**webhook_view(webhook), "secret": secret}


@router.get("", response_model=List[WebhookOut])
async def list_webhooks(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    webhooks = await OutboundWebhookService(session, user.id).list()
    return [webhook_view(webhook) for webhook in webhooks]


@router.get("/{webhook_id}", response_model=WebhookOut)
async def get_webhook(webhook_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    try:
        webhook = await OutboundWebhookService(session, user.id).get(webhook_id)
    except WebhookError as error:
        _raise(error)
    return webhook_view(webhook)


@router.patch("/{webhook_id}", response_model=WebhookOut)
async def update_webhook(
    webhook_id: int,
    payload: WebhookUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="Provide at least one field to change")
    try:
        webhook = await OutboundWebhookService(session, user.id).update(webhook_id, changes)
    except WebhookError as error:
        _raise(error)
    return webhook_view(webhook)


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook(webhook_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    try:
        await OutboundWebhookService(session, user.id).delete(webhook_id)
    except WebhookError as error:
        _raise(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{webhook_id}/rotate-secret", response_model=SecretOut)
async def rotate_secret(webhook_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    try:
        secret = await OutboundWebhookService(session, user.id).rotate_secret(webhook_id)
    except WebhookError as error:
        _raise(error)
    return {"secret": secret}


@router.post("/{webhook_id}/test", response_model=DeliveryOut)
async def send_test_event(webhook_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Send a signed test event now and return the recorded outcome."""
    try:
        delivery = await OutboundWebhookService(session, user.id).send_test(webhook_id)
    except WebhookError as error:
        _raise(error)
    return delivery_view(delivery)


@router.get("/{webhook_id}/deliveries", response_model=List[DeliveryOut])
async def list_deliveries(
    webhook_id: int,
    limit: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    try:
        deliveries = await OutboundWebhookService(session, user.id).list_deliveries(webhook_id, limit)
    except WebhookError as error:
        _raise(error)
    return [delivery_view(delivery) for delivery in deliveries]
