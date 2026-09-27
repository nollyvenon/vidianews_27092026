"""Services for Logging, Analytics & Documentation: Modules 46-50"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc, func
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from app.models.logging_analytics import *


class LoggingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_message(self, level: str, service: str, message: str, user_id: int = None, metadata: dict = {}) -> LogEntry:
        entry = LogEntry(level=level, service=service, message=message, user_id=user_id, metadata=metadata)
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def get_logs(self, service: str, level: str = None, limit: int = 100) -> List[LogEntry]:
        query = select(LogEntry).where(LogEntry.service == service)
        if level:
            query = query.where(LogEntry.level == level)
        query = query.order_by(desc(LogEntry.timestamp)).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def aggregate_logs(self, service: str) -> LogAggregation:
        error_count = await self.session.execute(
            select(func.count(LogEntry.id)).where(and_(LogEntry.service == service, LogEntry.level == "error"))
        )
        warning_count = await self.session.execute(
            select(func.count(LogEntry.id)).where(and_(LogEntry.service == service, LogEntry.level == "warning"))
        )

        agg = LogAggregation(service=service, error_count=error_count.scalar() or 0, warning_count=warning_count.scalar() or 0)
        self.session.add(agg)
        await self.session.commit()
        await self.session.refresh(agg)
        return agg


class ErrorTrackingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def report_error(self, error_type: str, message: str, user_id: int = None, stack_trace: str = None, severity: str = "medium") -> ErrorReport:
        error = ErrorReport(error_type=error_type, message=message, user_id=user_id, stack_trace=stack_trace, severity=severity)
        self.session.add(error)
        await self.session.commit()
        await self.session.refresh(error)
        return error

    async def record_error_session(self, error_id: int, session_id: str, device_info: dict = {}) -> ErrorSession:
        session = ErrorSession(error_report_id=error_id, session_id=session_id, device_info=device_info)
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_unresolved_errors(self) -> List[ErrorReport]:
        stmt = select(ErrorReport).where(ErrorReport.resolved == False).order_by(desc(ErrorReport.occurrence_count))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def resolve_error(self, error_id: int) -> None:
        stmt = update(ErrorReport).where(ErrorReport.id == error_id).values(resolved=True)
        await self.session.execute(stmt)
        await self.session.commit()


class FeatureFlagService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_feature_flag(self, name: str, description: str, status: str = "disabled") -> FeatureFlag:
        flag = FeatureFlag(name=name, description=description, status=status)
        self.session.add(flag)
        await self.session.commit()
        await self.session.refresh(flag)
        return flag

    async def get_feature_flag(self, name: str) -> Optional[FeatureFlag]:
        stmt = select(FeatureFlag).where(FeatureFlag.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_rollout(self, flag_id: int, percentage: int) -> None:
        stmt = update(FeatureFlag).where(FeatureFlag.id == flag_id).values(rollout_percentage=percentage)
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_ab_test(self, name: str, flag_id: int, variant_a: str, variant_b: str) -> ABTest:
        test = ABTest(name=name, feature_flag_id=flag_id, variant_a=variant_a, variant_b=variant_b)
        self.session.add(test)
        await self.session.commit()
        await self.session.refresh(test)
        return test


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def track_event(self, user_id: int, event_type: str, event_data: dict = {}, session_id: str = None) -> AnalyticsEvent:
        event = AnalyticsEvent(user_id=user_id, event_type=event_type, event_data=event_data, session_id=session_id)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def create_session(self, user_id: int) -> UserSession:
        session = UserSession(user_id=user_id, session_id=f"session_{user_id}_{int(datetime.now(timezone.utc).timestamp())}")
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def end_session(self, session_id: str, duration_seconds: int) -> None:
        stmt = update(UserSession).where(UserSession.session_id == session_id).values(
            ended_at=datetime.now(timezone.utc), duration_seconds=duration_seconds
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_event_stats(self, event_type: str) -> dict:
        count = await self.session.execute(
            select(func.count(AnalyticsEvent.id)).where(AnalyticsEvent.event_type == event_type)
        )
        return {"event_type": event_type, "total_events": count.scalar() or 0}


class DocumentationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_doc(self, title: str, slug: str, content: str, doc_type: str, author: str = None) -> Documentation:
        doc = Documentation(title=title, slug=slug, content=content, doc_type=doc_type, author=author)
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def get_doc(self, slug: str) -> Optional[Documentation]:
        stmt = select(Documentation).where(Documentation.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def publish_doc(self, doc_id: int) -> None:
        stmt = update(Documentation).where(Documentation.id == doc_id).values(published=True)
        await self.session.execute(stmt)
        await self.session.commit()

    async def document_api(self, endpoint: str, method: str, description: str, request_schema: dict, response_schema: dict) -> APIDocumentation:
        api_doc = APIDocumentation(endpoint=endpoint, method=method, description=description, request_schema=request_schema, response_schema=response_schema)
        self.session.add(api_doc)
        await self.session.commit()
        await self.session.refresh(api_doc)
        return api_doc

    async def get_api_docs(self) -> List[APIDocumentation]:
        stmt = select(APIDocumentation)
        result = await self.session.execute(stmt)
        return result.scalars().all()
