"""Organization service for managing organizations within tenants"""

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.organizations import Organization, OrganizationMember, OrganizationSettings, OrganizationInvitation
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError, ValidationError
from app.utils.logger import logger
import secrets


class OrganizationService:
    """Service for managing organizations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_organization(
        self,
        tenant_id: int,
        name: str,
        slug: str,
        user_id: int,
        description: str = None,
        logo_url: str = None,
        website: str = None,
        org_type: str = "department",
        parent_id: int = None,
        settings: dict = None,
    ) -> Organization:
        """Create new organization within tenant"""
        # Verify tenant exists and user is member
        from app.services.tenant_service import TenantService
        tenant_service = TenantService(self.session)
        await tenant_service.get_tenant(tenant_id)

        # Check if slug is unique within tenant
        stmt = select(Organization).where(
            and_(Organization.tenant_id == tenant_id, Organization.slug == slug)
        )
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError(f"Organization slug '{slug}' already exists in this tenant")

        # Validate parent organization if provided
        if parent_id:
            parent = await self.get_organization(parent_id)
            if parent.tenant_id != tenant_id:
                raise ValidationError("Parent organization must be in same tenant")

        organization = Organization(
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            description=description,
            logo_url=logo_url,
            website=website,
            org_type=org_type,
            parent_id=parent_id,
            settings=settings or {},
        )
        self.session.add(organization)
        await self.session.flush()

        # Add creator as lead
        member = OrganizationMember(
            organization_id=organization.id,
            user_id=user_id,
            role="admin",
            is_lead=True,
            status="active",
        )
        self.session.add(member)
        await self.session.commit()

        logger.info(f"Organization created: {organization.id} ({name}) in tenant {tenant_id}")
        return organization

    async def get_organization(self, org_id: int) -> Organization:
        """Get organization by ID"""
        stmt = select(Organization).where(Organization.id == org_id)
        org = (await self.session.execute(stmt)).scalar_one_or_none()
        if not org:
            raise NotFoundError(f"Organization {org_id} not found")
        return org

    async def get_organization_by_slug(self, tenant_id: int, slug: str) -> Organization:
        """Get organization by slug within tenant"""
        stmt = select(Organization).where(
            and_(Organization.tenant_id == tenant_id, Organization.slug == slug)
        )
        org = (await self.session.execute(stmt)).scalar_one_or_none()
        if not org:
            raise NotFoundError(f"Organization '{slug}' not found in tenant")
        return org

    async def update_organization(self, org_id: int, **kwargs) -> Organization:
        """Update organization"""
        org = await self.get_organization(org_id)

        # Validate slug uniqueness if being changed
        if "slug" in kwargs and kwargs["slug"] != org.slug:
            stmt = select(Organization).where(
                and_(Organization.tenant_id == org.tenant_id, Organization.slug == kwargs["slug"])
            )
            existing = (await self.session.execute(stmt)).scalar_one_or_none()
            if existing:
                raise ConflictError(f"Organization slug '{kwargs['slug']}' already exists")

        # Validate parent organization if being changed
        if "parent_id" in kwargs and kwargs["parent_id"]:
            parent = await self.get_organization(kwargs["parent_id"])
            if parent.tenant_id != org.tenant_id:
                raise ValidationError("Parent organization must be in same tenant")

        for key, value in kwargs.items():
            if hasattr(org, key):
                setattr(org, key, value)

        org.updated_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Organization updated: {org_id}")
        return org

    async def delete_organization(self, org_id: int) -> None:
        """Soft delete organization"""
        org = await self.get_organization(org_id)
        org.deleted_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Organization deleted: {org_id}")

    async def list_organizations(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        status: str = None,
        org_type: str = None,
        parent_id: int = None,
    ) -> tuple[list[Organization], int]:
        """List organizations in tenant"""
        filters = [Organization.tenant_id == tenant_id]
        if status:
            filters.append(Organization.status == status)
        if org_type:
            filters.append(Organization.org_type == org_type)
        if parent_id is not None:
            filters.append(Organization.parent_id == parent_id)

        # Count total
        count_stmt = select(func.count(Organization.id)).where(and_(*filters))
        total = (await self.session.execute(count_stmt)).scalar()

        # Get paginated results
        stmt = select(Organization).where(and_(*filters)).offset(skip).limit(limit)
        orgs = (await self.session.execute(stmt)).scalars().all()

        return orgs, total

    async def add_member(
        self,
        org_id: int,
        user_id: int,
        role: str = "member",
        is_lead: bool = False,
    ) -> OrganizationMember:
        """Add user to organization"""
        await self.get_organization(org_id)

        # Check if user exists
        user_stmt = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_stmt)).scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User {user_id} not found")

        # Check if already member
        stmt = select(OrganizationMember).where(
            and_(OrganizationMember.organization_id == org_id, OrganizationMember.user_id == user_id)
        )
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("User already member of organization")

        member = OrganizationMember(
            organization_id=org_id,
            user_id=user_id,
            role=role,
            is_lead=is_lead,
            status="active",
        )
        self.session.add(member)
        await self.session.commit()

        logger.info(f"Member added to organization {org_id}: user {user_id}")
        return member

    async def remove_member(self, org_id: int, user_id: int) -> None:
        """Remove user from organization"""
        stmt = select(OrganizationMember).where(
            and_(OrganizationMember.organization_id == org_id, OrganizationMember.user_id == user_id)
        )
        member = (await self.session.execute(stmt)).scalar_one_or_none()
        if not member:
            raise NotFoundError("Member not found in organization")

        if member.is_lead:
            raise UnauthorizedError("Cannot remove lead from organization")

        member.status = "inactive"
        member.left_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Member removed from organization {org_id}: user {user_id}")

    async def invite_user(
        self,
        org_id: int,
        email: str,
        role: str = "member",
        invited_by: int = None,
    ) -> OrganizationInvitation:
        """Invite user to organization"""
        await self.get_organization(org_id)

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        invitation = OrganizationInvitation(
            organization_id=org_id,
            email=email,
            role=role,
            token=token,
            invited_by=invited_by,
            expires_at=expires_at,
        )
        self.session.add(invitation)
        await self.session.commit()

        logger.info(f"User invited to organization {org_id}: {email}")
        return invitation

    async def accept_invitation(self, token: str, user_id: int) -> OrganizationMember:
        """Accept organization invitation"""
        stmt = select(OrganizationInvitation).where(
            and_(
                OrganizationInvitation.token == token,
                OrganizationInvitation.accepted_at == None,
                OrganizationInvitation.expires_at > datetime.now(timezone.utc),
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
        member = OrganizationMember(
            organization_id=invitation.organization_id,
            user_id=user_id,
            role=invitation.role,
            status="active",
            invited_at=invitation.created_at,
        )
        self.session.add(member)

        invitation.accepted_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Invitation accepted for organization {invitation.organization_id}: user {user_id}")
        return member

    async def get_user_organizations(self, tenant_id: int, user_id: int) -> list[Organization]:
        """Get all organizations for a user in a tenant"""
        stmt = (
            select(Organization)
            .join(OrganizationMember)
            .where(
                and_(
                    Organization.tenant_id == tenant_id,
                    OrganizationMember.user_id == user_id,
                    OrganizationMember.status == "active",
                )
            )
        )
        orgs = (await self.session.execute(stmt)).scalars().all()
        return orgs

    async def get_organization_members(self, org_id: int) -> list[OrganizationMember]:
        """Get all members of an organization"""
        await self.get_organization(org_id)

        stmt = select(OrganizationMember).where(
            and_(OrganizationMember.organization_id == org_id, OrganizationMember.status == "active")
        )
        members = (await self.session.execute(stmt)).scalars().all()
        return members

    async def get_organization_hierarchy(self, org_id: int) -> dict:
        """Get organization hierarchy (parent and children)"""
        org = await self.get_organization(org_id)

        # Get parent
        parent = None
        if org.parent_id:
            parent = await self.get_organization(org.parent_id)

        # Get children
        stmt = select(Organization).where(Organization.parent_id == org_id)
        children = (await self.session.execute(stmt)).scalars().all()

        return {
            "organization": org,
            "parent": parent,
            "children": children,
        }

    async def move_organization(self, org_id: int, new_parent_id: int = None) -> Organization:
        """Move organization in hierarchy"""
        org = await self.get_organization(org_id)

        # Validate new parent
        if new_parent_id:
            parent = await self.get_organization(new_parent_id)
            if parent.tenant_id != org.tenant_id:
                raise ValidationError("Parent must be in same tenant")
            if parent.id == org_id:
                raise ValidationError("Cannot be own parent")

        org.parent_id = new_parent_id
        await self.session.commit()

        logger.info(f"Organization moved: {org_id} to parent {new_parent_id}")
        return org

    async def set_organization_setting(self, org_id: int, key: str, value: dict) -> OrganizationSettings:
        """Set or update organization setting"""
        await self.get_organization(org_id)

        stmt = select(OrganizationSettings).where(
            and_(OrganizationSettings.organization_id == org_id, OrganizationSettings.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()

        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = OrganizationSettings(organization_id=org_id, key=key, value=value)
            self.session.add(setting)

        await self.session.commit()
        return setting

    async def get_organization_setting(self, org_id: int, key: str) -> dict:
        """Get specific organization setting"""
        stmt = select(OrganizationSettings).where(
            and_(OrganizationSettings.organization_id == org_id, OrganizationSettings.key == key)
        )
        setting = (await self.session.execute(stmt)).scalar_one_or_none()
        if not setting:
            raise NotFoundError(f"Setting '{key}' not found")
        return {"key": setting.key, "value": setting.value}
