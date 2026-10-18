"""Social login endpoints (public login flow) and admin management of provider credentials."""

from app.core.security import get_current_user
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse
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
    """Local JWTs, or ``handoff=True`` when the tokens were parked for a mobile ticket."""

    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    handoff: bool = False


class HandoffPendingResponse(BaseModel):
    status: str = "pending"


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


TICKET_LENGTH = {"min_length": 32, "max_length": 128}


@router.get("/{provider}/authorize", response_model=AuthorizationUrlResponse)
async def get_authorization_url(
    provider: str,
    ticket: Optional[str] = Query(None, **TICKET_LENGTH, description="Mobile handoff ticket chosen by the app"),
    session: AsyncSession = Depends(get_db),
):
    """Consent URL the browser should be sent to for the given provider.

    Mobile apps pass a random ``ticket`` they keep to themselves and later claim the
    tokens with ``GET /auth/social/handoff/{ticket}``.
    """
    try:
        url = await SocialAuthService(session).build_authorization_url(provider, ticket=ticket)
    except SocialAuthError as error:
        _raise(error)
    return {"authorization_url": url}


@router.get(
    "/handoff/{ticket}",
    response_model=SocialTokenResponse,
    response_model_exclude_none=True,
    responses={202: {"model": HandoffPendingResponse}},
)
async def claim_handoff(
    ticket: str = Path(**TICKET_LENGTH),
    session: AsyncSession = Depends(get_db),
):
    """Tokens for a mobile sign-in. 202 while the browser step is still pending; 404 if unknown or expired.

    The tokens are returned once and then removed.
    """
    try:
        tokens = await SocialAuthService(session).claim_handoff(ticket)
    except SocialAuthError as error:
        _raise(error)
    if tokens is None:
        return JSONResponse(status_code=202, content={"status": "pending"})
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}


@router.post("/{provider}/exchange", response_model=SocialTokenResponse, response_model_exclude_none=True)
async def exchange_social_code(
    provider: str,
    payload: SocialExchangeRequest,
    session: AsyncSession = Depends(get_db),
):
    """Complete the login: exchange the provider code and return local JWTs.

    For a mobile sign-in (state carries a ticket) the JWTs are parked for the app and the
    response only says ``handoff: true``.
    """
    try:
        access, refresh, _user = await SocialAuthService(session).exchange_code(
            provider, payload.code, payload.state
        )
    except SocialAuthError as error:
        _raise(error)
    if access is None:
        return {"handoff": True}
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@admin_router.get("", response_model=list[SocialProviderAdminView])
async def list_social_providers(
    _admin: User = Depends(require_social_admin),
    session: AsyncSession = Depends(get_db),
 current_user: User = Depends(get_current_user),):
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
