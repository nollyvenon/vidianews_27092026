"""Tests for Content Quality Modules 61-65"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.content_quality import *
from app.services.content_quality_service import (
    ContentCalendarService,
    ProofreadingService,
    PlagiarismDetectionService,
    ReadabilityService,
    BrandVoiceService
)


class TestContentCalendarService:
    """Module 61: Content Calendar Integration Tests"""

    @pytest.mark.asyncio
    async def test_create_calendar_event(self, db: AsyncSession):
        """Test creating calendar event"""
        service = ContentCalendarService(db)

        event = await service.create_calendar_event(
            organization_id=1,
            event_type=CalendarEventType.SCHEDULED_POST,
            title="Test Post",
            scheduled_for=datetime.now(timezone.utc) + timedelta(days=1),
            creator_user_id=1
        )

        assert event.id is not None
        assert event.title == "Test Post"
        assert event.event_type == CalendarEventType.SCHEDULED_POST

    @pytest.mark.asyncio
    async def test_get_calendar_events(self, db: AsyncSession):
        """Test retrieving calendar events"""
        service = ContentCalendarService(db)

        # Create test events
        now = datetime.now(timezone.utc)
        await service.create_calendar_event(
            organization_id=1,
            event_type=CalendarEventType.SCHEDULED_POST,
            title="Event 1",
            scheduled_for=now + timedelta(days=1)
        )

        await service.create_calendar_event(
            organization_id=1,
            event_type=CalendarEventType.SCHEDULED_POST,
            title="Event 2",
            scheduled_for=now + timedelta(days=2)
        )

        events = await service.get_calendar_events(
            organization_id=1,
            start_date=now,
            end_date=now + timedelta(days=3)
        )

        assert len(events) >= 2

    @pytest.mark.asyncio
    async def test_create_scheduling_recommendation(self, db: AsyncSession):
        """Test creating scheduling recommendation"""
        service = ContentCalendarService(db)

        optimal_time = datetime.now(timezone.utc) + timedelta(hours=12)
        rec = await service.create_scheduling_recommendation(
            organization_id=1,
            content_id=1,
            optimal_publish_time=optimal_time,
            confidence_score=0.85,
            predicted_reach=5000,
            predicted_engagement=500,
            basis={"historical_data": "high", "audience_timezone": "EST"}
        )

        assert rec.id is not None
        assert rec.confidence_score == 0.85
        assert rec.predicted_reach == 5000

    @pytest.mark.asyncio
    async def test_accept_recommendation(self, db: AsyncSession):
        """Test accepting recommendation"""
        service = ContentCalendarService(db)

        rec = await service.create_scheduling_recommendation(
            organization_id=1,
            content_id=1,
            optimal_publish_time=datetime.now(timezone.utc),
            confidence_score=0.75
        )

        accepted = await service.accept_recommendation(rec.id)

        assert accepted.accepted is True
        assert accepted.accepted_at is not None


class TestProofreadingService:
    """Module 62: AI Proofreading Tests"""

    @pytest.mark.asyncio
    async def test_create_proofreading_check(self, db: AsyncSession):
        """Test creating proofreading check"""
        service = ProofreadingService(db)

        text = "This is a test content with some spelling mistaks."
        check = await service.create_proofreading_check(
            content_id=1,
            organization_id=1,
            original_text=text
        )

        assert check.id is not None
        assert check.total_word_count > 0
        assert check.original_text == text

    @pytest.mark.asyncio
    async def test_add_proofreading_issue(self, db: AsyncSession):
        """Test adding proofreading issue"""
        service = ProofreadingService(db)

        check = await service.create_proofreading_check(
            content_id=1,
            organization_id=1,
            original_text="Test content"
        )

        issue = await service.add_proofreading_issue(
            check_id=check.id,
            issue_type=ProofreadingIssueType.SPELLING,
            severity=IssueSeverity.ERROR,
            position=10,
            length=5,
            text="test",
            suggestion="Test",
            explanation="Capitalization error"
        )

        assert issue.id is not None
        assert issue.issue_type == ProofreadingIssueType.SPELLING

    @pytest.mark.asyncio
    async def test_update_proofreading_results(self, db: AsyncSession):
        """Test updating proofreading results"""
        service = ProofreadingService(db)

        check = await service.create_proofreading_check(
            content_id=1,
            organization_id=1,
            original_text="Test content"
        )

        updated = await service.update_proofreading_results(
            check_id=check.id,
            grammar_issues=2,
            spelling_issues=1,
            punctuation_issues=0,
            style_issues=1
        )

        assert updated.total_issues == 4
        assert updated.quality_score < 100
        assert updated.overall_rating in ["Excellent", "Good", "Fair", "Poor"]

    @pytest.mark.asyncio
    async def test_get_latest_proofreading_check(self, db: AsyncSession):
        """Test getting latest proofreading check"""
        service = ProofreadingService(db)

        await service.create_proofreading_check(
            content_id=1,
            organization_id=1,
            original_text="Content 1"
        )

        latest = await service.get_latest_proofreading_check(content_id=1)

        assert latest is not None


class TestPlagiarismDetectionService:
    """Module 63: Plagiarism Detection Tests"""

    @pytest.mark.asyncio
    async def test_create_plagiarism_check(self, db: AsyncSession):
        """Test creating plagiarism check"""
        service = PlagiarismDetectionService(db)

        text = "This is original content that will be checked for plagiarism."
        check = await service.create_plagiarism_check(
            content_id=1,
            organization_id=1,
            text_analyzed=text
        )

        assert check.id is not None
        assert check.status == PlagiarismCheckStatus.PENDING
        assert check.word_count > 0

    @pytest.mark.asyncio
    async def test_update_plagiarism_results(self, db: AsyncSession):
        """Test updating plagiarism results"""
        service = PlagiarismDetectionService(db)

        check = await service.create_plagiarism_check(
            content_id=1,
            organization_id=1,
            text_analyzed="Test content"
        )

        updated = await service.update_plagiarism_results(
            check_id=check.id,
            similarity_percentage=15.5,
            originality_percentage=84.5,
            total_sources_found=2,
            ai_content_percentage=5.0,
            human_content_percentage=95.0,
            detected_sources=[
                {"url": "https://example.com", "similarity_percent": 10},
                {"url": "https://test.com", "similarity_percent": 5.5}
            ],
            confidence_score=0.92
        )

        assert updated.similarity_percentage == 15.5
        assert updated.originality_percentage == 84.5
        assert updated.plagiarism_risk == "Low"
        assert updated.status == PlagiarismCheckStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_plagiarism_risk_levels(self, db: AsyncSession):
        """Test plagiarism risk level classification"""
        service = PlagiarismDetectionService(db)

        # Test critical risk
        check_critical = await service.create_plagiarism_check(
            content_id=1,
            organization_id=1,
            text_analyzed="Content"
        )
        updated_critical = await service.update_plagiarism_results(
            check_id=check_critical.id,
            similarity_percentage=85.0,
            originality_percentage=15.0
        )
        assert updated_critical.plagiarism_risk == "Critical"

        # Test high risk
        check_high = await service.create_plagiarism_check(
            content_id=2,
            organization_id=1,
            text_analyzed="Content"
        )
        updated_high = await service.update_plagiarism_results(
            check_id=check_high.id,
            similarity_percentage=65.0,
            originality_percentage=35.0
        )
        assert updated_high.plagiarism_risk == "High"


class TestReadabilityService:
    """Module 64: Content Readability Tests"""

    @pytest.mark.asyncio
    async def test_create_readability_score(self, db: AsyncSession):
        """Test creating readability score"""
        service = ReadabilityService(db)

        text = "This is a test. It has multiple sentences. The readability will be analyzed."
        score = await service.create_readability_score(
            content_id=1,
            organization_id=1,
            text_analyzed=text
        )

        assert score.id is not None
        assert score.word_count > 0
        assert score.sentence_count > 0

    @pytest.mark.asyncio
    async def test_update_readability_metrics(self, db: AsyncSession):
        """Test updating readability metrics"""
        service = ReadabilityService(db)

        score = await service.create_readability_score(
            content_id=1,
            organization_id=1,
            text_analyzed="Test content"
        )

        updated = await service.update_readability_metrics(
            score_id=score.id,
            flesch_kincaid_grade=8.5,
            flesch_reading_ease=60.0,
            gunning_fog_index=9.2,
            smog_index=9.0,
            dale_chall_score=8.5,
            automated_readability_index=8.9,
            avg_word_length=4.5,
            avg_sentence_length=15.0
        )

        assert updated.flesch_reading_ease == 60.0
        assert updated.readability_level == "Moderate"
        assert "grade" in updated.target_audience_grade_level.lower()

    @pytest.mark.asyncio
    async def test_readability_levels(self, db: AsyncSession):
        """Test readability level classification"""
        service = ReadabilityService(db)

        # Test easy readability
        score_easy = await service.create_readability_score(
            content_id=1,
            organization_id=1,
            text_analyzed="Simple text"
        )
        updated_easy = await service.update_readability_metrics(
            score_id=score_easy.id,
            flesch_reading_ease=95.0
        )
        assert updated_easy.readability_level == "Easy"
        assert updated_easy.complexity_score == 10

        # Test very difficult readability
        score_difficult = await service.create_readability_score(
            content_id=2,
            organization_id=1,
            text_analyzed="Complex text"
        )
        updated_difficult = await service.update_readability_metrics(
            score_id=score_difficult.id,
            flesch_reading_ease=20.0
        )
        assert updated_difficult.readability_level == "Very Difficult"
        assert updated_difficult.complexity_score == 90


class TestBrandVoiceService:
    """Module 65: Brand Voice Consistency Tests"""

    @pytest.mark.asyncio
    async def test_create_brand_voice_guide(self, db: AsyncSession):
        """Test creating brand voice guide"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Main Brand Voice",
            created_by_user_id=1,
            tone={"primary": "professional", "secondary": "friendly"},
            personality_traits=["confident", "helpful", "innovative"],
            vocabulary_level="Advanced"
        )

        assert guide.id is not None
        assert guide.name == "Main Brand Voice"
        assert guide.is_active is True

    @pytest.mark.asyncio
    async def test_get_active_guide_for_org(self, db: AsyncSession):
        """Test getting active brand voice guide"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Test Guide",
            tone={"primary": "casual"}
        )

        active = await service.get_active_guide_for_org(1)

        assert active is not None
        assert active.is_active is True

    @pytest.mark.asyncio
    async def test_update_brand_voice_guide(self, db: AsyncSession):
        """Test updating brand voice guide"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Original Name",
            tone={"primary": "formal"}
        )

        updated = await service.update_brand_voice_guide(
            guide_id=guide.id,
            name="Updated Name",
            tone={"primary": "casual", "secondary": "helpful"}
        )

        assert updated.name == "Updated Name"
        assert updated.tone["primary"] == "casual"

    @pytest.mark.asyncio
    async def test_create_brand_voice_check(self, db: AsyncSession):
        """Test creating brand voice check"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Test Guide"
        )

        check = await service.create_brand_voice_check(
            content_id=1,
            guide_id=guide.id,
            organization_id=1,
            text_analyzed="Test content that needs brand voice check"
        )

        assert check.id is not None
        assert check.check_result == BrandVoiceCheckResult.NEEDS_REVIEW

    @pytest.mark.asyncio
    async def test_update_brand_voice_check_results(self, db: AsyncSession):
        """Test updating brand voice check results"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Test Guide"
        )

        check = await service.create_brand_voice_check(
            content_id=1,
            guide_id=guide.id,
            organization_id=1,
            text_analyzed="Test content"
        )

        updated = await service.update_brand_voice_check_results(
            check_id=check.id,
            check_result=BrandVoiceCheckResult.COMPLIANT,
            compliance_score=95.0,
            tone_match_score=90.0,
            consistency_score=92.0,
            tone_analysis={"detected": ["professional"], "expected": ["professional"]},
            active_voice_percentage=85.0,
            recommendations=["Excellent brand voice match"]
        )

        assert updated.check_result == BrandVoiceCheckResult.COMPLIANT
        assert updated.overall_score > 80
        assert updated.active_voice_percentage == 85.0

    @pytest.mark.asyncio
    async def test_get_latest_brand_voice_check(self, db: AsyncSession):
        """Test getting latest brand voice check"""
        service = BrandVoiceService(db)

        guide = await service.create_brand_voice_guide(
            organization_id=1,
            name="Test Guide"
        )

        check = await service.create_brand_voice_check(
            content_id=1,
            guide_id=guide.id,
            organization_id=1,
            text_analyzed="Content"
        )

        latest = await service.get_latest_brand_voice_check(content_id=1)

        assert latest is not None
        assert latest.id == check.id


# Integration tests

class TestContentQualityIntegration:
    """Integration tests for all content quality modules"""

    @pytest.mark.asyncio
    async def test_complete_content_workflow(self, db: AsyncSession):
        """Test complete content quality workflow"""
        # Calendar service
        calendar_service = ContentCalendarService(db)
        now = datetime.now(timezone.utc)

        event = await calendar_service.create_calendar_event(
            organization_id=1,
            event_type=CalendarEventType.SCHEDULED_POST,
            title="Blog Post",
            scheduled_for=now + timedelta(days=7),
            creator_user_id=1
        )

        # Proofreading service
        proofread_service = ProofreadingService(db)
        text = "This is content for proofreading."

        check = await proofread_service.create_proofreading_check(
            content_id=1,
            organization_id=1,
            original_text=text
        )

        await proofread_service.update_proofreading_results(
            check_id=check.id,
            grammar_issues=0,
            spelling_issues=1
        )

        # Plagiarism service
        plagiarism_service = PlagiarismDetectionService(db)
        plagiarism_check = await plagiarism_service.create_plagiarism_check(
            content_id=1,
            organization_id=1,
            text_analyzed=text
        )

        await plagiarism_service.update_plagiarism_results(
            check_id=plagiarism_check.id,
            similarity_percentage=5.0,
            originality_percentage=95.0
        )

        # Readability service
        readability_service = ReadabilityService(db)
        readability = await readability_service.create_readability_score(
            content_id=1,
            organization_id=1,
            text_analyzed=text
        )

        await readability_service.update_readability_metrics(
            score_id=readability.id,
            flesch_reading_ease=75.0,
            flesch_kincaid_grade=6.5
        )

        # Brand voice service
        brand_service = BrandVoiceService(db)
        guide = await brand_service.create_brand_voice_guide(
            organization_id=1,
            name="Brand Guide"
        )

        brand_check = await brand_service.create_brand_voice_check(
            content_id=1,
            guide_id=guide.id,
            organization_id=1,
            text_analyzed=text
        )

        await brand_service.update_brand_voice_check_results(
            check_id=brand_check.id,
            check_result=BrandVoiceCheckResult.COMPLIANT,
            compliance_score=90.0,
            tone_match_score=88.0,
            consistency_score=92.0
        )

        # Verify all checks completed
        assert event.id is not None
        assert check.total_issues == 1
        assert plagiarism_check.similarity_percentage == 5.0
        assert readability.readability_level == "Moderate"
        assert brand_check.check_result == BrandVoiceCheckResult.COMPLIANT
