"""Content Quality Services: Modules 61-65"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import httpx
import json
import re
from app.models.content_quality import (
    ContentCalendarEvent, ContentCalendarRecommendation,
    ProofreadingCheck, ProofreadingIssue,
    PlagiarismCheck,
    ReadabilityScore,
    BrandVoiceGuide, BrandVoiceCheck,
    CalendarEventType, ProofreadingIssueType, IssueSeverity,
    PlagiarismCheckStatus, BrandVoiceCheckResult
)
from app.models.content import Content
from app.models.organizations import Organization


class ContentCalendarService:
    """Module 61: Content Calendar Integration with AI-powered scheduling"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_calendar_event(self, organization_id: int, event_type: CalendarEventType,
                                   title: str, scheduled_for: datetime,
                                   content_id: Optional[int] = None,
                                   creator_user_id: Optional[int] = None,
                                   **kwargs) -> ContentCalendarEvent:
        """Create a new calendar event"""
        event = ContentCalendarEvent(
            organization_id=organization_id,
            event_type=event_type,
            title=title,
            scheduled_for=scheduled_for,
            content_id=content_id,
            creator_user_id=creator_user_id,
            **kwargs
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_calendar_events(self, organization_id: int, start_date: datetime,
                                end_date: datetime, limit: int = 100) -> List[ContentCalendarEvent]:
        """Get calendar events for date range"""
        stmt = select(ContentCalendarEvent).where(
            and_(
                ContentCalendarEvent.organization_id == organization_id,
                ContentCalendarEvent.scheduled_for >= start_date,
                ContentCalendarEvent.scheduled_for <= end_date
            )
        ).order_by(ContentCalendarEvent.scheduled_for).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_calendar_recommendation(self, organization_id: int,
                                       content_id: int) -> Optional[ContentCalendarRecommendation]:
        """Get AI recommendation for content scheduling"""
        stmt = select(ContentCalendarRecommendation).where(
            and_(
                ContentCalendarRecommendation.organization_id == organization_id,
                ContentCalendarRecommendation.content_id == content_id
            )
        ).order_by(desc(ContentCalendarRecommendation.created_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_scheduling_recommendation(self, organization_id: int, content_id: int,
                                            optimal_publish_time: datetime,
                                            confidence_score: float,
                                            predicted_reach: int = 0,
                                            predicted_engagement: int = 0,
                                            basis: Dict = None) -> ContentCalendarRecommendation:
        """Create AI-powered scheduling recommendation"""
        if basis is None:
            basis = {}

        rec = ContentCalendarRecommendation(
            organization_id=organization_id,
            content_id=content_id,
            optimal_publish_time=optimal_publish_time,
            confidence_score=confidence_score,
            predicted_reach=predicted_reach,
            predicted_engagement=predicted_engagement,
            basis=basis
        )
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def accept_recommendation(self, recommendation_id: int) -> Optional[ContentCalendarRecommendation]:
        """Mark recommendation as accepted"""
        stmt = update(ContentCalendarRecommendation).where(
            ContentCalendarRecommendation.id == recommendation_id
        ).values(accepted=True, accepted_at=datetime.now(timezone.utc))
        await self.session.execute(stmt)
        await self.session.commit()

        stmt = select(ContentCalendarRecommendation).where(
            ContentCalendarRecommendation.id == recommendation_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class ProofreadingService:
    """Module 62: AI Proofreading with grammar, spelling, and style checking"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_proofreading_check(self, content_id: int, organization_id: int,
                                       original_text: str, **kwargs) -> ProofreadingCheck:
        """Create proofreading check"""
        word_count = len(original_text.split())

        check = ProofreadingCheck(
            content_id=content_id,
            organization_id=organization_id,
            original_text=original_text,
            total_word_count=word_count,
            **kwargs
        )
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_proofreading_check(self, check_id: int) -> Optional[ProofreadingCheck]:
        """Get proofreading check with issues"""
        stmt = select(ProofreadingCheck).where(
            ProofreadingCheck.id == check_id
        ).options(selectinload(ProofreadingCheck.issues))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_proofreading_issue(self, check_id: int, issue_type: ProofreadingIssueType,
                                    severity: IssueSeverity, position: int, length: int,
                                    text: str, suggestion: str = "", explanation: str = "") -> ProofreadingIssue:
        """Add individual proofreading issue"""
        issue = ProofreadingIssue(
            check_id=check_id,
            issue_type=issue_type,
            severity=severity,
            position=position,
            length=length,
            text=text,
            suggestion=suggestion,
            explanation=explanation
        )
        self.session.add(issue)
        await self.session.commit()
        await self.session.refresh(issue)
        return issue

    async def update_proofreading_results(self, check_id: int,
                                        grammar_issues: int = 0,
                                        spelling_issues: int = 0,
                                        punctuation_issues: int = 0,
                                        style_issues: int = 0,
                                        tone_issues: int = 0,
                                        clarity_issues: int = 0,
                                        consistency_issues: int = 0) -> Optional[ProofreadingCheck]:
        """Update proofreading check with issue counts and scores"""
        total_issues = (grammar_issues + spelling_issues + punctuation_issues +
                       style_issues + tone_issues + clarity_issues + consistency_issues)

        # Calculate quality score based on issues
        # Assume no issues = 100, scale down based on issue count
        quality_score = max(0, 100 - (total_issues * 2))

        # Determine overall rating
        if quality_score >= 90:
            overall_rating = "Excellent"
        elif quality_score >= 75:
            overall_rating = "Good"
        elif quality_score >= 60:
            overall_rating = "Fair"
        else:
            overall_rating = "Poor"

        stmt = update(ProofreadingCheck).where(
            ProofreadingCheck.id == check_id
        ).values(
            grammar_issues=grammar_issues,
            spelling_issues=spelling_issues,
            punctuation_issues=punctuation_issues,
            style_issues=style_issues,
            tone_issues=tone_issues,
            clarity_issues=clarity_issues,
            consistency_issues=consistency_issues,
            total_issues=total_issues,
            quality_score=quality_score,
            overall_rating=overall_rating
        )
        await self.session.execute(stmt)
        await self.session.commit()

        stmt = select(ProofreadingCheck).where(ProofreadingCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_proofreading_check(self, content_id: int) -> Optional[ProofreadingCheck]:
        """Get most recent proofreading check for content"""
        stmt = select(ProofreadingCheck).where(
            ProofreadingCheck.content_id == content_id
        ).order_by(desc(ProofreadingCheck.created_at)).limit(1).options(
            selectinload(ProofreadingCheck.issues)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class PlagiarismDetectionService:
    """Module 63: Plagiarism detection with originality scoring"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_plagiarism_check(self, content_id: int, organization_id: int,
                                     text_analyzed: str) -> PlagiarismCheck:
        """Create plagiarism check"""
        word_count = len(text_analyzed.split())

        check = PlagiarismCheck(
            content_id=content_id,
            organization_id=organization_id,
            text_analyzed=text_analyzed,
            word_count=word_count,
            status=PlagiarismCheckStatus.PENDING
        )
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_plagiarism_check(self, check_id: int) -> Optional[PlagiarismCheck]:
        """Get plagiarism check result"""
        stmt = select(PlagiarismCheck).where(PlagiarismCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_plagiarism_results(self, check_id: int,
                                       similarity_percentage: float,
                                       originality_percentage: float,
                                       total_sources_found: int = 0,
                                       ai_content_percentage: float = 0.0,
                                       human_content_percentage: float = 0.0,
                                       detected_sources: List[Dict] = None,
                                       confidence_score: float = 0.0) -> Optional[PlagiarismCheck]:
        """Update plagiarism check with results"""
        if detected_sources is None:
            detected_sources = []

        # Determine plagiarism risk
        if similarity_percentage > 80:
            plagiarism_risk = "Critical"
        elif similarity_percentage > 60:
            plagiarism_risk = "High"
        elif similarity_percentage > 30:
            plagiarism_risk = "Medium"
        else:
            plagiarism_risk = "Low"

        stmt = update(PlagiarismCheck).where(
            PlagiarismCheck.id == check_id
        ).values(
            similarity_percentage=similarity_percentage,
            originality_percentage=originality_percentage,
            total_sources_found=total_sources_found,
            ai_content_percentage=ai_content_percentage,
            human_content_percentage=human_content_percentage,
            detected_sources=detected_sources,
            confidence_score=confidence_score,
            plagiarism_risk=plagiarism_risk,
            status=PlagiarismCheckStatus.COMPLETED,
            check_completed_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

        stmt = select(PlagiarismCheck).where(PlagiarismCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_plagiarism_check(self, content_id: int) -> Optional[PlagiarismCheck]:
        """Get most recent plagiarism check for content"""
        stmt = select(PlagiarismCheck).where(
            PlagiarismCheck.content_id == content_id
        ).order_by(desc(PlagiarismCheck.created_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class ReadabilityService:
    """Module 64: Content readability analysis with multiple metrics"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_readability_score(self, content_id: int, organization_id: int,
                                      text_analyzed: str) -> ReadabilityScore:
        """Create readability analysis"""
        word_count = len(text_analyzed.split())
        sentences = re.split(r'[.!?]+', text_analyzed)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraphs = text_analyzed.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])

        score = ReadabilityScore(
            content_id=content_id,
            organization_id=organization_id,
            text_analyzed=text_analyzed,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count
        )
        self.session.add(score)
        await self.session.commit()
        await self.session.refresh(score)
        return score

    async def get_readability_score(self, score_id: int) -> Optional[ReadabilityScore]:
        """Get readability score"""
        stmt = select(ReadabilityScore).where(ReadabilityScore.id == score_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_readability_metrics(self, score_id: int,
                                        flesch_kincaid_grade: float = 0.0,
                                        flesch_reading_ease: float = 0.0,
                                        gunning_fog_index: float = 0.0,
                                        smog_index: float = 0.0,
                                        dale_chall_score: float = 0.0,
                                        automated_readability_index: float = 0.0,
                                        avg_word_length: float = 0.0,
                                        avg_sentence_length: float = 0.0) -> Optional[ReadabilityScore]:
        """Update readability metrics"""

        # Determine target grade level
        avg_grade = (flesch_kincaid_grade + gunning_fog_index + smog_index) / 3
        if avg_grade < 6:
            target_grade = "5-6 (Elementary)"
        elif avg_grade < 9:
            target_grade = "7-8 (Middle School)"
        elif avg_grade < 13:
            target_grade = "9-12 (High School)"
        else:
            target_grade = "12+ (College)"

        # Determine readability level based on Flesch Reading Ease
        if flesch_reading_ease >= 90:
            readability_level = "Easy"
            complexity_score = 10
        elif flesch_reading_ease >= 80:
            readability_level = "Moderate"
            complexity_score = 30
        elif flesch_reading_ease >= 70:
            readability_level = "Moderate"
            complexity_score = 50
        elif flesch_reading_ease >= 60:
            readability_level = "Moderate"
            complexity_score = 60
        elif flesch_reading_ease >= 50:
            readability_level = "Difficult"
            complexity_score = 70
        else:
            readability_level = "Very Difficult"
            complexity_score = 90

        stmt = update(ReadabilityScore).where(
            ReadabilityScore.id == score_id
        ).values(
            flesch_kincaid_grade=flesch_kincaid_grade,
            flesch_reading_ease=flesch_reading_ease,
            gunning_fog_index=gunning_fog_index,
            smog_index=smog_index,
            dale_chall_score=dale_chall_score,
            automated_readability_index=automated_readability_index,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            target_audience_grade_level=target_grade,
            readability_level=readability_level,
            complexity_score=complexity_score
        )
        await self.session.execute(stmt)
        await self.session.commit()

        stmt = select(ReadabilityScore).where(ReadabilityScore.id == score_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_readability_score(self, content_id: int) -> Optional[ReadabilityScore]:
        """Get most recent readability score for content"""
        stmt = select(ReadabilityScore).where(
            ReadabilityScore.content_id == content_id
        ).order_by(desc(ReadabilityScore.created_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class BrandVoiceService:
    """Module 65: Brand voice consistency checking and enforcement"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_brand_voice_guide(self, organization_id: int,
                                      name: str,
                                      created_by_user_id: Optional[int] = None,
                                      **kwargs) -> BrandVoiceGuide:
        """Create brand voice guide"""
        guide = BrandVoiceGuide(
            organization_id=organization_id,
            name=name,
            created_by_user_id=created_by_user_id,
            **kwargs
        )
        self.session.add(guide)
        await self.session.commit()
        await self.session.refresh(guide)
        return guide

    async def get_brand_voice_guide(self, guide_id: int) -> Optional[BrandVoiceGuide]:
        """Get brand voice guide"""
        stmt = select(BrandVoiceGuide).where(BrandVoiceGuide.id == guide_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_guide_for_org(self, organization_id: int) -> Optional[BrandVoiceGuide]:
        """Get active brand voice guide for organization"""
        stmt = select(BrandVoiceGuide).where(
            and_(
                BrandVoiceGuide.organization_id == organization_id,
                BrandVoiceGuide.is_active == True
            )
        ).order_by(desc(BrandVoiceGuide.updated_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_brand_voice_guide(self, guide_id: int, **kwargs) -> Optional[BrandVoiceGuide]:
        """Update brand voice guide"""
        stmt = update(BrandVoiceGuide).where(
            BrandVoiceGuide.id == guide_id
        ).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_brand_voice_guide(guide_id)

    async def create_brand_voice_check(self, content_id: int, guide_id: int,
                                      organization_id: int,
                                      text_analyzed: str) -> BrandVoiceCheck:
        """Create brand voice check"""
        check = BrandVoiceCheck(
            content_id=content_id,
            guide_id=guide_id,
            organization_id=organization_id,
            text_analyzed=text_analyzed,
            check_result=BrandVoiceCheckResult.NEEDS_REVIEW
        )
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_brand_voice_check(self, check_id: int) -> Optional[BrandVoiceCheck]:
        """Get brand voice check"""
        stmt = select(BrandVoiceCheck).where(BrandVoiceCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_brand_voice_check_results(self, check_id: int,
                                              check_result: BrandVoiceCheckResult,
                                              compliance_score: float,
                                              tone_match_score: float,
                                              consistency_score: float,
                                              tone_analysis: Dict = None,
                                              terminology_issues: List[Dict] = None,
                                              style_compliance_issues: List[Dict] = None,
                                              active_voice_percentage: float = 0.0,
                                              recommendations: List[str] = None) -> Optional[BrandVoiceCheck]:
        """Update brand voice check with analysis results"""
        if tone_analysis is None:
            tone_analysis = {}
        if terminology_issues is None:
            terminology_issues = []
        if style_compliance_issues is None:
            style_compliance_issues = []
        if recommendations is None:
            recommendations = []

        # Calculate overall score
        overall_score = (compliance_score + tone_match_score + consistency_score) / 3

        stmt = update(BrandVoiceCheck).where(
            BrandVoiceCheck.id == check_id
        ).values(
            check_result=check_result,
            compliance_score=compliance_score,
            tone_match_score=tone_match_score,
            consistency_score=consistency_score,
            overall_score=overall_score,
            tone_analysis=tone_analysis,
            terminology_issues=terminology_issues,
            style_compliance_issues=style_compliance_issues,
            active_voice_percentage=active_voice_percentage,
            recommendations=recommendations
        )
        await self.session.execute(stmt)
        await self.session.commit()

        stmt = select(BrandVoiceCheck).where(BrandVoiceCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_brand_voice_check(self, content_id: int) -> Optional[BrandVoiceCheck]:
        """Get most recent brand voice check for content"""
        stmt = select(BrandVoiceCheck).where(
            BrandVoiceCheck.content_id == content_id
        ).order_by(desc(BrandVoiceCheck.created_at)).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
