"""Analytics and admin API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.analytics_admin_service import (
    AnalyticsEventService, UserMetricService, RevenueMetricService,
    EngagementMetricService, ReportService, AdminLogService,
    SystemHealthService, UserBehaviorService, NotificationPreferenceService,
    PermissionPolicyService, SystemAlertService
)
from app.models.auth import User
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()


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
def log_event(
    req: AnalyticsEventRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log analytics event"""
    return AnalyticsEventService.log_event(
        db, 1, current_user.id, req.event_type, req.event_data,
        req.session_id, req.ip_address, req.user_agent
    )


@router.get("/analytics/events/user/{user_id}")
def get_user_events(
    user_id: int,
    limit: int = Query(100, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get events by user"""
    return AnalyticsEventService.get_events_by_user(db, user_id, limit)


@router.get("/analytics/metrics/user/{user_id}")
def get_user_metrics(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user metrics"""
    metrics = UserMetricService.get_or_create_user_metric(db, user_id)
    return metrics


@router.put("/analytics/metrics/user/{user_id}")
def update_user_metrics(
    user_id: int,
    total_logins: Optional[int] = None,
    courses_enrolled: Optional[int] = None,
    courses_completed: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user metrics"""
    update_data = {}
    if total_logins is not None:
        update_data['total_logins'] = total_logins
    if courses_enrolled is not None:
        update_data['courses_enrolled'] = courses_enrolled
    if courses_completed is not None:
        update_data['courses_completed'] = courses_completed

    return UserMetricService.update_user_metric(db, user_id, **update_data)


@router.get("/analytics/revenue")
def get_revenue_metrics(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get revenue metrics"""
    return RevenueMetricService.get_revenue_range(db, 1, start_date, end_date)


@router.get("/analytics/engagement")
def get_engagement_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get engagement trend"""
    return EngagementMetricService.get_engagement_trend(db, 1, days)


@router.post("/reports")
def create_report(
    req: ReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create report"""
    return ReportService.create_report(
        db, 1, req.report_type, req.title, req.start_date, req.end_date,
        current_user.id, req.data
    )


@router.get("/reports/{report_id}")
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get report"""
    report = ReportService.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/admin/logs")
def get_admin_logs(
    limit: int = Query(100, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get admin logs"""
    return AdminLogService.get_admin_logs(db, 1, limit)


@router.get("/system/health")
def get_system_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system health"""
    health = SystemHealthService.get_latest_health(db, 1)
    if not health:
        raise HTTPException(status_code=404, detail="No health data available")
    return health


@router.get("/system/health/history")
def get_system_health_history(
    hours: int = Query(24, ge=1, le=720),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system health history"""
    return SystemHealthService.get_health_history(db, 1, hours)


@router.post("/notifications/preferences")
def update_notification_preferences(
    req: NotificationPreferenceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update notification preferences"""
    return NotificationPreferenceService.update_preference(
        db, current_user.id, **req.dict()
    )


@router.get("/notifications/preferences")
def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification preferences"""
    return NotificationPreferenceService.get_or_create_preference(db, current_user.id)


@router.get("/system/alerts")
def get_system_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active system alerts"""
    return SystemAlertService.get_active_alerts(db, 1)
