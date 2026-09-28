from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.enterprise_features_service import (
    SecurityService, ModerationService, RateLimitService,
    NotificationService, ReportingService
)
from app.models.enterprise_features import (
    AccessLevel, PermissionType, ModerationStatus,
    NotificationType, ReportFormat
)


# Pydantic Schemas
class SecurityAuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    resource_type: Optional[str]
    resource_id: Optional[int]
    status: Optional[str]
    ip_address: Optional[str]
    severity: str
    created_at: datetime

    class Config:
        from_attributes = True


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
    id: int
    user_id: int
    resource_type: str
    resource_id: int
    access_level: str
    permissions: List[str]
    granted_at: datetime

    class Config:
        from_attributes = True


class RoleAssignmentRequest(BaseModel):
    role: str
    permissions: List[str]
    can_edit_content: bool = False
    can_delete_content: bool = False
    can_manage_users: bool = False
    can_access_analytics: bool = False
    can_access_admin: bool = False


class RoleResponse(BaseModel):
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

    class Config:
        from_attributes = True


class ModerationQueueRequest(BaseModel):
    content_id: int
    content_type: str
    reason: str
    flags: Optional[List[str]] = None


class ModerationReviewRequest(BaseModel):
    status: ModerationStatus
    decision: str


class ModerationQueueResponse(BaseModel):
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

    class Config:
        from_attributes = True


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
    id: int
    user_id: int
    email_enabled: bool
    push_enabled: bool
    sms_enabled: bool
    in_app_enabled: bool
    frequency: str
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationRequest(BaseModel):
    notification_type: NotificationType
    title: str
    message: str
    data: Optional[dict] = None
    action_url: Optional[str] = None
    source: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    notification_type: str
    title: str
    message: str
    read: bool
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class AlertConfigRequest(BaseModel):
    alert_type: str
    condition: str
    threshold: Optional[float] = None
    notification_channels: Optional[List[str]] = None


class AlertConfigResponse(BaseModel):
    id: int
    user_id: int
    alert_type: str
    condition: str
    threshold: Optional[float]
    enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ReportRequest(BaseModel):
    name: str
    report_type: str
    format: ReportFormat
    query: Optional[dict] = None
    filters: Optional[dict] = None


class ReportResponse(BaseModel):
    id: int
    user_id: int
    name: str
    report_type: str
    format: str
    status: str
    generated_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ReportTemplateRequest(BaseModel):
    name: str
    report_type: str
    sections: List[str]
    format: ReportFormat
    description: Optional[str] = None
    schedule: Optional[str] = None


class ReportTemplateResponse(BaseModel):
    id: int
    name: str
    report_type: str
    sections: List[str]
    format: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduledReportRequest(BaseModel):
    template_id: int
    name: str
    cron_expression: str
    recipient_emails: List[str]


class ScheduledReportResponse(BaseModel):
    id: int
    user_id: int
    name: str
    cron_expression: str
    enabled: bool
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ExportJobRequest(BaseModel):
    export_type: str
    format: ReportFormat
    filters: Optional[dict] = None


class ExportJobResponse(BaseModel):
    id: int
    user_id: int
    export_type: str
    format: str
    status: str
    progress: int
    record_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Routers
security_router = APIRouter(prefix="/security", tags=["security"])
moderation_router = APIRouter(prefix="/moderation", tags=["moderation"])
rate_limit_router = APIRouter(prefix="/rate-limits", tags=["rate-limiting"])
notification_router = APIRouter(prefix="/notifications", tags=["notifications"])
reporting_router = APIRouter(prefix="/reports", tags=["reporting"])


# Security Endpoints
@security_router.get("/audit-logs", response_model=List[SecurityAuditLogResponse])
async def get_audit_logs(
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    days: int = Query(30),
    limit: int = Query(100),
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    return await service.get_audit_logs(user_id, action, severity, days, limit)


@security_router.post("/audit-logs")
async def log_audit_event(
    user_id: int,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    severity: str = "info",
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    log = await service.log_audit_event(
        user_id, action, resource_type, resource_id, severity=severity
    )
    return {"id": log.id, "created_at": log.created_at}


@security_router.post("/access-control/{user_id}", response_model=AccessControlResponse)
async def grant_access(
    user_id: int,
    req: AccessControlRequest,
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    access = await service.grant_access(
        user_id,
        req.resource_type,
        req.resource_id,
        req.access_level,
        req.permissions,
        req.granted_by,
        req.expires_at,
    )
    return access


@security_router.delete("/access-control/{user_id}/{resource_type}/{resource_id}")
async def revoke_access(
    user_id: int,
    resource_type: str,
    resource_id: int,
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    success = await service.revoke_access(user_id, resource_type, resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="Access control not found")
    return {"revoked": True}


@security_router.post("/check-permission")
async def check_permission(
    user_id: int,
    resource_type: str,
    resource_id: int,
    permission: str,
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    has_permission = await service.check_permission(
        user_id, resource_type, resource_id, permission
    )
    return {"has_permission": has_permission}


@security_router.post("/roles/{user_id}", response_model=RoleResponse)
async def assign_role(
    user_id: int,
    req: RoleAssignmentRequest,
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    role = await service.assign_role(
        user_id,
        req.role,
        req.permissions,
        req.can_edit_content,
        req.can_delete_content,
        req.can_manage_users,
        req.can_access_analytics,
        req.can_access_admin,
    )
    return role


@security_router.get("/roles/{user_id}", response_model=RoleResponse)
async def get_user_role(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = SecurityService(db)
    role = await service.get_user_role(user_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Moderation Endpoints
@moderation_router.post("/queue", response_model=ModerationQueueResponse)
async def submit_for_moderation(
    req: ModerationQueueRequest,
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    item = await service.submit_for_moderation(
        req.content_id, req.content_type, req.reason, req.flags
    )
    return item


@moderation_router.get("/queue/pending", response_model=List[ModerationQueueResponse])
async def get_pending_items(
    limit: int = Query(50),
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    return await service.get_pending_items(limit)


@moderation_router.post("/queue/{item_id}/assign/{moderator_id}")
async def assign_moderator(
    item_id: int,
    moderator_id: int,
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    item = await service.assign_moderator(item_id, moderator_id)
    if not item:
        raise HTTPException(status_code=404, detail="Moderation item not found")
    return {"assigned": True, "moderator_id": moderator_id}


@moderation_router.post("/queue/{item_id}/review")
async def review_content(
    item_id: int,
    reviewer_id: int,
    req: ModerationReviewRequest,
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    item = await service.review_content(item_id, reviewer_id, req.status, req.decision)
    if not item:
        raise HTTPException(status_code=404, detail="Moderation item not found")
    return {"reviewed": True, "status": req.status.value}


@moderation_router.post("/rules", response_model=dict)
async def create_compliance_rule(
    req: ComplianceRuleRequest,
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    rule = await service.add_compliance_rule(
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
    db: Session = Depends(get_db),
):
    service = ModerationService(db)
    return await service.check_compliance(req.text)


# Rate Limiting Endpoints
@rate_limit_router.post("/check", response_model=RateLimitStatusResponse)
async def check_rate_limit(
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    endpoint: str = "*",
    db: Session = Depends(get_db),
):
    service = RateLimitService(db)
    return await service.check_rate_limit(user_id, ip_address, endpoint)


@rate_limit_router.post("/config", response_model=dict)
async def create_rate_limit_config(
    req: RateLimitConfigRequest,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = RateLimitService(db)
    config = await service.create_rate_limit_config(
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
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    prefs = await service.get_preferences(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return prefs


@notification_router.put("/preferences/{user_id}", response_model=NotificationPreferenceResponse)
async def update_preferences(
    user_id: int,
    req: NotificationPreferenceRequest,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    return await service.update_preferences(
        user_id,
        req.email_enabled,
        req.push_enabled,
        req.sms_enabled,
        req.in_app_enabled,
        req.frequency,
        req.do_not_disturb_start,
        req.do_not_disturb_end,
    )


@notification_router.post("/", response_model=NotificationResponse)
async def create_notification(
    user_id: int,
    req: NotificationRequest,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    notification = await service.create_notification(
        user_id,
        req.notification_type,
        req.title,
        req.message,
        req.data,
        req.action_url,
        req.source,
    )
    return notification


@notification_router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: int,
    unread_only: bool = Query(False),
    limit: int = Query(50),
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    return await service.get_user_notifications(user_id, unread_only, limit)


@notification_router.post("/{notification_id}/mark-read")
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    notif = await service.mark_as_read(notification_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"read": True}


@notification_router.post("/alerts/config", response_model=AlertConfigResponse)
async def create_alert_config(
    user_id: int,
    req: AlertConfigRequest,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)
    config = await service.create_alert_config(
        user_id,
        req.alert_type,
        req.condition,
        req.threshold,
        req.notification_channels,
    )
    return config


# Reporting Endpoints
@reporting_router.post("/", response_model=ReportResponse)
async def create_report(
    user_id: int,
    req: ReportRequest,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    report = await service.create_report(
        user_id, req.name, req.report_type, req.format, req.query, req.filters
    )
    return report


@reporting_router.get("/", response_model=List[ReportResponse])
async def get_reports(
    user_id: int,
    limit: int = Query(50),
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    return await service.get_user_reports(user_id, limit)


@reporting_router.post("/templates", response_model=ReportTemplateResponse)
async def create_report_template(
    req: ReportTemplateRequest,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    template = await service.create_template(
        req.name, req.report_type, req.sections, req.format, req.description, req.schedule
    )
    return template


@reporting_router.post("/scheduled", response_model=ScheduledReportResponse)
async def create_scheduled_report(
    user_id: int,
    req: ScheduledReportRequest,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    schedule = await service.create_scheduled_report(
        user_id, req.template_id, req.name, req.cron_expression, req.recipient_emails
    )
    return schedule


@reporting_router.post("/exports", response_model=ExportJobResponse)
async def create_export_job(
    user_id: int,
    req: ExportJobRequest,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    job = await service.create_export_job(user_id, req.export_type, req.format, req.filters)
    return job


@reporting_router.get("/exports/{job_id}", response_model=ExportJobResponse)
async def get_export_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    job = await service.get_export_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")
    return job


@reporting_router.put("/exports/{job_id}/progress")
async def update_export_progress(
    job_id: int,
    progress: int,
    record_count: int = 0,
    db: Session = Depends(get_db),
):
    service = ReportingService(db)
    job = await service.update_export_progress(job_id, progress, record_count)
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")
    return {"progress": job.progress, "status": job.status}
