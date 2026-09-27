"""Integration APIs: Modules 21-25"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.integrations_service import (
    AnalyticsService, WebhookService, NotificationService,
    AuditService, SearchService
)
from pydantic import BaseModel

router = APIRouter(prefix="/system", tags=["system"])

# ==================== MODULE 21: ANALYTICS ====================

class ReportCreate(BaseModel):
    report_type: str
    title: str
    data: Dict[str, Any]

class ReportResponse(BaseModel):
    id: int
    report_type: str
    title: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(req: ReportCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create analytics report"""
    service = AnalyticsService(session)
    return await service.create_report(current_user.organization_id, req.report_type, req.title, req.data)

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, session: AsyncSession = Depends(get_db)):
    """Get report"""
    service = AnalyticsService(session)
    report = await service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return report

@router.get("/reports", response_model=List[ReportResponse])
async def list_reports(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List reports"""
    service = AnalyticsService(session)
    return await service.list_reports(current_user.organization_id)

class MetricCreate(BaseModel):
    metric_type: str
    value: float

@router.post("/metrics", status_code=status.HTTP_201_CREATED)
async def record_metric(req: MetricCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Record metric"""
    service = AnalyticsService(session)
    return await service.record_metric(current_user.organization_id, req.metric_type, req.value)

class DashboardCreate(BaseModel):
    name: str
    description: Optional[str] = None

@router.post("/dashboards", status_code=status.HTTP_201_CREATED)
async def create_dashboard(req: DashboardCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create dashboard"""
    service = AnalyticsService(session)
    return await service.create_dashboard(current_user.id, current_user.organization_id, req.name)

@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id: int, session: AsyncSession = Depends(get_db)):
    """Get dashboard"""
    service = AnalyticsService(session)
    dashboard = await service.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return dashboard

@router.get("/dashboards")
async def list_dashboards(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List dashboards"""
    service = AnalyticsService(session)
    return await service.list_dashboards(current_user.organization_id)

# ==================== MODULE 22: WEBHOOKS & INTEGRATIONS ====================

class IntegrationCreate(BaseModel):
    integration_type: str
    name: str
    config: Dict[str, Any]

@router.post("/integrations", status_code=status.HTTP_201_CREATED)
async def create_integration(req: IntegrationCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create integration"""
    service = WebhookService(session)
    return await service.create_integration(current_user.organization_id, req.integration_type, req.name, req.config)

@router.get("/integrations")
async def list_integrations(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List integrations"""
    service = WebhookService(session)
    return await service.list_integrations(current_user.organization_id)

class WebhookCreate(BaseModel):
    event_type: str
    url: str

@router.post("/webhooks", status_code=status.HTTP_201_CREATED)
async def create_webhook(req: WebhookCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create webhook"""
    service = WebhookService(session)
    return await service.create_webhook(current_user.organization_id, req.event_type, req.url)

@router.get("/webhooks")
async def list_webhooks(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List webhooks"""
    service = WebhookService(session)
    return await service.list_webhooks(current_user.organization_id)

@router.get("/webhooks/{webhook_id}/events")
async def get_webhook_events(webhook_id: int, session: AsyncSession = Depends(get_db)):
    """Get webhook events"""
    service = WebhookService(session)
    return await service.get_webhook_events(webhook_id)

# ==================== MODULE 23: NOTIFICATIONS ====================

class NotificationPrefUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None

@router.get("/notifications/preferences")
async def get_preferences(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get notification preferences"""
    service = NotificationService(session)
    prefs = await service.get_preferences(current_user.id)
    if not prefs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return prefs

@router.put("/notifications/preferences")
async def update_preferences(req: NotificationPrefUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Update notification preferences"""
    service = NotificationService(session)
    kwargs = req.dict(exclude_unset=True)
    return await service.update_preferences(current_user.id, **kwargs)

@router.get("/notifications")
async def list_notifications(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get notifications"""
    service = NotificationService(session)
    return await service.get_notifications(current_user.id)

@router.post("/notifications/{notification_id}/read")
async def mark_read(notification_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Mark notification as read"""
    service = NotificationService(session)
    success = await service.mark_as_read(notification_id)
    return {"success": success}

# ==================== MODULE 24: AUDIT & COMPLIANCE ====================

@router.get("/audit/logs")
async def get_audit_logs(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get audit logs"""
    service = AuditService(session)
    return await service.get_audit_logs(current_user.organization_id)

@router.get("/audit/logs/user")
async def get_user_audit_logs(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get user audit logs"""
    service = AuditService(session)
    return await service.get_user_audit_logs(current_user.id)

@router.post("/compliance/reports", status_code=status.HTTP_201_CREATED)
async def create_compliance_report(report_type: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create compliance report"""
    service = AuditService(session)
    return await service.create_compliance_report(current_user.organization_id, report_type)

@router.get("/compliance/reports")
async def get_compliance_reports(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get compliance reports"""
    service = AuditService(session)
    return await service.get_compliance_reports(current_user.organization_id)

# ==================== MODULE 25: SEARCH & DISCOVERY ====================

@router.get("/search")
async def search(q: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Search resources"""
    service = SearchService(session)
    return await service.search(current_user.organization_id, q)

@router.get("/recommendations")
async def get_recommendations(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get recommendations"""
    service = SearchService(session)
    return await service.get_recommendations(current_user.id)

@router.post("/recommendations/{rec_id}/accept")
async def accept_recommendation(rec_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Accept recommendation"""
    service = SearchService(session)
    success = await service.accept_recommendation(rec_id)
    return {"accepted": success}
