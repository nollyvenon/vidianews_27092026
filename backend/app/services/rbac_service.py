"""Role-Based Access Control service"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.rbac import Role, Permission, role_permissions, user_roles, ResourcePermission, AuditLog
from app.models.user import User
from app.utils.exceptions import NotFoundError, ForbiddenError, ConflictError
from app.utils.logger import logger
from datetime import datetime, timezone


class RBACService:
    """Role-Based Access Control service"""

    def __init__(self, session: AsyncSession, current_user_id: int = None):
        self.session = session
        self.current_user_id = current_user_id

    # PERMISSIONS

    async def create_permission(self, name: str, resource: str, action: str, category: str = None, description: str = None) -> Permission:
        """Create new permission"""
        stmt = select(Permission).where(Permission.name == name)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("Permission already exists")

        permission = Permission(
            name=name,
            resource=resource,
            action=action,
            category=category,
            description=description,
        )
        self.session.add(permission)
        await self.session.commit()
        logger.info(f"Permission created: {name}")
        return permission

    async def get_permissions(self, skip: int = 0, limit: int = 100):
        """List all permissions"""
        stmt = select(Permission).offset(skip).limit(limit)
        return (await self.session.execute(stmt)).scalars().all()

    # ROLES

    async def create_role(self, name: str, description: str = None, is_system: bool = False) -> Role:
        """Create new role"""
        stmt = select(Role).where(Role.name == name)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("Role already exists")

        role = Role(
            name=name,
            description=description,
            is_system=is_system,
        )
        self.session.add(role)
        await self.session.commit()

        await self._audit_log("ROLE_CREATED", "role", role.id, new_value=name)
        logger.info(f"Role created: {name}")
        return role

    async def get_role(self, role_id: int) -> Role:
        """Get role by ID"""
        role = await self.session.get(Role, role_id)
        if not role:
            raise NotFoundError("Role")
        return role

    async def get_roles(self, skip: int = 0, limit: int = 100):
        """List all roles"""
        stmt = select(Role).offset(skip).limit(limit)
        return (await self.session.execute(stmt)).scalars().all()

    async def grant_permission_to_role(self, role_id: int, permission_id: int):
        """Grant permission to role"""
        role = await self.get_role(role_id)
        permission = await self.session.get(Permission, permission_id)
        if not permission:
            raise NotFoundError("Permission")

        stmt = select(role_permissions).where(
            and_(
                role_permissions.c.role_id == role_id,
                role_permissions.c.permission_id == permission_id,
            )
        )
        existing = (await self.session.execute(stmt)).first()
        if existing:
            raise ConflictError("Permission already granted to role")

        stmt = role_permissions.insert().values(role_id=role_id, permission_id=permission_id)
        await self.session.execute(stmt)
        await self.session.commit()

        await self._audit_log("PERMISSION_GRANTED", "role", role_id, new_value=f"{role.name}:{permission.name}")
        logger.info(f"Permission {permission.name} granted to role {role.name}")

    async def revoke_permission_from_role(self, role_id: int, permission_id: int):
        """Revoke permission from role"""
        role = await self.get_role(role_id)

        stmt = role_permissions.delete().where(
            and_(
                role_permissions.c.role_id == role_id,
                role_permissions.c.permission_id == permission_id,
            )
        )
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("Role permission")

        await self.session.commit()
        await self._audit_log("PERMISSION_REVOKED", "role", role_id, new_value=f"role_id:{role_id},permission_id:{permission_id}")
        logger.info(f"Permission revoked from role {role.name}")

    # USER ROLES

    async def assign_role_to_user(self, user_id: int, role_id: int):
        """Assign role to user"""
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User")

        role = await self.get_role(role_id)

        stmt = select(user_roles).where(
            and_(
                user_roles.c.user_id == user_id,
                user_roles.c.role_id == role_id,
            )
        )
        existing = (await self.session.execute(stmt)).first()
        if existing:
            raise ConflictError("User already has this role")

        stmt = user_roles.insert().values(user_id=user_id, role_id=role_id)
        await self.session.execute(stmt)
        await self.session.commit()

        await self._audit_log("ROLE_ASSIGNED", "user", user_id, new_value=f"{user.email}:{role.name}")
        logger.info(f"Role {role.name} assigned to user {user.email}")

    async def revoke_role_from_user(self, user_id: int, role_id: int):
        """Revoke role from user"""
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User")

        stmt = user_roles.delete().where(
            and_(
                user_roles.c.user_id == user_id,
                user_roles.c.role_id == role_id,
            )
        )
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("User role")

        await self.session.commit()
        await self._audit_log("ROLE_REVOKED", "user", user_id, new_value=f"user_id:{user_id},role_id:{role_id}")
        logger.info(f"Role revoked from user {user.email}")

    async def get_user_roles(self, user_id: int):
        """Get all roles for user"""
        stmt = select(Role).join(user_roles).where(user_roles.c.user_id == user_id)
        return (await self.session.execute(stmt)).scalars().all()

    async def get_user_permissions(self, user_id: int):
        """Get all permissions for user (via roles)"""
        stmt = select(Permission).join(
            role_permissions
        ).join(
            Role
        ).join(
            user_roles
        ).where(user_roles.c.user_id == user_id)
        return (await self.session.execute(stmt)).scalars().all()

    # PERMISSION CHECKS

    async def has_permission(self, user_id: int, resource: str, action: str) -> bool:
        """Check if user has permission"""
        stmt = select(Permission).join(
            role_permissions
        ).join(
            Role
        ).join(
            user_roles
        ).where(
            and_(
                user_roles.c.user_id == user_id,
                Permission.resource == resource,
                Permission.action == action,
            )
        )
        return bool((await self.session.execute(stmt)).scalar_one_or_none())

    async def has_resource_permission(self, user_id: int, resource_type: str, resource_id: int, permission: str) -> bool:
        """Check if user has resource-level permission"""
        stmt = select(ResourcePermission).where(
            and_(
                ResourcePermission.user_id == user_id,
                ResourcePermission.resource_type == resource_type,
                ResourcePermission.resource_id == resource_id,
                ResourcePermission.permission == permission,
            )
        )
        perm = (await self.session.execute(stmt)).scalar_one_or_none()
        if not perm:
            return False
        if perm.expires_at and perm.expires_at < datetime.now(timezone.utc):
            return False
        return True

    # AUDIT LOGGING

    async def _audit_log(self, action: str, resource_type: str, resource_id: int, old_value: str = None, new_value: str = None):
        """Log permission changes"""
        log = AuditLog(
            user_id=self.current_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(log)
        await self.session.commit()
