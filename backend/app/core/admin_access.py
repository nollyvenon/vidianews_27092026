"""Admin access guard shared by administrative endpoints.

A user is an administrator when they hold an ``admin`` or ``super_admin`` role in
either role system (legacy ``roles``/``user_roles`` or RBAC ``rbac_roles``/
``rbac_user_roles``), or when they hold the RBAC permission ``<resource>:manage``.
"""

from typing import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.rbac import Role as RBACRole, user_roles as rbac_user_roles
from app.models.user import Role, User, user_roles
from app.services.rbac_service import RBACService

ADMIN_ROLE_NAMES = frozenset({"admin", "super_admin"})
MANAGE_ACTION = "manage"


async def _role_names(session: AsyncSession, user_id: int) -> set:
    legacy = (await session.execute(
        select(Role.name)
        .join(user_roles, user_roles.c.role_id == Role.id)
        .where(user_roles.c.user_id == user_id)
    )).scalars().all()
    rbac = (await session.execute(
        select(RBACRole.name)
        .join(rbac_user_roles, rbac_user_roles.c.role_id == RBACRole.id)
        .where(rbac_user_roles.c.user_id == user_id)
    )).scalars().all()
    return {*legacy, *rbac}


def require_admin(resource: str) -> Callable:
    """Build a FastAPI dependency that admits admins and holders of ``resource:manage``."""

    async def dependency(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
    ) -> User:
        if ADMIN_ROLE_NAMES & await _role_names(session, user.id):
            return user
        if await RBACService(session).has_permission(user.id, resource, MANAGE_ACTION):
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return dependency
