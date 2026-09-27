from sqlalchemy import func, select, and_, or_
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib
import re
from app.models.enterprise_features import (
    SecurityAuditLog, AccessControl, RoleBasedAccess, ModerationQueue,
    ComplianceRule, RateLimitConfig, ThrottleLog, NotificationPreference,
    RealTimeNotification, AlertConfiguration, AdvancedReport, ReportTemplate,
    ReportSchedule, ExportJob, AccessLevel, PermissionType, ModerationStatus,
    NotificationType, ReportFormat
)


class SecurityService:
    def __init__(self, db: Session):
        self.db = db

    async def log_audit_event(
        self,
        user_id: int,
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        status: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        severity: str = "info",
        changes: Optional[Dict] = None,
    ) -> SecurityAuditLog:
        log = SecurityAuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            changes=changes or {},
        )
        self.db.add(log)
        self.db.commit()
        return log

    async def get_audit_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        severity: Optional[str] = None,
        days: int = 30,
        limit: int = 100,
    ) -> List[SecurityAuditLog]:
        query = self.db.query(SecurityAuditLog)
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(SecurityAuditLog.created_at >= cutoff_date)

        if user_id:
            query = query.filter(SecurityAuditLog.user_id == user_id)
        if action:
            query = query.filter(SecurityAuditLog.action == action)
        if severity:
            query = query.filter(SecurityAuditLog.severity == severity)

        return query.order_by(SecurityAuditLog.created_at.desc()).limit(limit).all()

    async def grant_access(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
        access_level: AccessLevel,
        permissions: List[str],
        granted_by: int,
        expires_at: Optional[datetime] = None,
    ) -> AccessControl:
        access = AccessControl(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            access_level=access_level,
            permissions=permissions,
            granted_by=granted_by,
            expires_at=expires_at,
        )
        self.db.add(access)
        self.db.commit()
        return access

    async def revoke_access(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
    ) -> bool:
        access = self.db.query(AccessControl).filter(
            and_(
                AccessControl.user_id == user_id,
                AccessControl.resource_type == resource_type,
                AccessControl.resource_id == resource_id,
            )
        ).first()
        if access:
            self.db.delete(access)
            self.db.commit()
            return True
        return False

    async def check_permission(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
        permission: str,
    ) -> bool:
        access = self.db.query(AccessControl).filter(
            and_(
                AccessControl.user_id == user_id,
                AccessControl.resource_type == resource_type,
                AccessControl.resource_id == resource_id,
            )
        ).first()

        if not access:
            return False

        if access.expires_at and access.expires_at < datetime.utcnow():
            self.db.delete(access)
            self.db.commit()
            return False

        return permission in access.permissions

    async def assign_role(
        self,
        user_id: int,
        role: str,
        permissions: List[str],
        can_edit_content: bool = False,
        can_delete_content: bool = False,
        can_manage_users: bool = False,
        can_access_analytics: bool = False,
        can_access_admin: bool = False,
    ) -> RoleBasedAccess:
        role_access = RoleBasedAccess(
            user_id=user_id,
            role=role,
            permissions=permissions,
            can_edit_content=can_edit_content,
            can_delete_content=can_delete_content,
            can_manage_users=can_manage_users,
            can_access_analytics=can_access_analytics,
            can_access_admin=can_access_admin,
        )
        self.db.add(role_access)
        self.db.commit()
        return role_access

    async def get_user_role(self, user_id: int) -> Optional[RoleBasedAccess]:
        return self.db.query(RoleBasedAccess).filter(
            RoleBasedAccess.user_id == user_id
        ).first()


class ModerationService:
    def __init__(self, db: Session):
        self.db = db

    async def submit_for_moderation(
        self,
        content_id: int,
        content_type: str,
        reason: str,
        flags: Optional[List[str]] = None,
    ) -> ModerationQueue:
        queue_item = ModerationQueue(
            content_id=content_id,
            content_type=content_type,
            reason=reason,
            flags=flags or [],
        )
        self.db.add(queue_item)
        self.db.commit()
        return queue_item

    async def get_pending_items(self, limit: int = 50) -> List[ModerationQueue]:
        return self.db.query(ModerationQueue).filter(
            ModerationQueue.status == ModerationStatus.PENDING
        ).order_by(ModerationQueue.created_at).limit(limit).all()

    async def assign_moderator(
        self,
        item_id: int,
        moderator_id: int,
    ) -> Optional[ModerationQueue]:
        item = self.db.query(ModerationQueue).filter(
            ModerationQueue.id == item_id
        ).first()
        if item:
            item.assigned_to = moderator_id
            self.db.commit()
        return item

    async def review_content(
        self,
        item_id: int,
        reviewer_id: int,
        status: ModerationStatus,
        decision: str,
    ) -> Optional[ModerationQueue]:
        item = self.db.query(ModerationQueue).filter(
            ModerationQueue.id == item_id
        ).first()
        if item:
            item.status = status
            item.reviewed_by = reviewer_id
            item.reviewed_at = datetime.utcnow()
            item.decision = decision
            self.db.commit()
        return item

    async def add_compliance_rule(
        self,
        name: str,
        rule_type: str,
        description: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        patterns: Optional[List[str]] = None,
        severity: str = "medium",
        auto_action: Optional[str] = None,
    ) -> ComplianceRule:
        rule = ComplianceRule(
            name=name,
            rule_type=rule_type,
            description=description,
            keywords=keywords or [],
            patterns=patterns or [],
            severity=severity,
            auto_action=auto_action,
        )
        self.db.add(rule)
        self.db.commit()
        return rule

    async def check_compliance(self, text: str) -> Dict[str, Any]:
        rules = self.db.query(ComplianceRule).filter(
            ComplianceRule.enabled == True
        ).all()

        violations = []
        for rule in rules:
            for keyword in rule.keywords:
                if keyword.lower() in text.lower():
                    violations.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "severity": rule.severity,
                        "match_type": "keyword",
                    })

            for pattern in rule.patterns:
                try:
                    if re.search(pattern, text, re.IGNORECASE):
                        violations.append({
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "severity": rule.severity,
                            "match_type": "pattern",
                        })
                except re.error:
                    pass

        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "violation_count": len(violations),
        }


class RateLimitService:
    def __init__(self, db: Session):
        self.db = db

    async def check_rate_limit(
        self,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        endpoint: str = "*",
    ) -> Dict[str, Any]:
        config = self.db.query(RateLimitConfig).filter(
            and_(
                RateLimitConfig.enabled == True,
                or_(
                    and_(
                        RateLimitConfig.user_id == user_id,
                        RateLimitConfig.endpoint == endpoint,
                    ),
                    and_(
                        RateLimitConfig.ip_address == ip_address,
                        RateLimitConfig.endpoint == endpoint,
                    ),
                ),
            )
        ).first()

        if not config:
            return {"limited": False, "remaining": None}

        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)

        minute_requests = self.db.query(func.count(ThrottleLog.id)).filter(
            and_(
                or_(
                    ThrottleLog.user_id == user_id,
                    ThrottleLog.ip_address == ip_address,
                ),
                ThrottleLog.endpoint == endpoint,
                ThrottleLog.throttled_at >= minute_ago,
            )
        ).scalar()

        hour_requests = self.db.query(func.count(ThrottleLog.id)).filter(
            and_(
                or_(
                    ThrottleLog.user_id == user_id,
                    ThrottleLog.ip_address == ip_address,
                ),
                ThrottleLog.endpoint == endpoint,
                ThrottleLog.throttled_at >= hour_ago,
            )
        ).scalar()

        day_requests = self.db.query(func.count(ThrottleLog.id)).filter(
            and_(
                or_(
                    ThrottleLog.user_id == user_id,
                    ThrottleLog.ip_address == ip_address,
                ),
                ThrottleLog.endpoint == endpoint,
                ThrottleLog.throttled_at >= day_ago,
            )
        ).scalar()

        return {
            "limited": (
                minute_requests >= config.requests_per_minute
                or hour_requests >= config.requests_per_hour
                or day_requests >= config.requests_per_day
            ),
            "minute_remaining": max(0, config.requests_per_minute - minute_requests),
            "hour_remaining": max(0, config.requests_per_hour - hour_requests),
            "day_remaining": max(0, config.requests_per_day - day_requests),
        }

    async def log_throttle(
        self,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        endpoint: str = "*",
        requests_count: int = 1,
        limit_type: str = "minute",
    ) -> ThrottleLog:
        log = ThrottleLog(
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            requests_count=requests_count,
            limit_type=limit_type,
        )
        self.db.add(log)
        self.db.commit()
        return log

    async def create_rate_limit_config(
        self,
        endpoint: str,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        burst_limit: int = 100,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> RateLimitConfig:
        config = RateLimitConfig(
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            requests_per_minute=requests_per_minute,
            requests_per_hour=requests_per_hour,
            requests_per_day=requests_per_day,
            burst_limit=burst_limit,
        )
        self.db.add(config)
        self.db.commit()
        return config


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def get_preferences(self, user_id: int) -> Optional[NotificationPreference]:
        return self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()

    async def update_preferences(
        self,
        user_id: int,
        email_enabled: Optional[bool] = None,
        push_enabled: Optional[bool] = None,
        sms_enabled: Optional[bool] = None,
        in_app_enabled: Optional[bool] = None,
        frequency: Optional[str] = None,
        do_not_disturb_start: Optional[str] = None,
        do_not_disturb_end: Optional[str] = None,
    ) -> NotificationPreference:
        prefs = await self.get_preferences(user_id)
        if not prefs:
            prefs = NotificationPreference(user_id=user_id)
            self.db.add(prefs)

        if email_enabled is not None:
            prefs.email_enabled = email_enabled
        if push_enabled is not None:
            prefs.push_enabled = push_enabled
        if sms_enabled is not None:
            prefs.sms_enabled = sms_enabled
        if in_app_enabled is not None:
            prefs.in_app_enabled = in_app_enabled
        if frequency is not None:
            prefs.frequency = frequency
        if do_not_disturb_start is not None:
            prefs.do_not_disturb_start = do_not_disturb_start
        if do_not_disturb_end is not None:
            prefs.do_not_disturb_end = do_not_disturb_end

        self.db.commit()
        return prefs

    async def create_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict] = None,
        action_url: Optional[str] = None,
        source: Optional[str] = None,
    ) -> RealTimeNotification:
        notification = RealTimeNotification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
            action_url=action_url,
            source=source,
        )
        self.db.add(notification)
        self.db.commit()
        return notification

    async def mark_as_read(self, notification_id: int) -> Optional[RealTimeNotification]:
        notif = self.db.query(RealTimeNotification).filter(
            RealTimeNotification.id == notification_id
        ).first()
        if notif:
            notif.read = True
            notif.read_at = datetime.utcnow()
            self.db.commit()
        return notif

    async def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50,
    ) -> List[RealTimeNotification]:
        query = self.db.query(RealTimeNotification).filter(
            RealTimeNotification.user_id == user_id
        )
        if unread_only:
            query = query.filter(RealTimeNotification.read == False)
        return query.order_by(RealTimeNotification.created_at.desc()).limit(limit).all()

    async def create_alert_config(
        self,
        user_id: int,
        alert_type: str,
        condition: str,
        threshold: Optional[float] = None,
        notification_channels: Optional[List[str]] = None,
    ) -> AlertConfiguration:
        config = AlertConfiguration(
            user_id=user_id,
            alert_type=alert_type,
            condition=condition,
            threshold=threshold,
            notification_channels=notification_channels or [],
        )
        self.db.add(config)
        self.db.commit()
        return config


class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    async def create_report(
        self,
        user_id: int,
        name: str,
        report_type: str,
        format: ReportFormat,
        query: Optional[Dict] = None,
        filters: Optional[Dict] = None,
    ) -> AdvancedReport:
        report = AdvancedReport(
            user_id=user_id,
            name=name,
            report_type=report_type,
            format=format,
            query=query or {},
            filters=filters or {},
            status="pending",
        )
        self.db.add(report)
        self.db.commit()
        return report

    async def update_report_status(
        self,
        report_id: int,
        status: str,
        data: Optional[Dict] = None,
        file_path: Optional[str] = None,
    ) -> Optional[AdvancedReport]:
        report = self.db.query(AdvancedReport).filter(
            AdvancedReport.id == report_id
        ).first()
        if report:
            report.status = status
            if data is not None:
                report.data = data
            if file_path is not None:
                report.file_path = file_path
            if status == "completed":
                report.generated_at = datetime.utcnow()
                report.expires_at = datetime.utcnow() + timedelta(days=30)
            self.db.commit()
        return report

    async def get_user_reports(
        self,
        user_id: int,
        limit: int = 50,
    ) -> List[AdvancedReport]:
        return self.db.query(AdvancedReport).filter(
            AdvancedReport.user_id == user_id
        ).order_by(AdvancedReport.created_at.desc()).limit(limit).all()

    async def create_template(
        self,
        name: str,
        report_type: str,
        sections: List[str],
        format: ReportFormat,
        description: Optional[str] = None,
        schedule: Optional[str] = None,
    ) -> ReportTemplate:
        template = ReportTemplate(
            name=name,
            report_type=report_type,
            sections=sections,
            format=format,
            description=description,
            schedule=schedule,
        )
        self.db.add(template)
        self.db.commit()
        return template

    async def create_scheduled_report(
        self,
        user_id: int,
        template_id: int,
        name: str,
        cron_expression: str,
        recipient_emails: List[str],
    ) -> ReportSchedule:
        schedule = ReportSchedule(
            user_id=user_id,
            template_id=template_id,
            name=name,
            cron_expression=cron_expression,
            recipient_emails=recipient_emails,
        )
        self.db.add(schedule)
        self.db.commit()
        return schedule

    async def create_export_job(
        self,
        user_id: int,
        export_type: str,
        format: ReportFormat,
        filters: Optional[Dict] = None,
    ) -> ExportJob:
        job = ExportJob(
            user_id=user_id,
            export_type=export_type,
            format=format,
            filters=filters or {},
            status="pending",
        )
        self.db.add(job)
        self.db.commit()
        return job

    async def update_export_progress(
        self,
        job_id: int,
        progress: int,
        record_count: int = 0,
    ) -> Optional[ExportJob]:
        job = self.db.query(ExportJob).filter(
            ExportJob.id == job_id
        ).first()
        if job:
            job.progress = min(progress, 100)
            job.record_count = record_count
            if progress >= 100:
                job.status = "completed"
                job.completed_at = datetime.utcnow()
            self.db.commit()
        return job

    async def get_export_job(self, job_id: int) -> Optional[ExportJob]:
        return self.db.query(ExportJob).filter(
            ExportJob.id == job_id
        ).first()
