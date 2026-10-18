"""Tests for analytics and admin services (async)."""

from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.models.analytics_admin import SystemAlert
from app.services.analytics_admin_service import (
    AdminLogService,
    AnalyticsEventService,
    EngagementMetricService,
    NotificationPreferenceService,
    PermissionPolicyService,
    ReportService,
    RevenueMetricService,
    SystemAlertService,
    SystemHealthService,
    UserBehaviorService,
    UserMetricService,
)
from app.utils.exceptions import NotFoundError


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


class TestAnalyticsEventService:
    async def test_log_event(self, session):
        event = await AnalyticsEventService(session).log_event(1, 1, "page_view", {"page": "/dashboard"})
        assert event.id is not None
        assert event.event_type == "page_view"
        assert event.user_id == 1

    async def test_get_events_by_user_is_newest_first(self, session):
        service = AnalyticsEventService(session)
        first = await service.log_event(1, 1, "page_view")
        second = await service.log_event(1, 1, "search")

        events = await service.get_events_by_user(1)
        assert [event.id for event in events][:2] == [second.id, first.id]

    async def test_get_events_by_type(self, session):
        service = AnalyticsEventService(session)
        await service.log_event(1, 1, "page_view")
        await service.log_event(1, 2, "page_view")
        await service.log_event(1, 2, "search")

        events = await service.get_events_by_type(1, "page_view")
        assert len(events) == 2


class TestUserMetricService:
    async def test_get_or_create_user_metric(self, session):
        metric = await UserMetricService(session).get_or_create_user_metric(1)
        assert metric.id is not None
        assert metric.user_id == 1

    async def test_update_user_metric(self, session):
        service = UserMetricService(session)
        updated = await service.update_user_metric(1, total_logins=5, courses_enrolled=3)
        assert updated.total_logins == 5
        assert updated.courses_enrolled == 3

    async def test_calculate_engagement_score(self, session):
        service = UserMetricService(session)
        await service.update_user_metric(1, total_logins=10, courses_completed=2, total_spend=100.0)
        score = await service.calculate_engagement_score(1)
        assert score == 10 * 2 + 2 * 50 + 0 / 60 + 100.0 / 10


class TestRevenueMetricService:
    async def test_create_revenue_metric(self, session):
        metric = await RevenueMetricService(session).create_or_update_revenue_metric(
            1, datetime.now(timezone.utc), 1000.0, 700.0, 300.0,
        )
        assert metric.total_revenue == 1000.0
        assert metric.course_revenue == 700.0
        assert metric.membership_revenue == 300.0

    async def test_get_revenue_range(self, session):
        service = RevenueMetricService(session)
        today = datetime.now(timezone.utc)
        await service.create_or_update_revenue_metric(1, today, 1000.0)
        await service.create_or_update_revenue_metric(1, today + timedelta(days=1), 1200.0)

        metrics = await service.get_revenue_range(1, today - timedelta(days=1), today + timedelta(days=2))
        assert len(metrics) == 2


class TestEngagementMetricService:
    async def test_create_engagement_metric(self, session):
        metric = await EngagementMetricService(session).create_engagement_metric(
            1, datetime.now(timezone.utc), 500, 50,
        )
        assert metric.active_users == 500
        assert metric.new_users == 50

    async def test_get_engagement_trend(self, session):
        service = EngagementMetricService(session)
        today = datetime.now(timezone.utc)
        await service.create_engagement_metric(1, today, 500, 50)
        await service.create_engagement_metric(1, today - timedelta(days=1), 480, 45)

        trend = await service.get_engagement_trend(1, days=30)
        assert len(trend) == 2


class TestReportService:
    async def test_create_report(self, session):
        end = datetime.now(timezone.utc)
        report = await ReportService(session).create_report(
            1, "revenue", "Monthly Revenue Report", end - timedelta(days=30), end, 1,
        )
        assert report.id is not None
        assert report.report_type == "revenue"

    async def test_get_report(self, session):
        service = ReportService(session)
        end = datetime.now(timezone.utc)
        created = await service.create_report(1, "revenue", "Monthly Revenue Report", end - timedelta(days=30), end, 1)
        retrieved = await service.get_report(created.id)
        assert retrieved.id == created.id

    async def test_get_missing_report_returns_none(self, session):
        assert await ReportService(session).get_report(999999) is None

    async def test_get_organization_reports_filters_by_type(self, session):
        service = ReportService(session)
        end = datetime.now(timezone.utc)
        await service.create_report(1, "revenue", "Report 1", end - timedelta(days=30), end, 1)
        await service.create_report(1, "users", "Report 2", end - timedelta(days=30), end, 1)

        assert len(await service.get_organization_reports(1)) == 2
        assert [r.title for r in await service.get_organization_reports(1, "users")] == ["Report 2"]


class TestAdminLogService:
    async def test_log_admin_action(self, session):
        log = await AdminLogService(session).log_admin_action(1, 1, "create", "course", 5, {"name": "Python 101"})
        assert log.id is not None
        assert log.action == "create"
        assert log.resource_type == "course"

    async def test_get_admin_logs_and_by_admin(self, session):
        service = AdminLogService(session)
        await service.log_admin_action(1, 1, "create", "course", 5)
        await service.log_admin_action(1, 1, "update", "user", 10)

        assert len(await service.get_admin_logs(1)) == 2
        assert len(await service.get_logs_by_admin(1)) == 2


class TestSystemHealthService:
    async def test_create_health_check(self, session):
        health = await SystemHealthService(session).create_health_check(1, 45.5, 62.3, 75.0, 125.0, 0.5)
        assert health.cpu_usage == 45.5
        assert health.memory_usage == 62.3
        assert health.uptime_percentage == 99.5

    async def test_get_latest_health_is_the_newest(self, session):
        service = SystemHealthService(session)
        await service.create_health_check(1, 45.5, 62.3, 75.0, 125.0, 0.5)
        newest = await service.create_health_check(1, 50.0, 65.0, 78.0, 130.0, 1.0)
        latest = await service.get_latest_health(1)
        assert latest.id == newest.id

    async def test_get_latest_health_is_none_without_data(self, session):
        assert await SystemHealthService(session).get_latest_health(1) is None

    async def test_get_health_history(self, session):
        service = SystemHealthService(session)
        await service.create_health_check(1, 45.5, 62.3, 75.0, 125.0, 0.5)
        await service.create_health_check(1, 50.0, 65.0, 78.0, 130.0, 1.0)
        assert len(await service.get_health_history(1, hours=24)) == 2


class TestUserBehaviorService:
    async def test_log_behavior(self, session):
        behavior = await UserBehaviorService(session).log_behavior(1, "/dashboard", 300, "mobile", "Chrome", "iOS")
        assert behavior.user_id == 1
        assert behavior.page_visited == "/dashboard"
        assert behavior.time_spent == 300

    async def test_get_user_behavior(self, session):
        service = UserBehaviorService(session)
        await service.log_behavior(1, "/dashboard", 300)
        await service.log_behavior(1, "/courses", 450)
        assert len(await service.get_user_behavior(1)) == 2


class TestNotificationPreferenceService:
    async def test_get_or_create_preference(self, session):
        pref = await NotificationPreferenceService(session).get_or_create_preference(1)
        assert pref.user_id == 1
        assert pref.email_enabled is True

    async def test_update_preference(self, session):
        updated = await NotificationPreferenceService(session).update_preference(1, email_enabled=False, sms_enabled=True)
        assert updated.email_enabled is False
        assert updated.sms_enabled is True


class TestPermissionPolicyService:
    async def test_create_and_get_policy(self, session):
        service = PermissionPolicyService(session)
        created = await service.create_policy("editor", {"courses": "edit", "users": "read"})
        assert created.permissions["courses"] == "edit"
        assert (await service.get_policy(created.id)).id == created.id
        assert (await service.get_policy_by_name("editor")).name == "editor"


class TestSystemAlertService:
    async def test_create_alert(self, session):
        alert = await SystemAlertService(session).create_alert(1, "high_cpu", "CPU usage above 90%", "critical")
        assert alert.alert_type == "high_cpu"
        assert alert.severity == "critical"

    async def test_resolve_alert(self, session):
        service = SystemAlertService(session)
        alert = await service.create_alert(1, "high_cpu", "CPU usage above 90%", "critical")
        await service.resolve_alert(alert.id)

        resolved = (await session.execute(select(SystemAlert).where(SystemAlert.id == alert.id))).scalar_one()
        assert resolved.is_resolved is True
        assert resolved.resolved_at is not None

    async def test_resolving_a_missing_alert_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await SystemAlertService(session).resolve_alert(999999)

    async def test_get_active_alerts_excludes_resolved_ones(self, session):
        service = SystemAlertService(session)
        await service.create_alert(1, "high_cpu", "CPU high", "critical")
        resolved = await service.create_alert(1, "memory_high", "Memory high", "warning")
        await service.resolve_alert(resolved.id)

        active = await service.get_active_alerts(1)
        assert [alert.alert_type for alert in active] == ["high_cpu"]
