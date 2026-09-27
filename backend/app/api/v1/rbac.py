"""RBAC endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.rbac_service import RBACService
from app.core.security import decode_token
from pydantic import BaseModel
from typing import List

router = APIRouter()


class PermissionCreate(BaseModel):
    name: str
    resource: str
    action: str
    category: str = None
    description: str = None


class RoleCreate(BaseModel):
    name: str
    description: str = None


class PermissionResponse(BaseModel):
    id: int
    name: str
    resource: str
    action: str
    category: str = None

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str = None
    is_system: bool

    class Config:
        from_attributes = True


async def get_current_user_id(authorization: str = None) -> int:
    """Get current user ID from token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("user_id")


@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    request: PermissionCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create new permission"""
    rbac = RBACService(session)
    return await rbac.create_permission(
        request.name,
        request.resource,
        request.action,
        request.category,
        request.description,
    )


@router.get("/permissions", response_model=List[PermissionResponse])
async def list_permissions(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """List all permissions"""
    rbac = RBACService(session)
    return await rbac.get_permissions(skip, limit)


@router.post("/roles", response_model=RoleResponse)
async def create_role(
    request: RoleCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create new role"""
    rbac = RBACService(session)
    return await rbac.create_role(request.name, request.description)


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """List all roles"""
    rbac = RBACService(session)
    return await rbac.get_roles(skip, limit)


@router.post("/roles/{role_id}/permissions/{permission_id}")
async def grant_permission_to_role(
    role_id: int,
    permission_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Grant permission to role"""
    rbac = RBACService(session)
    await rbac.grant_permission_to_role(role_id, permission_id)
    return {"message": "Permission granted"}


@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def revoke_permission_from_role(
    role_id: int,
    permission_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Revoke permission from role"""
    rbac = RBACService(session)
    await rbac.revoke_permission_from_role(role_id, permission_id)
    return {"message": "Permission revoked"}


@router.post("/users/{user_id}/roles/{role_id}")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Assign role to user"""
    rbac = RBACService(session)
    await rbac.assign_role_to_user(user_id, role_id)
    return {"message": "Role assigned"}


@router.delete("/users/{user_id}/roles/{role_id}")
async def revoke_role_from_user(
    user_id: int,
    role_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Revoke role from user"""
    rbac = RBACService(session)
    await rbac.revoke_role_from_user(user_id, role_id)
    return {"message": "Role revoked"}


@router.get("/users/{user_id}/roles", response_model=List[RoleResponse])
async def get_user_roles(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get user roles"""
    rbac = RBACService(session)
    return await rbac.get_user_roles(user_id)


@router.post("/check-permission")
async def check_permission(
    resource: str,
    action: str,
    authorization: str = None,
    session: AsyncSession = Depends(get_session),
):
    """Check if user has permission"""
    user_id = await get_current_user_id(authorization)
    rbac = RBACService(session, user_id)
    has_perm = await rbac.has_permission(user_id, resource, action)
    return {"has_permission": has_perm}
