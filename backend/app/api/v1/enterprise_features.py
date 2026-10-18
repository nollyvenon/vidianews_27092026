"""Enterprise endpoints: security, moderation, rate limiting, notifications and reporting (async).

Access rules:
- Granting access, assigning roles, writing audit entries and creating notifications for other users are
  administrator operations. Granting a role is privilege management, so it is never open to the user it affects.
- Preferences, alert configurations, reports and export jobs belong to their user; administrators may act for any user.
- Moderation decisions, moderator assignment, compliance rules, report templates and export progress are for
  administrators with the matching resource access.
- Reading or marking a notification is limited to its owner, and administrators.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import admin_status, require_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.enterprise_features import (
    AccessLevel, ModerationStatus,
    NotificationType, RateLimitConfig, ReportFormat,
)
from app.models.user import User
from app.services.enterprise_features_service import (
    ModerationService, NotificationService, RateLimitService,
    ReportingService, SecurityService,
)

require_security_admin = require_admin("security")
require_moderation_admin = require_admin("moderation")
require_notification_admin = require_admin("notifications")
require_report_admin = require_admin("reports")


def _forbidden(detail: str) -> HTTPException:
    return HTTPException(status_code=403, detail=detail)


# Pydantic Schemas
class SecurityAuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    action: str
    resource_type: Optional[str]
    resource_id: Optional[int]
    status: Optional[str]
    ip_address: Optional[str]
    severity: str
    created_at: datetime


class AuditLogsRequest(BaseModel):
    user_id: Optional[int] = None
    action: Optional[str] = None
    severity: Optional[str] = None
    days: int = 30
    limit: int = 100


class AccessControlRequest(BaseModel):
    resource_type: str
    resource_id: int
    access_level: AccessLevel
    permissions: List[str]
    granted_by: int
    expires_at: Optional[datetime] = None


class AccessControlResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resource_type: str
    resource_id: int
    access_level: str
    permissions: List[str]
    granted_at: datetime


class RoleAssignmentRequest(BaseModel):
    role: str
    permissions: List[str]
    can_edit_content: bool = False
    can_delete_content: bool = False
    can_manage_users: bool = False
    can_access_analytics: bool = False
    can_access_admin: bool = False


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    role: str
    permissions: List[str]
    can_edit_content: bool
    can_delete_content: bool
    can_manage_users: bool
    can_access_analytics: bool
    can_access_admin: bool
    created_at: datetime


class ModerationQueueRequest(BaseModel):
    content_id: int
    content_type: str
    reason: str
    flags: Optional[List[str]] = None


class ModerationReviewRequest(BaseModel):
    status: ModerationStatus
    decision: str


class ModerationQueueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content_id: int
    content_type: str
    status: str
    reason: str
    confidence_score: float
    assigned_to: Optional[int]
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    created_at: datetime


class ComplianceRuleRequest(BaseModel):
    name: str
    rule_type: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    patterns: Optional[List[str]] = None
    severity: str = "medium"
    auto_action: Optional[str] = None


class ComplianceCheckRequest(BaseModel):
    text: str


class ComplianceCheckResponse(BaseModel):
    is_compliant: bool
    violations: List[dict]
    violation_count: int


class RateLimitConfigRequest(BaseModel):
    endpoint: str
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_limit: int = 100


class RateLimitStatusResponse(BaseModel):
    limited: bool
    minute_remaining: Optional[int]
    hour_remaining: Optional[int]
    day_remaining: Optional[int]


class NotificationPreferenceRequest(BaseModel):
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    frequency: Optional[str] = None
    do_not_disturb_start: Optional[str] = None
    do_not_disturb_end: Optional[str] = None


class NotificationPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    email_enabled: bool
    push_enabled: bool
    sms_enabled: bool
    in_app_enabled: bool
    frequency: str
    created_at: datetime


class NotificationRequest(BaseModel):
    notification_type: NotificationType
    title: str
    message: str
    data: Optional[dict] = None
    action_url: Optional[str] = None
    source: Optional[str] = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    notification_type: str
    title: str
    message: str
    read: bool
    read_at: Optional[datetime]
    created_at: datetime


class AlertConfigRequest(BaseModel):
    alert_type: str
    condition: str
    threshold: Optional[float] = None
    notification_channels: Optional[List[str]] = None


class AlertConfigResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    alert_type: str
    condition: str
    threshold: Optional[float]
    enabled: bool
    created_at: datetime


class ReportRequest(BaseModel):
    name: str
    report_type: str
    format: ReportFormat
    query: Optional[dict] = None
    filters: Optional[dict] = None


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    report_type: str
    format: str
    status: str
    generated_at: Optional[datetime]
    created_at: datetime


class ReportTemplateRequest(BaseModel):
    name: str
    report_type: str
    sections: List[str]
    format: ReportFormat
    description: Optional[str] = None
    schedule: Optional[str] = None


class ReportTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    report_type: str
    sections: List[str]
    format: str
    created_at: datetime


class ScheduledReportRequest(BaseModel):
    template_id: int
    name: str
    cron_expression: str
    recipient_emails: List[str]


class ScheduledReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    cron_expression: str
    enabled: bool
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime


class ExportJobRequest(BaseModel):
    export_type: str
    format: ReportFormat
    filters: Optional[dict] = None


class ExportJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    export_type: str
    format: str
    status: str
    progress: int
    record_count: int
    created_at: datetime


# Routers
security_router = APIRouter(prefix="/security", tags=["security"])
moderation_router = APIRouter(prefix="/moderation", tags=["moderation"])
rate_limit_router = APIRouter(prefix="/rate-limits", tags=["rate-limiting"])
notification_router = APIRouter(prefix="/enterprise/notifications", tags=["notifications"])
reporting_router = APIRouter(prefix="/reports", tags=["reporting"])


# Security Endpoints
@security_router.get("/audit-logs", response_model=List[SecurityAuditLogResponse])
async def get_audit_logs(
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=3650),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("security")),
):
    """Audit entries. Administrators see every user's entries; everyone else sees only their own."""
    if not caller_is_admin:
        if user_id is not None and user_id != current_user.id:
            raise _forbidden("You can only view your own audit log")
        user_id = current_user.id
    return await SecurityService(db).get_audit_logs(user_id, action, severity, days, limit)


@security_router.post("/audit-logs", status_code=201)
async def log_audit_event(
    user_id: int,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    severity: str = "info",
    _admin: User = Depends(require_security_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record an audit entry (administrators only, so entries cannot be forged by users)"""
    log = await SecurityService(db).log_audit_event(
        user_id, action, resource_type, resource_id, severity=severity
    )
    return {"id": log.id, "created_at": log.created_at}


@security_router.post("/access-control/{user_id}", response_model=AccessControlResponse, status_code=201)
async def grant_access(
    user_id: int,
    req: AccessControlRequest,
    _admin: User = Depends(require_security_admin),
    db: AsyncSession = Depends(get_db),
):
    """Grant a user access to a resource (administrators only)"""
    return await SecurityService(db).grant_access(
        user_id,
        req.resource_type,
        req.resource_id,
        req.access_level,
        req.permissions,
        req.granted_by,
        req.expires_at,
    )


@security_router.delete("/access-control/{user_id}/{resource_type}/{resource_id}")
async def revoke_access(
    user_id: int,
    resource_type: str,
    resource_id: int,
    _admin: User = Depends(require_security_admin),
    db: AsyncSession = Depends(get_db),
):
    """Revoke a user's access to a resource (administrators only)"""
    if not await SecurityService(db).revoke_access(user_id, resource_type, resource_id):
        raise HTTPException(status_code=404, detail="Access control not found")
    return {"revoked": True}


@security_router.post("/check-permission")
async def check_permission(
    user_id: int,
    resource_type: str,
    resource_id: int,
    permission: str,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("security")),
    db: AsyncSession = Depends(get_db),
):
    """Whether a user holds a permission. Users may check only themselves."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only check your own permissions")
    has_permission = await SecurityService(db).check_permission(
        user_id, resource_type, resource_id, permission
    )
    return {"has_permission": has_permission}


@security_router.post("/roles/{user_id}", response_model=RoleResponse, status_code=201)
async def assign_role(
    user_id: int,
    req: RoleAssignmentRequest,
    _admin: User = Depends(require_security_admin),
    db: AsyncSession = Depends(get_db),
):
    """Assign a role and its permissions to a user (administrators only)"""
    return await SecurityService(db).assign_role(
        user_id,
        req.role,
        req.permissions,
        req.can_edit_content,
        req.can_delete_content,
        req.can_manage_users,
        req.can_access_analytics,
        req.can_access_admin,
    )


@security_router.get("/roles/{user_id}", response_model=RoleResponse)
async def get_user_role(
    user_id: int,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("security")),
    db: AsyncSession = Depends(get_db),
):
    """A user's role. Users may read only their own."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only view your own role")
    role = await SecurityService(db).get_user_role(user_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Moderation Endpoints
@moderation_router.post("/queue", response_model=ModerationQueueResponse, status_code=201)
async def submit_for_moderation(
    req: ModerationQueueRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Flag content for review by a moderator"""
    return await ModerationService(db).submit_for_moderation(
        req.content_id, req.content_type, req.reason, req.flags
    )


@moderation_router.get("/queue/pending", response_model=List[ModerationQueueResponse])
async def get_pending_items(
    limit: int = Query(50, ge=1, le=200),
    _moderator: User = Depends(require_moderation_admin),
    db: AsyncSession = Depends(get_db),
):
    """Items awaiting a decision (moderators only)"""
    return await ModerationService(db).get_pending_items(limit)


@moderation_router.post("/queue/{item_id}/assign/{moderator_id}")
async def assign_moderator(
    item_id: int,
    moderator_id: int,
    _moderator: User = Depends(require_moderation_admin),
    db: AsyncSession = Depends(get_db),
):
    """Assign a moderation item to a moderator (moderators only)"""
    item = await ModerationService(db).assign_moderator(item_id, moderator_id)
    if not item:
        raise HTTPException(status_code=404, detail="Moderation item not found")
    return {"assigned": True, "moderator_id": moderator_id}


@moderation_router.post("/queue/{item_id}/review")
async def review_content(
    item_id: int,
    req: ModerationReviewRequest,
    moderator: User = Depends(require_moderation_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record a moderation decision (moderators only). The reviewer is the authenticated caller."""
    item = await ModerationService(db).review_content(item_id, moderator.id, req.status, req.decision)
    if not item:
        raise HTTPException(status_code=404, detail="Moderation item not found")
    return {"reviewed": True, "status": req.status.value}


@moderation_router.post("/rules", response_model=dict, status_code=201)
async def create_compliance_rule(
    req: ComplianceRuleRequest,
    _moderator: User = Depends(require_moderation_admin),
    db: AsyncSession = Depends(get_db),
):
    """Add a compliance rule (moderators only)"""
    rule = await ModerationService(db).add_compliance_rule(
        req.name,
        req.rule_type,
        req.description,
        req.keywords,
        req.patterns,
        req.severity,
        req.auto_action,
    )
    return {"id": rule.id, "name": rule.name}


@moderation_router.post("/check-compliance", response_model=ComplianceCheckResponse)
async def check_compliance(
    req: ComplianceCheckRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check text against the enabled compliance rules"""
    return await ModerationService(db).check_compliance(req.text)


# Rate Limiting Endpoints
@rate_limit_router.post("/check", response_model=RateLimitStatusResponse)
async def check_rate_limit(
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    endpoint: str = "*",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remaining allowance for a caller on an endpoint"""
    return await RateLimitService(db).check_rate_limit(user_id, ip_address, endpoint)


@rate_limit_router.get("/configs")
async def list_rate_limit_configs(
    _admin: User = Depends(require_admin("rate_limits")),
    db: AsyncSession = Depends(get_db),
):
    """Every configured rate limit (administrators only)"""
    rows = (await db.execute(
        select(RateLimitConfig).order_by(RateLimitConfig.endpoint, RateLimitConfig.id)
    )).scalars().all()
    return [
        {
            "id": row.id,
            "endpoint": row.endpoint,
            "user_id": row.user_id,
            "ip_address": row.ip_address,
            "requests_per_minute": row.requests_per_minute,
            "requests_per_hour": row.requests_per_hour,
            "requests_per_day": row.requests_per_day,
            "burst_limit": row.burst_limit,
        }
        for row in rows
    ]


@rate_limit_router.post("/config", response_model=dict, status_code=201)
async def create_rate_limit_config(
    req: RateLimitConfigRequest,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    _admin: User = Depends(require_admin("rate_limits")),
    db: AsyncSession = Depends(get_db),
):
    """Create a rate limit (administrators only)"""
    config = await RateLimitService(db).create_rate_limit_config(
        req.endpoint,
        req.requests_per_minute,
        req.requests_per_hour,
        req.requests_per_day,
        req.burst_limit,
        user_id,
        ip_address,
    )
    return {"id": config.id, "endpoint": config.endpoint}


# Notification Endpoints
@notification_router.get("/preferences/{user_id}", response_model=NotificationPreferenceResponse)
async def get_preferences(
    user_id: int,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("notifications")),
    db: AsyncSession = Depends(get_db),
):
    """A user's notification preferences. Users may read only their own."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only view your own notification preferences")
    prefs = await NotificationService(db).get_preferences(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return prefs


@notification_router.put("/preferences/{user_id}", response_model=NotificationPreferenceResponse)
async def update_preferences(
    user_id: int,
    req: NotificationPreferenceRequest,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("notifications")),
    db: AsyncSession = Depends(get_db),
):
    """Update a user's notification preferences. Users may change only their own."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only change your own notification preferences")
    return await NotificationService(db).update_preferences(
        user_id,
        req.email_enabled,
        req.push_enabled,
        req.sms_enabled,
        req.in_app_enabled,
        req.frequency,
        req.do_not_disturb_start,
        req.do_not_disturb_end,
    )


@notification_router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification(
    user_id: int,
    req: NotificationRequest,
    _admin: User = Depends(require_notification_admin),
    db: AsyncSession = Depends(get_db),
):
    """Send a notification to a user (administrators only)"""
    return await NotificationService(db).create_notification(
        user_id,
        req.notification_type,
        req.title,
        req.message,
        req.data,
        req.action_url,
        req.source,
    )


@notification_router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: Optional[int] = Query(None),
    unread_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("notifications")),
    db: AsyncSession = Depends(get_db),
):
    """The caller's own notifications. Reading another user's needs administrator access."""
    target = user_id if user_id is not None else current_user.id
    if target != current_user.id and not caller_is_admin:
        raise _forbidden("You can only view your own notifications")
    return await NotificationService(db).get_user_notifications(target, unread_only, limit)


@notification_router.post("/{notification_id}/mark-read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("notifications")),
    db: AsyncSession = Depends(get_db),
):
    """Mark one of the caller's notifications as read"""
    service = NotificationService(db)
    notification = await service.get_notification(notification_id)
    if notification is None or (notification.user_id != current_user.id and not caller_is_admin):
        raise HTTPException(status_code=404, detail="Notification not found")
    await service.mark_as_read(notification_id)
    return {"read": True}


@notification_router.post("/alerts/config", response_model=AlertConfigResponse, status_code=201)
async def create_alert_config(
    user_id: int,
    req: AlertConfigRequest,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("notifications")),
    db: AsyncSession = Depends(get_db),
):
    """Create an alert for a user. Users may configure only their own alerts."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only configure your own alerts")
    return await NotificationService(db).create_alert_config(
        user_id,
        req.alert_type,
        req.condition,
        req.threshold,
        req.notification_channels,
    )


# Reporting Endpoints
@reporting_router.post("/", response_model=ReportResponse, status_code=201)
async def create_report(
    user_id: int,
    req: ReportRequest,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("reports")),
    db: AsyncSession = Depends(get_db),
):
    """Request a report for a user. Users may request reports only for themselves."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only request your own reports")
    return await ReportingService(db).create_report(
        user_id, req.name, req.report_type, req.format, req.query, req.filters
    )


@reporting_router.get("/", response_model=List[ReportResponse])
async def get_reports(
    user_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("reports")),
    db: AsyncSession = Depends(get_db),
):
    """The caller's own reports. Reading another user's needs administrator access."""
    target = user_id if user_id is not None else current_user.id
    if target != current_user.id and not caller_is_admin:
        raise _forbidden("You can only view your own reports")
    return await ReportingService(db).get_user_reports(target, limit)


@reporting_router.post("/templates", response_model=ReportTemplateResponse, status_code=201)
async def create_report_template(
    req: ReportTemplateRequest,
    _admin: User = Depends(require_report_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a report template shared by all users (administrators only)"""
    return await ReportingService(db).create_template(
        req.name, req.report_type, req.sections, req.format, req.description, req.schedule
    )


@reporting_router.post("/scheduled", response_model=ScheduledReportResponse, status_code=201)
async def create_scheduled_report(
    user_id: int,
    req: ScheduledReportRequest,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("reports")),
    db: AsyncSession = Depends(get_db),
):
    """Schedule a report for a user. Users may schedule only their own."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only schedule your own reports")
    return await ReportingService(db).create_scheduled_report(
        user_id, req.template_id, req.name, req.cron_expression, req.recipient_emails
    )


@reporting_router.post("/exports", response_model=ExportJobResponse, status_code=201)
async def create_export_job(
    user_id: int,
    req: ExportJobRequest,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("reports")),
    db: AsyncSession = Depends(get_db),
):
    """Start an export for a user. Users may export only their own data."""
    if user_id != current_user.id and not caller_is_admin:
        raise _forbidden("You can only export your own data")
    return await ReportingService(db).create_export_job(user_id, req.export_type, req.format, req.filters)


@reporting_router.get("/exports/{job_id}", response_model=ExportJobResponse)
async def get_export_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    caller_is_admin: bool = Depends(admin_status("reports")),
    db: AsyncSession = Depends(get_db),
):
    """An export job. Visible to the user who requested it, and to administrators."""
    job = await ReportingService(db).get_export_job(job_id)
    if job is None or (job.user_id != current_user.id and not caller_is_admin):
        raise HTTPException(status_code=404, detail="Export job not found")
    return job


@reporting_router.put("/exports/{job_id}/progress")
async def update_export_progress(
    job_id: int,
    progress: int = Query(..., ge=0),
    record_count: int = Query(0, ge=0),
    _admin: User = Depends(require_report_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record export progress from the worker (administrators only)"""
    job = await ReportingService(db).update_export_progress(job_id, progress, record_count)
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")
    return {"progress": job.progress, "status": job.status}
