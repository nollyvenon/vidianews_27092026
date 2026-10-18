"""API Routes for Publishing, Distribution & Optimization: Modules 66-70"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import func, select

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.publishing_distribution_service import (
    PublishingService, DistributionService, AnalyticsService,
    ABTestingService, RecommendationService
)
from app.models.publishing_distribution import (
    ABTestCampaign, ABTestVariant, PublishingStatus, SyndicationLog, SyndicationProfile, RecommendationEngine, RecommendationLog,
    RecommendationType, UserPreferenceCategory
)

# ==================== ROUTERS ====================

router = APIRouter(tags=["publishing-distribution"])
publishing_router = APIRouter(prefix="/publishing", tags=["publishing"])
distribution_router = APIRouter(prefix="/distribution", tags=["distribution"])
analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])
ab_test_router = APIRouter(prefix="/ab-testing", tags=["ab-testing"])
# Not "/recommendations": advanced_features mounts /recommendations/{user_id}, which would shadow these routes.
recommendation_router = APIRouter(prefix="/content-recommendations", tags=["recommendations"])


async def current_org_id(current_user: User = Depends(get_current_user)) -> int:
    """Organization of the signed-in user; the caller never supplies it."""
    if current_user.organization_id is None:
        raise HTTPException(status_code=422, detail="Your account has no organization yet. Create one under Organizations first.")
    return current_user.organization_id


async def current_user_id(current_user: User = Depends(get_current_user)) -> int:
    """Id of the signed-in user; the caller never supplies it."""
    return current_user.id


async def _owned_campaign(session: AsyncSession, org_id: int, campaign_id: int) -> ABTestCampaign:
    """Campaign in the caller's organization. Other organizations' campaigns look like missing ones."""
    campaign = (
        await session.execute(
            select(ABTestCampaign).where(ABTestCampaign.id == campaign_id, ABTestCampaign.organization_id == org_id)
        )
    ).scalar_one_or_none()
    if campaign is None:
        raise HTTPException(status_code=404, detail="A/B test campaign not found")
    return campaign


async def _owned_variant(session: AsyncSession, org_id: int, variant_id: int) -> ABTestVariant:
    """Variant whose campaign belongs to the caller's organization."""
    variant = (
        await session.execute(
            select(ABTestVariant)
            .join(ABTestCampaign, ABTestVariant.ab_test_campaign_id == ABTestCampaign.id)
            .where(ABTestVariant.id == variant_id, ABTestCampaign.organization_id == org_id)
        )
    ).scalar_one_or_none()
    if variant is None:
        raise HTTPException(status_code=404, detail="A/B test variant not found")
    return variant


async def _owned_engine(session: AsyncSession, org_id: int, engine_id: int) -> RecommendationEngine:
    """Recommendation engine owned by the caller's organization."""
    engine = (
        await session.execute(
            select(RecommendationEngine).where(
                RecommendationEngine.id == engine_id, RecommendationEngine.organization_id == org_id
            )
        )
    ).scalar_one_or_none()
    if engine is None:
        raise HTTPException(status_code=404, detail="Recommendation engine not found")
    return engine


class ABTestVariantResponse(BaseModel):
    """One variant of an A/B test with its measured results"""
    id: int
    variant_name: str
    variant_type: str
    impressions: int
    clicks: int
    conversions: int
    ctr: float
    conversion_rate: float


class ABTestCampaignResponse(BaseModel):
    """An A/B test campaign and its variants"""
    id: int
    name: str
    content_id: int
    test_metric: str
    status: str
    winner: Optional[str] = None
    is_statistically_significant: bool
    variants: List[ABTestVariantResponse]


class RecommendationEngineRequest(BaseModel):
    """Recommendation engine creation request"""
    name: str = Field(..., min_length=1, max_length=255)
    recommendation_type: RecommendationType


class RecommendationEngineResponse(BaseModel):
    """Recommendation engine"""
    id: int
    name: str
    recommendation_type: str
    is_active: bool


def _variant_response(variant: ABTestVariant) -> ABTestVariantResponse:
    return ABTestVariantResponse(
        id=variant.id,
        variant_name=variant.variant_name,
        variant_type=variant.variant_type,
        impressions=variant.impressions or 0,
        clicks=variant.clicks or 0,
        conversions=variant.conversions or 0,
        # The model stores rates as fractions (clicks / impressions); the API reports percentages.
        ctr=float(variant.ctr or 0.0) * 100,
        conversion_rate=float(variant.conversion_rate or 0.0) * 100,
    )


def _engine_response(engine: RecommendationEngine) -> RecommendationEngineResponse:
    return RecommendationEngineResponse(
        id=engine.id,
        name=engine.name,
        recommendation_type=engine.recommendation_type.value,
        is_active=bool(engine.is_active),
    )


# ==================== SCHEMAS ====================

class PublishingJobRequest(BaseModel):
    """Publishing job creation request"""
    content_id: int
    title: str
    scheduled_publish_time: datetime
    distribution_channels: List[str]
    auto_promote: bool = False


class PublishingJobResponse(BaseModel):
    """Publishing job response"""
    id: int
    title: Optional[str] = None
    status: str
    scheduled_publish_time: datetime
    actual_publish_time: Optional[datetime] = None
    distribution_channels: List[str]


class EngagementRequest(BaseModel):
    """Engagement tracking request"""
    content_id: int
    action_type: str
    device_type: str
    referrer_url: Optional[str] = None


class EngagementMetricsResponse(BaseModel):
    """Engagement metrics response"""
    content_id: int
    total_views: int
    total_clicks: int
    total_shares: int
    engagement_score: float
    engagement_trend: Optional[str]


class ABTestRequest(BaseModel):
    """A/B test creation request"""
    content_id: int
    name: str
    test_metric: str
    hypothesis: str
    sample_size_percent: float = 50.0


class ABTestVariantRequest(BaseModel):
    """A/B test variant request"""
    variant_name: str
    variant_type: str
    title_variant: Optional[str] = None
    cta_text_variant: Optional[str] = None


class RecommendationRequest(BaseModel):
    """Recommendation generation request"""
    # Optional: when supplied it must be the signed-in user, which is always the one used.
    user_id: Optional[int] = None
    content_pool: List[int]
    num_recommendations: int = 5


class UserPreferenceRequest(BaseModel):
    """User preference request"""
    category: str
    value: str
    weight: float = 1.0


# ==================== MODULE 66: PUBLISHING ====================

@publishing_router.post("/jobs")
async def create_publishing_job(
    request: PublishingJobRequest,
    org_id: int = Depends(current_org_id),
    user_id: int = Depends(current_user_id),
    session: AsyncSession = Depends(get_db),
) -> PublishingJobResponse:
    """Create a new publishing job"""
    try:
        job = await PublishingService.create_publishing_job(
            session=session,
            org_id=org_id,
            content_id=request.content_id,
            user_id=user_id,
            title=request.title,
            scheduled_publish_time=request.scheduled_publish_time,
            distribution_channels=request.distribution_channels,
            auto_promote=request.auto_promote,
        )
        await session.commit()

        return PublishingJobResponse(
            id=job.id,
            title=job.title,
            status=job.status.value,
            scheduled_publish_time=job.scheduled_publish_time,
            distribution_channels=job.distribution_channels,
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@publishing_router.get("/jobs/pending")
async def get_pending_jobs(
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> List[PublishingJobResponse]:
    """Get all pending publishing jobs"""
    try:
        jobs = await PublishingService.get_pending_jobs(session, org_id)

        return [
            PublishingJobResponse(
                id=job.id,
                title=job.title,
                status=job.status.value,
                scheduled_publish_time=job.scheduled_publish_time,
                distribution_channels=job.distribution_channels,
            )
            for job in jobs
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@publishing_router.patch("/jobs/{job_id}/status")
async def update_job_status(
    job_id: int,
    status: str = Query(...),
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> PublishingJobResponse:
    """Update publishing job status"""
    try:
        job = await PublishingService.update_publishing_job_status(
            session=session,
            job_id=job_id,
            status=PublishingStatus(status),
            publish_time=datetime.now(timezone.utc) if status == "published" else None,
        )
        await session.commit()

        return PublishingJobResponse(
            id=job.id,
            status=job.status.value,
            scheduled_publish_time=job.scheduled_publish_time,
            actual_publish_time=job.actual_publish_time,
            distribution_channels=job.distribution_channels,
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MODULE 67: DISTRIBUTION ====================

@distribution_router.get("/channels")
async def get_distribution_channels(
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> List[dict]:
    """Get active distribution channels"""
    try:
        channels = await DistributionService.get_active_distribution_channels(session, org_id)

        return [
            {
                "id": channel.id,
                "type": channel.channel_type.value,
                "display_name": channel.display_name,
                "success_rate": channel.success_rate,
                "priority": channel.priority,
            }
            for channel in channels
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SyndicationProfileRequest(BaseModel):
    """A syndication partner the organization publishes to"""
    partner_name: str = Field(..., min_length=1, max_length=255)
    partner_type: str = Field(..., min_length=1, max_length=100)
    api_endpoint: Optional[str] = Field(None, max_length=2048)


@distribution_router.get("/syndication-profiles")
async def list_syndication_profiles(
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> List[dict]:
    """Syndication partners with the articles syndicated to each and the impressions they produced"""
    profiles = (await session.execute(
        select(SyndicationProfile).where(SyndicationProfile.organization_id == org_id).order_by(SyndicationProfile.id)
    )).scalars().all()
    totals = {
        row[0]: (int(row[1]), int(row[2]))
        for row in (await session.execute(
            select(SyndicationLog.syndication_profile_id, func.count(SyndicationLog.id), func.coalesce(func.sum(SyndicationLog.impressions), 0))
            .where(SyndicationLog.organization_id == org_id)
            .group_by(SyndicationLog.syndication_profile_id)
        )).all()
    }
    return [
        {
            "id": profile.id,
            "partner_name": profile.partner_name,
            "partner_type": profile.partner_type,
            "articles_syndicated": totals.get(profile.id, (0, 0))[0],
            "reach": totals.get(profile.id, (0, 0))[1],
        }
        for profile in profiles
    ]


@distribution_router.post("/syndication-profiles", status_code=201)
async def create_syndication_profile(
    request: SyndicationProfileRequest,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Add a syndication partner for the organization"""
    try:
        profile = await DistributionService.create_syndication_profile(
            session=session,
            org_id=org_id,
            partner_name=request.partner_name,
            partner_type=request.partner_type,
            api_endpoint=request.api_endpoint,
        )
        await session.commit()
        return {"id": profile.id, "partner_name": profile.partner_name, "partner_type": profile.partner_type}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@distribution_router.post("/syndicate")
async def syndicate_content(
    content_id: int = Query(...),
    profile_id: int = Query(...),
    syndication_url: str = Query(...),
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Syndicate content to a partner"""
    try:
        log = await DistributionService.syndicate_content(
            session=session,
            org_id=org_id,
            content_id=content_id,
            profile_id=profile_id,
            syndication_url=syndication_url,
        )
        await session.commit()

        return {
            "id": log.id,
            "status": log.status,
            "syndicated_url": log.syndicated_url,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MODULE 68: ANALYTICS ====================

@analytics_router.post("/engagement")
async def record_engagement(
    request: EngagementRequest,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Record user engagement"""
    try:
        tracker = await AnalyticsService.record_engagement(
            session=session,
            org_id=org_id,
            content_id=request.content_id,
            user_id=None,
            action_type=request.action_type,
            device_type=request.device_type,
            referrer_url=request.referrer_url,
        )
        await session.commit()

        return {
            "id": tracker.id,
            "action_type": tracker.action_type,
            "recorded_at": tracker.created_at,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@analytics_router.get("/metrics/{content_id}")
async def get_engagement_metrics(
    content_id: int,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> EngagementMetricsResponse:
    """Get engagement metrics for content"""
    try:
        metrics = await AnalyticsService.get_engagement_metrics(session, org_id, content_id)

        if not metrics:
            raise HTTPException(status_code=404, detail="Metrics not found")

        return EngagementMetricsResponse(
            content_id=metrics.content_id,
            total_views=metrics.total_views,
            total_clicks=metrics.total_clicks,
            total_shares=metrics.total_shares,
            engagement_score=metrics.engagement_score,
            engagement_trend=metrics.engagement_trend,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@analytics_router.post("/metrics/update")
async def update_engagement_metrics(
    content_id: int = Query(...),
    org_id: int = Depends(current_org_id),
    views: int = Query(...),
    clicks: int = Query(...),
    shares: int = Query(...),
    comments: int = Query(...),
    reactions: int = Query(...),
    session: AsyncSession = Depends(get_db),
) -> EngagementMetricsResponse:
    """Update engagement metrics"""
    try:
        metrics = await AnalyticsService.update_engagement_metrics(
            session=session,
            org_id=org_id,
            content_id=content_id,
            views=views,
            clicks=clicks,
            shares=shares,
            comments=comments,
            reactions=reactions,
        )
        await session.commit()

        return EngagementMetricsResponse(
            content_id=metrics.content_id,
            total_views=metrics.total_views,
            total_clicks=metrics.total_clicks,
            total_shares=metrics.total_shares,
            engagement_score=metrics.engagement_score,
            engagement_trend=metrics.engagement_trend,
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MODULE 69: A/B TESTING ====================

@ab_test_router.get("/campaigns", response_model=List[ABTestCampaignResponse])
async def list_ab_tests(
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> List[ABTestCampaignResponse]:
    """List the organization's A/B test campaigns with their variant results"""
    campaigns = (
        await session.execute(
            select(ABTestCampaign)
            .where(ABTestCampaign.organization_id == org_id)
            .order_by(ABTestCampaign.id.desc())
        )
    ).scalars().all()
    if not campaigns:
        return []

    variants = (
        await session.execute(
            select(ABTestVariant)
            .where(ABTestVariant.ab_test_campaign_id.in_([campaign.id for campaign in campaigns]))
            .order_by(ABTestVariant.id)
        )
    ).scalars().all()
    variants_by_campaign: dict = {}
    for variant in variants:
        variants_by_campaign.setdefault(variant.ab_test_campaign_id, []).append(_variant_response(variant))

    return [
        ABTestCampaignResponse(
            id=campaign.id,
            name=campaign.name,
            content_id=campaign.content_id,
            test_metric=campaign.test_metric,
            status=campaign.status.value,
            winner=campaign.winner,
            is_statistically_significant=bool(campaign.is_statistically_significant),
            variants=variants_by_campaign.get(campaign.id, []),
        )
        for campaign in campaigns
    ]


@ab_test_router.post("/campaigns")
async def create_ab_test(
    request: ABTestRequest,
    org_id: int = Depends(current_org_id),
    user_id: int = Depends(current_user_id),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Create A/B test campaign"""
    try:
        campaign = await ABTestingService.create_ab_test(
            session=session,
            org_id=org_id,
            content_id=request.content_id,
            user_id=user_id,
            name=request.name,
            test_metric=request.test_metric,
            hypothesis=request.hypothesis,
        )
        await session.commit()

        return {
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status.value,
            "test_metric": campaign.test_metric,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@ab_test_router.post("/campaigns/{campaign_id}/variants")
async def create_variant(
    campaign_id: int,
    request: ABTestVariantRequest,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Create test variant"""
    await _owned_campaign(session, org_id, campaign_id)
    try:
        variant = await ABTestingService.create_test_variant(
            session=session,
            campaign_id=campaign_id,
            variant_name=request.variant_name,
            variant_type=request.variant_type,
            title_variant=request.title_variant,
            cta_text_variant=request.cta_text_variant,
        )
        await session.commit()

        return {
            "id": variant.id,
            "variant_name": variant.variant_name,
            "variant_type": variant.variant_type,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@ab_test_router.patch("/variants/{variant_id}/performance")
async def record_variant_performance(
    variant_id: int,
    impressions: int = Query(...),
    clicks: int = Query(...),
    conversions: int = Query(...),
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Record variant performance"""
    await _owned_variant(session, org_id, variant_id)
    try:
        variant = await ABTestingService.record_variant_performance(
            session=session,
            variant_id=variant_id,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
        )
        await session.commit()

        return {
            "id": variant.id,
            "ctr": variant.ctr,
            "conversion_rate": variant.conversion_rate,
            "performance_score": variant.performance_score,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@ab_test_router.post("/campaigns/{campaign_id}/analyze")
async def analyze_test(
    campaign_id: int,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Analyze A/B test results"""
    await _owned_campaign(session, org_id, campaign_id)
    try:
        result = await ABTestingService.analyze_test_results(session, campaign_id)
        await session.commit()

        return {
            "id": result.id,
            "p_value": result.p_value,
            "is_significant": result.is_significant,
            "improvement_percent": result.improvement_percent,
            "recommended_action": result.recommended_action,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MODULE 70: RECOMMENDATIONS ====================

@recommendation_router.get("/engines", response_model=List[RecommendationEngineResponse])
async def list_recommendation_engines(
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> List[RecommendationEngineResponse]:
    """List the organization's recommendation engines"""
    engines = (
        await session.execute(
            select(RecommendationEngine)
            .where(RecommendationEngine.organization_id == org_id)
            .order_by(RecommendationEngine.id)
        )
    ).scalars().all()
    return [_engine_response(engine) for engine in engines]


@recommendation_router.post("/engines", response_model=RecommendationEngineResponse, status_code=201)
async def create_recommendation_engine(
    request: RecommendationEngineRequest,
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
) -> RecommendationEngineResponse:
    """Create a recommendation engine for the organization"""
    try:
        engine = await RecommendationService.create_recommendation_engine(
            session=session,
            org_id=org_id,
            name=request.name,
            recommendation_type=request.recommendation_type,
        )
        await session.commit()
        return _engine_response(engine)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@recommendation_router.post("/generate")
async def generate_recommendations(
    request: RecommendationRequest,
    org_id: int = Depends(current_org_id),
    user_id: int = Depends(current_user_id),
    engine_id: int = Query(...),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Generate content recommendations for the signed-in user"""
    if request.user_id is not None and request.user_id != user_id:
        raise HTTPException(status_code=403, detail="Recommendations can only be generated for the signed-in user")
    await _owned_engine(session, org_id, engine_id)
    try:
        log = await RecommendationService.generate_recommendations(
            session=session,
            org_id=org_id,
            user_id=user_id,
            engine_id=engine_id,
            content_pool=request.content_pool,
            num_recommendations=request.num_recommendations,
        )
        await session.commit()

        return {
            "id": log.id,
            "recommended_content_ids": log.recommended_content_ids,
            "recommendation_scores": log.recommendation_scores,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@recommendation_router.post("/preferences")
async def record_preference(
    request: UserPreferenceRequest,
    org_id: int = Depends(current_org_id),
    user_id: int = Depends(current_user_id),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Record user preference"""
    try:
        preference = await RecommendationService.record_user_preference(
            session=session,
            org_id=org_id,
            user_id=user_id,
            category=UserPreferenceCategory(request.category),
            value=request.value,
            weight=request.weight,
        )
        await session.commit()

        return {
            "id": preference.id,
            "category": preference.preference_category.value,
            "value": preference.preference_value,
            "weight": preference.preference_weight,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@recommendation_router.post("/logs/{log_id}/click")
async def record_recommendation_click(
    log_id: int,
    clicked_content_id: int = Query(...),
    org_id: int = Depends(current_org_id),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Record recommendation click"""
    log = (
        await session.execute(
            select(RecommendationLog).where(
                RecommendationLog.id == log_id, RecommendationLog.organization_id == org_id
            )
        )
    ).scalar_one_or_none()
    if log is None:
        raise HTTPException(status_code=404, detail="Recommendation log not found")
    try:
        log = await RecommendationService.record_recommendation_click(
            session=session,
            log_id=log_id,
            clicked_content_id=clicked_content_id,
        )
        await session.commit()

        return {
            "id": log.id,
            "was_clicked": log.was_clicked,
            "clicked_content_id": log.clicked_content_id,
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ==================== ROUTER REGISTRATION ====================

router.include_router(publishing_router)
router.include_router(distribution_router)
router.include_router(analytics_router)
router.include_router(ab_test_router)
router.include_router(recommendation_router)
