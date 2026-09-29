"""Tests for analytics and admin services"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.analytics_admin import (
    AnalyticsEvent, UserMetric, RevenueMetric, EngagementMetric,
    Report, AdminLog, SystemHealth, UserBehavior,
    NotificationPreference, PermissionPolicy, SystemAlert
)
from app.services.analytics_admin_service import (
    AnalyticsEventService, UserMetricService, RevenueMetricService,
    EngagementMetricService, ReportService, AdminLogService,
    SystemHealthService, UserBehaviorService, NotificationPreferenceService,
    PermissionPolicyService, SystemAlertService
)


class TestAnalyticsEventService:
    def test_log_event(self, db):
        event = AnalyticsEventService.log_event(
            db, 1, 1, "page_view", {"page": "/dashboard"}
        )
        assert event.id is not None
        assert event.event_type == "page_view"
        assert event.user_id == 1

    def test_get_events_by_user(self, db):
        AnalyticsEventService.log_event(db, 1, 1, "page_view")
        AnalyticsEventService.log_event(db, 1, 1, "search")

        events = AnalyticsEventService.get_events_by_user(db, 1)
        assert len(events) >= 2

    def test_get_events_by_type(self, db):
        AnalyticsEventService.log_event(db, 1, 1, "page_view")
        AnalyticsEventService.log_event(db, 1, 2, "page_view")

        events = AnalyticsEventService.get_events_by_type(db, 1, "page_view")
        assert len(events) >= 2


class TestUserMetricService:
    def test_get_or_create_user_metric(self, db):
        metric = UserMetricService.get_or_create_user_metric(db, 1)
        assert metric.id is not None
        assert metric.user_id == 1

    def test_update_user_metric(self, db):
        UserMetricService.get_or_create_user_metric(db, 1)
        updated = UserMetricService.update_user_metric(
            db, 1, total_logins=5, courses_enrolled=3
        )
        assert updated.total_logins == 5
        assert updated.courses_enrolled == 3

    def test_calculate_engagement_score(self, db):
        UserMetricService.update_user_metric(
            db, 1, total_logins=10, courses_completed=2, total_spend=100.0
        )
        score = UserMetricService.calculate_engagement_score(db, 1)
        assert score > 0


class TestRevenueMetricService:
    def test_create_revenue_metric(self, db):
        today = datetime.now(timezone.utc)
        metric = RevenueMetricService.create_or_update_revenue_metric(
            db, 1, today, 1000.0, 700.0, 300.0
        )
        assert metric.total_revenue == 1000.0
        assert metric.course_revenue == 700.0
        assert metric.membership_revenue == 300.0

    def test_get_revenue_range(self, db):
        today = datetime.now(timezone.utc)
        RevenueMetricService.create_or_update_revenue_metric(db, 1, today, 1000.0)
        RevenueMetricService.create_or_update_revenue_metric(
            db, 1, today + timedelta(days=1), 1200.0
        )

        metrics = RevenueMetricService.get_revenue_range(
            db, 1, today - timedelta(days=1), today + timedelta(days=2)
        )
        assert len(metrics) >= 2


class TestEngagementMetricService:
    def test_create_engagement_metric(self, db):
        today = datetime.now(timezone.utc)
        metric = EngagementMetricService.create_engagement_metric(
            db, 1, today, 500, 50
        )
        assert metric.active_users == 500
        assert metric.new_users == 50

    def test_get_engagement_trend(self, db):
        today = datetime.now(timezone.utc)
        EngagementMetricService.create_engagement_metric(db, 1, today, 500, 50)
        EngagementMetricService.create_engagement_metric(
            db, 1, today - timedelta(days=1), 480, 45
        )

        trend = EngagementMetricService.get_engagement_trend(db, 1, days=30)
        assert len(trend) >= 1


class TestReportService:
    def test_create_report(self, db):
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)

        report = ReportService.create_report(
            db, 1, "revenue", "Monthly Revenue Report", start_date, end_date, 1
        )
        assert report.id is not None
        assert report.report_type == "revenue"

    def test_get_report(self, db):
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)

        created = ReportService.create_report(
            db, 1, "revenue", "Monthly Revenue Report", start_date, end_date, 1
        )
        retrieved = ReportService.get_report(db, created.id)
        assert retrieved.id == created.id

    def test_get_organization_reports(self, db):
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)

        ReportService.create_report(
            db, 1, "revenue", "Report 1", start_date, end_date, 1
        )
        ReportService.create_report(
            db, 1, "users", "Report 2", start_date, end_date, 1
        )

        reports = ReportService.get_organization_reports(db, 1)
        assert len(reports) >= 2


class TestAdminLogService:
    def test_log_admin_action(self, db):
        log = AdminLogService.log_admin_action(
            db, 1, 1, "create", "course", 5, {"name": "Python 101"}
        )
        assert log.id is not None
        assert log.action == "create"
        assert log.resource_type == "course"

    def test_get_admin_logs(self, db):
        AdminLogService.log_admin_action(db, 1, 1, "create", "course", 5)
        AdminLogService.log_admin_action(db, 1, 1, "update", "user", 10)

        logs = AdminLogService.get_admin_logs(db, 1)
        assert len(logs) >= 2

    def test_get_logs_by_admin(self, db):
        AdminLogService.log_admin_action(db, 1, 1, "create", "course", 5)
        AdminLogService.log_admin_action(db, 1, 1, "update", "user", 10)

        logs = AdminLogService.get_logs_by_admin(db, 1)
        assert len(logs) >= 2


class TestSystemHealthService:
    def test_create_health_check(self, db):
        health = SystemHealthService.create_health_check(
            db, 1, 45.5, 62.3, 75.0, 125.0, 0.5
        )
        assert health.cpu_usage == 45.5
        assert health.memory_usage == 62.3
        assert health.uptime_percentage == 99.5

    def test_get_latest_health(self, db):
        SystemHealthService.create_health_check(db, 1, 45.5, 62.3, 75.0, 125.0, 0.5)
        latest = SystemHealthService.get_latest_health(db, 1)
        assert latest is not None

    def test_get_health_history(self, db):
        SystemHealthService.create_health_check(db, 1, 45.5, 62.3, 75.0, 125.0, 0.5)
        SystemHealthService.create_health_check(db, 1, 50.0, 65.0, 78.0, 130.0, 1.0)

        history = SystemHealthService.get_health_history(db, 1, hours=24)
        assert len(history) >= 1


class TestUserBehaviorService:
    def test_log_behavior(self, db):
        behavior = UserBehaviorService.log_behavior(
            db, 1, "/dashboard", 300, "mobile", "Chrome", "iOS"
        )
        assert behavior.user_id == 1
        assert behavior.page_visited == "/dashboard"
        assert behavior.time_spent == 300

    def test_get_user_behavior(self, db):
        UserBehaviorService.log_behavior(db, 1, "/dashboard", 300)
        UserBehaviorService.log_behavior(db, 1, "/courses", 450)

        behavior = UserBehaviorService.get_user_behavior(db, 1)
        assert len(behavior) >= 2


class TestNotificationPreferenceService:
    def test_get_or_create_preference(self, db):
        pref = NotificationPreferenceService.get_or_create_preference(db, 1)
        assert pref.user_id == 1
        assert pref.email_enabled is True

    def test_update_preference(self, db):
        NotificationPreferenceService.get_or_create_preference(db, 1)
        updated = NotificationPreferenceService.update_preference(
            db, 1, email_enabled=False, sms_enabled=True
        )
        assert updated.email_enabled is False
        assert updated.sms_enabled is True


class TestPermissionPolicyService:
    def test_create_policy(self, db):
        policy = PermissionPolicyService.create_policy(
            db, "admin", {"courses": "all", "users": "all"}
        )
        assert policy.name == "admin"
        assert policy.permissions["courses"] == "all"

    def test_get_policy(self, db):
        created = PermissionPolicyService.create_policy(
            db, "editor", {"courses": "edit", "users": "read"}
        )
        retrieved = PermissionPolicyService.get_policy(db, created.id)
        assert retrieved.id == created.id

    def test_get_policy_by_name(self, db):
        PermissionPolicyService.create_policy(
            db, "viewer", {"courses": "read", "users": "none"}
        )
        retrieved = PermissionPolicyService.get_policy_by_name(db, "viewer")
        assert retrieved.name == "viewer"


class TestSystemAlertService:
    def test_create_alert(self, db):
        alert = SystemAlertService.create_alert(
            db, 1, "high_cpu", "CPU usage above 90%", "critical"
        )
        assert alert.alert_type == "high_cpu"
        assert alert.severity == "critical"

    def test_resolve_alert(self, db):
        alert = SystemAlertService.create_alert(
            db, 1, "high_cpu", "CPU usage above 90%", "critical"
        )
        SystemAlertService.resolve_alert(db, alert.id)

        resolved = db.query(SystemAlert).filter_by(id=alert.id).first()
        assert resolved.is_resolved is True

    def test_get_active_alerts(self, db):
        SystemAlertService.create_alert(db, 1, "high_cpu", "CPU high", "critical")
        SystemAlertService.create_alert(db, 1, "memory_high", "Memory high", "warning")

        alerts = SystemAlertService.get_active_alerts(db, 1)
        assert len(alerts) >= 2
