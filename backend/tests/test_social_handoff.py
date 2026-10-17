"""Mobile sign-in handoff: the app starts a ticketed sign-in and later claims the tokens."""

from datetime import datetime, timedelta, timezone

import httpx
import pytest
import respx
from sqlalchemy import select

from app.models.social_auth import SocialLoginHandoff
from app.services.social_auth_service import hash_ticket
from tests.test_social_auth import (  # noqa: F401  (fixtures and helpers shared with the social login suite)
    _auth_header,
    _configure,
    _state_for,
    admin_user,
    regular_user,
    social_client,
)

GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO = "https://openidconnect.googleapis.com/v1/userinfo"
TICKET = "t" * 40
OTHER_TICKET = "u" * 40


@pytest.fixture
async def google_enabled(social_client, admin_user):
    await _configure(social_client, _auth_header(admin_user), "google")


def _google_mock(mock, email="app.user@example.com"):
    mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "g"}))
    mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json={
        "sub": "google-app-1", "email": email, "email_verified": True, "given_name": "App",
    }))


class TestStartingAMobileSignIn:
    @pytest.mark.asyncio
    async def test_authorize_with_ticket_creates_a_pending_handoff(self, social_client, google_enabled, session):
        response = await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        assert response.status_code == 200
        assert "state=" in response.json()["authorization_url"]

        row = (await session.execute(select(SocialLoginHandoff))).scalar_one()
        assert row.ticket_hash == hash_ticket(TICKET)
        assert row.payload_encrypted is None

    @pytest.mark.asyncio
    async def test_ticket_must_be_long_enough(self, social_client, google_enabled):
        response = await social_client.get("/api/v1/auth/social/google/authorize?ticket=short")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_authorize_without_ticket_stores_nothing(self, social_client, google_enabled, session):
        assert (await social_client.get("/api/v1/auth/social/google/authorize")).status_code == 200
        assert (await session.execute(select(SocialLoginHandoff))).scalars().all() == []


class TestCompletingAndClaiming:
    @pytest.mark.asyncio
    async def test_full_mobile_flow_hands_tokens_over_once(self, social_client, google_enabled, session):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        state = _state_for("google", ticket_hash=hash_ticket(TICKET))

        # Browser step: the provider redirects back and the web page exchanges the code.
        with respx.mock() as mock:
            _google_mock(mock)
            exchange = await social_client.post(
                "/api/v1/auth/social/google/exchange", json={"code": "c", "state": state},
            )
        assert exchange.status_code == 200
        assert exchange.json() == {"handoff": True}

        # App step: claim the tokens with the ticket it kept.
        claim = await social_client.get(f"/api/v1/auth/social/handoff/{TICKET}")
        assert claim.status_code == 200
        body = claim.json()
        assert body["access_token"] and body["refresh_token"] and body["token_type"] == "bearer"

        # A second claim finds nothing: tokens are handed over once.
        again = await social_client.get(f"/api/v1/auth/social/handoff/{TICKET}")
        assert again.status_code == 404
        assert (await session.execute(select(SocialLoginHandoff))).scalars().all() == []

    @pytest.mark.asyncio
    async def test_claim_is_pending_until_the_browser_step_completes(self, social_client, google_enabled):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        response = await social_client.get(f"/api/v1/auth/social/handoff/{TICKET}")
        assert response.status_code == 202
        assert response.json() == {"status": "pending"}

    @pytest.mark.asyncio
    async def test_unknown_ticket_is_not_found(self, social_client):
        response = await social_client.get(f"/api/v1/auth/social/handoff/{OTHER_TICKET}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_expired_handoff_is_not_found_and_removed(self, social_client, google_enabled, session):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        row = (await session.execute(select(SocialLoginHandoff))).scalar_one()
        row.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        await session.commit()

        response = await social_client.get(f"/api/v1/auth/social/handoff/{TICKET}")
        assert response.status_code == 404
        assert (await session.execute(select(SocialLoginHandoff))).scalars().all() == []

    @pytest.mark.asyncio
    async def test_tokens_are_encrypted_at_rest(self, social_client, google_enabled, session):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        state = _state_for("google", ticket_hash=hash_ticket(TICKET))
        with respx.mock() as mock:
            _google_mock(mock)
            await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": state})

        row = (await session.execute(select(SocialLoginHandoff))).scalar_one()
        assert row.payload_encrypted and "access_token" not in row.payload_encrypted

    @pytest.mark.asyncio
    async def test_exchange_with_ticket_state_but_no_pending_handoff_is_refused(self, social_client, google_enabled):
        state = _state_for("google", ticket_hash=hash_ticket(OTHER_TICKET))
        with respx.mock() as mock:
            _google_mock(mock)
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": state})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_expired_pending_handoff_refuses_the_exchange(self, social_client, google_enabled, session):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        row = (await session.execute(select(SocialLoginHandoff))).scalar_one()
        row.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        await session.commit()

        state = _state_for("google", ticket_hash=hash_ticket(TICKET))
        with respx.mock() as mock:
            _google_mock(mock)
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": state})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_another_ticket_cannot_claim_the_tokens(self, social_client, google_enabled):
        await social_client.get(f"/api/v1/auth/social/google/authorize?ticket={TICKET}")
        state = _state_for("google", ticket_hash=hash_ticket(TICKET))
        with respx.mock() as mock:
            _google_mock(mock)
            await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": state})

        response = await social_client.get(f"/api/v1/auth/social/handoff/{OTHER_TICKET}")
        assert response.status_code == 404
        assert (await social_client.get(f"/api/v1/auth/social/handoff/{TICKET}")).status_code == 200
