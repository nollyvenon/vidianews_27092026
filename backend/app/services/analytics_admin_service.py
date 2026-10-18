"""Analytics and admin services (async).

Timestamps are naive UTC to match the analytics_admin columns. Callers pass aware or naive
datetimes; ``to_naive_utc`` normalises them.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics_admin import (
    AdminLog,
    AnalyticsEvent,
    EngagementMetric,
    NotificationPreference,
    PermissionPolicy,
    Report,
    RevenueMetric,
    SystemAlert,
    SystemHealth,
    UserBehavior,
    UserMetric,
    utc_now_naive,
)
from app.utils.exceptions import NotFoundError


def to_naive_utc(value: datetime) -> datetime:
    """Aware datetimes are converted to UTC; naive ones are taken as UTC already."""
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


class AnalyticsEventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_event(self, org_id: int, user_id: int, event_type: str, event_data: Optional[dict] = None,
                        session_id: Optional[str] = None, ip_address: Optional[str] = None,
                        user_agent: Optional[str] = None) -> AnalyticsEvent:
        event = AnalyticsEvent(
            organization_id=org_id,
            user_id=user_id,
            event_type=event_type,
            event_data=event_data or {},
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_events_by_user(self, user_id: int, limit: int = 100) -> List[AnalyticsEvent]:
        result = await self.session.execute(
            select(AnalyticsEvent)
            .where(AnalyticsEvent.user_id == user_id)
            .order_by(AnalyticsEvent.created_at.desc(), AnalyticsEvent.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_events_by_type(self, org_id: int, event_type: str, days: int = 7) -> List[AnalyticsEvent]:
        start_date = utc_now_naive() - timedelta(days=days)
        result = await self.session.execute(
            select(AnalyticsEvent).where(and_(
                AnalyticsEvent.organization_id == org_id,
                AnalyticsEvent.event_type == event_type,
                AnalyticsEvent.created_at >= start_date,
            ))
        )
        return list(result.scalars().all())


class UserMetricService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user_metric(self, user_id: int) -> UserMetric:
        metric = (await self.session.execute(
            select(UserMetric).where(UserMetric.user_id == user_id)
        )).scalar_one_or_none()
        if metric is None:
            metric = UserMetric(user_id=user_id)
            self.session.add(metric)
            await self.session.commit()
            await self.session.refresh(metric)
        return metric

    async def update_user_metric(self, user_id: int, **kwargs: Any) -> UserMetric:
        metric = await self.get_or_create_user_metric(user_id)
        for key, value in kwargs.items():
            if hasattr(metric, key):
                setattr(metric, key, value)
        metric.updated_at = utc_now_naive()
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def calculate_engagement_score(self, user_id: int) -> float:
        metric = await self.get_or_create_user_metric(user_id)
        score = (
            metric.total_logins * 2
            + metric.courses_completed * 50
            + metric.total_session_time / 60
            + metric.total_spend / 10
        )
        await self.update_user_metric(user_id, engagement_score=score)
        return score


class RevenueMetricService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_or_update_revenue_metric(self, org_id: int, date: datetime, total_revenue: float,
                                              course_revenue: float = 0.0,
                                              membership_revenue: float = 0.0) -> RevenueMetric:
        date = to_naive_utc(date)
        metric = (await self.session.execute(
            select(RevenueMetric).where(and_(
                RevenueMetric.organization_id == org_id,
                RevenueMetric.date == date,
            ))
        )).scalar_one_or_none()

        if metric is not None:
            metric.total_revenue = total_revenue
            metric.course_revenue = course_revenue
            metric.membership_revenue = membership_revenue
            metric.transaction_count += 1
            metric.average_transaction = total_revenue / metric.transaction_count if metric.transaction_count > 0 else 0
        else:
            metric = RevenueMetric(
                organization_id=org_id,
                date=date,
                total_revenue=total_revenue,
                course_revenue=course_revenue,
                membership_revenue=membership_revenue,
                transaction_count=1,
                average_transaction=total_revenue,
            )
            self.session.add(metric)

        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def get_revenue_range(self, org_id: int, start_date: datetime, end_date: datetime) -> List[RevenueMetric]:
        result = await self.session.execute(
            select(RevenueMetric).where(and_(
                RevenueMetric.organization_id == org_id,
                RevenueMetric.date >= to_naive_utc(start_date),
                RevenueMetric.date <= to_naive_utc(end_date),
            )).order_by(RevenueMetric.date)
        )
        return list(result.scalars().all())


class EngagementMetricService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_engagement_metric(self, org_id: int, date: datetime, active_users: int,
                                       new_users: int) -> EngagementMetric:
        metric = EngagementMetric(
            organization_id=org_id, date=to_naive_utc(date), active_users=active_users, new_users=new_users,
        )
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def get_engagement_trend(self, org_id: int, days: int = 30) -> List[EngagementMetric]:
        start_date = utc_now_naive() - timedelta(days=days)
        result = await self.session.execute(
            select(EngagementMetric).where(and_(
                EngagementMetric.organization_id == org_id,
                EngagementMetric.date >= start_date,
            )).order_by(EngagementMetric.date)
        )
        return list(result.scalars().all())


class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_report(self, org_id: int, report_type: str, title: str, start_date: datetime,
                            end_date: datetime, created_by: int, data: Optional[dict] = None) -> Report:
        report = Report(
            organization_id=org_id,
            report_type=report_type,
            title=title,
            start_date=to_naive_utc(start_date),
            end_date=to_naive_utc(end_date),
            report_data=data or {},
            created_by=created_by,
            generated_at=utc_now_naive(),
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get_report(self, report_id: int) -> Optional[Report]:
        return await self.session.get(Report, report_id)

    async def get_organization_reports(self, org_id: int, report_type: Optional[str] = None) -> List[Report]:
        stmt = select(Report).where(Report.organization_id == org_id)
        if report_type:
            stmt = stmt.where(Report.report_type == report_type)
        result = await self.session.execute(stmt.order_by(Report.generated_at.desc()))
        return list(result.scalars().all())


class AdminLogService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_admin_action(self, org_id: int, admin_id: int, action: str, resource_type: str,
                               resource_id: Optional[int] = None, changes: Optional[dict] = None,
                               reason: Optional[str] = None, ip_address: Optional[str] = None) -> AdminLog:
        log = AdminLog(
            organization_id=org_id,
            admin_id=admin_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes or {},
            reason=reason,
            ip_address=ip_address,
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_admin_logs(self, org_id: int, limit: int = 100) -> List[AdminLog]:
        result = await self.session.execute(
            select(AdminLog)
            .where(AdminLog.organization_id == org_id)
            .order_by(AdminLog.created_at.desc(), AdminLog.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_logs_by_admin(self, admin_id: int, limit: int = 100) -> List[AdminLog]:
        result = await self.session.execute(
            select(AdminLog)
            .where(AdminLog.admin_id == admin_id)
            .order_by(AdminLog.created_at.desc(), AdminLog.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


class SystemHealthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_health_check(self, org_id: int, cpu_usage: float, memory_usage: float, disk_usage: float,
                                  api_response_time: float, error_rate: float) -> SystemHealth:
        health = SystemHealth(
            organization_id=org_id,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            api_response_time=api_response_time,
            error_rate=error_rate,
            uptime_percentage=100.0 - error_rate,
        )
        self.session.add(health)
        await self.session.commit()
        await self.session.refresh(health)
        return health

    async def get_latest_health(self, org_id: int) -> Optional[SystemHealth]:
        result = await self.session.execute(
            select(SystemHealth)
            .where(SystemHealth.organization_id == org_id)
            .order_by(SystemHealth.created_at.desc(), SystemHealth.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_health_history(self, org_id: int, hours: int = 24) -> List[SystemHealth]:
        start_time = utc_now_naive() - timedelta(hours=hours)
        result = await self.session.execute(
            select(SystemHealth).where(and_(
                SystemHealth.organization_id == org_id,
                SystemHealth.created_at >= start_time,
            )).order_by(SystemHealth.created_at)
        )
        return list(result.scalars().all())


class UserBehaviorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_behavior(self, user_id: int, page_visited: str, time_spent: int,
                           device_type: Optional[str] = None, browser: Optional[str] = None,
                           os: Optional[str] = None) -> UserBehavior:
        behavior = UserBehavior(
            user_id=user_id,
            page_visited=page_visited,
            time_spent=time_spent,
            device_type=device_type,
            browser=browser,
            operating_system=os,
        )
        self.session.add(behavior)
        await self.session.commit()
        await self.session.refresh(behavior)
        return behavior

    async def get_user_behavior(self, user_id: int, days: int = 30) -> List[UserBehavior]:
        start_date = utc_now_naive() - timedelta(days=days)
        result = await self.session.execute(
            select(UserBehavior).where(and_(
                UserBehavior.user_id == user_id,
                UserBehavior.created_at >= start_date,
            )).order_by(UserBehavior.created_at.desc())
        )
        return list(result.scalars().all())


class NotificationPreferenceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_preference(self, user_id: int) -> NotificationPreference:
        pref = (await self.session.execute(
            select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        )).scalar_one_or_none()
        if pref is None:
            pref = NotificationPreference(user_id=user_id)
            self.session.add(pref)
            await self.session.commit()
            await self.session.refresh(pref)
        return pref

    async def update_preference(self, user_id: int, **kwargs: Any) -> NotificationPreference:
        pref = await self.get_or_create_preference(user_id)
        for key, value in kwargs.items():
            if hasattr(pref, key):
                setattr(pref, key, value)
        pref.updated_at = utc_now_naive()
        await self.session.commit()
        await self.session.refresh(pref)
        return pref


class PermissionPolicyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_policy(self, name: str, permissions: dict, description: Optional[str] = None) -> PermissionPolicy:
        policy = PermissionPolicy(name=name, description=description, permissions=permissions)
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def get_policy(self, policy_id: int) -> Optional[PermissionPolicy]:
        return await self.session.get(PermissionPolicy, policy_id)

    async def get_policy_by_name(self, name: str) -> Optional[PermissionPolicy]:
        return (await self.session.execute(
            select(PermissionPolicy).where(PermissionPolicy.name == name)
        )).scalar_one_or_none()


class SystemAlertService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_alert(self, org_id: int, alert_type: str, message: str, severity: str = "warning") -> SystemAlert:
        alert = SystemAlert(organization_id=org_id, alert_type=alert_type, message=message, severity=severity)
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def resolve_alert(self, alert_id: int) -> None:
        alert = await self.session.get(SystemAlert, alert_id)
        if alert is None:
            raise NotFoundError("Alert")
        alert.is_resolved = True
        alert.resolved_at = utc_now_naive()
        await self.session.commit()

    async def get_active_alerts(self, org_id: int) -> List[SystemAlert]:
        result = await self.session.execute(
            select(SystemAlert).where(and_(
                SystemAlert.organization_id == org_id,
                SystemAlert.is_resolved == False,  # noqa: E712 - SQL comparison
            )).order_by(SystemAlert.created_at.desc())
        )
        return list(result.scalars().all())
