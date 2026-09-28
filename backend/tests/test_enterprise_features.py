import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch, AsyncMock

from app.models.enterprise_features import (
    SecurityAuditLog, AccessControl, RoleBasedAccess, ModerationQueue,
    ComplianceRule, RateLimitConfig, ThrottleLog, NotificationPreference,
    RealTimeNotification, AlertConfiguration, AdvancedReport, ReportTemplate,
    ReportSchedule, ExportJob, AccessLevel, ModerationStatus,
    NotificationType, ReportFormat
)
from app.services.enterprise_features_service import (
    SecurityService, ModerationService, RateLimitService,
    NotificationService, ReportingService
)


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def security_service(mock_db):
    return SecurityService(mock_db)


@pytest.fixture
def moderation_service(mock_db):
    return ModerationService(mock_db)


@pytest.fixture
def rate_limit_service(mock_db):
    return RateLimitService(mock_db)


@pytest.fixture
def notification_service(mock_db):
    return NotificationService(mock_db)


@pytest.fixture
def reporting_service(mock_db):
    return ReportingService(mock_db)


# Security Service Tests
@pytest.mark.asyncio
async def test_log_audit_event(security_service, mock_db):
    mock_log = SecurityAuditLog(
        id=1,
        user_id=123,
        action="login",
        resource_type="user",
        resource_id=456,
        severity="info",
    )
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await security_service.log_audit_event(
        user_id=123,
        action="login",
        resource_type="user",
        resource_id=456,
        severity="info",
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_audit_logs(security_service, mock_db):
    mock_logs = [
        SecurityAuditLog(id=1, user_id=123, action="login", severity="info"),
        SecurityAuditLog(id=2, user_id=123, action="logout", severity="info"),
    ]
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_logs
    mock_db.query.return_value = mock_query

    result = await security_service.get_audit_logs(user_id=123)

    assert len(result) == 2
    assert result[0].user_id == 123


@pytest.mark.asyncio
async def test_grant_access(security_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await security_service.grant_access(
        user_id=123,
        resource_type="content",
        resource_id=456,
        access_level=AccessLevel.PROTECTED,
        permissions=["read", "write"],
        granted_by=789,
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_revoke_access(security_service, mock_db):
    mock_access = Mock(spec=AccessControl)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_access
    mock_db.query.return_value = mock_query
    mock_db.delete = Mock()
    mock_db.commit = Mock()

    result = await security_service.revoke_access(
        user_id=123,
        resource_type="content",
        resource_id=456,
    )

    assert result is True
    mock_db.delete.assert_called_once()


@pytest.mark.asyncio
async def test_check_permission(security_service, mock_db):
    mock_access = Mock(spec=AccessControl)
    mock_access.permissions = ["read", "write"]
    mock_access.expires_at = None
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_access
    mock_db.query.return_value = mock_query

    result = await security_service.check_permission(
        user_id=123,
        resource_type="content",
        resource_id=456,
        permission="read",
    )

    assert result is True


@pytest.mark.asyncio
async def test_check_permission_no_access(security_service, mock_db):
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    mock_db.query.return_value = mock_query

    result = await security_service.check_permission(
        user_id=123,
        resource_type="content",
        resource_id=456,
        permission="read",
    )

    assert result is False


@pytest.mark.asyncio
async def test_assign_role(security_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await security_service.assign_role(
        user_id=123,
        role="admin",
        permissions=["read", "write", "delete"],
        can_access_admin=True,
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


# Moderation Service Tests
@pytest.mark.asyncio
async def test_submit_for_moderation(moderation_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await moderation_service.submit_for_moderation(
        content_id=123,
        content_type="article",
        reason="Contains inappropriate content",
        flags=["spam", "violence"],
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_pending_items(moderation_service, mock_db):
    mock_items = [
        Mock(id=1, status=ModerationStatus.PENDING),
        Mock(id=2, status=ModerationStatus.PENDING),
    ]
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_items
    mock_db.query.return_value = mock_query

    result = await moderation_service.get_pending_items()

    assert len(result) == 2


@pytest.mark.asyncio
async def test_assign_moderator(moderation_service, mock_db):
    mock_item = Mock(spec=ModerationQueue)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_item
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await moderation_service.assign_moderator(
        item_id=1,
        moderator_id=123,
    )

    assert result is not None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_review_content(moderation_service, mock_db):
    mock_item = Mock(spec=ModerationQueue)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_item
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await moderation_service.review_content(
        item_id=1,
        reviewer_id=123,
        status=ModerationStatus.APPROVED,
        decision="Content is acceptable",
    )

    assert result is not None


@pytest.mark.asyncio
async def test_add_compliance_rule(moderation_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await moderation_service.add_compliance_rule(
        name="Spam Detection",
        rule_type="keyword",
        keywords=["viagra", "casino"],
        severity="high",
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_check_compliance_with_keywords(moderation_service, mock_db):
    mock_rule = Mock(spec=ComplianceRule)
    mock_rule.keywords = ["viagra", "casino"]
    mock_rule.patterns = []
    mock_rule.id = 1
    mock_rule.name = "Spam"
    mock_rule.severity = "high"

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [mock_rule]
    mock_db.query.return_value = mock_query

    result = await moderation_service.check_compliance("Buy viagra now")

    assert result["is_compliant"] is False
    assert len(result["violations"]) > 0


# Rate Limit Service Tests
@pytest.mark.asyncio
async def test_check_rate_limit_not_limited(rate_limit_service, mock_db):
    mock_config = Mock(spec=RateLimitConfig)
    mock_config.requests_per_minute = 60
    mock_config.requests_per_hour = 1000
    mock_config.requests_per_day = 10000

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_config

    mock_count_query = Mock()
    mock_count_query.filter.return_value = mock_count_query
    mock_count_query.scalar.return_value = 10

    mock_db.query.side_effect = [mock_query, mock_count_query, mock_count_query, mock_count_query]

    result = await rate_limit_service.check_rate_limit(user_id=123, endpoint="/api/test")

    assert result["limited"] is False


@pytest.mark.asyncio
async def test_log_throttle(rate_limit_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await rate_limit_service.log_throttle(
        user_id=123,
        endpoint="/api/test",
        limit_type="minute",
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rate_limit_config(rate_limit_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await rate_limit_service.create_rate_limit_config(
        endpoint="/api/test",
        requests_per_minute=60,
    )

    mock_db.add.assert_called_once()


# Notification Service Tests
@pytest.mark.asyncio
async def test_get_preferences(notification_service, mock_db):
    mock_prefs = Mock(spec=NotificationPreference)
    mock_prefs.email_enabled = True
    mock_prefs.push_enabled = True

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_prefs
    mock_db.query.return_value = mock_query

    result = await notification_service.get_preferences(user_id=123)

    assert result is not None
    assert result.email_enabled is True


@pytest.mark.asyncio
async def test_update_preferences_new(notification_service, mock_db):
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    mock_db.query.return_value = mock_query
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await notification_service.update_preferences(
        user_id=123,
        email_enabled=False,
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_notification(notification_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await notification_service.create_notification(
        user_id=123,
        notification_type=NotificationType.ALERT,
        title="Test Alert",
        message="This is a test",
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_mark_as_read(notification_service, mock_db):
    mock_notif = Mock(spec=RealTimeNotification)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_notif
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await notification_service.mark_as_read(notification_id=1)

    assert result is not None
    assert result.read is True


@pytest.mark.asyncio
async def test_get_user_notifications(notification_service, mock_db):
    mock_notifs = [
        Mock(id=1, read=False),
        Mock(id=2, read=False),
    ]
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_notifs
    mock_db.query.return_value = mock_query

    result = await notification_service.get_user_notifications(user_id=123)

    assert len(result) == 2


# Reporting Service Tests
@pytest.mark.asyncio
async def test_create_report(reporting_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await reporting_service.create_report(
        user_id=123,
        name="Monthly Report",
        report_type="analytics",
        format=ReportFormat.PDF,
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_update_report_status(reporting_service, mock_db):
    mock_report = Mock(spec=AdvancedReport)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_report
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await reporting_service.update_report_status(
        report_id=1,
        status="completed",
        data={"total": 100},
    )

    assert result is not None


@pytest.mark.asyncio
async def test_get_user_reports(reporting_service, mock_db):
    mock_reports = [
        Mock(id=1, user_id=123, name="Report 1"),
        Mock(id=2, user_id=123, name="Report 2"),
    ]
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_reports
    mock_db.query.return_value = mock_query

    result = await reporting_service.get_user_reports(user_id=123)

    assert len(result) == 2


@pytest.mark.asyncio
async def test_create_export_job(reporting_service, mock_db):
    mock_db.add = Mock()
    mock_db.commit = Mock()

    result = await reporting_service.create_export_job(
        user_id=123,
        export_type="user_data",
        format=ReportFormat.CSV,
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_update_export_progress(reporting_service, mock_db):
    mock_job = Mock(spec=ExportJob)
    mock_job.progress = 0
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_job
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()

    result = await reporting_service.update_export_progress(
        job_id=1,
        progress=50,
        record_count=5000,
    )

    assert result is not None
    assert result.progress == 50
