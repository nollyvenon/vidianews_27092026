"""Test reports: CI uploads per-suite results; counts come from the results; admin-only writes."""

import httpx
import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.api_monitoring import TestResult, TestSuite
from app.models.user import Role, User

RUN = {
    "suite": "Unit Tests",
    "coverage_percentage": 94.5,
    "results": [
        {"name": "test_a", "status": "passed", "duration_ms": 12.5},
        {"name": "test_b", "status": "passed", "duration_ms": 3},
        {"name": "test_c", "status": "failed", "duration_ms": 40, "error_message": "AssertionError: 1 != 2"},
        {"name": "test_d", "status": "skipped", "duration_ms": 0},
    ],
}


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


@pytest.fixture
async def admin(session):
    return await _user(session, "ci-admin@example.com", admin=True)


@pytest.fixture
async def member(session):
    return await _user(session, "member@example.com")


class TestRecordingRuns:
    @pytest.mark.asyncio
    async def test_admin_records_a_run_and_counts_come_from_the_results(self, client, admin, session):
        response = await client.post("/api/v1/test-reports/runs", json=RUN, headers=_headers(admin))
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Unit Tests"
        assert (body["test_count"], body["passed"], body["failed"], body["skipped"]) == (4, 2, 1, 1)
        assert body["pass_rate"] == 66.7
        assert body["coverage_percentage"] == 94.5
        assert body["last_run_at"] is not None

        rows = (await session.execute(select(TestResult))).scalars().all()
        assert len(rows) == 4

    @pytest.mark.asyncio
    async def test_a_second_run_updates_the_suite_and_keeps_history(self, client, admin, session):
        await client.post("/api/v1/test-reports/runs", json=RUN, headers=_headers(admin))
        second = {**RUN, "coverage_percentage": None, "results": [{"name": "test_a", "status": "passed", "duration_ms": 9}]}
        response = await client.post("/api/v1/test-reports/runs", json=second, headers=_headers(admin))

        assert response.status_code == 201
        body = response.json()
        assert (body["test_count"], body["passed"], body["failed"]) == (1, 1, 0)
        assert body["pass_rate"] == 100.0
        assert body["coverage_percentage"] == 94.5  # not sent this time, so the last known value stays
        assert len((await session.execute(select(TestResult))).scalars().all()) == 5
        assert len((await session.execute(select(TestSuite))).scalars().all()) == 1

    @pytest.mark.asyncio
    async def test_suite_with_only_skipped_tests_has_no_pass_rate(self, client, admin):
        payload = {"suite": "Smoke", "results": [{"name": "t", "status": "skipped", "duration_ms": 0}]}
        body = (await client.post("/api/v1/test-reports/runs", json=payload, headers=_headers(admin))).json()
        assert body["pass_rate"] is None

    @pytest.mark.asyncio
    async def test_client_cannot_override_the_counts(self, client, admin):
        payload = {**RUN, "passed": 999, "failed": 0, "test_count": 999}
        body = (await client.post("/api/v1/test-reports/runs", json=payload, headers=_headers(admin))).json()
        assert (body["passed"], body["failed"], body["test_count"]) == (2, 1, 4)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("change", [
        {"results": []},
        {"results": [{"name": "t", "status": "maybe", "duration_ms": 1}]},
        {"results": [{"name": "t", "status": "passed", "duration_ms": -1}]},
        {"coverage_percentage": 140},
        {"suite": ""},
    ])
    async def test_invalid_reports_are_rejected(self, client, admin, change):
        response = await client.post("/api/v1/test-reports/runs", json={**RUN, **change}, headers=_headers(admin))
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_members_cannot_record_runs(self, client, member):
        response = await client.post("/api/v1/test-reports/runs", json=RUN, headers=_headers(member))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_anonymous_requests_are_rejected(self, client):
        assert (await client.post("/api/v1/test-reports/runs", json=RUN)).status_code == 401


class TestReading:
    @pytest.mark.asyncio
    async def test_members_can_read_suites_and_results(self, client, admin, member):
        await client.post("/api/v1/test-reports/runs", json=RUN, headers=_headers(admin))
        suites = (await client.get("/api/v1/test-reports/suites", headers=_headers(member))).json()
        assert [item["name"] for item in suites] == ["Unit Tests"]

        suite_id = suites[0]["id"]
        detail = (await client.get(f"/api/v1/test-reports/suites/{suite_id}", headers=_headers(member))).json()
        assert detail["suite"]["failed"] == 1
        assert len(detail["results"]) == 4

    @pytest.mark.asyncio
    async def test_results_can_be_filtered_to_failures(self, client, admin, member):
        await client.post("/api/v1/test-reports/runs", json=RUN, headers=_headers(admin))
        suite_id = (await client.get("/api/v1/test-reports/suites", headers=_headers(member))).json()[0]["id"]
        failures = (await client.get(
            f"/api/v1/test-reports/suites/{suite_id}?status=failed", headers=_headers(member),
        )).json()["results"]
        assert [item["test_name"] for item in failures] == ["test_c"]
        assert failures[0]["error_message"] == "AssertionError: 1 != 2"

    @pytest.mark.asyncio
    async def test_unknown_suite_is_not_found(self, client, member):
        response = await client.get("/api/v1/test-reports/suites/9999", headers=_headers(member))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_results_limit_is_enforced(self, client, member):
        response = await client.get("/api/v1/test-reports/suites/1?limit=500", headers=_headers(member))
        assert response.status_code == 422
