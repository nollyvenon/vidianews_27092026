"""Integration tests for profile endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.user import User
from app.core.security import hash_password, create_access_token


@pytest.fixture
async def auth_user(async_client: AsyncClient, session: AsyncSession):
    """Create authenticated user"""
    user = User(
        email="profile_test@example.com",
        password_hash=hash_password("pass123"),
        first_name="Profile",
        last_name="Test",
        status="active",
    )
    session.add(user)
    await session.flush()

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"user": user, "token": token}


class TestProfileAPI:
    async def test_get_profile(self, async_client: AsyncClient, auth_user):
        """Test getting profile"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            f"/api/v1/profiles/{auth_user['user'].id}",
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json()["user_id"] == auth_user["user"].id

    async def test_update_profile(self, async_client: AsyncClient, auth_user):
        """Test updating profile"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.put(
            "/api/v1/profiles/me",
            json={
                "bio": "Test bio",
                "title": "Senior Developer",
                "location": "SF",
            },
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Senior Developer"

    async def test_get_profile_summary(self, async_client: AsyncClient, auth_user):
        """Test getting profile summary"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.get(
            f"/api/v1/profiles/{auth_user['user'].id}/summary",
            headers=headers,
        )

        assert response.status_code == 200
        assert "skills_count" in response.json()


class TestSkillsAPI:
    async def test_add_skill(self, async_client: AsyncClient, auth_user):
        """Test adding skill"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.post(
            "/api/v1/profiles/me/skills",
            json={
                "name": "Python",
                "category": "backend",
                "proficiency": "expert",
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Python"

    async def test_get_skills(self, async_client: AsyncClient, auth_user):
        """Test getting skills"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        # Add skills
        await async_client.post(
            "/api/v1/profiles/me/skills",
            json={"name": "Python"},
            headers=headers,
        )
        await async_client.post(
            "/api/v1/profiles/me/skills",
            json={"name": "JavaScript"},
            headers=headers,
        )

        response = await async_client.get(
            f"/api/v1/profiles/{auth_user['user'].id}/skills",
            headers=headers,
        )

        assert response.status_code == 200
        assert len(response.json()) >= 2


class TestExperienceAPI:
    async def test_add_experience(self, async_client: AsyncClient, auth_user):
        """Test adding experience"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.post(
            "/api/v1/profiles/me/experiences",
            json={
                "company": "Acme",
                "title": "Senior Dev",
                "start_date": datetime.now(timezone.utc).isoformat(),
                "current": True,
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["company"] == "Acme"

    async def test_get_experiences(self, async_client: AsyncClient, auth_user):
        """Test getting experiences"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        # Add experience
        await async_client.post(
            "/api/v1/profiles/me/experiences",
            json={
                "company": "Acme",
                "title": "Dev",
                "start_date": datetime.now(timezone.utc).isoformat(),
            },
            headers=headers,
        )

        response = await async_client.get(
            f"/api/v1/profiles/{auth_user['user'].id}/experiences",
            headers=headers,
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1


class TestEducationAPI:
    async def test_add_education(self, async_client: AsyncClient, auth_user):
        """Test adding education"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        response = await async_client.post(
            "/api/v1/profiles/me/educations",
            json={
                "school": "MIT",
                "degree": "BS",
                "field": "CS",
                "start_date": datetime.now(timezone.utc).isoformat(),
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["school"] == "MIT"

    async def test_get_educations(self, async_client: AsyncClient, auth_user):
        """Test getting educations"""
        headers = {"Authorization": f"Bearer {auth_user['token']}"}

        # Add education
        await async_client.post(
            "/api/v1/profiles/me/educations",
            json={
                "school": "MIT",
                "start_date": datetime.now(timezone.utc).isoformat(),
            },
            headers=headers,
        )

        response = await async_client.get(
            f"/api/v1/profiles/{auth_user['user'].id}/educations",
            headers=headers,
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1
