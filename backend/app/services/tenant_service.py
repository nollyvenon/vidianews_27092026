"""Tenant service for multi-tenancy management"""

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.tenants import Tenant, TenantMember, TenantSettings, TenantInvitation
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError, ValidationError
from app.utils.logger import logger
import secrets
import string


class TenantService:
    """Service for managing tenants and multi-tenancy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tenant(
        self,
        name: str,
        slug: str,
        user_id: int,
        description: str = None,
        logo_url: str = None,
        website: str = None,
        plan: str = "free",
        settings: dict = None,
    ) -> Tenant:
        """Create new tenant"""
        # Check if slug already exists
        stmt = select(Tenant).where(Tenant.slug == slug)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError(f"Tenant slug '{slug}' already exists")

        tenant = Tenant(
            name=name,
            slug=slug,
            description=description,
            logo_url=logo_url,
            website=website,
            plan=plan,
            settings=settings or {},
        )
        self.session.add(tenant)
        await self.session.flush()

        # Add creator as owner
        member = TenantMember(
            tenant_id=tenant.id,
            user_id=user_id,
            role="admin",
            is_owner=True,
            status="active",
        )
        self.session.add(member)
        await self.session.commit()

        logger.info(f"Tenant created: {tenant.id} ({name}) by user {user_id}")
        return tenant

    async def get_tenant(self, tenant_id: int) -> Tenant:
        """Get tenant by ID"""
        stmt = select(Tenant).where(Tenant.id == tenant_id)
        tenant = (await self.session.execute(stmt)).scalar_one_or_none()
        if not tenant:
            raise NotFoundError(f"Tenant {tenant_id} not found")
        return tenant

    async def get_tenant_by_slug(self, slug: str) -> Tenant:
        """Get tenant by slug"""
        stmt = select(Tenant).where(Tenant.slug == slug)
        tenant = (await self.session.execute(stmt)).scalar_one_or_none()
        if not tenant:
            raise NotFoundError(f"Tenant '{slug}' not found")
        return tenant

    async def update_tenant(self, tenant_id: int, **kwargs) -> Tenant:
        """Update tenant"""
        tenant = await self.get_tenant(tenant_id)

        # Validate slug uniqueness if being changed
        if "slug" in kwargs and kwargs["slug"] != tenant.slug:
            stmt = select(Tenant).where(Tenant.slug == kwargs["slug"])
            existing = (await self.session.execute(stmt)).scalar_one_or_none()
            if existing:
                raise ConflictError(f"Tenant slug '{kwargs['slug']}' already exists")

        for key, value in kwargs.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)

        tenant.updated_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Tenant updated: {tenant_id}")
        return tenant

    async def delete_tenant(self, tenant_id: int) -> None:
        """Soft delete tenant"""
        tenant = await self.get_tenant(tenant_id)
        tenant.deleted_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Tenant deleted: {tenant_id}")

    async def list_tenants(
        self,
        skip: int = 0,
        limit: int = 20,
        status: str = None,
        plan: str = None,
    ) -> tuple[list[Tenant], int]:
        """List tenants with pagination"""
        filters = []
        if status:
            filters.append(Tenant.status == status)
        if plan:
            filters.append(Tenant.plan == plan)

        # Count total
        count_stmt = select(func.count(Tenant.id)).where(and_(*filters) if filters else True)
        total = (await self.session.execute(count_stmt)).scalar()

        # Get paginated results
        stmt = select(Tenant).where(and_(*filters) if filters else True).offset(skip).limit(limit)
        tenants = (await self.session.execute(stmt)).scalars().all()

        return tenants, total

    async def add_member(
        self,
        tenant_id: int,
        user_id: int,
        role: str = "member",
        is_owner: bool = False,
    ) -> TenantMember:
        """Add user to tenant"""
        await self.get_tenant(tenant_id)

        # Check if user exists
        user_stmt = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_stmt)).scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User {user_id} not found")

        # Check if already member
        stmt = select(TenantMember).where(
            and_(TenantMember.tenant_id == tenant_id, TenantMember.user_id == user_id)
        )
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("User already member of tenant")

        member = TenantMember(
            tenant_id=tenant_id,
            user_id=user_id,
            role=role,
            is_owner=is_owner,
            status="active",
        )
        self.session.add(member)
        await self.session.commit()

        logger.info(f"Member added to tenant {tenant_id}: user {user_id}")
        return member

    async def remove_member(self, tenant_id: int, user_id: int) -> None:
        """Remove user from tenant"""
        stmt = select(TenantMember).where(
            and_(TenantMember.tenant_id == tenant_id, TenantMember.user_id == user_id)
        )
        member = (await self.session.execute(stmt)).scalar_one_or_none()
        if not member:
            raise NotFoundError("Member not found in tenant")

        if member.is_owner:
            raise UnauthorizedError("Cannot remove owner from tenant")

        member.status = "inactive"
        member.left_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Member removed from tenant {tenant_id}: user {user_id}")

    async def invite_user(
        self,
        tenant_id: int,
        email: str,
        role: str = "member",
        invited_by: int = None,
    ) -> TenantInvitation:
        """Invite user to tenant"""
        await self.get_tenant(tenant_id)

        # Generate unique token
        token = secrets.token_urlsafe(32)

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        invitation = TenantInvitation(
            tenant_id=tenant_id,
            email=email,
            role=role,
            token=token,
            invited_by=invited_by,
            expires_at=expires_at,
        )
        self.session.add(invitation)
        await self.session.commit()

        logger.info(f"User invited to tenant {tenant_id}: {email}")
        return invitation

    async def accept_invitation(self, token: str, user_id: int) -> TenantMember:
        """Accept tenant invitation"""
        stmt = select(TenantInvitation).where(
            and_(
                TenantInvitation.token == token,
                TenantInvitation.accepted_at == None,
                TenantInvitation.expires_at > datetime.now(timezone.utc),
            )
        )
        invitation = (await self.session.execute(stmt)).scalar_one_or_none()
        if not invitation:
            raise NotFoundError("Invitation not found or expired")

        # Check user exists
        user_stmt = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_stmt)).scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User {user_id} not found")

        # Create membership
        member = TenantMember(
            tenant_id=invitation.tenant_id,
            user_id=user_id,
            role=invitation.role,
            status="active",
            invited_at=invitation.created_at,
        )
        self.session.add(member)

        invitation.accepted_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Invitation accepted for tenant {invitation.tenant_id}: user {user_id}")
        return member

    async def get_user_tenants(self, user_id: int) -> list[Tenant]:
        """Get all tenants for a user"""
        stmt = (
            select(Tenant)
            .join(TenantMember)
            .where(
                and_(
                    TenantMember.user_id == user_id,
                    TenantMember.status == "active",
                )
            )
        )
        tenants = (await self.session.execute(stmt)).scalars().all()
        return tenants

    async def get_tenant_members(self, tenant_id: int) -> list[TenantMember]:
        """Get all members of a tenant"""
        await self.get_tenant(tenant_id)

        stmt = select(TenantMember).where(
            and_(TenantMember.tenant_id == tenant_id, TenantMember.status == "active")
        )
        members = (await self.session.execute(stmt)).scalars().all()
        return members

    async def check_tenant_limit(self, tenant_id: int, resource_name: str, current_count: int) -> bool:
        """Check if tenant can create more resources"""
        tenant = await self.get_tenant(tenant_id)

        if resource_name == "users":
            return current_count < tenant.max_users
        elif resource_name == "storage":
            return current_count < tenant.max_storage_gb

        return True

    async def get_tenant_setting(self, tenant_id: int, key: str) -> dict:
        """Get specific tenant setting"""
        stmt = select(TenantSettings).where(
            and_(TenantSettings.tenant_id == tenant_id, TenantSettings.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()
        if not setting:
            raise NotFoundError(f"Setting '{key}' not found")
        return {"key": setting.key, "value": setting.value}

    async def set_tenant_setting(self, tenant_id: int, key: str, value: dict) -> TenantSettings:
        """Set or update tenant setting"""
        await self.get_tenant(tenant_id)

        stmt = select(TenantSettings).where(
            and_(TenantSettings.tenant_id == tenant_id, TenantSettings.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()

        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = TenantSettings(tenant_id=tenant_id, key=key, value=value)
            self.session.add(setting)

        await self.session.commit()
        return setting
