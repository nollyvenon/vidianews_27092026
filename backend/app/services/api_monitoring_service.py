"""Services for API, Monitoring & Testing: Modules 41-45"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc
from typing import Optional, List
from datetime import datetime, timezone
from app.models.api_monitoring import *
import hashlib
import hmac


class APIVersionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_endpoint_version(self, endpoint: str, version: str, schema: dict) -> APIEndpointVersion:
        ep = APIEndpointVersion(endpoint=endpoint, version=version, schema=schema)
        self.session.add(ep)
        await self.session.commit()
        await self.session.refresh(ep)
        return ep

    async def deprecate_version(self, endpoint: str, version: str, sunset_date: datetime) -> APIEndpointVersion:
        stmt = update(APIEndpointVersion).where(
            and_(APIEndpointVersion.endpoint == endpoint, APIEndpointVersion.version == version)
        ).values(deprecated=True, sunset_date=sunset_date)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_endpoint_version(endpoint, version)

    async def get_endpoint_version(self, endpoint: str, version: str) -> Optional[APIEndpointVersion]:
        stmt = select(APIEndpointVersion).where(
            and_(APIEndpointVersion.endpoint == endpoint, APIEndpointVersion.version == version)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class GraphQLService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_query(self, name: str, query_string: str, schema: dict) -> GraphQLQuery:
        query = GraphQLQuery(name=name, query_string=query_string, response_schema=schema)
        self.session.add(query)
        await self.session.commit()
        await self.session.refresh(query)
        return query

    async def record_query_execution(self, query_id: int, execution_time_ms: float) -> None:
        query = await self.session.get(GraphQLQuery, query_id)
        if query:
            query.execution_count += 1
            query.avg_execution_time_ms = (query.avg_execution_time_ms + execution_time_ms) / 2
            await self.session.commit()

    async def get_all_queries(self) -> List[GraphQLQuery]:
        stmt = select(GraphQLQuery)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class WebhookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_webhook(self, user_id: int, url: str, event_type: str) -> Webhook:
        secret = hashlib.sha256(f"{user_id}{url}{event_type}".encode()).hexdigest()
        webhook = Webhook(user_id=user_id, url=url, event_type=event_type, secret=secret)
        self.session.add(webhook)
        await self.session.commit()
        await self.session.refresh(webhook)
        return webhook

    async def get_user_webhooks(self, user_id: int) -> List[Webhook]:
        stmt = select(Webhook).where(Webhook.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_event(self, webhook_id: int, event_type: str, payload: dict) -> WebhookEvent:
        event = WebhookEvent(webhook_id=webhook_id, event_type=event_type, payload=payload)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def update_event_status(self, event_id: int, status: int, response: str) -> None:
        stmt = update(WebhookEvent).where(WebhookEvent.id == event_id).values(
            response_status=status, response_body=response
        )
        await self.session.execute(stmt)
        await self.session.commit()


class TestingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_test_suite(self, name: str, test_count: int) -> TestSuite:
        suite = TestSuite(name=name, test_count=test_count)
        self.session.add(suite)
        await self.session.commit()
        await self.session.refresh(suite)
        return suite

    async def record_test_result(self, suite_id: int, test_name: str, status: str, duration_ms: float) -> TestResult:
        result = TestResult(test_suite_id=suite_id, test_name=test_name, status=status, duration_ms=duration_ms)
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def update_suite_stats(self, suite_id: int, passed: int, failed: int, coverage: float) -> None:
        stmt = update(TestSuite).where(TestSuite.id == suite_id).values(
            passed=passed, failed=failed, coverage_percentage=coverage, last_run_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_test_suite(self, suite_id: int) -> Optional[TestSuite]:
        return await self.session.get(TestSuite, suite_id)


class MonitoringService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_metric(self, metric_type: str, value: float, unit: str = None) -> SystemMetric:
        metric = SystemMetric(metric_type=metric_type, value=value, unit=unit)
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def create_alert(self, metric_type: str, severity: str, threshold: float, current_value: float, message: str) -> PerformanceAlert:
        alert = PerformanceAlert(metric_type=metric_type, severity=severity, threshold=threshold, current_value=current_value, message=message)
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def resolve_alert(self, alert_id: int) -> None:
        stmt = update(PerformanceAlert).where(PerformanceAlert.id == alert_id).values(
            resolved=True, resolved_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def record_health_check(self, service_name: str, status: str, response_time_ms: float) -> HealthCheck:
        check = HealthCheck(service_name=service_name, status=status, response_time_ms=response_time_ms)
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_alerts(self, unresolved_only: bool = True) -> List[PerformanceAlert]:
        if unresolved_only:
            stmt = select(PerformanceAlert).where(PerformanceAlert.resolved == False).order_by(desc(PerformanceAlert.created_at))
        else:
            stmt = select(PerformanceAlert).order_by(desc(PerformanceAlert.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()
