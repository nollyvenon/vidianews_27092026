"""Tests for Community, Gamification & Compliance services"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.community_compliance import *
from app.services.community_compliance_service import *


@pytest.fixture
async def db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestCommunityService:
    @pytest.mark.asyncio
    async def test_create_thread(self, db):
        service = CommunityService(db)
        thread = await service.create_thread(1, "general", "Hello World")
        assert thread.title == "Hello World"

    @pytest.mark.asyncio
    async def test_add_reply(self, db):
        thread = ForumThread(creator_id=1, category="general", title="Test")
        db.add(thread)
        await db.commit()

        service = CommunityService(db)
        reply = await service.add_reply(thread.id, 2, "Great thread!")
        assert reply.content == "Great thread!"


class TestGamificationService:
    @pytest.mark.asyncio
    async def test_create_badge(self, db):
        service = GamificationService(db)
        badge = await service.create_badge("Power User", "100K views", "achievement")
        assert badge.name == "Power User"

    @pytest.mark.asyncio
    async def test_award_badge(self, db):
        badge = Badge(name="Test", badge_type="achievement")
        db.add(badge)
        await db.commit()

        service = GamificationService(db)
        user_badge = await service.award_badge(1, badge.id)
        assert user_badge.user_id == 1


class TestReportingService:
    @pytest.mark.asyncio
    async def test_generate_report(self, db):
        service = ReportingService(db)
        report = await service.generate_report(1, "views", {})
        assert report.creator_id == 1


class TestComplianceService:
    @pytest.mark.asyncio
    async def test_log_audit(self, db):
        service = ComplianceService(db)
        log = await service.log_audit(1, "login", "user")
        assert log.action == "login"


class TestLocalizationService:
    @pytest.mark.asyncio
    async def test_get_or_create_language(self, db):
        service = LocalizationService(db)
        lang = await service.get_or_create_language("en", "English")
        assert lang.code == "en"
