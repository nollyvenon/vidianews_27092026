"""Tenant API endpoints"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.tenant_service import TenantService
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError, ValidationError
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])


# Request/Response schemas
class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    plan: str = "free"


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    plan: Optional[str] = None


class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    logo_url: Optional[str]
    website: Optional[str]
    status: str
    plan: str
    max_users: int
    max_storage_gb: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantMemberCreate(BaseModel):
    user_id: int
    role: str = "member"


class TenantMemberResponse(BaseModel):
    id: int
    tenant_id: int
    user_id: int
    role: str
    is_owner: bool
    status: str
    joined_at: datetime

    class Config:
        from_attributes = True


class TenantInviteRequest(BaseModel):
    email: EmailStr
    role: str = "member"


class TenantInvitationResponse(BaseModel):
    id: int
    tenant_id: int
    email: str
    role: str
    token: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class TenantSettingRequest(BaseModel):
    key: str
    value: dict


class TenantSettingResponse(BaseModel):
    key: str
    value: dict

    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    data: list[TenantResponse]
    total: int
    skip: int
    limit: int


# Dependency for authorization
async def verify_tenant_owner(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    """Verify user is owner of tenant"""
    service = TenantService(session)
    tenant = await service.get_tenant(tenant_id)
    members = await service.get_tenant_members(tenant_id)

    is_owner = any(m.user_id == current_user.id and m.is_owner for m in members)
    if not is_owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


async def verify_tenant_member(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    """Verify user is member of tenant"""
    service = TenantService(session)
    members = await service.get_tenant_members(tenant_id)

    is_member = any(m.user_id == current_user.id and m.status == "active" for m in members)
    if not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a tenant member")


# Endpoints
@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant: TenantCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new tenant"""
    try:
        service = TenantService(session)
        result = await service.create_tenant(
            name=tenant.name,
            slug=tenant.slug,
            user_id=current_user.id,
            description=tenant.description,
            logo_url=tenant.logo_url,
            website=tenant.website,
            plan=tenant.plan,
        )
        return result
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("", response_model=TenantListResponse)
async def list_tenants(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    plan: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """List user's tenants"""
    service = TenantService(session)
    tenants, total = await service.list_tenants(skip=skip, limit=limit, status=status, plan=plan)

    return TenantListResponse(data=tenants, total=total, skip=skip, limit=limit)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_member),
):
    """Get tenant details"""
    try:
        service = TenantService(session)
        return await service.get_tenant(tenant_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    tenant_update: TenantUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Update tenant"""
    try:
        service = TenantService(session)
        return await service.update_tenant(tenant_id, **tenant_update.dict(exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Delete tenant"""
    try:
        service = TenantService(session)
        await service.delete_tenant(tenant_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Member endpoints
@router.post("/{tenant_id}/members", response_model=TenantMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    tenant_id: int,
    member: TenantMemberCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Add member to tenant"""
    try:
        service = TenantService(session)
        return await service.add_member(tenant_id, member.user_id, member.role)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{tenant_id}/members", response_model=list[TenantMemberResponse])
async def list_members(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_member),
):
    """List tenant members"""
    try:
        service = TenantService(session)
        return await service.get_tenant_members(tenant_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{tenant_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    tenant_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Remove member from tenant"""
    try:
        service = TenantService(session)
        await service.remove_member(tenant_id, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# Invitation endpoints
@router.post("/{tenant_id}/invite", response_model=TenantInvitationResponse, status_code=status.HTTP_201_CREATED)
async def invite_user(
    tenant_id: int,
    invite: TenantInviteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Invite user to tenant"""
    try:
        service = TenantService(session)
        return await service.invite_user(tenant_id, invite.email, invite.role, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Settings endpoints
@router.get("/{tenant_id}/settings/{key}", response_model=TenantSettingResponse)
async def get_setting(
    tenant_id: int,
    key: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_member),
):
    """Get tenant setting"""
    try:
        service = TenantService(session)
        return await service.get_tenant_setting(tenant_id, key)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{tenant_id}/settings/{key}", response_model=TenantSettingResponse)
async def update_setting(
    tenant_id: int,
    key: str,
    setting: TenantSettingRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    _=Depends(verify_tenant_owner),
):
    """Update tenant setting"""
    try:
        service = TenantService(session)
        return await service.set_tenant_setting(tenant_id, key, setting.value)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
