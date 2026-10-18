"""Route tests for analytics and admin: who may read what, and what stays inside a tenant."""

from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import insert

from app.models.user import Role, user_roles
from app.services.analytics_admin_service import AdminLogService, AnalyticsEventService, ReportService

WINDOW = {
    "start_date": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
    "end_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
}


async def _make_analytics_admin(session, user_id: int) -> None:
    role = Role(name="admin", description="Administrator")
    session.add(role)
    await session.flush()
    await session.execute(insert(user_roles).values(user_id=user_id, role_id=role.id))
    await session.commit()


class TestAdminOnlyRoutes:
    @pytest.mark.parametrize("path", [
        "/api/v1/system/alerts",
        "/api/v1/admin/logs",
        "/api/v1/system/health",
        "/api/v1/analytics/engagement",
    ])
    async def test_members_without_the_admin_role_are_refused(self, async_client, org_member, reference_data, path):
        response = await async_client.get(path, headers=org_member)
        assert response.status_code == 403

    async def test_revenue_is_refused_to_members(self, async_client, org_member, reference_data):
        response = await async_client.get("/api/v1/analytics/revenue", params=WINDOW, headers=org_member)
        assert response.status_code == 403

    async def test_administrator_reads_their_tenants_alerts_and_logs(self, async_client, org_member, reference_data, session):
        await _make_analytics_admin(session, 1)
        await AdminLogService(session).log_admin_action(1, 1, "update", "course", 5)

        alerts = await async_client.get("/api/v1/system/alerts", headers=org_member)
        logs = await async_client.get("/api/v1/admin/logs", headers=org_member)

        assert alerts.status_code == 200 and alerts.json() == []
        assert logs.status_code == 200
        assert [item["action"] for item in logs.json()] == ["update"]

    async def test_administrator_gets_not_found_for_missing_health_data(self, async_client, org_member, reference_data, session):
        await _make_analytics_admin(session, 1)
        response = await async_client.get("/api/v1/system/health", headers=org_member)
        assert response.status_code == 404

    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/system/alerts")).status_code == 401


class TestSelfAndOtherUsersRecords:
    async def test_members_read_their_own_events(self, async_client, org_member, reference_data, session):
        await AnalyticsEventService(session).log_event(1, 1, "page_view")
        response = await async_client.get("/api/v1/analytics/events/user/1", headers=org_member)
        assert response.status_code == 200
        assert [item["event_type"] for item in response.json()] == ["page_view"]

    async def test_members_cannot_read_another_users_events(self, async_client, org_member, reference_data, session):
        await AnalyticsEventService(session).log_event(1, 2, "page_view")
        response = await async_client.get("/api/v1/analytics/events/user/2", headers=org_member)
        assert response.status_code == 403

    async def test_members_cannot_change_another_users_metrics(self, async_client, org_member, reference_data):
        response = await async_client.put("/api/v1/analytics/metrics/user/2?total_logins=99", headers=org_member)
        assert response.status_code == 403

    async def test_members_update_their_own_metrics(self, async_client, org_member, reference_data):
        response = await async_client.put("/api/v1/analytics/metrics/user/1?total_logins=4", headers=org_member)
        assert response.status_code == 200
        assert response.json()["total_logins"] == 4

    async def test_events_are_logged_for_the_callers_tenant(self, async_client, org_member, reference_data):
        response = await async_client.post(
            "/api/v1/analytics/events", json={"event_type": "search", "event_data": {"q": "x"}}, headers=org_member,
        )
        assert response.status_code == 200
        assert response.json()["organization_id"] == 1
        assert response.json()["user_id"] == 1

    async def test_notification_preferences_are_per_user(self, async_client, org_member, reference_data):
        updated = await async_client.post(
            "/api/v1/notifications/preferences", json={"email_enabled": False}, headers=org_member,
        )
        assert updated.status_code == 200
        assert updated.json()["email_enabled"] is False


class TestReports:
    async def test_administrator_creates_and_reads_a_report_in_their_tenant(self, async_client, org_member, reference_data, session):
        await _make_analytics_admin(session, 1)
        created = await async_client.post(
            "/api/v1/admin/reports",
            json={"report_type": "revenue", "title": "Q1", **WINDOW},
            headers=org_member,
        )
        assert created.status_code == 201
        assert created.json()["organization_id"] == 1

        fetched = await async_client.get(f"/api/v1/reports/{created.json()['id']}", headers=org_member)
        assert fetched.status_code == 200

    async def test_a_report_from_another_tenant_is_not_found(self, async_client, org_member, reference_data, session):
        await _make_analytics_admin(session, 1)
        other = await ReportService(session).create_report(
            99, "revenue", "Elsewhere", datetime.now(timezone.utc), datetime.now(timezone.utc), 2,
        )
        response = await async_client.get(f"/api/v1/reports/{other.id}", headers=org_member)
        assert response.status_code == 404

    async def test_members_cannot_read_reports(self, async_client, org_member, reference_data, session):
        report = await ReportService(session).create_report(
            1, "revenue", "Internal", datetime.now(timezone.utc), datetime.now(timezone.utc), 1,
        )
        response = await async_client.get(f"/api/v1/reports/{report.id}", headers=org_member)
        assert response.status_code == 403
