"""Tests for API Monitoring services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.api_monitoring import *
from app.services.api_monitoring_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestAPIVersionService:
    @pytest.mark.asyncio
    async def test_create_endpoint_version(self, db):
        service = APIVersionService(db)
        ep = await service.create_endpoint_version("/api/users", "v1", {"type": "object"})

        assert ep.endpoint == "/api/users"
        assert ep.version == "v1"

    @pytest.mark.asyncio
    async def test_get_endpoint_version(self, db):
        ep = APIEndpointVersion(endpoint="/api/posts", version="v2", schema={})
        db.add(ep)
        await db.commit()

        service = APIVersionService(db)
        result = await service.get_endpoint_version("/api/posts", "v2")

        assert result is not None
        assert result.endpoint == "/api/posts"


class TestGraphQLService:
    @pytest.mark.asyncio
    async def test_register_query(self, db):
        service = GraphQLService(db)
        query = await service.register_query("GetUser", "query { user { id } }", {})

        assert query.name == "GetUser"
        assert query.execution_count == 0

    @pytest.mark.asyncio
    async def test_record_query_execution(self, db):
        query = GraphQLQuery(name="GetPosts", query_string="query { posts }", response_schema={})
        db.add(query)
        await db.commit()

        service = GraphQLService(db)
        await service.record_query_execution(query.id, 50.0)

        updated = await db.get(GraphQLQuery, query.id)
        assert updated.execution_count == 1


class TestWebhookService:
    @pytest.mark.asyncio
    async def test_register_webhook(self, db):
        service = WebhookService(db)
        webhook = await service.register_webhook(1, "https://example.com/hook", "user.created")

        assert webhook.user_id == 1
        assert webhook.url == "https://example.com/hook"
        assert webhook.event_type == "user.created"

    @pytest.mark.asyncio
    async def test_record_event(self, db):
        webhook = Webhook(user_id=1, url="https://example.com", event_type="content.uploaded", secret="secret")
        db.add(webhook)
        await db.commit()

        service = WebhookService(db)
        event = await service.record_event(webhook.id, "content.uploaded", {"id": 123})

        assert event.webhook_id == webhook.id


class TestTestingService:
    @pytest.mark.asyncio
    async def test_create_test_suite(self, db):
        service = TestingService(db)
        suite = await service.create_test_suite("Unit Tests", 50)

        assert suite.name == "Unit Tests"
        assert suite.test_count == 50

    @pytest.mark.asyncio
    async def test_record_test_result(self, db):
        suite = TestSuite(name="Integration Tests", test_count=10)
        db.add(suite)
        await db.commit()

        service = TestingService(db)
        result = await service.record_test_result(suite.id, "test_user_creation", "passed", 250.0)

        assert result.status == "passed"

    @pytest.mark.asyncio
    async def test_update_suite_stats(self, db):
        suite = TestSuite(name="Regression Tests", test_count=20)
        db.add(suite)
        await db.commit()

        service = TestingService(db)
        await service.update_suite_stats(suite.id, 18, 2, 95.5)

        updated = await db.get(TestSuite, suite.id)
        assert updated.passed == 18
        assert updated.coverage_percentage == 95.5


class TestMonitoringService:
    @pytest.mark.asyncio
    async def test_record_metric(self, db):
        service = MonitoringService(db)
        metric = await service.record_metric("response_time", 45.5, "ms")

        assert metric.metric_type == "response_time"
        assert metric.value == 45.5

    @pytest.mark.asyncio
    async def test_create_alert(self, db):
        service = MonitoringService(db)
        alert = await service.create_alert("cpu_usage", "high", 80.0, 85.5, "CPU usage exceeded threshold")

        assert alert.severity == "high"
        assert alert.resolved == False

    @pytest.mark.asyncio
    async def test_resolve_alert(self, db):
        alert = PerformanceAlert(metric_type="memory_usage", severity="critical", threshold=90.0, current_value=92.0, message="Memory alert")
        db.add(alert)
        await db.commit()

        service = MonitoringService(db)
        await service.resolve_alert(alert.id)

        updated = await db.get(PerformanceAlert, alert.id)
        assert updated.resolved == True

    @pytest.mark.asyncio
    async def test_record_health_check(self, db):
        service = MonitoringService(db)
        check = await service.record_health_check("database", "healthy", 120.0)

        assert check.service_name == "database"
        assert check.status == "healthy"
