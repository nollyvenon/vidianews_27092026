"""Outbound webhooks: registration, signed delivery and delivery history.

Every delivery is signed with the endpoint's secret:
``X-Webhook-Signature: t=<unix time>,v1=<hex HMAC-SHA256 of "<t>.<body>">``.
Receivers should reject timestamps that are too old and compare signatures in constant time.

Endpoint URLs must be HTTPS and must not resolve to private, loopback, link-local or reserved
addresses; the check runs at registration and again before every delivery.
"""

import asyncio
import hashlib
import hmac
import ipaddress
import json
import secrets
import socket
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlsplit

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import decrypt_value, encrypt_value
from app.models.outbound_webhooks import OutboundWebhook, OutboundWebhookDelivery
from app.utils.logger import logger

EVENT_CATALOG: Dict[str, str] = {
    "content.published": "A content item was published",
    "content.updated": "A content item was edited",
    "content.deleted": "A content item was deleted",
    "user.created": "A user account was created",
    "subscription.changed": "A subscription tier or status changed",
    "payment.completed": "A payment completed",
    "webhook.test": "Test event sent from the webhook settings",
}

DELIVERY_TIMEOUT_SECONDS = 10.0
MAX_URL_LENGTH = 500
MAX_EVENTS_PER_ENDPOINT = len(EVENT_CATALOG)


class WebhookError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


async def _resolve_addresses(hostname: str) -> List[str]:
    """Every IP address the host resolves to."""
    loop = asyncio.get_running_loop()
    try:
        infos = await loop.getaddrinfo(hostname, 443, type=3)
    except socket.gaierror as exc:
        raise WebhookError("The webhook host cannot be resolved", 422) from exc
    return sorted({info[4][0] for info in infos})


def _is_public(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    return not (
        ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
        or ip.is_multicast or ip.is_unspecified
    )


async def validate_endpoint_url(url: str) -> str:
    """Raise WebhookError unless ``url`` is an HTTPS URL on a public host. Returns the normalized URL."""
    if not url or len(url) > MAX_URL_LENGTH:
        raise WebhookError("Endpoint URL is required and must be at most 500 characters", 422)
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise WebhookError("Endpoint URL must use HTTPS", 422)
    if not parts.hostname:
        raise WebhookError("Endpoint URL must include a host name", 422)
    if parts.username or parts.password:
        raise WebhookError("Endpoint URL must not contain credentials", 422)
    if parts.port not in (None, 443):
        raise WebhookError("Endpoint URL must use the default HTTPS port", 422)

    try:
        ipaddress.ip_address(parts.hostname)
        addresses = [parts.hostname]
    except ValueError:
        addresses = await _resolve_addresses(parts.hostname)
    if not addresses or not all(_is_public(address) for address in addresses):
        raise WebhookError("Endpoint URL must not point to a private or reserved address", 422)
    return url


def validate_events(events: Sequence[str]) -> List[str]:
    if not events:
        raise WebhookError("Select at least one event", 422)
    unknown = sorted(set(events) - set(EVENT_CATALOG))
    if unknown:
        raise WebhookError(f"Unknown event(s): {', '.join(unknown)}", 422)
    return sorted(set(events))


def sign_payload(secret: str, timestamp: int, body: bytes) -> str:
    message = f"{timestamp}.".encode() + body
    digest = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def _event_body(event: str, payload: Dict[str, Any]) -> bytes:
    document = {
        "event": event,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "data": payload,
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":"), default=str).encode()


def webhook_view(webhook: OutboundWebhook) -> Dict[str, Any]:
    return {
        "id": webhook.id,
        "url": webhook.url,
        "description": webhook.description,
        "events": list(webhook.events or []),
        "is_active": bool(webhook.is_active),
        "created_at": webhook.created_at,
        "updated_at": webhook.updated_at,
    }


def delivery_view(delivery: OutboundWebhookDelivery) -> Dict[str, Any]:
    return {
        "id": delivery.id,
        "webhook_id": delivery.webhook_id,
        "event": delivery.event,
        "status": delivery.status,
        "response_status": delivery.response_status,
        "error": delivery.error,
        "created_at": delivery.created_at,
    }


class OutboundWebhookService:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def _owned(self, webhook_id: int) -> OutboundWebhook:
        webhook = (await self.session.execute(
            select(OutboundWebhook).where(
                OutboundWebhook.id == webhook_id,
                OutboundWebhook.user_id == self.user_id,
            )
        )).scalar_one_or_none()
        if webhook is None:
            raise WebhookError("Webhook not found", 404)
        return webhook

    async def create(self, url: str, description: Optional[str], events: Sequence[str]) -> Tuple[OutboundWebhook, str]:
        url = await validate_endpoint_url(url)
        events = validate_events(events)
        secret = secrets.token_urlsafe(32)
        webhook = OutboundWebhook(
            user_id=self.user_id,
            url=url,
            description=(description or None),
            events=events,
            secret_encrypted=encrypt_value(secret),
            is_active=True,
        )
        self.session.add(webhook)
        await self.session.commit()
        await self.session.refresh(webhook)
        logger.info(f"Outbound webhook {webhook.id} created by user {self.user_id}")
        return webhook, secret

    async def list(self) -> List[OutboundWebhook]:
        result = await self.session.execute(
            select(OutboundWebhook)
            .where(OutboundWebhook.user_id == self.user_id)
            .order_by(OutboundWebhook.id)
        )
        return list(result.scalars().all())

    async def get(self, webhook_id: int) -> OutboundWebhook:
        return await self._owned(webhook_id)

    async def update(self, webhook_id: int, changes: Dict[str, Any]) -> OutboundWebhook:
        webhook = await self._owned(webhook_id)
        if "url" in changes and changes["url"] is not None:
            webhook.url = await validate_endpoint_url(changes["url"])
        if "events" in changes and changes["events"] is not None:
            webhook.events = validate_events(changes["events"])
        if "description" in changes:
            webhook.description = changes["description"] or None
        if "is_active" in changes and changes["is_active"] is not None:
            webhook.is_active = bool(changes["is_active"])
        await self.session.commit()
        await self.session.refresh(webhook)
        return webhook

    async def delete(self, webhook_id: int) -> None:
        webhook = await self._owned(webhook_id)
        await self.session.delete(webhook)
        await self.session.commit()

    async def rotate_secret(self, webhook_id: int) -> str:
        webhook = await self._owned(webhook_id)
        secret = secrets.token_urlsafe(32)
        webhook.secret_encrypted = encrypt_value(secret)
        await self.session.commit()
        return secret

    async def list_deliveries(self, webhook_id: int, limit: int = 50) -> List[OutboundWebhookDelivery]:
        await self._owned(webhook_id)
        result = await self.session.execute(
            select(OutboundWebhookDelivery)
            .where(OutboundWebhookDelivery.webhook_id == webhook_id)
            .order_by(OutboundWebhookDelivery.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def send_test(self, webhook_id: int) -> OutboundWebhookDelivery:
        webhook = await self._owned(webhook_id)
        return await deliver(
            self.session, webhook, "webhook.test",
            {"message": "This is a test event from your webhook settings."},
        )

    async def dispatch(self, event: str, payload: Dict[str, Any]) -> List[OutboundWebhookDelivery]:
        """Deliver ``event`` to every active endpoint of this user subscribed to it."""
        if event not in EVENT_CATALOG:
            raise WebhookError(f"Unknown event: {event}", 422)
        result = await self.session.execute(
            select(OutboundWebhook).where(
                OutboundWebhook.user_id == self.user_id,
                OutboundWebhook.is_active.is_(True),
            )
        )
        deliveries = []
        for webhook in result.scalars().all():
            if event in (webhook.events or []):
                deliveries.append(await deliver(self.session, webhook, event, payload))
        return deliveries


async def deliver(
    session: AsyncSession,
    webhook: OutboundWebhook,
    event: str,
    payload: Dict[str, Any],
) -> OutboundWebhookDelivery:
    """One signed POST to the endpoint. Records the outcome whether or not delivery succeeded."""
    body = _event_body(event, payload)
    status: str
    response_status: Optional[int] = None
    error: Optional[str] = None
    try:
        url = await validate_endpoint_url(webhook.url)
        timestamp = int(time.time())
        secret = decrypt_value(webhook.secret_encrypted)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "AetherCMS-Webhooks/1.0",
            "X-Webhook-Event": event,
            "X-Webhook-Signature": sign_payload(secret, timestamp, body),
        }
        async with httpx.AsyncClient(timeout=DELIVERY_TIMEOUT_SECONDS, follow_redirects=False) as client:
            response = await client.post(url, content=body, headers=headers)
        response_status = response.status_code
        status = "delivered" if 200 <= response.status_code < 300 else "failed"
        if status == "failed":
            error = f"Endpoint answered HTTP {response.status_code}"
    except WebhookError as exc:
        status, error = "failed", exc.message
    except httpx.HTTPError as exc:
        status, error = "failed", f"Request failed: {type(exc).__name__}"

    delivery = OutboundWebhookDelivery(
        webhook_id=webhook.id,
        event=event,
        payload=payload,
        status=status,
        response_status=response_status,
        error=error,
    )
    session.add(delivery)
    await session.commit()
    await session.refresh(delivery)
    logger.info(f"Outbound webhook {webhook.id} event {event}: {status}")
    return delivery
