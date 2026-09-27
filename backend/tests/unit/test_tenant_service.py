"""Unit tests for TenantService"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.tenant_service import TenantService
from app.models.tenants import Tenant, TenantMember, TenantSettings, TenantInvitation
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, UnauthorizedError
from app.core.security import hash_password


@pytest.fixture
async def test_user(session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        email="test@example.com",
        password_hash=hash_password("password"),
        first_name="Test",
        last_name="User",
        status="active",
    )
    session.add(user)
    await session.flush()
    return user


@pytest.fixture
async def test_user_2(session: AsyncSession) -> User:
    """Create second test user"""
    user = User(
        email="test2@example.com",
        password_hash=hash_password("password"),
        first_name="Test",
        last_name="User2",
        status="active",
    )
    session.add(user)
    await session.flush()
    return user


class TestCreateTenant:
    async def test_create_tenant_success(self, session: AsyncSession, test_user: User):
        """Test creating a tenant successfully"""
        service = TenantService(session)

        tenant = await service.create_tenant(
            name="Test Tenant",
            slug="test-tenant",
            user_id=test_user.id,
            plan="pro",
        )

        assert tenant.id is not None
        assert tenant.name == "Test Tenant"
        assert tenant.slug == "test-tenant"
        assert tenant.plan == "pro"
        assert tenant.status == "active"

    async def test_create_tenant_duplicate_slug(self, session: AsyncSession, test_user: User):
        """Test creating tenant with duplicate slug"""
        service = TenantService(session)

        await service.create_tenant("Tenant 1", "test-slug", test_user.id)

        with pytest.raises(ConflictError):
            await service.create_tenant("Tenant 2", "test-slug", test_user.id)

    async def test_create_tenant_adds_owner(self, session: AsyncSession, test_user: User):
        """Test that creator becomes owner"""
        service = TenantService(session)

        tenant = await service.create_tenant("Test", "test", test_user.id)
        members = await service.get_tenant_members(tenant.id)

        assert len(members) == 1
        assert members[0].user_id == test_user.id
        assert members[0].is_owner is True


class TestGetTenant:
    async def test_get_tenant_by_id(self, session: AsyncSession, test_user: User):
        """Test getting tenant by ID"""
        service = TenantService(session)
        created = await service.create_tenant("Test", "test", test_user.id)

        tenant = await service.get_tenant(created.id)
        assert tenant.id == created.id

    async def test_get_tenant_not_found(self, session: AsyncSession):
        """Test getting non-existent tenant"""
        service = TenantService(session)

        with pytest.raises(NotFoundError):
            await service.get_tenant(9999)

    async def test_get_tenant_by_slug(self, session: AsyncSession, test_user: User):
        """Test getting tenant by slug"""
        service = TenantService(session)
        created = await service.create_tenant("Test", "test-slug", test_user.id)

        tenant = await service.get_tenant_by_slug("test-slug")
        assert tenant.id == created.id

    async def test_get_tenant_by_slug_not_found(self, session: AsyncSession):
        """Test getting tenant by non-existent slug"""
        service = TenantService(session)

        with pytest.raises(NotFoundError):
            await service.get_tenant_by_slug("nonexistent")


class TestUpdateTenant:
    async def test_update_tenant(self, session: AsyncSession, test_user: User):
        """Test updating tenant"""
        service = TenantService(session)
        tenant = await service.create_tenant("Original", "original", test_user.id)

        updated = await service.update_tenant(
            tenant.id,
            name="Updated",
            description="New description",
        )

        assert updated.name == "Updated"
        assert updated.description == "New description"

    async def test_update_tenant_duplicate_slug(self, session: AsyncSession, test_user: User):
        """Test updating to duplicate slug"""
        service = TenantService(session)
        await service.create_tenant("Tenant 1", "slug1", test_user.id)
        tenant2 = await service.create_tenant("Tenant 2", "slug2", test_user.id)

        with pytest.raises(ConflictError):
            await service.update_tenant(tenant2.id, slug="slug1")


class TestDeleteTenant:
    async def test_delete_tenant(self, session: AsyncSession, test_user: User):
        """Test soft deleting tenant"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        await service.delete_tenant(tenant.id)

        # Check soft delete
        stmt = select(Tenant).where(Tenant.id == tenant.id)
        result = (await session.execute(stmt)).scalar_one_or_none()
        assert result.deleted_at is not None


class TestListTenants:
    async def test_list_tenants(self, session: AsyncSession, test_user: User):
        """Test listing tenants"""
        service = TenantService(session)
        await service.create_tenant("Tenant 1", "slug1", test_user.id)
        await service.create_tenant("Tenant 2", "slug2", test_user.id)

        tenants, total = await service.list_tenants()

        assert total >= 2
        assert len(tenants) >= 2

    async def test_list_tenants_pagination(self, session: AsyncSession, test_user: User):
        """Test pagination"""
        service = TenantService(session)
        for i in range(5):
            await service.create_tenant(f"Tenant {i}", f"slug{i}", test_user.id)

        tenants, total = await service.list_tenants(skip=0, limit=2)

        assert len(tenants) == 2


class TestMembers:
    async def test_add_member(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test adding member"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        member = await service.add_member(tenant.id, test_user_2.id, "editor")

        assert member.user_id == test_user_2.id
        assert member.role == "editor"
        assert member.status == "active"

    async def test_add_duplicate_member(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test adding duplicate member"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        await service.add_member(tenant.id, test_user_2.id)

        with pytest.raises(ConflictError):
            await service.add_member(tenant.id, test_user_2.id)

    async def test_add_nonexistent_user(self, session: AsyncSession, test_user: User):
        """Test adding non-existent user"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        with pytest.raises(NotFoundError):
            await service.add_member(tenant.id, 9999)

    async def test_remove_member(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test removing member"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)
        await service.add_member(tenant.id, test_user_2.id)

        await service.remove_member(tenant.id, test_user_2.id)

        members = await service.get_tenant_members(tenant.id)
        assert all(m.user_id != test_user_2.id for m in members)

    async def test_remove_owner(self, session: AsyncSession, test_user: User):
        """Test cannot remove owner"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        with pytest.raises(UnauthorizedError):
            await service.remove_member(tenant.id, test_user.id)

    async def test_get_tenant_members(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test getting tenant members"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)
        await service.add_member(tenant.id, test_user_2.id)

        members = await service.get_tenant_members(tenant.id)

        assert len(members) == 2
        user_ids = [m.user_id for m in members]
        assert test_user.id in user_ids
        assert test_user_2.id in user_ids


class TestInvitations:
    async def test_invite_user(self, session: AsyncSession, test_user: User):
        """Test inviting user"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        invitation = await service.invite_user(
            tenant.id,
            "invited@example.com",
            "member",
            test_user.id,
        )

        assert invitation.email == "invited@example.com"
        assert invitation.role == "member"
        assert invitation.accepted_at is None

    async def test_accept_invitation(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test accepting invitation"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        invitation = await service.invite_user(tenant.id, test_user_2.email, "editor")

        member = await service.accept_invitation(invitation.token, test_user_2.id)

        assert member.user_id == test_user_2.id
        assert member.role == "editor"

    async def test_accept_expired_invitation(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test cannot accept expired invitation"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        # Create expired invitation manually
        expired = TenantInvitation(
            tenant_id=tenant.id,
            email=test_user_2.email,
            role="member",
            token="expired-token",
            invited_by=test_user.id,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        session.add(expired)
        await session.flush()

        with pytest.raises(NotFoundError):
            await service.accept_invitation("expired-token", test_user_2.id)


class TestUserTenants:
    async def test_get_user_tenants(self, session: AsyncSession, test_user: User, test_user_2: User):
        """Test getting user's tenants"""
        service = TenantService(session)

        tenant1 = await service.create_tenant("Tenant 1", "slug1", test_user.id)
        tenant2 = await service.create_tenant("Tenant 2", "slug2", test_user_2.id)

        # Add test_user to tenant2
        await service.add_member(tenant2.id, test_user.id)

        user_tenants = await service.get_user_tenants(test_user.id)

        tenant_ids = [t.id for t in user_tenants]
        assert tenant1.id in tenant_ids
        assert tenant2.id in tenant_ids


class TestSettings:
    async def test_set_tenant_setting(self, session: AsyncSession, test_user: User):
        """Test setting tenant setting"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        setting = await service.set_tenant_setting(
            tenant.id,
            "notification_email",
            {"enabled": True, "frequency": "daily"},
        )

        assert setting.key == "notification_email"
        assert setting.value["enabled"] is True

    async def test_get_tenant_setting(self, session: AsyncSession, test_user: User):
        """Test getting tenant setting"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        await service.set_tenant_setting(
            tenant.id,
            "webhook_url",
            {"url": "https://example.com/webhook"},
        )

        setting = await service.get_tenant_setting(tenant.id, "webhook_url")

        assert setting["key"] == "webhook_url"
        assert setting["value"]["url"] == "https://example.com/webhook"

    async def test_get_nonexistent_setting(self, session: AsyncSession, test_user: User):
        """Test getting non-existent setting"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        with pytest.raises(NotFoundError):
            await service.get_tenant_setting(tenant.id, "nonexistent")


class TestResourceLimits:
    async def test_check_user_limit(self, session: AsyncSession, test_user: User):
        """Test checking user limit"""
        service = TenantService(session)
        tenant = await service.create_tenant("Test", "test", test_user.id)

        # Default max_users is 10
        can_add = await service.check_tenant_limit(tenant.id, "users", 9)
        assert can_add is True

        cannot_add = await service.check_tenant_limit(tenant.id, "users", 11)
        assert cannot_add is False
