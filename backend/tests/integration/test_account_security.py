"""Route tests for account security: two-factor authentication, password reset, and the cache and privacy controls"""

import time
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.services.mfa_service import code_at


def _login(client, email: str, password: str, otp_code: str = None):
    body = {"email": email, "password": password}
    if otp_code is not None:
        body["otp_code"] = otp_code
    return client.post("/api/v1/auth/login", json=body)


class TestTwoFactorAuthentication:
    async def test_setup_and_enable_require_a_correct_code(self, async_client, org_member):
        setup = await async_client.post("/api/v1/auth/mfa/setup", headers=org_member)
        assert setup.status_code == 200
        secret = setup.json()["secret"]
        assert setup.json()["otpauth_uri"].startswith("otpauth://totp/")

        wrong = await async_client.post("/api/v1/auth/mfa/enable", json={"code": "000000"}, headers=org_member)
        status_before = await async_client.get("/api/v1/auth/mfa", headers=org_member)
        right = await async_client.post(
            "/api/v1/auth/mfa/enable", json={"code": code_at(secret, time.time())}, headers=org_member
        )

        assert wrong.status_code == 422
        assert status_before.json() == {"enabled": False}
        assert right.status_code == 200
        assert (await async_client.get("/api/v1/auth/mfa", headers=org_member)).json() == {"enabled": True}

    async def test_enable_needs_a_setup_first(self, async_client, org_member):
        response = await async_client.post("/api/v1/auth/mfa/enable", json={"code": "123456"}, headers=org_member)

        assert response.status_code == 422

    async def test_login_requires_the_current_code_once_enabled(self, async_client, org_member, reference_data, reset_test_database):
        setup = await async_client.post("/api/v1/auth/mfa/setup", headers=org_member)
        secret = setup.json()["secret"]
        await async_client.post("/api/v1/auth/mfa/enable", json={"code": code_at(secret, time.time())}, headers=org_member)

        with Session(reset_test_database) as session:
            user = session.get(User, 1)
            user.password_hash = hash_password("Passw0rd!test")
            session.commit()
            email = user.email

        without = await async_client.post("/api/v1/auth/login", json={"email": email, "password": "Passw0rd!test"})
        wrong = await async_client.post(
            "/api/v1/auth/login", json={"email": email, "password": "Passw0rd!test", "otp_code": "000000"}
        )
        right = await async_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Passw0rd!test", "otp_code": code_at(secret, time.time())},
        )

        assert without.status_code == 401
        assert without.json()["detail"]["error"]["message"] == "MFA code required"
        assert wrong.status_code == 401
        assert right.status_code == 200
        assert "access_token" in right.json()

    async def test_disable_needs_a_current_code_and_turns_the_factor_off(self, async_client, org_member):
        secret = (await async_client.post("/api/v1/auth/mfa/setup", headers=org_member)).json()["secret"]
        await async_client.post("/api/v1/auth/mfa/enable", json={"code": code_at(secret, time.time())}, headers=org_member)

        refused = await async_client.post("/api/v1/auth/mfa/disable", json={"code": "000000"}, headers=org_member)
        disabled = await async_client.post(
            "/api/v1/auth/mfa/disable", json={"code": code_at(secret, time.time())}, headers=org_member
        )

        assert refused.status_code == 422
        assert disabled.status_code == 200
        assert (await async_client.get("/api/v1/auth/mfa", headers=org_member)).json() == {"enabled": False}

    async def test_mfa_routes_need_a_signed_in_user(self, async_client):
        response = await async_client.post("/api/v1/auth/mfa/setup")

        assert response.status_code in (401, 403)

    async def test_legacy_mfa_setup_issues_a_server_generated_secret(self, async_client, org_member):
        response = await async_client.post("/api/v1/mfa/setup", headers=org_member)

        assert response.status_code == 200
        assert response.json()["method"] == "totp"
        assert len(response.json()["secret"]) >= 16


class TestPasswordReset:
    async def test_a_reset_link_is_emailed_for_an_existing_account(self, async_client, reference_data, reset_test_database):
        with patch("app.api.v1.auth.send_password_reset_email", new=AsyncMock(return_value=True)) as send:
            with Session(reset_test_database) as session:
                email = session.get(User, 1).email
            response = await async_client.post("/api/v1/auth/forgot-password", json={"email": email})

        assert response.status_code == 200
        send.assert_awaited_once()
        assert send.await_args.args[0] == email
        assert "/auth/reset-password?token=" in send.await_args.args[1]

    async def test_no_email_is_sent_for_an_unknown_address_but_the_answer_is_the_same(self, async_client):
        with patch("app.api.v1.auth.send_password_reset_email", new=AsyncMock(return_value=True)) as send:
            response = await async_client.post("/api/v1/auth/forgot-password", json={"email": "nobody@example.com"})

        assert response.status_code == 200
        assert "password reset link has been sent" in response.json()["message"]
        send.assert_not_awaited()


class TestCacheControls:
    async def test_a_policy_is_saved_and_listed_with_its_hit_rate(self, async_client, platform_admin):
        saved = await async_client.put(
            "/api/v1/cache/policies/content",
            json={"cache_type": "redis", "ttl_seconds": 600, "max_size_mb": 64},
            headers=platform_admin,
        )
        listed = await async_client.get("/api/v1/cache/policies", headers=platform_admin)

        assert saved.status_code == 200
        assert saved.json()["ttl_seconds"] == 600
        assert [policy["resource_type"] for policy in listed.json()] == ["content"]
        assert listed.json()[0]["hit_rate"] == 0.0

    async def test_policy_changes_are_refused_without_the_admin_role(self, async_client, org_member):
        response = await async_client.put(
            "/api/v1/cache/policies/content",
            json={"cache_type": "redis", "ttl_seconds": 600},
            headers=org_member,
        )

        assert response.status_code == 403

    async def test_an_unknown_policy_is_not_found(self, async_client, org_member):
        response = await async_client.get("/api/v1/cache/policy/missing", headers=org_member)

        assert response.status_code == 404

    async def test_policy_ttl_outside_the_allowed_range_is_refused(self, async_client, platform_admin):
        response = await async_client.put(
            "/api/v1/cache/policies/content",
            json={"cache_type": "redis", "ttl_seconds": 0},
            headers=platform_admin,
        )

        assert response.status_code == 422

    async def test_flush_and_optimize_are_administrator_only(self, async_client, unaffiliated_user, platform_admin):
        refused = await async_client.post("/api/v1/cache/flush", headers=unaffiliated_user)
        flushed = await async_client.post("/api/v1/cache/flush", headers=platform_admin)
        optimized = await async_client.post("/api/v1/cache/optimize", headers=platform_admin)

        assert refused.status_code == 403
        assert flushed.status_code == 200
        assert set(flushed.json()) == {"removed"}
        assert optimized.status_code == 200
        assert set(optimized.json()) == {"removed", "remaining"}


class TestPrivacyAndQuota:
    async def test_privacy_settings_are_created_with_defaults_and_updated(self, async_client, org_member):
        before = await async_client.get("/api/v1/privacy/settings", headers=org_member)
        updated = await async_client.put(
            "/api/v1/privacy/settings?profile_visibility=private&content_visibility=friends_only",
            headers=org_member,
        )

        assert before.status_code == 200
        assert before.json()["profile_visibility"] == "public"
        assert updated.json()["profile_visibility"] == "private"
        assert updated.json()["content_visibility"] == "friends_only"

    async def test_an_unknown_privacy_level_is_refused(self, async_client, org_member):
        response = await async_client.put("/api/v1/privacy/settings?profile_visibility=secret", headers=org_member)

        assert response.status_code == 422

    async def test_quota_is_zero_before_any_usage_is_recorded(self, async_client, org_member):
        response = await async_client.get("/api/v1/quota/usage", headers=org_member)

        assert response.status_code == 200
        assert response.json() == {"api_calls": 0, "api_call_limit": 10000, "storage_gb": 0.0, "bandwidth_gb": 0.0}

    async def test_an_unsupported_oauth_provider_is_refused(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/oauth/connect?provider=myspace&provider_user_id=abc&token=t", headers=org_member
        )

        assert response.status_code == 422
