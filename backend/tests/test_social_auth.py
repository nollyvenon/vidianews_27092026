"""Social login: public OAuth flow and admin management of provider credentials."""

import httpx
import pytest
import respx
from cryptography.fernet import Fernet
from jose import jwt
from sqlalchemy import select

from app.core.config import settings
from app.db.session import get_db, get_session
from app.main import app
from app.core.security import create_access_token, hash_password
from app.models.rbac import Permission, Role as RBACRole, role_permissions, user_roles as rbac_user_roles
from app.models.security_performance import AuthProvider, OAuthProvider
from app.models.social_auth import SocialLoginProvider
from app.models.user import Role, User
from app.services.social_auth_service import (
    STATE_TOKEN_TYPE,
    SocialAuthError,
    decrypt_client_secret,
    encrypt_client_secret,
)

GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO = "https://openidconnect.googleapis.com/v1/userinfo"
GITHUB_TOKEN = "https://github.com/login/oauth/access_token"
GITHUB_USER = "https://api.github.com/user"
GITHUB_EMAILS = "https://api.github.com/user/emails"
MICROSOFT_TOKEN = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MICROSOFT_USERINFO = "https://graph.microsoft.com/oidc/userinfo"


@pytest.fixture
async def social_client(test_session):
    """HTTP client bound to the app with every DB dependency routed to the test session.

    Built on ASGITransport so it works with the installed httpx (conftest's ``app=`` form
    requires httpx<0.28).
    """
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


async def _make_user(session, email, roles=(), status="active"):
    user = User(
        email=email,
        password_hash=hash_password("Passw0rd!long"),
        first_name="Test",
        last_name="User",
        status=status,
    )
    user.roles = list(roles)
    session.add(user)
    await session.commit()
    return user


def _auth_header(user):
    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def admin_user(session):
    return await _make_user(session, "admin@example.com", roles=[Role(name="admin", description="Administrator")])


@pytest.fixture
async def regular_user(session):
    return await _make_user(session, "member@example.com")


async def _configure(client, headers, provider, **overrides):
    body = {
        "enabled": True,
        "client_id": f"{provider}-client-id",
        "client_secret": f"{provider}-client-secret",
        "redirect_uri": f"https://app.example.com/auth/social/{provider}/callback",
    }
    body.update(overrides)
    return await client.put(f"/api/v1/admin/social-providers/{provider}", json=body, headers=headers)


def _state_for(provider, **extra):
    claims = {"provider": provider, "nonce": "n", "type": STATE_TOKEN_TYPE, "exp": 4102444800, **extra}
    return jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


class TestCredentialEncryption:
    def test_round_trip(self):
        assert decrypt_client_secret(encrypt_client_secret("s3cret")) == "s3cret"

    def test_ciphertext_does_not_contain_plaintext(self):
        assert "s3cret" not in encrypt_client_secret("s3cret")

    def test_undecryptable_secret_raises_server_error(self):
        with pytest.raises(SocialAuthError) as info:
            decrypt_client_secret(Fernet.generate_key().decode())
        assert info.value.status_code == 500


class TestProviderAdministration:
    @pytest.mark.asyncio
    async def test_anonymous_request_is_rejected(self, social_client):
        response = await social_client.get("/api/v1/admin/social-providers")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_non_admin_is_forbidden(self, social_client, regular_user):
        response = await social_client.get("/api/v1/admin/social-providers", headers=_auth_header(regular_user))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_legacy_admin_role_grants_access(self, social_client, admin_user):
        response = await social_client.get("/api/v1/admin/social-providers", headers=_auth_header(admin_user))
        assert response.status_code == 200
        assert [item["provider"] for item in response.json()] == ["google", "github", "microsoft"]

    @pytest.mark.asyncio
    async def test_rbac_permission_grants_access(self, social_client, session):
        user = await _make_user(session, "rbac@example.com")
        permission = Permission(name="social_login:manage", resource="social_login", action="manage")
        rbac_role = RBACRole(name="social_manager", description="Manages social login")
        session.add_all([permission, rbac_role])
        await session.flush()
        await session.execute(role_permissions.insert().values(role_id=rbac_role.id, permission_id=permission.id))
        await session.execute(rbac_user_roles.insert().values(user_id=user.id, role_id=rbac_role.id))
        await session.commit()

        response = await social_client.get("/api/v1/admin/social-providers", headers=_auth_header(user))
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_listing_never_returns_secrets(self, social_client, admin_user):
        headers = _auth_header(admin_user)
        await _configure(social_client, headers, "google")
        listing = (await social_client.get("/api/v1/admin/social-providers", headers=headers)).json()
        google = next(item for item in listing if item["provider"] == "google")
        assert google["client_secret_set"] is True
        assert "client_secret" not in google
        assert "google-client-secret" not in str(listing)

    @pytest.mark.asyncio
    async def test_secret_is_stored_encrypted(self, social_client, admin_user, session):
        await _configure(social_client, _auth_header(admin_user), "github")
        row = (await session.execute(
            select(SocialLoginProvider).where(SocialLoginProvider.provider == "github")
        )).scalar_one()
        assert row.client_secret_encrypted != "github-client-secret"
        assert decrypt_client_secret(row.client_secret_encrypted) == "github-client-secret"

    @pytest.mark.asyncio
    async def test_update_without_secret_keeps_existing_secret(self, social_client, admin_user, session):
        headers = _auth_header(admin_user)
        await _configure(social_client, headers, "google")
        before = (await session.execute(select(SocialLoginProvider.client_secret_encrypted))).scalar_one()
        response = await social_client.put(
            "/api/v1/admin/social-providers/google",
            json={"enabled": True, "client_id": "rotated-id"},
            headers=headers,
        )
        assert response.status_code == 200
        after = (await session.execute(select(SocialLoginProvider.client_secret_encrypted))).scalar_one()
        assert after == before

    @pytest.mark.asyncio
    async def test_enabling_without_credentials_is_rejected(self, social_client, admin_user):
        response = await social_client.put(
            "/api/v1/admin/social-providers/google",
            json={"enabled": True},
            headers=_auth_header(admin_user),
        )
        assert response.status_code == 422
        assert "client_id" in response.json()["detail"]
        assert "client_secret" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_unknown_provider_is_not_found(self, social_client, admin_user):
        response = await social_client.put(
            "/api/v1/admin/social-providers/myspace",
            json={"enabled": False},
            headers=_auth_header(admin_user),
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_disabling_keeps_credentials(self, social_client, admin_user, session):
        headers = _auth_header(admin_user)
        await _configure(social_client, headers, "google")
        response = await social_client.put(
            "/api/v1/admin/social-providers/google", json={"enabled": False}, headers=headers
        )
        assert response.status_code == 200
        assert response.json()["enabled"] is False
        assert response.json()["client_secret_set"] is True


class TestPublicFlow:
    @pytest.mark.asyncio
    async def test_only_enabled_providers_are_listed(self, social_client, admin_user):
        headers = _auth_header(admin_user)
        await _configure(social_client, headers, "google")
        await _configure(social_client, headers, "github", enabled=False)
        response = await social_client.get("/api/v1/auth/social/providers")
        assert response.status_code == 200
        assert response.json() == [{"provider": "google", "display_name": "Google"}]

    @pytest.mark.asyncio
    async def test_authorization_url_carries_client_and_signed_state(self, social_client, admin_user):
        await _configure(social_client, _auth_header(admin_user), "github", scopes="read:user")
        response = await social_client.get("/api/v1/auth/social/github/authorize")
        assert response.status_code == 200
        url = response.json()["authorization_url"]
        assert url.startswith("https://github.com/login/oauth/authorize?")
        assert "client_id=github-client-id" in url
        assert "scope=read%3Auser" in url
        state = url.split("state=")[1]
        claims = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert claims["provider"] == "github" and claims["type"] == STATE_TOKEN_TYPE

    @pytest.mark.asyncio
    async def test_authorize_for_disabled_provider_is_not_found(self, social_client):
        response = await social_client.get("/api/v1/auth/social/google/authorize")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_authorize_for_unknown_provider_is_not_found(self, social_client):
        response = await social_client.get("/api/v1/auth/social/myspace/authorize")
        assert response.status_code == 404


class TestCodeExchange:
    @pytest.fixture
    async def google_enabled(self, social_client, admin_user):
        await _configure(social_client, _auth_header(admin_user), "google")

    @pytest.mark.asyncio
    async def test_new_google_user_is_created_and_linked(self, social_client, google_enabled, session):
        with respx.mock(assert_all_called=True) as mock:
            token_route = mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "g-token"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json={
                "sub": "google-123", "email": "New.Person@Example.com", "email_verified": True,
                "given_name": "New", "family_name": "Person", "picture": "https://img/x.png",
            }))
            response = await social_client.post(
                "/api/v1/auth/social/google/exchange",
                json={"code": "auth-code", "state": _state_for("google")},
            )
        assert response.status_code == 200
        body = response.json()
        assert body["access_token"] and body["refresh_token"] and body["token_type"] == "bearer"

        sent = token_route.calls.last.request.content.decode()
        assert "code=auth-code" in sent and "client_secret=google-client-secret" in sent

        user = (await session.execute(select(User).where(User.email == "new.person@example.com"))).scalar_one()
        assert user.first_name == "New" and user.status == "active"
        link = (await session.execute(select(OAuthProvider).where(OAuthProvider.user_id == user.id))).scalar_one()
        assert link.provider == AuthProvider.GOOGLE and link.provider_user_id == "google-123"

    @pytest.mark.asyncio
    async def test_returning_user_reuses_link(self, social_client, google_enabled, session):
        profile = {"sub": "google-9", "email": "repeat@example.com", "email_verified": True}
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "t"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json=profile))
            first = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c1", "state": _state_for("google")})
            second = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c2", "state": _state_for("google")})
        assert first.status_code == second.status_code == 200
        users = (await session.execute(select(User).where(User.email == "repeat@example.com"))).scalars().all()
        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_verified_email_links_existing_account(self, social_client, google_enabled, session, regular_user):
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "t"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json={
                "sub": "google-existing", "email": regular_user.email, "email_verified": True,
            }))
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("google")})
        assert response.status_code == 200
        links = (await session.execute(select(OAuthProvider).where(OAuthProvider.user_id == regular_user.id))).scalars().all()
        assert [link.provider_user_id for link in links] == ["google-existing"]

    @pytest.mark.asyncio
    async def test_unverified_email_cannot_take_over_account(self, social_client, google_enabled, session, regular_user):
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "t"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json={
                "sub": "attacker", "email": regular_user.email, "email_verified": False,
            }))
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("google")})
        assert response.status_code == 401
        links = (await session.execute(select(OAuthProvider))).scalars().all()
        assert links == []

    @pytest.mark.asyncio
    async def test_inactive_account_is_refused(self, social_client, google_enabled, session):
        await _make_user(session, "suspended@example.com", status="suspended")
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "t"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(200, json={
                "sub": "susp", "email": "suspended@example.com", "email_verified": True,
            }))
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("google")})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_provider_code_rejection_returns_unauthorized(self, social_client, google_enabled):
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(400, json={"error": "invalid_grant"}))
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "bad", "state": _state_for("google")})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_missing_state_is_rejected(self, social_client, google_enabled):
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": "not-a-jwt"})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_expired_state_is_rejected(self, social_client, google_enabled):
        expired = jwt.encode(
            {"provider": "google", "type": STATE_TOKEN_TYPE, "exp": 1000},
            settings.SECRET_KEY, algorithm=settings.ALGORITHM,
        )
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": expired})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_state_issued_for_another_provider_is_rejected(self, social_client, google_enabled):
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("github")})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_state_without_social_type_is_rejected(self, social_client, google_enabled):
        plain = jwt.encode({"provider": "google", "exp": 4102444800}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": plain})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_exchange_for_disabled_provider_is_not_found(self, social_client):
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("google")})
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_github_uses_primary_verified_email_when_profile_hides_it(self, social_client, admin_user, session):
        await _configure(social_client, _auth_header(admin_user), "github")
        with respx.mock() as mock:
            mock.post(GITHUB_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "gh"}))
            mock.get(GITHUB_USER).mock(return_value=httpx.Response(200, json={
                "id": 4242, "email": None, "name": "Octo Cat", "avatar_url": "https://img/gh.png",
            }))
            mock.get(GITHUB_EMAILS).mock(return_value=httpx.Response(200, json=[
                {"email": "old@example.com", "primary": False, "verified": True},
                {"email": "octo@example.com", "primary": True, "verified": True},
            ]))
            response = await social_client.post("/api/v1/auth/social/github/exchange", json={"code": "c", "state": _state_for("github")})
        assert response.status_code == 200
        user = (await session.execute(select(User).where(User.email == "octo@example.com"))).scalar_one()
        assert user.first_name == "Octo" and user.last_name == "Cat"

    @pytest.mark.asyncio
    async def test_github_unverified_primary_email_is_refused(self, social_client, admin_user):
        await _configure(social_client, _auth_header(admin_user), "github")
        with respx.mock() as mock:
            mock.post(GITHUB_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "gh"}))
            mock.get(GITHUB_USER).mock(return_value=httpx.Response(200, json={"id": 7, "email": "x@example.com"}))
            mock.get(GITHUB_EMAILS).mock(return_value=httpx.Response(200, json=[
                {"email": "x@example.com", "primary": True, "verified": False},
            ]))
            response = await social_client.post("/api/v1/auth/social/github/exchange", json={"code": "c", "state": _state_for("github")})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_github_without_any_email_is_refused(self, social_client, admin_user):
        await _configure(social_client, _auth_header(admin_user), "github")
        with respx.mock() as mock:
            mock.post(GITHUB_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "gh"}))
            mock.get(GITHUB_USER).mock(return_value=httpx.Response(200, json={"id": 8, "email": None}))
            mock.get(GITHUB_EMAILS).mock(return_value=httpx.Response(200, json=[]))
            response = await social_client.post("/api/v1/auth/social/github/exchange", json={"code": "c", "state": _state_for("github")})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_microsoft_flow_creates_user(self, social_client, admin_user, session):
        await _configure(social_client, _auth_header(admin_user), "microsoft")
        with respx.mock() as mock:
            mock.post(MICROSOFT_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "ms"}))
            mock.get(MICROSOFT_USERINFO).mock(return_value=httpx.Response(200, json={
                "sub": "ms-1", "email": "ms.user@example.com", "name": "Ms User",
            }))
            response = await social_client.post("/api/v1/auth/social/microsoft/exchange", json={"code": "c", "state": _state_for("microsoft")})
        assert response.status_code == 200
        link = (await session.execute(select(OAuthProvider))).scalar_one()
        assert link.provider == AuthProvider.MICROSOFT and link.provider_user_id == "ms-1"

    @pytest.mark.asyncio
    async def test_provider_profile_failure_is_bad_gateway(self, social_client, google_enabled):
        with respx.mock() as mock:
            mock.post(GOOGLE_TOKEN).mock(return_value=httpx.Response(200, json={"access_token": "t"}))
            mock.get(GOOGLE_USERINFO).mock(return_value=httpx.Response(500, json={}))
            response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": _state_for("google")})
        assert response.status_code == 502

    @pytest.mark.asyncio
    async def test_stored_secret_is_unreadable_after_key_change(self, social_client, google_enabled, session, monkeypatch):
        monkeypatch.setattr(settings, "SECRET_KEY", "a-different-secret-key-entirely")
        # The state is signed with the new key so validation passes and the stored secret is what fails.
        state = _state_for("google")
        response = await social_client.post("/api/v1/auth/social/google/exchange", json={"code": "c", "state": state})
        assert response.status_code == 500


class TestServiceErrorType:
    def test_error_carries_status_and_message(self):
        error = SocialAuthError("nope", 418)
        assert error.status_code == 418 and error.message == "nope"
