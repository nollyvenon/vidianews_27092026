"""Authentication integration tests"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from tests.db_config import TEST_DATABASE_URL
from sqlalchemy.pool import NullPool
from app.main import app
from app.db.base import Base
from app.db.session import get_session
from app.models.user import User
from app.core.security import hash_password


@pytest.fixture
async def test_db():
    """Setup test database"""
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    yield engine

    await engine.dispose()


@pytest.fixture
def client(test_db):
    """Test client"""
    return TestClient(app)


def verify_account(email: str) -> None:
    """Confirm the account's email, as the link sent at registration would."""
    from sqlalchemy import create_engine, text
    from tests.db_config import TEST_SYNC_DATABASE_URL

    engine = create_engine(TEST_SYNC_DATABASE_URL)
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE users SET status = 'active' WHERE email = :email"),
            {"email": email},
        )
    engine.dispose()


def login_token(client, email: str = "test@example.com", password: str = "TestPassword123!") -> str:
    """Confirm the account, sign in, and return the access token."""
    verify_account(email)
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        # Registration sends a confirmation email; no session is issued until the address is confirmed.
        assert data["requires_verification"] is True
        assert data["access_token"] is None

    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "DifferentPassword!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 422

    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Another",
                "last_name": "User",
            },
        )

        assert response.status_code == 409

    def test_login_success(self, client):
        """Test successful login"""
        # Register first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        verify_account("test@example.com")

        # Then login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "TestPassword123!",
            },
        )

        assert response.status_code == 401

    def test_login_invalid_password(self, client):
        """Test login with wrong password"""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword!",
            },
        )

        assert response.status_code == 401

    def test_get_current_user(self, client):
        """Test getting current user"""
        reg_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert reg_response.status_code == 201
        token = login_token(client)

        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"

    def test_get_current_user_invalid_token(self, client):
        """Test get current user with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401

    def test_get_current_user_no_header(self, client):
        """Test get current user without auth header"""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_logout(self, client):
        """Test logout"""
        reg_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
                "password_confirm": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert reg_response.status_code == 201
        token = login_token(client)

        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"
