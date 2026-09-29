"""Analytics and admin services"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.analytics_admin import (
    AnalyticsEvent, AnalyticsDashboard, UserMetric, RevenueMetric,
    EngagementMetric, Report, AdminLog, SystemHealth, UserBehavior,
    NotificationPreference, ContentModeration, PermissionPolicy, UserRole,
    SystemAlert
)
from datetime import datetime, timezone, timedelta


class AnalyticsEventService:
    @staticmethod
    def log_event(db: Session, org_id: int, user_id: int, event_type: str,
                 event_data: dict = None, session_id: str = None,
                 ip_address: str = None, user_agent: str = None) -> AnalyticsEvent:
        event = AnalyticsEvent(
            organization_id=org_id,
            user_id=user_id,
            event_type=event_type,
            event_data=event_data or {},
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_events_by_user(db: Session, user_id: int, limit: int = 100):
        return db.query(AnalyticsEvent).filter(
            AnalyticsEvent.user_id == user_id
        ).order_by(AnalyticsEvent.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_events_by_type(db: Session, org_id: int, event_type: str, days: int = 7):
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.query(AnalyticsEvent).filter(
            and_(
                AnalyticsEvent.organization_id == org_id,
                AnalyticsEvent.event_type == event_type,
                AnalyticsEvent.created_at >= start_date
            )
        ).all()


class UserMetricService:
    @staticmethod
    def get_or_create_user_metric(db: Session, user_id: int) -> UserMetric:
        metric = db.query(UserMetric).filter(UserMetric.user_id == user_id).first()
        if not metric:
            metric = UserMetric(user_id=user_id)
            db.add(metric)
            db.commit()
            db.refresh(metric)
        return metric

    @staticmethod
    def update_user_metric(db: Session, user_id: int, **kwargs):
        metric = UserMetricService.get_or_create_user_metric(db, user_id)
        for key, value in kwargs.items():
            if hasattr(metric, key):
                setattr(metric, key, value)
        metric.updated_at = datetime.now(timezone.utc)
        db.commit()
        return metric

    @staticmethod
    def calculate_engagement_score(db: Session, user_id: int) -> float:
        metric = UserMetricService.get_or_create_user_metric(db, user_id)
        score = 0.0
        score += metric.total_logins * 2
        score += metric.courses_completed * 50
        score += metric.total_session_time / 60
        score += metric.total_spend / 10
        UserMetricService.update_user_metric(db, user_id, engagement_score=score)
        return score


class RevenueMetricService:
    @staticmethod
    def create_or_update_revenue_metric(db: Session, org_id: int, date: datetime,
                                       total_revenue: float, course_revenue: float = 0.0,
                                       membership_revenue: float = 0.0) -> RevenueMetric:
        metric = db.query(RevenueMetric).filter(
            and_(
                RevenueMetric.organization_id == org_id,
                RevenueMetric.date == date.date()
            )
        ).first()

        if metric:
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
                average_transaction=total_revenue
            )
            db.add(metric)

        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def get_revenue_range(db: Session, org_id: int, start_date: datetime, end_date: datetime):
        return db.query(RevenueMetric).filter(
            and_(
                RevenueMetric.organization_id == org_id,
                RevenueMetric.date >= start_date,
                RevenueMetric.date <= end_date
            )
        ).order_by(RevenueMetric.date).all()


class EngagementMetricService:
    @staticmethod
    def create_engagement_metric(db: Session, org_id: int, date: datetime,
                                active_users: int, new_users: int) -> EngagementMetric:
        metric = EngagementMetric(
            organization_id=org_id,
            date=date,
            active_users=active_users,
            new_users=new_users
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def get_engagement_trend(db: Session, org_id: int, days: int = 30):
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.query(EngagementMetric).filter(
            and_(
                EngagementMetric.organization_id == org_id,
                EngagementMetric.date >= start_date
            )
        ).order_by(EngagementMetric.date).all()


class ReportService:
    @staticmethod
    def create_report(db: Session, org_id: int, report_type: str, title: str,
                     start_date: datetime, end_date: datetime,
                     created_by: int, data: dict = None) -> Report:
        report = Report(
            organization_id=org_id,
            report_type=report_type,
            title=title,
            start_date=start_date,
            end_date=end_date,
            report_data=data or {},
            created_by=created_by,
            generated_at=datetime.now(timezone.utc)
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_report(db: Session, report_id: int) -> Report:
        return db.query(Report).filter(Report.id == report_id).first()

    @staticmethod
    def get_organization_reports(db: Session, org_id: int, report_type: str = None):
        query = db.query(Report).filter(Report.organization_id == org_id)
        if report_type:
            query = query.filter(Report.report_type == report_type)
        return query.order_by(Report.generated_at.desc()).all()


class AdminLogService:
    @staticmethod
    def log_admin_action(db: Session, org_id: int, admin_id: int, action: str,
                        resource_type: str, resource_id: int = None,
                        changes: dict = None, reason: str = None,
                        ip_address: str = None) -> AdminLog:
        log = AdminLog(
            organization_id=org_id,
            admin_id=admin_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes or {},
            reason=reason,
            ip_address=ip_address
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_admin_logs(db: Session, org_id: int, limit: int = 100):
        return db.query(AdminLog).filter(
            AdminLog.organization_id == org_id
        ).order_by(AdminLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_logs_by_admin(db: Session, admin_id: int, limit: int = 100):
        return db.query(AdminLog).filter(
            AdminLog.admin_id == admin_id
        ).order_by(AdminLog.created_at.desc()).limit(limit).all()


class SystemHealthService:
    @staticmethod
    def create_health_check(db: Session, org_id: int, cpu_usage: float,
                          memory_usage: float, disk_usage: float,
                          api_response_time: float, error_rate: float) -> SystemHealth:
        health = SystemHealth(
            organization_id=org_id,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            api_response_time=api_response_time,
            error_rate=error_rate,
            uptime_percentage=100.0 - error_rate
        )
        db.add(health)
        db.commit()
        db.refresh(health)
        return health

    @staticmethod
    def get_latest_health(db: Session, org_id: int) -> SystemHealth:
        return db.query(SystemHealth).filter(
            SystemHealth.organization_id == org_id
        ).order_by(SystemHealth.created_at.desc()).first()

    @staticmethod
    def get_health_history(db: Session, org_id: int, hours: int = 24):
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        return db.query(SystemHealth).filter(
            and_(
                SystemHealth.organization_id == org_id,
                SystemHealth.created_at >= start_time
            )
        ).order_by(SystemHealth.created_at).all()


class UserBehaviorService:
    @staticmethod
    def log_behavior(db: Session, user_id: int, page_visited: str,
                    time_spent: int, device_type: str = None,
                    browser: str = None, os: str = None) -> UserBehavior:
        behavior = UserBehavior(
            user_id=user_id,
            page_visited=page_visited,
            time_spent=time_spent,
            device_type=device_type,
            browser=browser,
            operating_system=os
        )
        db.add(behavior)
        db.commit()
        db.refresh(behavior)
        return behavior

    @staticmethod
    def get_user_behavior(db: Session, user_id: int, days: int = 30):
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.query(UserBehavior).filter(
            and_(
                UserBehavior.user_id == user_id,
                UserBehavior.created_at >= start_date
            )
        ).order_by(UserBehavior.created_at.desc()).all()


class NotificationPreferenceService:
    @staticmethod
    def get_or_create_preference(db: Session, user_id: int) -> NotificationPreference:
        pref = db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
        if not pref:
            pref = NotificationPreference(user_id=user_id)
            db.add(pref)
            db.commit()
            db.refresh(pref)
        return pref

    @staticmethod
    def update_preference(db: Session, user_id: int, **kwargs) -> NotificationPreference:
        pref = NotificationPreferenceService.get_or_create_preference(db, user_id)
        for key, value in kwargs.items():
            if hasattr(pref, key):
                setattr(pref, key, value)
        pref.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(pref)
        return pref


class PermissionPolicyService:
    @staticmethod
    def create_policy(db: Session, name: str, permissions: dict,
                     description: str = None) -> PermissionPolicy:
        policy = PermissionPolicy(
            name=name,
            description=description,
            permissions=permissions
        )
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy

    @staticmethod
    def get_policy(db: Session, policy_id: int) -> PermissionPolicy:
        return db.query(PermissionPolicy).filter(PermissionPolicy.id == policy_id).first()

    @staticmethod
    def get_policy_by_name(db: Session, name: str) -> PermissionPolicy:
        return db.query(PermissionPolicy).filter(PermissionPolicy.name == name).first()


class SystemAlertService:
    @staticmethod
    def create_alert(db: Session, org_id: int, alert_type: str, message: str,
                    severity: str = "warning") -> SystemAlert:
        alert = SystemAlert(
            organization_id=org_id,
            alert_type=alert_type,
            message=message,
            severity=severity
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def resolve_alert(db: Session, alert_id: int):
        alert = db.query(SystemAlert).filter(SystemAlert.id == alert_id).first()
        alert.is_resolved = True
        alert.resolved_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def get_active_alerts(db: Session, org_id: int):
        return db.query(SystemAlert).filter(
            and_(
                SystemAlert.organization_id == org_id,
                SystemAlert.is_resolved == False
            )
        ).order_by(SystemAlert.created_at.desc()).all()
