"""Admin audit logs are visible to administrators only."""

import httpx
import pytest

from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.user import Role, User


@pytest.fixture
async def client(test_session):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as http:
        yield http
    app.dependency_overrides.clear()


async def _user(session, email, admin=False):
    user = User(email=email, password_hash=hash_password("Passw0rd!long"), first_name="T", last_name="U", status="active")
    if admin:
        user.roles = [Role(name="admin", description="Administrator")]
    session.add(user)
    await session.commit()
    return user


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


class TestAuditLogAccess:
    @pytest.mark.asyncio
    async def test_ordinary_member_cannot_read_the_audit_trail(self, client, session):
        member = await _user(session, "member@example.com")
        response = await client.get("/api/v1/admin/audit-logs", headers=_headers(member))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_member_cannot_read_a_single_audit_entry(self, client, session):
        member = await _user(session, "member2@example.com")
        response = await client.get("/api/v1/admin/audit-logs/1", headers=_headers(member))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_administrator_can_read_the_audit_trail(self, client, session):
        admin = await _user(session, "admin@example.com", admin=True)
        response = await client.get("/api/v1/admin/audit-logs", headers=_headers(admin))
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_anonymous_request_is_rejected(self, client):
        assert (await client.get("/api/v1/admin/audit-logs")).status_code == 401
