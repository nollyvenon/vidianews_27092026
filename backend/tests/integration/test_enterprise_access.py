"""Route tests for enterprise access: audit logs, the moderation queue, notifications, reports, and rate limits.

These routes expose platform-wide or other users' records, so each test checks who may read them.
"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models.enterprise_features import (
    AdvancedReport, ModerationQueue, NotificationType, RateLimitConfig, RealTimeNotification, SecurityAuditLog,
)


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


def _seed_records(engine):
    with Session(engine) as session:
        session.add_all([
            SecurityAuditLog(user_id=1, action="login", severity="info", created_at=datetime.utcnow()),
            SecurityAuditLog(user_id=2, action="user_delete", severity="high", created_at=datetime.utcnow()),
            ModerationQueue(content_id=1, content_type="article", reason="Possible spam", confidence_score=0.92),
            RealTimeNotification(user_id=1, notification_type=NotificationType.INFO, title="Mine", message="For user 1"),
            RealTimeNotification(user_id=2, notification_type=NotificationType.ALERT, title="Theirs", message="For user 2"),
            AdvancedReport(user_id=1, name="My report", report_type="analytics", status="completed"),
            AdvancedReport(user_id=2, name="Their report", report_type="compliance", status="pending"),
            RateLimitConfig(endpoint="/api/v1/content", requests_per_minute=60, requests_per_hour=1000,
                            requests_per_day=10000, burst_limit=100),
        ])
        session.commit()


class TestAuditLogs:
    async def test_non_administrators_see_only_their_own_audit_entries(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/security/audit-logs", headers=org_member)

        assert response.status_code == 200
        assert [row["action"] for row in response.json()] == ["login"]

    async def test_non_administrators_cannot_read_another_users_audit_entries(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/security/audit-logs?user_id=2", headers=org_member)

        assert response.status_code == 403
        assert response.json()["detail"] == "You can only view your own audit log"

    async def test_administrators_see_every_users_audit_entries(self, async_client, platform_admin, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/security/audit-logs", headers=platform_admin)

        assert response.status_code == 200
        assert sorted(row["action"] for row in response.json()) == ["login", "user_delete"]


class TestModerationQueue:
    async def test_the_pending_queue_is_refused_to_non_moderators(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/moderation/queue/pending", headers=org_member)

        assert response.status_code == 403

    async def test_moderators_see_the_pending_items(self, async_client, platform_admin, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/moderation/queue/pending", headers=platform_admin)

        assert response.status_code == 200
        rows = response.json()
        assert [(row["content_type"], row["content_id"], row["reason"]) for row in rows] == [("article", 1, "Possible spam")]
        assert rows[0]["confidence_score"] == pytest.approx(0.92)


class TestNotifications:
    async def test_by_default_the_caller_sees_only_their_own_notifications(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/enterprise/notifications/", headers=org_member)

        assert response.status_code == 200
        assert [row["title"] for row in response.json()] == ["Mine"]
        assert response.json()[0]["read"] is False

    async def test_reading_another_users_notifications_is_refused(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/enterprise/notifications/?user_id=2", headers=org_member)

        assert response.status_code == 403
        assert response.json()["detail"] == "You can only view your own notifications"

    async def test_an_administrator_can_read_another_users_notifications(self, async_client, platform_admin, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/enterprise/notifications/?user_id=2", headers=platform_admin)

        assert response.status_code == 200
        assert [row["title"] for row in response.json()] == ["Theirs"]


class TestReports:
    async def test_by_default_the_caller_sees_only_their_own_reports(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/reports/", headers=org_member)

        assert response.status_code == 200
        assert [row["name"] for row in response.json()] == ["My report"]

    async def test_reading_another_users_reports_is_refused(self, async_client, org_member, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/reports/?user_id=2", headers=org_member)

        assert response.status_code == 403
        assert response.json()["detail"] == "You can only view your own reports"

    async def test_an_administrator_can_read_another_users_reports(self, async_client, platform_admin, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/reports/?user_id=2", headers=platform_admin)

        assert response.status_code == 200
        assert [row["name"] for row in response.json()] == ["Their report"]


class TestRateLimitConfigs:
    async def test_rate_limit_configs_are_refused_to_non_administrators(self, async_client, unaffiliated_user, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/rate-limits/configs", headers=unaffiliated_user)

        assert response.status_code == 403

    async def test_administrators_see_each_configured_limit(self, async_client, platform_admin, reset_test_database):
        _seed_records(reset_test_database)

        response = await async_client.get("/api/v1/rate-limits/configs", headers=platform_admin)

        assert response.status_code == 200
        assert response.json()[0]["endpoint"] == "/api/v1/content"
        assert response.json()[0]["requests_per_minute"] == 60
