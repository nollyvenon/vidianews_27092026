"""Integration services for Modules 21-25"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.models.integrations import (
    AnalyticsReport, Metric, Dashboard, Integration, Webhook, WebhookEvent,
    NotificationPreference, Notification, AuditTrail, ComplianceReport,
    SearchIndex, Recommendation
)


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_report(self, org_id: int, report_type: str, title: str, data: Dict) -> AnalyticsReport:
        report = AnalyticsReport(
            organization_id=org_id, report_type=report_type, title=title, data=data
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get_report(self, report_id: int) -> Optional[AnalyticsReport]:
        stmt = select(AnalyticsReport).where(AnalyticsReport.id == report_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_reports(self, org_id: int) -> List[AnalyticsReport]:
        stmt = select(AnalyticsReport).where(
            AnalyticsReport.organization_id == org_id
        ).order_by(desc(AnalyticsReport.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_metric(self, org_id: int, metric_type: str, value: float) -> Metric:
        metric = Metric(organization_id=org_id, metric_type=metric_type, value=value)
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def create_dashboard(self, user_id: int, org_id: int, name: str) -> Dashboard:
        dashboard = Dashboard(user_id=user_id, organization_id=org_id, name=name)
        self.session.add(dashboard)
        await self.session.commit()
        await self.session.refresh(dashboard)
        return dashboard

    async def get_dashboard(self, dashboard_id: int) -> Optional[Dashboard]:
        stmt = select(Dashboard).where(Dashboard.id == dashboard_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_dashboards(self, org_id: int) -> List[Dashboard]:
        stmt = select(Dashboard).where(Dashboard.organization_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class WebhookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_integration(self, org_id: int, integ_type: str, name: str, config: Dict) -> Integration:
        integration = Integration(
            organization_id=org_id, integration_type=integ_type, name=name, config=config
        )
        self.session.add(integration)
        await self.session.commit()
        await self.session.refresh(integration)
        return integration

    async def get_integration(self, integ_id: int) -> Optional[Integration]:
        stmt = select(Integration).where(Integration.id == integ_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_integrations(self, org_id: int) -> List[Integration]:
        stmt = select(Integration).where(Integration.organization_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_webhook(self, org_id: int, event_type: str, url: str) -> Webhook:
        webhook = Webhook(organization_id=org_id, event_type=event_type, url=url)
        self.session.add(webhook)
        await self.session.commit()
        await self.session.refresh(webhook)
        return webhook

    async def get_webhook(self, webhook_id: int) -> Optional[Webhook]:
        stmt = select(Webhook).where(Webhook.id == webhook_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_webhooks(self, org_id: int) -> List[Webhook]:
        stmt = select(Webhook).where(Webhook.organization_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def log_webhook_event(self, webhook_id: int, event_type: str, payload: Dict) -> WebhookEvent:
        event = WebhookEvent(webhook_id=webhook_id, event_type=event_type, payload=payload)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_webhook_events(self, webhook_id: int) -> List[WebhookEvent]:
        stmt = select(WebhookEvent).where(WebhookEvent.webhook_id == webhook_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_preferences(self, user_id: int) -> Optional[NotificationPreference]:
        stmt = select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_preferences(self, user_id: int, **kwargs) -> NotificationPreference:
        stmt = update(NotificationPreference).where(
            NotificationPreference.user_id == user_id
        ).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_preferences(user_id)

    async def create_notification(self, user_id: int, notif_type: str, title: str, message: str) -> Notification:
        notification = Notification(
            user_id=user_id, notification_type=notif_type, title=title, message=message
        )
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def get_notifications(self, user_id: int) -> List[Notification]:
        stmt = select(Notification).where(Notification.user_id == user_id).order_by(
            desc(Notification.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int) -> bool:
        stmt = update(Notification).where(Notification.id == notification_id).values(is_read=True)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0


class AuditService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_action(self, user_id: int, org_id: int, action: str, resource_type: str, resource_id: Optional[int] = None) -> AuditTrail:
        log = AuditTrail(
            user_id=user_id, organization_id=org_id, action=action,
            resource_type=resource_type, resource_id=resource_id
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_audit_logs(self, org_id: int, limit: int = 100) -> List[AuditTrail]:
        stmt = select(AuditTrail).where(
            AuditTrail.organization_id == org_id
        ).order_by(desc(AuditTrail.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_audit_logs(self, user_id: int) -> List[AuditTrail]:
        stmt = select(AuditTrail).where(AuditTrail.user_id == user_id).order_by(
            desc(AuditTrail.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_compliance_report(self, org_id: int, report_type: str) -> ComplianceReport:
        report = ComplianceReport(
            organization_id=org_id, report_type=report_type,
            period_start=datetime.now(timezone.utc), period_end=datetime.now(timezone.utc)
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get_compliance_reports(self, org_id: int) -> List[ComplianceReport]:
        stmt = select(ComplianceReport).where(ComplianceReport.organization_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class SearchService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def index_resource(self, org_id: int, resource_type: str, resource_id: int, title: str, content: str) -> SearchIndex:
        index = SearchIndex(
            organization_id=org_id, resource_type=resource_type, resource_id=resource_id,
            title=title, content=content
        )
        self.session.add(index)
        await self.session.commit()
        await self.session.refresh(index)
        return index

    async def search(self, org_id: int, query: str) -> List[SearchIndex]:
        stmt = select(SearchIndex).where(
            and_(
                SearchIndex.organization_id == org_id,
                SearchIndex.title.ilike(f"%{query}%")
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_recommendation(self, user_id: int, rec_type: str, resource_type: str, resource_id: int, score: float = 0.0) -> Recommendation:
        rec = Recommendation(
            user_id=user_id, recommendation_type=rec_type,
            recommended_resource_type=resource_type, recommended_resource_id=resource_id,
            score=score
        )
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def get_recommendations(self, user_id: int) -> List[Recommendation]:
        stmt = select(Recommendation).where(Recommendation.user_id == user_id).order_by(
            desc(Recommendation.score)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def accept_recommendation(self, rec_id: int) -> bool:
        stmt = update(Recommendation).where(Recommendation.id == rec_id).values(is_accepted=True)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
