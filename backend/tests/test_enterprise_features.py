"""Enterprise services: security, moderation, rate limiting, notifications and reporting, on the real database (async)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.enterprise_features import (
    AccessControl,
    AccessLevel,
    ComplianceRule,
    ExportJob,
    ModerationQueue,
    ModerationStatus,
    NotificationPreference,
    NotificationType,
    RateLimitConfig,
    RealTimeNotification,
    ReportFormat,
    ThrottleLog,
)
from app.services.enterprise_features_service import (
    ModerationService,
    NotificationService,
    RateLimitService,
    ReportingService,
    SecurityService,
)


def _naive_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@pytest.fixture
async def users(reference_data):
    """Users 1 and 2 from the seeded reference data."""
    return (1, 2)


class TestSecurityService:
    async def test_log_audit_event(self, session, users):
        log = await SecurityService(session).log_audit_event(
            1, "login", "session", 7, status="ok", severity="warning", changes={"ip": "x"},
        )
        assert log.id is not None
        assert log.severity == "warning"
        assert log.changes == {"ip": "x"}
        assert log.created_at is not None

    async def test_get_audit_logs_filters_and_limits_by_window(self, session, users):
        service = SecurityService(session)
        await service.log_audit_event(1, "login", severity="info")
        old = await service.log_audit_event(2, "login", severity="info")
        await service.log_audit_event(2, "delete", severity="critical")
        old.created_at = _naive_utc() - timedelta(days=90)
        await session.commit()

        recent = await service.get_audit_logs(days=30)
        assert {log.action for log in recent} == {"login", "delete"}
        assert await service.get_audit_logs(user_id=1, days=30) != []
        assert [log.action for log in await service.get_audit_logs(severity="critical", days=30)] == ["delete"]
        assert len(await service.get_audit_logs(days=30, limit=1)) == 1

    async def test_grant_access(self, session, users):
        access = await SecurityService(session).grant_access(
            2, "course", 5, AccessLevel.PRIVATE, ["read", "write"], granted_by=1,
        )
        assert access.id is not None
        assert access.permissions == ["read", "write"]
        assert access.granted_at is not None

    async def test_revoke_access(self, session, users):
        service = SecurityService(session)
        await service.grant_access(2, "course", 5, AccessLevel.PRIVATE, ["read"], granted_by=1)
        assert await service.revoke_access(2, "course", 5) is True
        assert await service.revoke_access(2, "course", 5) is False

    async def test_check_permission(self, session, users):
        service = SecurityService(session)
        await service.grant_access(2, "course", 5, AccessLevel.PRIVATE, ["read"], granted_by=1)
        assert await service.check_permission(2, "course", 5, "read") is True
        assert await service.check_permission(2, "course", 5, "delete") is False

    async def test_check_permission_no_access(self, session, users):
        assert await SecurityService(session).check_permission(2, "course", 5, "read") is False

    async def test_expired_access_is_removed_on_check(self, session, users):
        service = SecurityService(session)
        access = await service.grant_access(
            2, "course", 5, AccessLevel.PRIVATE, ["read"], granted_by=1,
            expires_at=_naive_utc() - timedelta(minutes=1),
        )
        assert await service.check_permission(2, "course", 5, "read") is False
        assert await session.get(AccessControl, access.id) is None

    async def test_assign_role(self, session, users):
        service = SecurityService(session)
        role = await service.assign_role(2, "editor", ["content:write"], can_edit_content=True)
        assert role.id is not None
        assert role.can_edit_content is True
        assert role.can_delete_content is False
        assert (await service.get_user_role(2)).role == "editor"
        assert await service.get_user_role(1) is None


class TestModerationService:
    async def test_submit_for_moderation_starts_pending(self, session, users):
        item = await ModerationService(session).submit_for_moderation(10, "comment", "spam", flags=["links"])
        assert item.status == ModerationStatus.PENDING
        assert item.flags == ["links"]
        assert item.created_at is not None

    async def test_pending_items_are_oldest_first_and_limited(self, session, users):
        service = ModerationService(session)
        first = await service.submit_for_moderation(1, "post", "reason")
        second = await service.submit_for_moderation(2, "post", "reason")
        approved = await service.submit_for_moderation(3, "post", "reason")
        first.created_at = _naive_utc() - timedelta(hours=2)
        second.created_at = _naive_utc() - timedelta(hours=1)
        approved.status = ModerationStatus.APPROVED
        await session.commit()
        assert [i.id for i in await service.get_pending_items()] == [first.id, second.id]
        assert len(await service.get_pending_items(limit=1)) == 1

    async def test_assign_moderator(self, session, users):
        service = ModerationService(session)
        item = await service.submit_for_moderation(1, "post", "reason")
        assigned = await service.assign_moderator(item.id, 1)
        assert assigned.assigned_to == 1
        assert await service.assign_moderator(999999, 1) is None

    async def test_review_content_records_the_decision(self, session, users):
        service = ModerationService(session)
        item = await service.submit_for_moderation(1, "post", "reason")
        reviewed = await service.review_content(item.id, 1, ModerationStatus.REJECTED, "off topic")
        assert reviewed.status == ModerationStatus.REJECTED
        assert reviewed.reviewed_by == 1
        assert reviewed.reviewed_at is not None
        assert reviewed.decision == "off topic"
        assert await service.review_content(999999, 1, ModerationStatus.APPROVED, "x") is None

    async def test_compliance_rules_match_keywords_and_patterns(self, session, users):
        service = ModerationService(session)
        await service.add_compliance_rule("No spam words", "keyword", keywords=["FREE MONEY"], severity="high")
        await service.add_compliance_rule("Card numbers", "pattern", patterns=[r"\d{4}-\d{4}-\d{4}-\d{4}"])
        await service.add_compliance_rule("Broken pattern", "pattern", patterns=["(unclosed"])

        result = await service.check_compliance("Get your free money now, card 1234-5678-9012-3456")
        assert result["is_compliant"] is False
        assert result["violation_count"] == 2
        assert {v["match_type"] for v in result["violations"]} == {"keyword", "pattern"}

        clean = await service.check_compliance("A quiet afternoon")
        assert clean == {"is_compliant": True, "violations": [], "violation_count": 0}

    async def test_disabled_rules_are_ignored(self, session, users):
        service = ModerationService(session)
        rule = await service.add_compliance_rule("Off", "keyword", keywords=["secret"])
        rule.enabled = False
        await session.commit()
        assert (await service.check_compliance("a secret"))["is_compliant"] is True
        assert await session.get(ComplianceRule, rule.id) is not None


class TestRateLimitService:
    async def test_no_config_means_not_limited(self, session, users):
        result = await RateLimitService(session).check_rate_limit(user_id=2, endpoint="/search")
        assert result == {"limited": False, "minute_remaining": None, "hour_remaining": None, "day_remaining": None}

    async def test_limit_is_reached_after_the_minute_quota(self, session, users):
        service = RateLimitService(session)
        await service.create_rate_limit_config("/search", requests_per_minute=2, user_id=2)
        assert (await service.check_rate_limit(user_id=2, endpoint="/search"))["limited"] is False
        await service.log_throttle(user_id=2, endpoint="/search")
        await service.log_throttle(user_id=2, endpoint="/search")
        result = await service.check_rate_limit(user_id=2, endpoint="/search")
        assert result["limited"] is True
        assert result["minute_remaining"] == 0

    async def test_log_throttle_is_stored(self, session, users):
        log = await RateLimitService(session).log_throttle(ip_address="10.0.0.9", endpoint="/x", limit_type="hour")
        stored = await session.get(ThrottleLog, log.id)
        assert stored.ip_address == "10.0.0.9"
        assert stored.throttled_at is not None

    async def test_create_rate_limit_config(self, session, users):
        config = await RateLimitService(session).create_rate_limit_config("/api", requests_per_minute=5, ip_address="10.0.0.1")
        stored = await session.get(RateLimitConfig, config.id)
        assert stored.requests_per_minute == 5
        assert stored.requests_per_hour == 1000


class TestNotificationService:
    async def test_preferences_are_created_on_first_update(self, session, users):
        service = NotificationService(session)
        assert await service.get_preferences(2) is None
        prefs = await service.update_preferences(2, email_enabled=False, frequency="daily")
        assert prefs.email_enabled is False
        assert prefs.frequency == "daily"
        assert prefs.created_at is not None

    async def test_preferences_update_only_given_fields(self, session, users):
        service = NotificationService(session)
        await service.update_preferences(2, email_enabled=False, push_enabled=True)
        prefs = await service.update_preferences(2, sms_enabled=True)
        assert prefs.email_enabled is False
        assert prefs.push_enabled is True
        assert prefs.sms_enabled is True
        stored = await session.get(NotificationPreference, prefs.id)
        assert stored is prefs

    async def test_create_notification(self, session, users):
        notification = await NotificationService(session).create_notification(
            2, NotificationType.INFO, "Hello", "Welcome aboard", data={"k": 1}, action_url="/home", source="system",
        )
        assert notification.data == {"k": 1}
        assert notification.created_at is not None

    async def test_mark_as_read(self, session, users):
        service = NotificationService(session)
        notification = await service.create_notification(2, NotificationType.ALERT, "T", "M")
        marked = await service.mark_as_read(notification.id)
        assert marked.read is True
        assert marked.read_at is not None
        assert await service.mark_as_read(999999) is None
        assert (await service.get_notification(notification.id)).user_id == 2

    async def test_user_notifications_can_be_unread_only(self, session, users):
        service = NotificationService(session)
        read = await service.create_notification(2, NotificationType.INFO, "A", "a")
        await service.create_notification(2, NotificationType.INFO, "B", "b")
        await service.mark_as_read(read.id)
        unread = await service.get_user_notifications(2, unread_only=True)
        assert [n.title for n in unread] == ["B"]
        assert len(await service.get_user_notifications(2)) == 2
        assert await session.get(RealTimeNotification, read.id) is not None

    async def test_create_alert_config(self, session, users):
        config = await NotificationService(session).create_alert_config(
            2, "cpu", "above", threshold=90.0, notification_channels=["email"],
        )
        assert config.threshold == 90.0
        assert config.notification_channels == ["email"]


class TestReportingService:
    async def test_create_report_starts_pending(self, session, users):
        report = await ReportingService(session).create_report(2, "Sales", "sales", ReportFormat.CSV, query={"q": 1})
        assert report.status == "pending"
        assert report.query == {"q": 1}
        assert report.created_at is not None

    async def test_completed_report_gets_a_generation_and_expiry_date(self, session, users):
        service = ReportingService(session)
        report = await service.create_report(2, "Sales", "sales", ReportFormat.PDF)
        completed = await service.update_report_status(report.id, "completed", data={"rows": 3}, file_path="/r/1.pdf")
        assert completed.status == "completed"
        assert completed.data == {"rows": 3}
        assert completed.file_path == "/r/1.pdf"
        assert completed.expires_at - completed.generated_at == timedelta(days=30)
        assert await service.update_report_status(999999, "failed") is None

    async def test_user_reports_are_newest_first(self, session, users):
        service = ReportingService(session)
        first = await service.create_report(2, "First", "t", ReportFormat.CSV)
        second = await service.create_report(2, "Second", "t", ReportFormat.CSV)
        assert [r.id for r in await service.get_user_reports(2)] == [second.id, first.id]

    async def test_create_template_and_scheduled_report(self, session, users):
        service = ReportingService(session)
        template = await service.create_template("Weekly", "sales", ["summary", "detail"], ReportFormat.JSON, schedule="0 9 * * 1")
        assert template.sections == ["summary", "detail"]
        schedule = await service.create_scheduled_report(2, template.id, "Monday", "0 9 * * 1", ["ops@example.com"])
        assert schedule.recipient_emails == ["ops@example.com"]
        assert schedule.enabled is True

    async def test_export_job_progress_completes_at_100(self, session, users):
        service = ReportingService(session)
        job = await service.create_export_job(2, "orders", ReportFormat.EXCEL, filters={"year": 2026})
        assert job.status == "pending"
        partial = await service.update_export_progress(job.id, 40, record_count=40)
        assert partial.progress == 40
        assert partial.status == "pending"
        done = await service.update_export_progress(job.id, 150, record_count=150)
        assert done.progress == 100
        assert done.status == "completed"
        assert done.completed_at is not None
        assert (await service.get_export_job(job.id)).user_id == 2

    async def test_unknown_export_job_is_not_found(self, session, users):
        service = ReportingService(session)
        assert await service.update_export_progress(999999, 10) is None
        assert await service.get_export_job(999999) is None
        assert await session.get(ExportJob, 999999) is None
        assert await session.get(ModerationQueue, 999999) is None
