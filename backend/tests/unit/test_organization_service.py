"""Unit tests for OrganizationService"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.organization_service import OrganizationService
from app.services.tenant_service import TenantService
from app.models.organizations import Organization, OrganizationMember
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError
from app.core.security import hash_password


@pytest.fixture
async def test_tenant_and_users(session: AsyncSession):
    """Create test tenant and users"""
    # Create users
    user1 = User(
        email="user1@test.com",
        password_hash=hash_password("pass"),
        first_name="User",
        last_name="One",
        status="active",
    )
    user2 = User(
        email="user2@test.com",
        password_hash=hash_password("pass"),
        first_name="User",
        last_name="Two",
        status="active",
    )
    session.add_all([user1, user2])
    await session.flush()

    # Create tenant
    tenant_service = TenantService(session)
    tenant = await tenant_service.create_tenant("Test Tenant", "test-tenant", user1.id)

    return tenant, user1, user2


class TestCreateOrganization:
    async def test_create_organization(self, session: AsyncSession, test_tenant_and_users):
        """Test creating organization"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        org = await service.create_organization(
            tenant_id=tenant.id,
            name="Engineering",
            slug="engineering",
            user_id=user.id,
        )

        assert org.id is not None
        assert org.name == "Engineering"
        assert org.tenant_id == tenant.id

    async def test_create_duplicate_slug(self, session: AsyncSession, test_tenant_and_users):
        """Test duplicate slug in same tenant"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        await service.create_organization(tenant.id, "Dept1", "dept", user.id)

        with pytest.raises(ConflictError):
            await service.create_organization(tenant.id, "Dept2", "dept", user.id)


class TestOrganizationHierarchy:
    async def test_create_with_parent(self, session: AsyncSession, test_tenant_and_users):
        """Test creating child organization"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        parent = await service.create_organization(tenant.id, "Parent", "parent", user.id)
        child = await service.create_organization(
            tenant.id, "Child", "child", user.id, parent_id=parent.id
        )

        assert child.parent_id == parent.id

    async def test_get_hierarchy(self, session: AsyncSession, test_tenant_and_users):
        """Test getting org hierarchy"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        parent = await service.create_organization(tenant.id, "Parent", "parent", user.id)
        child = await service.create_organization(
            tenant.id, "Child", "child", user.id, parent_id=parent.id
        )

        hierarchy = await service.get_organization_hierarchy(child.id)

        assert hierarchy["parent"].id == parent.id
        assert len(hierarchy["children"]) == 0

    async def test_move_organization(self, session: AsyncSession, test_tenant_and_users):
        """Test moving org in hierarchy"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        parent1 = await service.create_organization(tenant.id, "P1", "p1", user.id)
        parent2 = await service.create_organization(tenant.id, "P2", "p2", user.id)
        child = await service.create_organization(
            tenant.id, "Child", "child", user.id, parent_id=parent1.id
        )

        moved = await service.move_organization(child.id, parent2.id)

        assert moved.parent_id == parent2.id


class TestMembers:
    async def test_add_member(self, session: AsyncSession, test_tenant_and_users):
        """Test adding member"""
        tenant, user1, user2 = test_tenant_and_users
        service = OrganizationService(session)

        org = await service.create_organization(tenant.id, "Test", "test", user1.id)
        member = await service.add_member(org.id, user2.id, "editor")

        assert member.user_id == user2.id
        assert member.role == "editor"

    async def test_get_members(self, session: AsyncSession, test_tenant_and_users):
        """Test listing members"""
        tenant, user1, user2 = test_tenant_and_users
        service = OrganizationService(session)

        org = await service.create_organization(tenant.id, "Test", "test", user1.id)
        await service.add_member(org.id, user2.id)

        members = await service.get_organization_members(org.id)

        assert len(members) == 2
        user_ids = [m.user_id for m in members]
        assert user1.id in user_ids
        assert user2.id in user_ids


class TestInvitations:
    async def test_invite_user(self, session: AsyncSession, test_tenant_and_users):
        """Test inviting user"""
        tenant, user, _ = test_tenant_and_users
        service = OrganizationService(session)

        org = await service.create_organization(tenant.id, "Test", "test", user.id)
        invitation = await service.invite_user(org.id, "new@test.com", "member")

        assert invitation.email == "new@test.com"
        assert invitation.token is not None
        assert invitation.accepted_at is None


class TestUserOrganizations:
    async def test_get_user_orgs(self, session: AsyncSession, test_tenant_and_users):
        """Test getting user's organizations"""
        tenant, user1, user2 = test_tenant_and_users
        service = OrganizationService(session)

        org1 = await service.create_organization(tenant.id, "Org1", "org1", user1.id)
        org2 = await service.create_organization(tenant.id, "Org2", "org2", user1.id)
        await service.add_member(org1.id, user2.id)

        user1_orgs = await service.get_user_organizations(tenant.id, user1.id)
        user2_orgs = await service.get_user_organizations(tenant.id, user2.id)

        assert len(user1_orgs) >= 2
        assert len(user2_orgs) >= 1
