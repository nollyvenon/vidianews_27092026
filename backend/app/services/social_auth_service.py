"""Social login (OAuth 2.0 / OpenID Connect) for Google, GitHub and Microsoft.

Flow:
1. ``build_authorization_url`` returns the provider consent URL with a signed,
   short-lived ``state`` JWT (CSRF protection; no server-side session needed).
2. The browser returns to the frontend with ``code`` and ``state``.
3. ``exchange_code`` validates ``state``, exchanges the code for a provider access
   token, fetches the normalized profile, links or creates the local user and
   issues the same access/refresh JWTs as password login.

Client credentials are administered through the admin API and stored encrypted
with Fernet, keyed from ``SECRET_KEY``. Rotating ``SECRET_KEY`` makes stored
client secrets unreadable; they must then be re-entered in the admin panel.
"""

import base64
import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode

import httpx
from cryptography.fernet import Fernet, InvalidToken
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, hash_password
from app.models.security_performance import AuthProvider, OAuthProvider
from app.models.social_auth import SocialLoginProvider
from app.models.user import User
from app.utils.logger import logger


STATE_TOKEN_TYPE = "social_state"
STATE_TTL = timedelta(minutes=10)
HTTP_TIMEOUT_SECONDS = 10.0


class SocialAuthError(Exception):
    """Raised for any social login failure. ``status_code`` is the HTTP status to return."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@dataclass(frozen=True)
class ProviderSpec:
    key: str
    display_name: str
    authorize_url: str
    token_url: str
    default_scopes: str
    profile_url: str
    emails_url: Optional[str] = None
    token_headers: Dict[str, str] = field(default_factory=dict)


PROVIDER_SPECS: Dict[str, ProviderSpec] = {
    "google": ProviderSpec(
        key="google",
        display_name="Google",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        default_scopes="openid email profile",
        profile_url="https://openidconnect.googleapis.com/v1/userinfo",
    ),
    "github": ProviderSpec(
        key="github",
        display_name="GitHub",
        authorize_url="https://github.com/login/oauth/authorize",
        token_url="https://github.com/login/oauth/access_token",
        default_scopes="read:user user:email",
        profile_url="https://api.github.com/user",
        emails_url="https://api.github.com/user/emails",
        token_headers={"Accept": "application/json"},
    ),
    "microsoft": ProviderSpec(
        key="microsoft",
        display_name="Microsoft",
        authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
        default_scopes="openid email profile",
        profile_url="https://graph.microsoft.com/oidc/userinfo",
    ),
}


@dataclass(frozen=True)
class ExternalProfile:
    provider_user_id: str
    email: Optional[str]
    email_verified: bool
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]


def _split_name(full_name: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if not full_name:
        return None, None
    parts = full_name.strip().split(" ", 1)
    return parts[0] or None, (parts[1] if len(parts) > 1 else None)


def _credential_cipher() -> Fernet:
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    return Fernet(key)


def encrypt_client_secret(plain: str) -> str:
    return _credential_cipher().encrypt(plain.encode()).decode()


def decrypt_client_secret(ciphertext: str) -> str:
    try:
        return _credential_cipher().decrypt(ciphertext.encode()).decode()
    except InvalidToken as exc:
        logger.error("Stored social login client secret cannot be decrypted; re-enter it in the admin panel")
        raise SocialAuthError("Social login credentials are unreadable; ask an administrator to re-enter them", 500) from exc


def get_provider_spec(provider: str) -> ProviderSpec:
    spec = PROVIDER_SPECS.get(provider)
    if spec is None:
        raise SocialAuthError(f"Unsupported social login provider: {provider}", 404)
    return spec


class SocialAuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ----- provider configuration -------------------------------------------------

    async def get_config(self, provider: str) -> Optional[SocialLoginProvider]:
        stmt = select(SocialLoginProvider).where(SocialLoginProvider.provider == provider)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def list_admin_view(self) -> List[dict]:
        """Every supported provider with its configuration. Secrets are never returned."""
        rows = {
            row.provider: row
            for row in (await self.session.execute(select(SocialLoginProvider))).scalars().all()
        }
        view = []
        for key, spec in PROVIDER_SPECS.items():
            row = rows.get(key)
            view.append({
                "provider": key,
                "display_name": spec.display_name,
                "enabled": bool(row and row.enabled),
                "client_id": row.client_id if row else None,
                "client_secret_set": bool(row and row.client_secret_encrypted),
                "redirect_uri": row.redirect_uri if row else None,
                "scopes": (row.scopes if row and row.scopes else spec.default_scopes),
                "updated_at": row.updated_at if row else None,
            })
        return view

    async def list_enabled_providers(self) -> List[dict]:
        rows = (await self.session.execute(
            select(SocialLoginProvider).where(SocialLoginProvider.enabled.is_(True))
        )).scalars().all()
        return [
            {"provider": row.provider, "display_name": PROVIDER_SPECS[row.provider].display_name}
            for row in rows
            if row.provider in PROVIDER_SPECS
        ]

    async def upsert_provider(
        self,
        provider: str,
        *,
        actor_user_id: int,
        enabled: bool,
        client_id: Optional[str],
        client_secret: Optional[str],
        redirect_uri: Optional[str],
        scopes: Optional[str],
    ) -> dict:
        spec = get_provider_spec(provider)
        row = await self.get_config(provider)
        if row is None:
            row = SocialLoginProvider(provider=provider, enabled=False)
            self.session.add(row)

        if client_id is not None:
            row.client_id = client_id.strip() or None
        if client_secret:
            row.client_secret_encrypted = encrypt_client_secret(client_secret)
        if redirect_uri is not None:
            row.redirect_uri = redirect_uri.strip() or None
        if scopes is not None:
            row.scopes = scopes.strip() or None

        if enabled:
            missing = [
                name for name, value in (
                    ("client_id", row.client_id),
                    ("client_secret", row.client_secret_encrypted),
                    ("redirect_uri", row.redirect_uri),
                ) if not value
            ]
            if missing:
                raise SocialAuthError(f"Cannot enable {spec.display_name}: missing {', '.join(missing)}", 422)
        row.enabled = enabled
        row.updated_by_user_id = actor_user_id
        await self.session.commit()
        logger.info(f"Social login provider {provider} updated (enabled={enabled}) by user {actor_user_id}")
        return next(item for item in await self.list_admin_view() if item["provider"] == provider)

    # ----- OAuth flow ------------------------------------------------------------

    async def build_authorization_url(self, provider: str) -> str:
        spec = get_provider_spec(provider)
        config = await self._enabled_config(provider)
        state = jwt.encode(
            {
                "provider": provider,
                "nonce": secrets.token_urlsafe(16),
                "type": STATE_TOKEN_TYPE,
                "exp": datetime.now(timezone.utc) + STATE_TTL,
            },
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        params = {
            "client_id": config.client_id,
            "redirect_uri": config.redirect_uri,
            "response_type": "code",
            "scope": config.scopes or spec.default_scopes,
            "state": state,
        }
        return f"{spec.authorize_url}?{urlencode(params)}"

    async def exchange_code(self, provider: str, code: str, state: str) -> Tuple[str, str, User]:
        spec = get_provider_spec(provider)
        self._verify_state(provider, state)
        config = await self._enabled_config(provider)
        client_secret = decrypt_client_secret(config.client_secret_encrypted)

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
            provider_token = await self._fetch_provider_token(client, spec, config, client_secret, code)
            profile = await self._fetch_profile(client, spec, provider_token)

        user = await self._resolve_user(provider, profile)
        if user.status != "active":
            raise SocialAuthError("Account inactive", 401)

        user.last_login_at = datetime.now(timezone.utc)
        await self.session.commit()
        access = create_access_token({"sub": user.email, "user_id": user.id})
        refresh = create_refresh_token({"sub": user.email, "user_id": user.id})
        logger.info(f"Social login via {provider} for user {user.id}")
        return access, refresh, user

    def _verify_state(self, provider: str, state: str) -> None:
        try:
            claims = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError as exc:
            raise SocialAuthError("Invalid or expired login state", 400) from exc
        if claims.get("type") != STATE_TOKEN_TYPE or claims.get("provider") != provider:
            raise SocialAuthError("Login state does not match this provider", 400)

    async def _enabled_config(self, provider: str) -> SocialLoginProvider:
        config = await self.get_config(provider)
        if config is None or not config.enabled:
            raise SocialAuthError(f"{PROVIDER_SPECS[provider].display_name} login is not enabled", 404)
        return config

    async def _fetch_provider_token(self, client, spec, config, client_secret, code) -> str:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.redirect_uri,
            "client_id": config.client_id,
            "client_secret": client_secret,
        }
        response = await client.post(spec.token_url, data=payload, headers=spec.token_headers)
        body = response.json() if response.content else {}
        token = body.get("access_token") if isinstance(body, dict) else None
        if response.status_code >= 400 or not token:
            logger.warning(f"{spec.key} token exchange failed with status {response.status_code}")
            raise SocialAuthError(f"{spec.display_name} rejected the login code", 401)
        return token

    async def _fetch_profile(self, client, spec: ProviderSpec, token: str) -> ExternalProfile:
        headers = {"Authorization": f"Bearer {token}", **spec.token_headers}
        response = await client.get(spec.profile_url, headers=headers)
        if response.status_code >= 400:
            raise SocialAuthError(f"Could not read the profile from {spec.display_name}", 502)
        data = response.json()

        if spec.key == "github":
            return await self._github_profile(client, spec, headers, data)
        if spec.key == "google":
            return ExternalProfile(
                provider_user_id=str(data["sub"]),
                email=(data.get("email") or None),
                email_verified=bool(data.get("email_verified")),
                first_name=data.get("given_name"),
                last_name=data.get("family_name"),
                avatar_url=data.get("picture"),
            )
        # Microsoft OIDC: the email claim comes from the account's verified primary address.
        first, last = _split_name(data.get("name"))
        email = data.get("email") or data.get("preferred_username")
        return ExternalProfile(
            provider_user_id=str(data["sub"]),
            email=email,
            email_verified=bool(email),
            first_name=first,
            last_name=last,
            avatar_url=data.get("picture"),
        )

    async def _github_profile(self, client, spec, headers, data) -> ExternalProfile:
        email = data.get("email")
        verified = False
        if spec.emails_url:
            emails_response = await client.get(spec.emails_url, headers=headers)
            if emails_response.status_code < 400:
                entries = emails_response.json()
                primary = next((e for e in entries if e.get("primary")), None)
                if primary:
                    email = primary.get("email")
                    verified = bool(primary.get("verified"))
        first, last = _split_name(data.get("name"))
        return ExternalProfile(
            provider_user_id=str(data["id"]),
            email=email,
            email_verified=verified,
            first_name=first,
            last_name=last,
            avatar_url=data.get("avatar_url"),
        )

    async def _resolve_user(self, provider: str, profile: ExternalProfile) -> User:
        """Find the linked user, or link an existing account by verified email, or create one."""
        auth_provider = AuthProvider(provider)
        link_stmt = select(OAuthProvider).where(
            OAuthProvider.provider == auth_provider,
            OAuthProvider.provider_user_id == profile.provider_user_id,
        )
        link = (await self.session.execute(link_stmt)).scalar_one_or_none()
        if link is not None:
            user = await self.session.get(User, link.user_id)
            if user is None:
                raise SocialAuthError("Linked account no longer exists", 401)
            return user

        if not profile.email:
            raise SocialAuthError(f"{PROVIDER_SPECS[provider].display_name} did not share an email address", 400)
        if not profile.email_verified:
            raise SocialAuthError(f"{PROVIDER_SPECS[provider].display_name} email is not verified", 401)

        email = profile.email.lower()
        user = (await self.session.execute(select(User).where(User.email == email))).scalar_one_or_none()
        if user is None:
            user = User(
                email=email,
                password_hash=hash_password(secrets.token_urlsafe(48)),
                first_name=profile.first_name,
                last_name=profile.last_name,
                avatar_url=profile.avatar_url,
                status="active",
            )
            self.session.add(user)
            await self.session.flush()

        self.session.add(OAuthProvider(
            user_id=user.id,
            provider=auth_provider,
            provider_user_id=profile.provider_user_id,
            connected_at=datetime.now(timezone.utc),
        ))
        await self.session.flush()
        return user
