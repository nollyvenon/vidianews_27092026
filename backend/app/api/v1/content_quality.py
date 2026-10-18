"""Content Quality API Endpoints: Modules 61-65"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime, timedelta
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.readability_analyzer import analyze
from app.services.content_analysis import (
    analyze_brand_voice, brand_voice_result, describe_guide, find_proofreading_issues,
)
from app.models.content_quality import *
from app.services.content_quality_service import (
    ContentCalendarService,
    ProofreadingService,
    PlagiarismDetectionService,
    ReadabilityService,
    BrandVoiceService
)
from pydantic import BaseModel

router = APIRouter()


def _org_id(current_user: User) -> int:
    """The caller's organization id, or 422 when the account has no organization."""
    if current_user.organization_id is None:
        raise HTTPException(
            status_code=422,
            detail="Your account has no organization yet. Create one under Organizations first.",
        )
    return current_user.organization_id

# ==================== REQUEST/RESPONSE SCHEMAS ====================

class CalendarEventCreate(BaseModel):
    event_type: str
    title: str
    description: Optional[str] = None
    scheduled_for: datetime
    duration_minutes: Optional[int] = 60
    content_id: Optional[int] = None

class CalendarEventResponse(BaseModel):
    id: int
    event_type: str
    title: str
    scheduled_for: datetime
    ai_recommended_time: Optional[datetime] = None
    ai_confidence_score: float = 0.0
    predicted_reach: Optional[int] = None
    predicted_engagement: Optional[int] = None

    class Config:
        from_attributes = True

class SchedulingRecommendationResponse(BaseModel):
    id: int
    optimal_publish_time: datetime
    confidence_score: float
    predicted_reach: int
    predicted_engagement: int

class ProofreadingCheckCreate(BaseModel):
    content_id: int
    text: str
    check_grammar: bool = True
    check_spelling: bool = True
    check_style: bool = True

class ProofreadingIssueResponse(BaseModel):
    id: int
    issue_type: str
    severity: str
    text: str
    suggestion: str
    position: int
    length: int

class ProofreadingCheckResponse(BaseModel):
    id: int
    content_id: int
    quality_score: float
    overall_rating: str
    total_issues: int
    grammar_issues: int
    spelling_issues: int
    punctuation_issues: int
    style_issues: int

class PlagiarismCheckCreate(BaseModel):
    content_id: int
    text: str

class PlagiarismCheckResponse(BaseModel):
    id: int
    content_id: int
    similarity_percentage: float
    originality_percentage: float
    plagiarism_risk: str
    status: str
    total_sources_found: int

class ReadabilityCheckCreate(BaseModel):
    content_id: int
    text: str

class ReadabilityScoreResponse(BaseModel):
    id: int
    content_id: int
    word_count: int
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    readability_level: str
    target_audience_grade_level: str
    complexity_score: float

class BrandVoiceGuideCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tone: Optional[dict] = {}
    personality_traits: Optional[list] = []
    vocabulary_level: Optional[str] = "Moderate"
    sentence_structure: Optional[str] = None
    paragraph_length: Optional[str] = None

class BrandVoiceGuideResponse(BaseModel):
    id: int
    name: str
    organization_id: int
    tone: dict
    personality_traits: list
    is_active: bool

class BrandVoiceCheckCreate(BaseModel):
    content_id: int
    text: str
    guide_id: Optional[int] = None

class BrandVoiceCheckResponse(BaseModel):
    id: int
    content_id: int
    check_result: str
    overall_score: float
    compliance_score: float
    tone_match_score: float
    consistency_score: float
    recommendations: List[str] = []


# ==================== MODULE 61: CONTENT CALENDAR ====================

@router.post("/calendar/events", response_model=CalendarEventResponse, tags=["content-calendar"])
async def create_calendar_event(
    event: CalendarEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new content calendar event with optional AI recommendations"""
    service = ContentCalendarService(db)

    db_event = await service.create_calendar_event(
        organization_id=_org_id(current_user),
        event_type=CalendarEventType[event.event_type.upper()],
        title=event.title,
        scheduled_for=event.scheduled_for,
        description=event.description,
        content_id=event.content_id,
        creator_user_id=current_user.id,
        duration_minutes=event.duration_minutes
    )
    return db_event


@router.get("/calendar/events", tags=["content-calendar"])
async def get_calendar_events(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    limit: int = Query(100, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get calendar events for date range"""
    service = ContentCalendarService(db)
    events = await service.get_calendar_events(
        _org_id(current_user),
        start_date,
        end_date,
        limit
    )
    return {
        "count": len(events),
        "events": [CalendarEventResponse.model_validate(event) for event in events],
    }


@router.get("/calendar/recommendation/{content_id}", response_model=SchedulingRecommendationResponse, tags=["content-calendar"])
async def get_scheduling_recommendation(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI scheduling recommendation for content"""
    service = ContentCalendarService(db)
    recommendation = await service.get_calendar_recommendation(
        _org_id(current_user),
        content_id
    )

    if not recommendation:
        raise HTTPException(status_code=404, detail="No recommendation found")

    return recommendation


@router.post("/calendar/recommendation/{content_id}/accept", tags=["content-calendar"])
async def accept_recommendation(
    content_id: int,
    recommendation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept AI scheduling recommendation"""
    service = ContentCalendarService(db)
    rec = await service.accept_recommendation(recommendation_id)

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return {"message": "Recommendation accepted", "recommendation": rec}


# ==================== MODULE 62: AI PROOFREADING ====================

@router.post("/proofread", response_model=ProofreadingCheckResponse, tags=["proofreading"])
async def check_proofreading(
    check: ProofreadingCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check content for grammar, spelling, and style issues"""
    organization_id = _org_id(current_user)
    issues = await find_proofreading_issues(check.text, check.check_grammar, check.check_spelling, check.check_style)

    service = ProofreadingService(db)
    db_check = await service.create_proofreading_check(
        content_id=check.content_id,
        organization_id=organization_id,
        original_text=check.text,
        check_grammar=check.check_grammar,
        check_spelling=check.check_spelling,
        check_style=check.check_style
    )
    counts = {"grammar": 0, "spelling": 0, "punctuation": 0, "style": 0}
    for issue in issues:
        await service.add_proofreading_issue(
            db_check.id,
            ProofreadingIssueType(issue["type"]),
            IssueSeverity(issue["severity"]),
            issue["position"],
            issue["length"],
            issue["text"],
            issue["suggestion"],
            issue["explanation"],
        )
        counts[issue["type"]] += 1

    return await service.update_proofreading_results(
        db_check.id,
        grammar_issues=counts["grammar"],
        spelling_issues=counts["spelling"],
        punctuation_issues=counts["punctuation"],
        style_issues=counts["style"],
    )


def _proofreading_payload(check) -> dict:
    """Response fields for a proofreading check (without its issues)."""
    return {
        "id": check.id,
        "content_id": check.content_id,
        "quality_score": check.quality_score,
        "overall_rating": check.overall_rating,
        "total_issues": check.total_issues,
        "grammar_issues": check.grammar_issues,
        "spelling_issues": check.spelling_issues,
        "punctuation_issues": check.punctuation_issues,
        "style_issues": check.style_issues,
    }


@router.get("/proofread/{check_id}", tags=["proofreading"])
async def get_proofreading_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get proofreading check details with all issues"""
    service = ProofreadingService(db)
    check = await service.get_proofreading_check(check_id)

    if not check:
        raise HTTPException(status_code=404, detail="Check not found")

    return {
        **_proofreading_payload(check),
        "issues": [
            {
                "id": issue.id,
                "type": issue.issue_type,
                "severity": issue.severity,
                "text": issue.text,
                "suggestion": issue.suggestion,
                "position": issue.position,
                "length": issue.length
            }
            for issue in check.issues
        ]
    }


@router.get("/proofread/content/{content_id}/latest", tags=["proofreading"])
async def get_latest_proofreading(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most recent proofreading check for content"""
    service = ProofreadingService(db)
    check = await service.get_latest_proofreading_check(content_id)

    if not check:
        raise HTTPException(status_code=404, detail="No proofreading check found")

    return check


# ==================== MODULE 63: PLAGIARISM DETECTION ====================

@router.post("/plagiarism/check", response_model=PlagiarismCheckResponse, tags=["plagiarism"])
async def check_plagiarism(
    check: PlagiarismCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check content for plagiarism and originality.

    Matching against published sources needs an external similarity-search provider (for example
    Copyscape or Turnitin). None is integrated, so the check is refused rather than answered with
    invented sources. No record is created for a refused check.
    """
    _org_id(current_user)
    raise HTTPException(
        status_code=503,
        detail="Plagiarism detection is not available: no similarity-search provider is configured on this server",
    )


@router.get("/plagiarism/check/{check_id}", tags=["plagiarism"])
async def get_plagiarism_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get plagiarism check results"""
    service = PlagiarismDetectionService(db)
    check = await service.get_plagiarism_check(check_id)

    if not check:
        raise HTTPException(status_code=404, detail="Check not found")

    return {
        "id": check.id,
        "content_id": check.content_id,
        "status": check.status,
        "similarity_percentage": check.similarity_percentage,
        "originality_percentage": check.originality_percentage,
        "plagiarism_risk": check.plagiarism_risk,
        "total_sources_found": check.total_sources_found,
        "ai_content_percentage": check.ai_content_percentage,
        "human_content_percentage": check.human_content_percentage,
        "detected_sources": check.detected_sources,
        "check_completed_at": check.check_completed_at
    }


@router.get("/plagiarism/content/{content_id}/latest", tags=["plagiarism"])
async def get_latest_plagiarism_check(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most recent plagiarism check for content"""
    service = PlagiarismDetectionService(db)
    check = await service.get_latest_plagiarism_check(content_id)

    if not check:
        raise HTTPException(status_code=404, detail="No plagiarism check found")

    return check


# ==================== MODULE 64: READABILITY ====================

@router.post("/readability/check", response_model=ReadabilityScoreResponse, tags=["readability"])
async def check_readability(
    check: ReadabilityCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze content readability metrics with the published formulas"""
    try:
        metrics = analyze(check.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    service = ReadabilityService(db)
    score = await service.create_readability_score(
        content_id=check.content_id,
        organization_id=_org_id(current_user),
        text_analyzed=check.text
    )
    stored = await service.store_readability_metrics(score.id, metrics)
    return _readability_payload(stored)


def _readability_payload(score) -> dict:
    """Response body for a readability score, shared by the analysis and the lookup."""
    return {
        "id": score.id,
        "content_id": score.content_id,
        "word_count": score.word_count,
        "sentence_count": score.sentence_count,
        "paragraph_count": score.paragraph_count,
        "flesch_reading_ease": score.flesch_reading_ease,
        "flesch_kincaid_grade": score.flesch_kincaid_grade,
        "gunning_fog_index": score.gunning_fog_index,
        "smog_index": score.smog_index,
        "readability_level": score.readability_level,
        "target_audience_grade_level": score.target_audience_grade_level,
        "complexity_score": score.complexity_score,
        "avg_word_length": score.avg_word_length,
        "avg_sentence_length": score.avg_sentence_length,
        "recommendations": score.recommendations
    }


@router.get("/readability/check/{score_id}", tags=["readability"])
async def get_readability_score(
    score_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get readability analysis"""
    service = ReadabilityService(db)
    score = await service.get_readability_score(score_id)

    if not score:
        raise HTTPException(status_code=404, detail="Score not found")

    return _readability_payload(score)


@router.get("/readability/content/{content_id}/latest", tags=["readability"])
async def get_latest_readability(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most recent readability analysis"""
    service = ReadabilityService(db)
    score = await service.get_latest_readability_score(content_id)

    if not score:
        raise HTTPException(status_code=404, detail="No readability analysis found")

    return score


# ==================== MODULE 65: BRAND VOICE ====================

@router.post("/brand-voice/guide", response_model=BrandVoiceGuideResponse, tags=["brand-voice"])
async def create_brand_voice_guide(
    guide: BrandVoiceGuideCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create brand voice and style guide"""
    service = BrandVoiceService(db)

    db_guide = await service.create_brand_voice_guide(
        organization_id=_org_id(current_user),
        name=guide.name,
        created_by_user_id=current_user.id,
        description=guide.description,
        tone=guide.tone,
        personality_traits=guide.personality_traits,
        vocabulary_level=guide.vocabulary_level,
        sentence_structure=guide.sentence_structure,
        paragraph_length=guide.paragraph_length
    )

    return db_guide


@router.get("/brand-voice/guide/{guide_id}", response_model=BrandVoiceGuideResponse, tags=["brand-voice"])
async def get_brand_voice_guide(
    guide_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get brand voice guide"""
    service = BrandVoiceService(db)
    guide = await service.get_brand_voice_guide(guide_id)

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    return guide


@router.get("/brand-voice/guide", tags=["brand-voice"])
async def get_active_brand_voice_guide(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active brand voice guide for organization"""
    service = BrandVoiceService(db)
    guide = await service.get_active_guide_for_org(_org_id(current_user))

    if not guide:
        raise HTTPException(status_code=404, detail="No active guide found")

    return guide


@router.put("/brand-voice/guide/{guide_id}", response_model=BrandVoiceGuideResponse, tags=["brand-voice"])
async def update_brand_voice_guide(
    guide_id: int,
    guide: BrandVoiceGuideCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update brand voice guide"""
    service = BrandVoiceService(db)

    updated = await service.update_brand_voice_guide(
        guide_id,
        name=guide.name,
        description=guide.description,
        tone=guide.tone,
        personality_traits=guide.personality_traits,
        vocabulary_level=guide.vocabulary_level,
        sentence_structure=guide.sentence_structure,
        paragraph_length=guide.paragraph_length
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Guide not found")

    return updated


@router.post("/brand-voice/check", response_model=BrandVoiceCheckResponse, tags=["brand-voice"])
async def check_brand_voice(
    check: BrandVoiceCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Score content against a brand voice guide (the provided guide, or the organization's active one)"""
    organization_id = _org_id(current_user)
    service = BrandVoiceService(db)

    if check.guide_id:
        guide = await service.get_brand_voice_guide(check.guide_id)
        if not guide or guide.organization_id != organization_id:
            raise HTTPException(status_code=404, detail="Brand voice guide not found")
    else:
        guide = await service.get_active_guide_for_org(organization_id)
    if guide is None:
        raise HTTPException(
            status_code=422,
            detail="Create a brand voice guide for your organization before checking content",
        )

    scores = await analyze_brand_voice(check.text, describe_guide(guide))
    db_check = await service.create_brand_voice_check(
        content_id=check.content_id,
        guide_id=guide.id,
        organization_id=organization_id,
        text_analyzed=check.text
    )
    result = await service.update_brand_voice_check_results(
        db_check.id,
        check_result=BrandVoiceCheckResult(brand_voice_result(scores["compliance_score"])),
        compliance_score=scores["compliance_score"],
        tone_match_score=scores["tone_match_score"],
        consistency_score=scores["consistency_score"],
        recommendations=scores["recommendations"],
    )
    overall = (scores["compliance_score"] + scores["tone_match_score"] + scores["consistency_score"]) / 3
    result.overall_score = round(overall, 2)
    await db.commit()
    await db.refresh(result)
    return result


@router.get("/brand-voice/check/{check_id}", tags=["brand-voice"])
async def get_brand_voice_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get brand voice check results"""
    service = BrandVoiceService(db)
    check = await service.get_brand_voice_check(check_id)

    if not check:
        raise HTTPException(status_code=404, detail="Check not found")

    return {
        "id": check.id,
        "content_id": check.content_id,
        "check_result": check.check_result,
        "overall_score": check.overall_score,
        "compliance_score": check.compliance_score,
        "tone_match_score": check.tone_match_score,
        "consistency_score": check.consistency_score,
        "tone_analysis": check.tone_analysis,
        "terminology_issues": check.terminology_issues,
        "style_compliance_issues": check.style_compliance_issues,
        "active_voice_percentage": check.active_voice_percentage,
        "recommendations": check.recommendations
    }


@router.get("/brand-voice/content/{content_id}/latest", tags=["brand-voice"])
async def get_latest_brand_voice_check(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most recent brand voice check for content"""
    service = BrandVoiceService(db)
    check = await service.get_latest_brand_voice_check(content_id)

    if not check:
        raise HTTPException(status_code=404, detail="No brand voice check found")

    return check
