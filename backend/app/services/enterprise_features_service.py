"""Security, moderation, rate limiting, notification and reporting services (async).

Timestamps are naive UTC to match the naive ``DateTime`` columns in ``app.models.enterprise_features``.
Objects returned from creates are refreshed so server-default columns (``created_at`` and similar) are loaded
before the response is serialized.
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, TypeVar

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enterprise_features import (
    SecurityAuditLog, AccessControl, RoleBasedAccess, ModerationQueue,
    ComplianceRule, RateLimitConfig, ThrottleLog, NotificationPreference,
    RealTimeNotification, AlertConfiguration, AdvancedReport, ReportTemplate,
    ReportSchedule, ExportJob, AccessLevel, ModerationStatus,
    NotificationType, ReportFormat
)

T = TypeVar("T")


def _utcnow() -> datetime:
    """Naive UTC, matching the naive DateTime columns"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _persist(db: AsyncSession, obj: T) -> T:
    """Add, commit and reload so server-default columns are populated."""
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


class SecurityService:
    def __init__(self, db: AsyncSession):
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
        return await _persist(self.db, SecurityAuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            changes=changes or {},
        ))

    async def get_audit_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        severity: Optional[str] = None,
        days: int = 30,
        limit: int = 100,
    ) -> List[SecurityAuditLog]:
        cutoff_date = _utcnow() - timedelta(days=days)
        stmt = select(SecurityAuditLog).where(SecurityAuditLog.created_at >= cutoff_date)

        if user_id:
            stmt = stmt.where(SecurityAuditLog.user_id == user_id)
        if action:
            stmt = stmt.where(SecurityAuditLog.action == action)
        if severity:
            stmt = stmt.where(SecurityAuditLog.severity == severity)

        result = await self.db.execute(stmt.order_by(SecurityAuditLog.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def _access(self, user_id: int, resource_type: str, resource_id: int) -> Optional[AccessControl]:
        return (await self.db.execute(select(AccessControl).where(and_(
            AccessControl.user_id == user_id,
            AccessControl.resource_type == resource_type,
            AccessControl.resource_id == resource_id,
        )))).scalars().first()

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
        return await _persist(self.db, AccessControl(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            access_level=access_level,
            permissions=permissions,
            granted_by=granted_by,
            expires_at=expires_at,
        ))

    async def revoke_access(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
    ) -> bool:
        access = await self._access(user_id, resource_type, resource_id)
        if access:
            await self.db.delete(access)
            await self.db.commit()
            return True
        return False

    async def check_permission(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
        permission: str,
    ) -> bool:
        access = await self._access(user_id, resource_type, resource_id)

        if not access:
            return False

        if access.expires_at and access.expires_at < _utcnow():
            await self.db.delete(access)
            await self.db.commit()
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
        return await _persist(self.db, RoleBasedAccess(
            user_id=user_id,
            role=role,
            permissions=permissions,
            can_edit_content=can_edit_content,
            can_delete_content=can_delete_content,
            can_manage_users=can_manage_users,
            can_access_analytics=can_access_analytics,
            can_access_admin=can_access_admin,
        ))

    async def get_user_role(self, user_id: int) -> Optional[RoleBasedAccess]:
        return (await self.db.execute(
            select(RoleBasedAccess).where(RoleBasedAccess.user_id == user_id)
        )).scalars().first()


class ModerationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_for_moderation(
        self,
        content_id: int,
        content_type: str,
        reason: str,
        flags: Optional[List[str]] = None,
    ) -> ModerationQueue:
        return await _persist(self.db, ModerationQueue(
            content_id=content_id,
            content_type=content_type,
            reason=reason,
            flags=flags or [],
        ))

    async def get_pending_items(self, limit: int = 50) -> List[ModerationQueue]:
        result = await self.db.execute(
            select(ModerationQueue).where(ModerationQueue.status == ModerationStatus.PENDING)
            .order_by(ModerationQueue.created_at).limit(limit)
        )
        return list(result.scalars().all())

    async def assign_moderator(
        self,
        item_id: int,
        moderator_id: int,
    ) -> Optional[ModerationQueue]:
        item = await self.db.get(ModerationQueue, item_id)
        if item:
            item.assigned_to = moderator_id
            await self.db.commit()
        return item

    async def review_content(
        self,
        item_id: int,
        reviewer_id: int,
        status: ModerationStatus,
        decision: str,
    ) -> Optional[ModerationQueue]:
        item = await self.db.get(ModerationQueue, item_id)
        if item:
            item.status = status
            item.reviewed_by = reviewer_id
            item.reviewed_at = _utcnow()
            item.decision = decision
            await self.db.commit()
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
        return await _persist(self.db, ComplianceRule(
            name=name,
            rule_type=rule_type,
            description=description,
            keywords=keywords or [],
            patterns=patterns or [],
            severity=severity,
            auto_action=auto_action,
        ))

    async def check_compliance(self, text: str) -> Dict[str, Any]:
        rules = (await self.db.execute(
            select(ComplianceRule).where(ComplianceRule.enabled == True)  # noqa: E712 - SQL comparison
        )).scalars().all()

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
                    # A pattern that is not a valid regular expression cannot match anything.
                    continue

        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "violation_count": len(violations),
        }


class RateLimitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _caller_identity(user_id: Optional[int], ip_address: Optional[str], column_user, column_ip) -> List[Any]:
        """Conditions that identify the caller. Only supplied identifiers count, so a missing IP never matches other callers' rows."""
        identity = []
        if user_id is not None:
            identity.append(column_user == user_id)
        if ip_address is not None:
            identity.append(column_ip == ip_address)
        return identity

    async def _count_throttled_since(self, user_id: Optional[int], ip_address: Optional[str], endpoint: str, since: datetime) -> int:
        identity = self._caller_identity(user_id, ip_address, ThrottleLog.user_id, ThrottleLog.ip_address)
        if not identity:
            return 0
        return (await self.db.execute(select(func.count(ThrottleLog.id)).where(and_(
            or_(*identity),
            ThrottleLog.endpoint == endpoint,
            ThrottleLog.throttled_at >= since,
        )))).scalar_one()

    async def check_rate_limit(
        self,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        endpoint: str = "*",
    ) -> Dict[str, Any]:
        identity = self._caller_identity(user_id, ip_address, RateLimitConfig.user_id, RateLimitConfig.ip_address)
        config = None
        if identity:
            config = (await self.db.execute(select(RateLimitConfig).where(and_(
                RateLimitConfig.enabled == True,  # noqa: E712 - SQL comparison
                RateLimitConfig.endpoint == endpoint,
                or_(*identity),
            )))).scalars().first()

        if not config:
            # No limit applies to this caller, so there is nothing left to count down.
            return {"limited": False, "minute_remaining": None, "hour_remaining": None, "day_remaining": None}

        now = _utcnow()
        minute_requests = await self._count_throttled_since(user_id, ip_address, endpoint, now - timedelta(minutes=1))
        hour_requests = await self._count_throttled_since(user_id, ip_address, endpoint, now - timedelta(hours=1))
        day_requests = await self._count_throttled_since(user_id, ip_address, endpoint, now - timedelta(days=1))

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
        return await _persist(self.db, ThrottleLog(
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            requests_count=requests_count,
            limit_type=limit_type,
        ))

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
        return await _persist(self.db, RateLimitConfig(
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            requests_per_minute=requests_per_minute,
            requests_per_hour=requests_per_hour,
            requests_per_day=requests_per_day,
            burst_limit=burst_limit,
        ))


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_preferences(self, user_id: int) -> Optional[NotificationPreference]:
        return (await self.db.execute(
            select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        )).scalars().first()

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

        await self.db.commit()
        await self.db.refresh(prefs)
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
        return await _persist(self.db, RealTimeNotification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
            action_url=action_url,
            source=source,
        ))

    async def get_notification(self, notification_id: int) -> Optional[RealTimeNotification]:
        return await self.db.get(RealTimeNotification, notification_id)

    async def mark_as_read(self, notification_id: int) -> Optional[RealTimeNotification]:
        notif = await self.db.get(RealTimeNotification, notification_id)
        if notif:
            notif.read = True
            notif.read_at = _utcnow()
            await self.db.commit()
        return notif

    async def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50,
    ) -> List[RealTimeNotification]:
        stmt = select(RealTimeNotification).where(RealTimeNotification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(RealTimeNotification.read == False)  # noqa: E712 - SQL comparison
        result = await self.db.execute(stmt.order_by(RealTimeNotification.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def create_alert_config(
        self,
        user_id: int,
        alert_type: str,
        condition: str,
        threshold: Optional[float] = None,
        notification_channels: Optional[List[str]] = None,
    ) -> AlertConfiguration:
        return await _persist(self.db, AlertConfiguration(
            user_id=user_id,
            alert_type=alert_type,
            condition=condition,
            threshold=threshold,
            notification_channels=notification_channels or [],
        ))


class ReportingService:
    def __init__(self, db: AsyncSession):
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
        return await _persist(self.db, AdvancedReport(
            user_id=user_id,
            name=name,
            report_type=report_type,
            format=format,
            query=query or {},
            filters=filters or {},
            status="pending",
        ))

    async def update_report_status(
        self,
        report_id: int,
        status: str,
        data: Optional[Dict] = None,
        file_path: Optional[str] = None,
    ) -> Optional[AdvancedReport]:
        report = await self.db.get(AdvancedReport, report_id)
        if report:
            report.status = status
            if data is not None:
                report.data = data
            if file_path is not None:
                report.file_path = file_path
            if status == "completed":
                now = _utcnow()
                report.generated_at = now
                report.expires_at = now + timedelta(days=30)
            await self.db.commit()
        return report

    async def get_user_reports(
        self,
        user_id: int,
        limit: int = 50,
    ) -> List[AdvancedReport]:
        result = await self.db.execute(
            select(AdvancedReport).where(AdvancedReport.user_id == user_id)
            .order_by(AdvancedReport.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def create_template(
        self,
        name: str,
        report_type: str,
        sections: List[str],
        format: ReportFormat,
        description: Optional[str] = None,
        schedule: Optional[str] = None,
    ) -> ReportTemplate:
        return await _persist(self.db, ReportTemplate(
            name=name,
            report_type=report_type,
            sections=sections,
            format=format,
            description=description,
            schedule=schedule,
        ))

    async def create_scheduled_report(
        self,
        user_id: int,
        template_id: int,
        name: str,
        cron_expression: str,
        recipient_emails: List[str],
    ) -> ReportSchedule:
        return await _persist(self.db, ReportSchedule(
            user_id=user_id,
            template_id=template_id,
            name=name,
            cron_expression=cron_expression,
            recipient_emails=recipient_emails,
        ))

    async def create_export_job(
        self,
        user_id: int,
        export_type: str,
        format: ReportFormat,
        filters: Optional[Dict] = None,
    ) -> ExportJob:
        return await _persist(self.db, ExportJob(
            user_id=user_id,
            export_type=export_type,
            format=format,
            filters=filters or {},
            status="pending",
        ))

    async def update_export_progress(
        self,
        job_id: int,
        progress: int,
        record_count: int = 0,
    ) -> Optional[ExportJob]:
        job = await self.db.get(ExportJob, job_id)
        if job:
            job.progress = min(progress, 100)
            job.record_count = record_count
            if progress >= 100:
                job.status = "completed"
                job.completed_at = _utcnow()
            await self.db.commit()
        return job

    async def get_export_job(self, job_id: int) -> Optional[ExportJob]:
        return await self.db.get(ExportJob, job_id)
