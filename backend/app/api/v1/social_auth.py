"""Social login endpoints (public login flow) and admin management of provider credentials."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import require_admin
from app.db.session import get_db
from app.models.user import User
from app.services.social_auth_service import SocialAuthError, SocialAuthService

router = APIRouter(prefix="/auth/social", tags=["social-auth"])
admin_router = APIRouter(prefix="/admin/social-providers", tags=["social-auth-admin"])

class SocialProviderSummary(BaseModel):
    provider: str
    display_name: str


class AuthorizationUrlResponse(BaseModel):
    authorization_url: str


class SocialExchangeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=2048)
    state: str = Field(..., min_length=1, max_length=4096)


class SocialTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SocialProviderUpdate(BaseModel):
    enabled: bool = False
    client_id: Optional[str] = Field(None, max_length=255)
    client_secret: Optional[str] = Field(None, min_length=1, max_length=512)
    redirect_uri: Optional[str] = Field(None, max_length=500)
    scopes: Optional[str] = Field(None, max_length=500)


class SocialProviderAdminView(BaseModel):
    provider: str
    display_name: str
    enabled: bool
    client_id: Optional[str]
    client_secret_set: bool
    redirect_uri: Optional[str]
    scopes: str
    updated_at: Optional[datetime]


require_social_admin = require_admin("social_login")


def _raise(error: SocialAuthError) -> None:
    raise HTTPException(status_code=error.status_code, detail=error.message)


@router.get("/providers", response_model=list[SocialProviderSummary])
async def list_enabled_providers(session: AsyncSession = Depends(get_db)):
    """Providers currently enabled for sign-in (public)."""
    return await SocialAuthService(session).list_enabled_providers()


@router.get("/{provider}/authorize", response_model=AuthorizationUrlResponse)
async def get_authorization_url(provider: str, session: AsyncSession = Depends(get_db)):
    """Consent URL the browser should be sent to for the given provider."""
    try:
        url = await SocialAuthService(session).build_authorization_url(provider)
    except SocialAuthError as error:
        _raise(error)
    return {"authorization_url": url}


@router.post("/{provider}/exchange", response_model=SocialTokenResponse)
async def exchange_social_code(
    provider: str,
    payload: SocialExchangeRequest,
    session: AsyncSession = Depends(get_db),
):
    """Complete the login: exchange the provider code and return local JWTs."""
    try:
        access, refresh, _user = await SocialAuthService(session).exchange_code(
            provider, payload.code, payload.state
        )
    except SocialAuthError as error:
        _raise(error)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@admin_router.get("", response_model=list[SocialProviderAdminView])
async def list_social_providers(
    _admin: User = Depends(require_social_admin),
    session: AsyncSession = Depends(get_db),
):
    """All supported providers with their configuration. Client secrets are never returned."""
    return await SocialAuthService(session).list_admin_view()


@admin_router.put("/{provider}", response_model=SocialProviderAdminView)
async def update_social_provider(
    provider: str,
    payload: SocialProviderUpdate,
    admin: User = Depends(require_social_admin),
    session: AsyncSession = Depends(get_db),
):
    """Create or update a provider's OAuth credentials.

    The client secret is write-only: omit it to keep the stored secret.
    Enabling a provider requires client_id, client_secret and redirect_uri.
    """
    try:
        return await SocialAuthService(session).upsert_provider(
            provider,
            actor_user_id=admin.id,
            enabled=payload.enabled,
            client_id=payload.client_id,
            client_secret=payload.client_secret,
            redirect_uri=payload.redirect_uri,
            scopes=payload.scopes,
        )
    except SocialAuthError as error:
        _raise(error)
