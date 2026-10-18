"""Analytics and admin API endpoints.

Access rules:
- A user reads and writes only their own events, metrics and notification preferences,
  unless they are an analytics administrator.
- Business and operational data (revenue, engagement, health, alerts, admin logs, reports)
  is available to analytics administrators, and is always limited to the caller's tenant.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import is_admin, require_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.analytics_admin_service import (
    AdminLogService,
    AnalyticsEventService,
    EngagementMetricService,
    NotificationPreferenceService,
    ReportService,
    RevenueMetricService,
    SystemAlertService,
    SystemHealthService,
    UserMetricService,
)

router = APIRouter()

require_analytics_admin = require_admin("analytics")


def tenant_scope(current_user: User) -> int:
    """Tenant of the signed-in user; the data read here is scoped to it."""
    if current_user.tenant_id is None:
        raise HTTPException(status_code=422, detail="Your account has no workspace yet. Create a tenant first.")
    return current_user.tenant_id


async def _self_or_admin(session: AsyncSession, current_user: User, user_id: int) -> None:
    if user_id == current_user.id:
        return
    if await is_admin(session, current_user.id, "analytics"):
        return
    raise HTTPException(status_code=403, detail="You can only access your own records")


class AnalyticsEventRequest(BaseModel):
    event_type: str
    event_data: dict = {}
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ReportRequest(BaseModel):
    report_type: str
    title: str
    start_date: datetime
    end_date: datetime
    data: dict = {}


class NotificationPreferenceRequest(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    marketing_emails: bool = True
    course_updates: bool = True


@router.post("/analytics/events")
async def log_event(
    req: AnalyticsEventRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Log an analytics event for the signed-in user, in their tenant"""
    return await AnalyticsEventService(session).log_event(
        tenant_scope(current_user), current_user.id, req.event_type, req.event_data,
        req.session_id, req.ip_address, req.user_agent,
    )


@router.get("/analytics/events/user/{user_id}")
async def get_user_events(
    user_id: int,
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Events of a user (own events, or any user's for an analytics administrator)"""
    await _self_or_admin(session, current_user, user_id)
    return await AnalyticsEventService(session).get_events_by_user(user_id, limit)


@router.get("/analytics/metrics/user/{user_id}")
async def get_user_metrics(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _self_or_admin(session, current_user, user_id)
    return await UserMetricService(session).get_or_create_user_metric(user_id)


@router.put("/analytics/metrics/user/{user_id}")
async def update_user_metrics(
    user_id: int,
    total_logins: Optional[int] = Query(None, ge=0),
    courses_enrolled: Optional[int] = Query(None, ge=0),
    courses_completed: Optional[int] = Query(None, ge=0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _self_or_admin(session, current_user, user_id)
    update_data = {}
    if total_logins is not None:
        update_data["total_logins"] = total_logins
    if courses_enrolled is not None:
        update_data["courses_enrolled"] = courses_enrolled
    if courses_completed is not None:
        update_data["courses_completed"] = courses_completed
    return await UserMetricService(session).update_user_metric(user_id, **update_data)


@router.get("/analytics/revenue")
async def get_revenue_metrics(
    start_date: datetime,
    end_date: datetime,
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Revenue for the administrator's tenant"""
    return await RevenueMetricService(session).get_revenue_range(tenant_scope(current_user), start_date, end_date)


@router.get("/analytics/engagement")
async def get_engagement_metrics(
    days: int = Query(30, ge=1, le=365),
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Engagement trend for the administrator's tenant"""
    return await EngagementMetricService(session).get_engagement_trend(tenant_scope(current_user), days)


@router.post("/admin/reports", status_code=201)
async def create_report(
    req: ReportRequest,
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create a report for the administrator's tenant"""
    return await ReportService(session).create_report(
        tenant_scope(current_user), req.report_type, req.title, req.start_date, req.end_date,
        current_user.id, req.data,
    )


@router.get("/reports/{report_id}")
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """A report of the caller's tenant, for an analytics administrator"""
    if not await is_admin(session, current_user.id, "analytics"):
        raise HTTPException(status_code=403, detail="Admin access required")
    report = await ReportService(session).get_report(report_id)
    if report is None or report.organization_id != tenant_scope(current_user):
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/admin/logs")
async def get_admin_logs(
    limit: int = Query(100, ge=1, le=1000),
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Admin activity for the administrator's tenant"""
    return await AdminLogService(session).get_admin_logs(tenant_scope(current_user), limit)


@router.get("/system/health")
async def get_system_health(
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    health = await SystemHealthService(session).get_latest_health(tenant_scope(current_user))
    if health is None:
        raise HTTPException(status_code=404, detail="No health data available")
    return health


@router.get("/system/health/history")
async def get_system_health_history(
    hours: int = Query(24, ge=1, le=720),
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await SystemHealthService(session).get_health_history(tenant_scope(current_user), hours)


@router.post("/notifications/preferences")
async def update_notification_preferences(
    req: NotificationPreferenceRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """The signed-in user's own notification preferences"""
    return await NotificationPreferenceService(session).update_preference(current_user.id, **req.model_dump())


@router.get("/notifications/preferences")
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await NotificationPreferenceService(session).get_or_create_preference(current_user.id)


@router.get("/system/alerts")
async def get_system_alerts(
    _admin: User = Depends(require_analytics_admin),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Unresolved system alerts for the administrator's tenant"""
    return await SystemAlertService(session).get_active_alerts(tenant_scope(current_user))
