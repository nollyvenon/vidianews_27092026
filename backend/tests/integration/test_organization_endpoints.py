"""Integration tests for organization endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, create_access_token
from app.services.tenant_service import TenantService


@pytest.fixture
async def test_setup(async_client: AsyncClient, session: AsyncSession):
    """Setup tenant and users"""
    user = User(
        email="test@example.com",
        password_hash=hash_password("pass123"),
        first_name="Test",
        last_name="User",
        status="active",
    )
    session.add(user)
    await session.flush()

    tenant_service = TenantService(session)
    tenant = await tenant_service.create_tenant("Test Tenant", "test-tenant", user.id)

    token = create_access_token({"sub": user.email, "user_id": user.id})

    return {"user": user, "tenant": tenant, "token": token}


class TestOrganizationCRUD:
    async def test_create_organization(self, async_client: AsyncClient, test_setup):
        """Test creating organization"""
        headers = {"Authorization": f"Bearer {test_setup['token']}"}

        response = await async_client.post(
            "/api/v1/organizations",
            json={
                "tenant_id": test_setup["tenant"].id,
                "name": "Engineering",
                "slug": "engineering",
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Engineering"

    async def test_list_organizations(self, async_client: AsyncClient, test_setup):
        """Test listing organizations"""
        headers = {"Authorization": f"Bearer {test_setup['token']}"}

        # Create orgs
        for i in range(3):
            await async_client.post(
                "/api/v1/organizations",
                json={
                    "tenant_id": test_setup["tenant"].id,
                    "name": f"Org{i}",
                    "slug": f"org{i}",
                },
                headers=headers,
            )

        response = await async_client.get(
            f"/api/v1/organizations?tenant_id={test_setup['tenant'].id}",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3

    async def test_delete_organization(self, async_client: AsyncClient, test_setup):
        """Test deleting organization"""
        headers = {"Authorization": f"Bearer {test_setup['token']}"}

        create_response = await async_client.post(
            "/api/v1/organizations",
            json={
                "tenant_id": test_setup["tenant"].id,
                "name": "Test",
                "slug": "test",
            },
            headers=headers,
        )
        org_id = create_response.json()["id"]

        delete_response = await async_client.delete(
            f"/api/v1/organizations/{org_id}",
            headers=headers,
        )

        assert delete_response.status_code == 204


class TestOrganizationHierarchy:
    async def test_hierarchy_endpoints(self, async_client: AsyncClient, test_setup):
        """Test hierarchy operations"""
        headers = {"Authorization": f"Bearer {test_setup['token']}"}
        tenant_id = test_setup["tenant"].id

        # Create parent
        parent_resp = await async_client.post(
            "/api/v1/organizations",
            json={"tenant_id": tenant_id, "name": "Parent", "slug": "parent"},
            headers=headers,
        )
        parent_id = parent_resp.json()["id"]

        # Create child
        child_resp = await async_client.post(
            "/api/v1/organizations",
            json={
                "tenant_id": tenant_id,
                "name": "Child",
                "slug": "child",
                "parent_id": parent_id,
            },
            headers=headers,
        )
        child_id = child_resp.json()["id"]

        # Get hierarchy
        response = await async_client.get(
            f"/api/v1/organizations/{child_id}/hierarchy",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["parent"]["id"] == parent_id


class TestOrganizationMembers:
    async def test_member_operations(self, async_client: AsyncClient, test_setup, session: AsyncSession):
        """Test member management"""
        headers = {"Authorization": f"Bearer {test_setup['token']}"}
        tenant_id = test_setup["tenant"].id

        # Create another user
        user2 = User(
            email="user2@example.com",
            password_hash=hash_password("pass123"),
            first_name="User",
            last_name="Two",
            status="active",
        )
        session.add(user2)
        await session.flush()

        # Create organization
        org_resp = await async_client.post(
            "/api/v1/organizations",
            json={"tenant_id": tenant_id, "name": "Test", "slug": "test"},
            headers=headers,
        )
        org_id = org_resp.json()["id"]

        # Add member
        add_resp = await async_client.post(
            f"/api/v1/organizations/{org_id}/members?user_id={user2.id}&role=editor",
            headers=headers,
        )

        assert add_resp.status_code == 201

        # List members
        list_resp = await async_client.get(
            f"/api/v1/organizations/{org_id}/members",
            headers=headers,
        )

        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 2

        # Remove member
        remove_resp = await async_client.delete(
            f"/api/v1/organizations/{org_id}/members/{user2.id}",
            headers=headers,
        )

        assert remove_resp.status_code == 204
