"""Organization API endpoints"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.organization_service import OrganizationService
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError, ValidationError
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


# Schemas
class OrganizationCreate(BaseModel):
    tenant_id: int
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    org_type: str = "department"
    parent_id: Optional[int] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    org_type: Optional[str] = None
    parent_id: Optional[int] = None


class OrganizationResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    slug: str
    description: Optional[str]
    logo_url: Optional[str]
    website: Optional[str]
    status: str
    org_type: str
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationMemberResponse(BaseModel):
    id: int
    organization_id: int
    user_id: int
    role: str
    is_lead: bool
    status: str
    joined_at: datetime

    class Config:
        from_attributes = True


class OrganizationInviteRequest(BaseModel):
    email: EmailStr
    role: str = "member"


class OrganizationInvitationResponse(BaseModel):
    id: int
    organization_id: int
    email: str
    role: str
    token: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    data: list[OrganizationResponse]
    total: int
    skip: int
    limit: int


# Endpoints
@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new organization"""
    try:
        service = OrganizationService(session)
        result = await service.create_organization(
            tenant_id=org.tenant_id,
            name=org.name,
            slug=org.slug,
            user_id=current_user.id,
            description=org.description,
            logo_url=org.logo_url,
            website=org.website,
            org_type=org.org_type,
            parent_id=org.parent_id,
        )
        return result
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=OrganizationListResponse)
async def list_organizations(
    tenant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    org_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """List organizations in tenant"""
    service = OrganizationService(session)
    orgs, total = await service.list_organizations(
        tenant_id=tenant_id,
        skip=skip,
        limit=limit,
        status=status,
        org_type=org_type,
    )
    return OrganizationListResponse(data=orgs, total=total, skip=skip, limit=limit)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get organization details"""
    try:
        service = OrganizationService(session)
        return await service.get_organization(org_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update organization"""
    try:
        service = OrganizationService(session)
        return await service.update_organization(org_id, **org_update.dict(exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete organization"""
    try:
        service = OrganizationService(session)
        await service.delete_organization(org_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Member endpoints
@router.post("/{org_id}/members", response_model=OrganizationMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    org_id: int,
    user_id: int = Query(...),
    role: str = Query("member"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add member to organization"""
    try:
        service = OrganizationService(session)
        return await service.add_member(org_id, user_id, role)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{org_id}/members", response_model=list[OrganizationMemberResponse])
async def list_members(
    org_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """List organization members"""
    try:
        service = OrganizationService(session)
        return await service.get_organization_members(org_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{org_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    org_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Remove member from organization"""
    try:
        service = OrganizationService(session)
        await service.remove_member(org_id, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# Invitation endpoints
@router.post("/{org_id}/invite", response_model=OrganizationInvitationResponse, status_code=status.HTTP_201_CREATED)
async def invite_user(
    org_id: int,
    invite: OrganizationInviteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Invite user to organization"""
    try:
        service = OrganizationService(session)
        return await service.invite_user(org_id, invite.email, invite.role, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Hierarchy endpoints
@router.get("/{org_id}/hierarchy", response_model=dict)
async def get_hierarchy(
    org_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get organization hierarchy"""
    try:
        service = OrganizationService(session)
        result = await service.get_organization_hierarchy(org_id)
        return {
            "organization": result["organization"],
            "parent": result["parent"],
            "children": result["children"],
        }
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{org_id}/move", response_model=OrganizationResponse)
async def move_organization(
    org_id: int,
    parent_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Move organization in hierarchy"""
    try:
        service = OrganizationService(session)
        return await service.move_organization(org_id, parent_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Settings endpoints
@router.get("/{org_id}/settings/{key}")
async def get_setting(
    org_id: int,
    key: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get organization setting"""
    try:
        service = OrganizationService(session)
        return await service.get_organization_setting(org_id, key)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{org_id}/settings/{key}")
async def update_setting(
    org_id: int,
    key: str,
    value: dict,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update organization setting"""
    try:
        service = OrganizationService(session)
        return await service.set_organization_setting(org_id, key, value)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
