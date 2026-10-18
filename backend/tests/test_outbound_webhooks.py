"""Outbound webhooks: registration rules, ownership, signed delivery and the delivery log."""

import httpx
import pytest
import respx
from sqlalchemy import select

from app.core.crypto import decrypt_value
from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.outbound_webhooks import OutboundWebhook
from app.models.user import User
from app.services import outbound_webhook_service as svc
from app.services.outbound_webhook_service import OutboundWebhookService, sign_payload

PUBLIC_IP = "93.184.216.34"
PRIVATE_IP = "10.0.0.5"
HOOK = "https://hooks.example.com/receive"


@pytest.fixture
async def client(test_session):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as http:
        yield http
    app.dependency_overrides.clear()


@pytest.fixture
def public_dns(monkeypatch):
    async def resolve(hostname):
        return [PUBLIC_IP]

    monkeypatch.setattr(svc, "_resolve_addresses", resolve)


async def _user(session, email):
    user = User(email=email, password_hash=hash_password("Passw0rd!long"), first_name="T", last_name="U", status="active")
    session.add(user)
    await session.commit()
    return user


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


@pytest.fixture
async def owner(session):
    return await _user(session, "owner@example.com")


@pytest.fixture
async def other(session):
    return await _user(session, "other@example.com")


async def _create(client, headers, url=HOOK, events=("content.published",), description="Main"):
    return await client.post(
        "/api/v1/outbound-webhooks",
        json={"url": url, "events": list(events), "description": description},
        headers=headers,
    )


class TestCatalogAndAccess:
    @pytest.mark.asyncio
    async def test_event_catalog_lists_supported_events(self, client, owner):
        response = await client.get("/api/v1/outbound-webhooks/events", headers=_headers(owner))
        assert response.status_code == 200
        names = [item["event"] for item in response.json()]
        assert "content.published" in names and "webhook.test" in names

    @pytest.mark.asyncio
    async def test_anonymous_request_is_rejected(self, client):
        assert (await client.get("/api/v1/outbound-webhooks")).status_code == 401


class TestRegistrationRules:
    @pytest.mark.asyncio
    async def test_create_returns_secret_once_and_list_hides_it(self, client, owner, public_dns, session):
        created = await _create(client, _headers(owner))
        assert created.status_code == 201
        body = created.json()
        assert body["secret"] and body["events"] == ["content.published"] and body["is_active"] is True

        listing = (await client.get("/api/v1/outbound-webhooks", headers=_headers(owner))).json()
        assert len(listing) == 1 and "secret" not in listing[0]

        row = (await session.execute(select(OutboundWebhook))).scalar_one()
        assert row.secret_encrypted != body["secret"]
        assert decrypt_value(row.secret_encrypted) == body["secret"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("url", [
        "http://hooks.example.com/receive",
        "https://user:pass@hooks.example.com/receive",
        "https://hooks.example.com:8443/receive",
        "https:///receive",
        "ftp://hooks.example.com/receive",
    ])
    async def test_unsafe_urls_are_rejected(self, client, owner, public_dns, url):
        response = await _create(client, _headers(owner), url=url)
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.parametrize("url", [
        "https://10.0.0.5/hook",
        "https://127.0.0.1/hook",
        "https://169.254.169.254/latest/meta-data",
        "https://[::1]/hook",
    ])
    async def test_literal_private_addresses_are_rejected(self, client, owner, public_dns, url):
        response = await _create(client, _headers(owner), url=url)
        assert response.status_code == 422
        assert "private or reserved" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_host_resolving_to_private_address_is_rejected(self, client, owner, monkeypatch):
        async def resolve(hostname):
            return [PUBLIC_IP, PRIVATE_IP]

        monkeypatch.setattr(svc, "_resolve_addresses", resolve)
        response = await _create(client, _headers(owner), url="https://internal.example.com/hook")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_unresolvable_host_is_rejected(self, client, owner, monkeypatch):
        async def resolve(hostname):
            raise svc.WebhookError("The webhook host cannot be resolved", 422)

        monkeypatch.setattr(svc, "_resolve_addresses", resolve)
        response = await _create(client, _headers(owner), url="https://missing.example.invalid/hook")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_unknown_event_is_rejected(self, client, owner, public_dns):
        response = await _create(client, _headers(owner), events=("content.exploded",))
        assert response.status_code == 422
        assert "content.exploded" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_at_least_one_event_is_required(self, client, owner, public_dns):
        response = await _create(client, _headers(owner), events=())
        assert response.status_code == 422


class TestOwnershipAndLifecycle:
    @pytest.mark.asyncio
    async def test_other_users_cannot_see_or_change_a_webhook(self, client, owner, other, public_dns):
        webhook_id = (await _create(client, _headers(owner))).json()["id"]
        headers = _headers(other)
        assert (await client.get(f"/api/v1/outbound-webhooks/{webhook_id}", headers=headers)).status_code == 404
        assert (await client.patch(f"/api/v1/outbound-webhooks/{webhook_id}", json={"is_active": False}, headers=headers)).status_code == 404
        assert (await client.delete(f"/api/v1/outbound-webhooks/{webhook_id}", headers=headers)).status_code == 404
        assert (await client.get(f"/api/v1/outbound-webhooks/{webhook_id}/deliveries", headers=headers)).status_code == 404
        assert (await client.post(f"/api/v1/outbound-webhooks/{webhook_id}/rotate-secret", headers=headers)).status_code == 404

    @pytest.mark.asyncio
    async def test_update_changes_events_and_active_state(self, client, owner, public_dns):
        webhook_id = (await _create(client, _headers(owner))).json()["id"]
        response = await client.patch(
            f"/api/v1/outbound-webhooks/{webhook_id}",
            json={"events": ["user.created", "payment.completed"], "is_active": False},
            headers=_headers(owner),
        )
        assert response.status_code == 200
        assert response.json()["events"] == ["payment.completed", "user.created"]
        assert response.json()["is_active"] is False

    @pytest.mark.asyncio
    async def test_update_revalidates_the_url(self, client, owner, public_dns):
        webhook_id = (await _create(client, _headers(owner))).json()["id"]
        response = await client.patch(
            f"/api/v1/outbound-webhooks/{webhook_id}", json={"url": "http://insecure.example.com"}, headers=_headers(owner),
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_empty_update_is_refused(self, client, owner, public_dns):
        webhook_id = (await _create(client, _headers(owner))).json()["id"]
        response = await client.patch(f"/api/v1/outbound-webhooks/{webhook_id}", json={}, headers=_headers(owner))
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_removes_the_webhook_and_its_history(self, client, owner, public_dns, session):
        webhook_id = (await _create(client, _headers(owner))).json()["id"]
        assert (await client.delete(f"/api/v1/outbound-webhooks/{webhook_id}", headers=_headers(owner))).status_code == 204
        assert (await client.get(f"/api/v1/outbound-webhooks/{webhook_id}", headers=_headers(owner))).status_code == 404
        assert (await session.execute(select(OutboundWebhook))).scalars().all() == []

    @pytest.mark.asyncio
    async def test_rotated_secret_replaces_the_old_one(self, client, owner, public_dns, session):
        created = (await _create(client, _headers(owner))).json()
        rotated = (await client.post(
            f"/api/v1/outbound-webhooks/{created['id']}/rotate-secret", headers=_headers(owner),
        )).json()["secret"]
        assert rotated != created["secret"]
        row = (await session.execute(select(OutboundWebhook))).scalar_one()
        assert decrypt_value(row.secret_encrypted) == rotated


class TestDelivery:
    @pytest.mark.asyncio
    async def test_test_event_is_signed_and_recorded_as_delivered(self, client, owner, public_dns, session):
        created = (await _create(client, _headers(owner))).json()
        with respx.mock() as mock:
            route = mock.post(HOOK).mock(return_value=httpx.Response(204))
            response = await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "delivered" and body["response_status"] == 204 and body["event"] == "webhook.test"

        sent = route.calls.last.request
        assert sent.headers["X-Webhook-Event"] == "webhook.test"
        signature = sent.headers["X-Webhook-Signature"]
        parts = dict(part.split("=", 1) for part in signature.split(","))
        expected = sign_payload(created["secret"], int(parts["t"]), sent.content)
        assert signature == expected

    @pytest.mark.asyncio
    async def test_non_2xx_answer_is_recorded_as_failed(self, client, owner, public_dns):
        created = (await _create(client, _headers(owner))).json()
        with respx.mock() as mock:
            mock.post(HOOK).mock(return_value=httpx.Response(500))
            response = await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))
        assert response.json()["status"] == "failed"
        assert response.json()["error"] == "Endpoint answered HTTP 500"

    @pytest.mark.asyncio
    async def test_transport_error_is_recorded_as_failed(self, client, owner, public_dns):
        created = (await _create(client, _headers(owner))).json()
        with respx.mock() as mock:
            mock.post(HOOK).mock(side_effect=httpx.ConnectError("refused"))
            response = await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))
        assert response.json()["status"] == "failed"
        assert response.json()["error"] == "Request failed: ConnectError"

    @pytest.mark.asyncio
    async def test_redirects_are_not_followed(self, client, owner, public_dns):
        created = (await _create(client, _headers(owner))).json()
        with respx.mock() as mock:
            mock.post(HOOK).mock(return_value=httpx.Response(302, headers={"Location": "https://10.0.0.5/x"}))
            response = await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))
        assert response.json()["status"] == "failed"
        assert response.json()["response_status"] == 302

    @pytest.mark.asyncio
    async def test_deliveries_are_listed_newest_first(self, client, owner, public_dns):
        created = (await _create(client, _headers(owner))).json()
        with respx.mock() as mock:
            mock.post(HOOK).mock(side_effect=[httpx.Response(200), httpx.Response(500)])
            await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))
            await client.post(f"/api/v1/outbound-webhooks/{created['id']}/test", headers=_headers(owner))
        history = (await client.get(
            f"/api/v1/outbound-webhooks/{created['id']}/deliveries", headers=_headers(owner),
        )).json()
        assert [item["status"] for item in history] == ["failed", "delivered"]

    @pytest.mark.asyncio
    async def test_dispatch_reaches_only_active_subscribed_endpoints(self, owner, public_dns, session):
        service = OutboundWebhookService(session, owner.id)
        subscribed, _ = await service.create(HOOK, "subscribed", ["user.created"])
        paused, _ = await service.create("https://paused.example.com/hook", "paused", ["user.created"])
        await service.update(paused.id, {"is_active": False})
        unrelated, _ = await service.create("https://other.example.com/hook", "other", ["payment.completed"])

        with respx.mock(assert_all_called=False) as mock:
            hook_route = mock.post(HOOK).mock(return_value=httpx.Response(200))
            paused_route = mock.post("https://paused.example.com/hook").mock(return_value=httpx.Response(200))
            other_route = mock.post("https://other.example.com/hook").mock(return_value=httpx.Response(200))
            deliveries = await service.dispatch("user.created", {"user_id": owner.id})

        assert [d.webhook_id for d in deliveries] == [subscribed.id]
        assert hook_route.called and not paused_route.called and not other_route.called

    @pytest.mark.asyncio
    async def test_dispatch_rejects_unknown_events(self, owner, session):
        with pytest.raises(svc.WebhookError):
            await OutboundWebhookService(session, owner.id).dispatch("made.up", {})

    @pytest.mark.asyncio
    async def test_delivery_to_an_endpoint_now_on_a_private_address_is_refused(self, owner, session, monkeypatch):
        service = OutboundWebhookService(session, owner.id)

        async def resolve_public(hostname):
            return [PUBLIC_IP]

        monkeypatch.setattr(svc, "_resolve_addresses", resolve_public)
        webhook, _ = await service.create(HOOK, None, ["user.created"])

        async def resolve_private(hostname):
            return [PRIVATE_IP]

        monkeypatch.setattr(svc, "_resolve_addresses", resolve_private)
        delivery = await svc.deliver(session, webhook, "user.created", {})
        assert delivery.status == "failed"
        assert "private or reserved" in delivery.error


class TestSigning:
    def test_signature_changes_with_secret_time_or_body(self):
        base = sign_payload("secret", 1000, b"{}")
        assert base == sign_payload("secret", 1000, b"{}")
        assert base != sign_payload("other", 1000, b"{}")
        assert base != sign_payload("secret", 1001, b"{}")
        assert base != sign_payload("secret", 1000, b"{ }")
