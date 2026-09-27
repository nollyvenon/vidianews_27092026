"""Tests for integration services (Modules 21-25)"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.base import Base
from app.models.integrations import *
from app.services.integrations_service import *


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


# Module 21: Analytics Tests
@pytest.mark.asyncio
async def test_create_report(test_db):
    service = AnalyticsService(test_db)
    report = await service.create_report(1, "performance", "Q3 Report", {"data": "value"})
    assert report.id is not None
    assert report.report_type == "performance"

@pytest.mark.asyncio
async def test_record_metric(test_db):
    service = AnalyticsService(test_db)
    metric = await service.record_metric(1, "views", 1000.0)
    assert metric.value == 1000.0

@pytest.mark.asyncio
async def test_create_dashboard(test_db):
    service = AnalyticsService(test_db)
    dashboard = await service.create_dashboard(1, 1, "Q3 Dashboard")
    assert dashboard.name == "Q3 Dashboard"

# Module 22: Webhooks Tests
@pytest.mark.asyncio
async def test_create_integration(test_db):
    service = WebhookService(test_db)
    integ = await service.create_integration(1, "slack", "Slack Notifications", {"webhook_url": "https://..."})
    assert integ.integration_type == "slack"

@pytest.mark.asyncio
async def test_create_webhook(test_db):
    service = WebhookService(test_db)
    webhook = await service.create_webhook(1, "content.published", "https://example.com/webhook")
    assert webhook.event_type == "content.published"

@pytest.mark.asyncio
async def test_log_webhook_event(test_db):
    service = WebhookService(test_db)
    webhook = await service.create_webhook(1, "test", "https://example.com")
    event = await service.log_webhook_event(webhook.id, "test", {"data": "value"})
    assert event.payload["data"] == "value"

# Module 23: Notification Tests
@pytest.mark.asyncio
async def test_create_notification(test_db):
    service = NotificationService(test_db)
    notif = await service.create_notification(1, "email", "Welcome", "Welcome to VidiNews!")
    assert notif.notification_type == "email"

@pytest.mark.asyncio
async def test_mark_notification_read(test_db):
    service = NotificationService(test_db)
    notif = await service.create_notification(1, "email", "Test", "Test message")
    success = await service.mark_as_read(notif.id)
    assert success

# Module 24: Audit Tests
@pytest.mark.asyncio
async def test_log_action(test_db):
    service = AuditService(test_db)
    log = await service.log_action(1, 1, "create", "content", 100)
    assert log.action == "create"
    assert log.resource_id == 100

@pytest.mark.asyncio
async def test_get_audit_logs(test_db):
    service = AuditService(test_db)
    await service.log_action(1, 1, "create", "content", 1)
    await service.log_action(1, 1, "update", "content", 2)
    logs = await service.get_audit_logs(1)
    assert len(logs) >= 2

@pytest.mark.asyncio
async def test_create_compliance_report(test_db):
    service = AuditService(test_db)
    report = await service.create_compliance_report(1, "gdpr")
    assert report.report_type == "gdpr"

# Module 25: Search Tests
@pytest.mark.asyncio
async def test_index_resource(test_db):
    service = SearchService(test_db)
    index = await service.index_resource(1, "content", 100, "My Video", "This is a great video")
    assert index.resource_type == "content"

@pytest.mark.asyncio
async def test_search(test_db):
    service = SearchService(test_db)
    await service.index_resource(1, "content", 1, "Python Tutorial", "Learn Python basics")
    await service.index_resource(1, "content", 2, "React Guide", "Learn React")
    results = await service.search(1, "Python")
    assert len(results) >= 1

@pytest.mark.asyncio
async def test_create_recommendation(test_db):
    service = SearchService(test_db)
    rec = await service.create_recommendation(1, "similar", "content", 100, 0.95)
    assert rec.score == 0.95

@pytest.mark.asyncio
async def test_accept_recommendation(test_db):
    service = SearchService(test_db)
    rec = await service.create_recommendation(1, "similar", "content", 100)
    success = await service.accept_recommendation(rec.id)
    assert success
