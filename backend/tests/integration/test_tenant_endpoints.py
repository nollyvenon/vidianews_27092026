"""Integration tests for tenant API endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, create_access_token


@pytest.fixture
async def test_user_with_token(async_client: AsyncClient, session: AsyncSession):
    """Create test user with auth token"""
    user = User(
        email="testuser@example.com",
        password_hash=hash_password("password123"),
        first_name="Test",
        last_name="User",
        status="active",
    )
    session.add(user)
    await session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})

    return {"user": user, "token": token}


@pytest.fixture
async def test_user_2_with_token(async_client: AsyncClient, session: AsyncSession):
    """Create second test user with token"""
    user = User(
        email="testuser2@example.com",
        password_hash=hash_password("password123"),
        first_name="Test",
        last_name="User2",
        status="active",
    )
    session.add(user)
    await session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})

    return {"user": user, "token": token}


class TestCreateTenant:
    async def test_create_tenant(self, async_client: AsyncClient, test_user_with_token):
        """Test creating tenant via API"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        response = await async_client.post(
            "/api/v1/tenants",
            json={
                "name": "Test Tenant",
                "slug": "test-tenant",
                "description": "A test tenant",
                "plan": "pro",
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Tenant"
        assert data["slug"] == "test-tenant"
        assert data["plan"] == "pro"

    async def test_create_tenant_duplicate_slug(self, async_client: AsyncClient, test_user_with_token):
        """Test cannot create duplicate slug"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create first tenant
        await async_client.post(
            "/api/v1/tenants",
            json={"name": "Tenant 1", "slug": "test-slug"},
            headers=headers,
        )

        # Try to create second with same slug
        response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Tenant 2", "slug": "test-slug"},
            headers=headers,
        )

        assert response.status_code == 409

    async def test_create_tenant_unauthorized(self, async_client: AsyncClient):
        """Test creating without auth"""
        response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
        )

        assert response.status_code == 401


class TestListTenants:
    async def test_list_tenants(self, async_client: AsyncClient, test_user_with_token):
        """Test listing tenants"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create multiple tenants
        for i in range(3):
            await async_client.post(
                "/api/v1/tenants",
                json={"name": f"Tenant {i}", "slug": f"slug{i}"},
                headers=headers,
            )

        response = await async_client.get(
            "/api/v1/tenants",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3

    async def test_list_tenants_pagination(self, async_client: AsyncClient, test_user_with_token):
        """Test pagination"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create 5 tenants
        for i in range(5):
            await async_client.post(
                "/api/v1/tenants",
                json={"name": f"Tenant {i}", "slug": f"slug{i}"},
                headers=headers,
            )

        response = await async_client.get(
            "/api/v1/tenants?skip=0&limit=2",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2


class TestGetTenant:
    async def test_get_tenant(self, async_client: AsyncClient, test_user_with_token):
        """Test getting tenant details"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Get tenant
        response = await async_client.get(
            f"/api/v1/tenants/{tenant_id}",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tenant_id

    async def test_get_tenant_not_found(self, async_client: AsyncClient, test_user_with_token):
        """Test getting non-existent tenant"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        response = await async_client.get(
            "/api/v1/tenants/99999",
            headers=headers,
        )

        assert response.status_code == 404


class TestUpdateTenant:
    async def test_update_tenant(self, async_client: AsyncClient, test_user_with_token):
        """Test updating tenant"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Original", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Update tenant
        response = await async_client.put(
            f"/api/v1/tenants/{tenant_id}",
            json={"name": "Updated", "description": "New description"},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["description"] == "New description"

    async def test_update_tenant_unauthorized(self, async_client: AsyncClient, test_user_with_token, test_user_2_with_token):
        """Test cannot update someone else's tenant"""
        headers1 = {"Authorization": f"Bearer {test_user_with_token['token']}"}
        headers2 = {"Authorization": f"Bearer {test_user_2_with_token['token']}"}

        # Create tenant as user 1
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers1,
        )
        tenant_id = create_response.json()["id"]

        # Try to update as user 2
        response = await async_client.put(
            f"/api/v1/tenants/{tenant_id}",
            json={"name": "Hacked"},
            headers=headers2,
        )

        assert response.status_code == 403


class TestDeleteTenant:
    async def test_delete_tenant(self, async_client: AsyncClient, test_user_with_token):
        """Test deleting tenant"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Delete tenant
        response = await async_client.delete(
            f"/api/v1/tenants/{tenant_id}",
            headers=headers,
        )

        assert response.status_code == 204


class TestMembers:
    async def test_add_member(self, async_client: AsyncClient, test_user_with_token, test_user_2_with_token):
        """Test adding member"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Add member
        response = await async_client.post(
            f"/api/v1/tenants/{tenant_id}/members",
            json={"user_id": test_user_2_with_token["user"].id, "role": "editor"},
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["role"] == "editor"

    async def test_list_members(self, async_client: AsyncClient, test_user_with_token, test_user_2_with_token):
        """Test listing members"""
        headers1 = {"Authorization": f"Bearer {test_user_with_token['token']}"}
        headers2 = {"Authorization": f"Bearer {test_user_2_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers1,
        )
        tenant_id = create_response.json()["id"]

        # Add member
        await async_client.post(
            f"/api/v1/tenants/{tenant_id}/members",
            json={"user_id": test_user_2_with_token["user"].id},
            headers=headers1,
        )

        # List members (as member)
        response = await async_client.get(
            f"/api/v1/tenants/{tenant_id}/members",
            headers=headers2,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    async def test_remove_member(self, async_client: AsyncClient, test_user_with_token, test_user_2_with_token):
        """Test removing member"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Add member
        await async_client.post(
            f"/api/v1/tenants/{tenant_id}/members",
            json={"user_id": test_user_2_with_token["user"].id},
            headers=headers,
        )

        # Remove member
        response = await async_client.delete(
            f"/api/v1/tenants/{tenant_id}/members/{test_user_2_with_token['user'].id}",
            headers=headers,
        )

        assert response.status_code == 204


class TestInvitations:
    async def test_invite_user(self, async_client: AsyncClient, test_user_with_token):
        """Test inviting user"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Invite user
        response = await async_client.post(
            f"/api/v1/tenants/{tenant_id}/invite",
            json={"email": "invited@example.com", "role": "editor"},
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "invited@example.com"
        assert data["token"] is not None


class TestSettings:
    async def test_set_setting(self, async_client: AsyncClient, test_user_with_token):
        """Test setting tenant setting"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Set setting
        response = await async_client.put(
            f"/api/v1/tenants/{tenant_id}/settings/webhook_url",
            json={"key": "webhook_url", "value": {"url": "https://example.com"}},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["value"]["url"] == "https://example.com"

    async def test_get_setting(self, async_client: AsyncClient, test_user_with_token):
        """Test getting tenant setting"""
        headers = {"Authorization": f"Bearer {test_user_with_token['token']}"}

        # Create tenant
        create_response = await async_client.post(
            "/api/v1/tenants",
            json={"name": "Test", "slug": "test"},
            headers=headers,
        )
        tenant_id = create_response.json()["id"]

        # Set setting
        await async_client.put(
            f"/api/v1/tenants/{tenant_id}/settings/config",
            json={"key": "config", "value": {"key": "value"}},
            headers=headers,
        )

        # Get setting
        response = await async_client.get(
            f"/api/v1/tenants/{tenant_id}/settings/config",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "config"
