"""Tests for Logging, Analytics & Documentation services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.logging_analytics import *
from app.services.logging_analytics_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestLoggingService:
    @pytest.mark.asyncio
    async def test_log_message(self, db):
        service = LoggingService(db)
        entry = await service.log_message("info", "api", "Request received", metadata={"endpoint": "/api/users"})

        assert entry.level == "info"
        assert entry.service == "api"

    @pytest.mark.asyncio
    async def test_get_logs(self, db):
        entry = LogEntry(level="error", service="database", message="Connection failed")
        db.add(entry)
        await db.commit()

        service = LoggingService(db)
        logs = await service.get_logs("database")

        assert len(logs) == 1
        assert logs[0].level == "error"


class TestErrorTrackingService:
    @pytest.mark.asyncio
    async def test_report_error(self, db):
        service = ErrorTrackingService(db)
        error = await service.report_error("ValueError", "Invalid input", severity="high")

        assert error.error_type == "ValueError"
        assert error.severity == "high"
        assert error.resolved == False

    @pytest.mark.asyncio
    async def test_record_error_session(self, db):
        error = ErrorReport(error_type="RuntimeError", message="System error", severity="critical")
        db.add(error)
        await db.commit()

        service = ErrorTrackingService(db)
        session = await service.record_error_session(error.id, "session_123")

        assert session.session_id == "session_123"

    @pytest.mark.asyncio
    async def test_resolve_error(self, db):
        error = ErrorReport(error_type="KeyError", message="Key not found", resolved=False)
        db.add(error)
        await db.commit()

        service = ErrorTrackingService(db)
        await service.resolve_error(error.id)

        updated = await db.get(ErrorReport, error.id)
        assert updated.resolved == True


class TestFeatureFlagService:
    @pytest.mark.asyncio
    async def test_create_feature_flag(self, db):
        service = FeatureFlagService(db)
        flag = await service.create_feature_flag("dark_mode", "Dark theme support")

        assert flag.name == "dark_mode"
        assert flag.status == "disabled"

    @pytest.mark.asyncio
    async def test_get_feature_flag(self, db):
        flag = FeatureFlag(name="new_ui", description="New interface", status="rollout")
        db.add(flag)
        await db.commit()

        service = FeatureFlagService(db)
        result = await service.get_feature_flag("new_ui")

        assert result is not None
        assert result.status == "rollout"

    @pytest.mark.asyncio
    async def test_update_rollout(self, db):
        flag = FeatureFlag(name="beta_feature", status="rollout", rollout_percentage=0)
        db.add(flag)
        await db.commit()

        service = FeatureFlagService(db)
        await service.update_rollout(flag.id, 50)

        updated = await db.get(FeatureFlag, flag.id)
        assert updated.rollout_percentage == 50


class TestAnalyticsService:
    @pytest.mark.asyncio
    async def test_track_event(self, db):
        service = AnalyticsService(db)
        event = await service.track_event(1, "page_view", {"page": "/home"})

        assert event.user_id == 1
        assert event.event_type == "page_view"

    @pytest.mark.asyncio
    async def test_create_session(self, db):
        service = AnalyticsService(db)
        session = await service.create_session(1)

        assert session.user_id == 1
        assert session.session_id is not None

    @pytest.mark.asyncio
    async def test_get_event_stats(self, db):
        event = AnalyticsEvent(user_id=1, event_type="video_play", event_data={})
        db.add(event)
        await db.commit()

        service = AnalyticsService(db)
        stats = await service.get_event_stats("video_play")

        assert stats["total_events"] == 1


class TestDocumentationService:
    @pytest.mark.asyncio
    async def test_create_doc(self, db):
        service = DocumentationService(db)
        doc = await service.create_doc("Getting Started", "getting-started", "# Guide", "guide", "admin")

        assert doc.title == "Getting Started"
        assert doc.published == False

    @pytest.mark.asyncio
    async def test_publish_doc(self, db):
        doc = Documentation(title="API Guide", slug="api-guide", content="Content", doc_type="reference", published=False)
        db.add(doc)
        await db.commit()

        service = DocumentationService(db)
        await service.publish_doc(doc.id)

        updated = await db.get(Documentation, doc.id)
        assert updated.published == True

    @pytest.mark.asyncio
    async def test_document_api(self, db):
        service = DocumentationService(db)
        api_doc = await service.document_api("/api/users", "GET", "Get user list", {}, {})

        assert api_doc.endpoint == "/api/users"
        assert api_doc.method == "GET"
