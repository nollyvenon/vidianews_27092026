"""API Routes for Publishing, Distribution & Optimization: Modules 66-70"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.services.publishing_distribution_service import (
    PublishingService, DistributionService, AnalyticsService,
    ABTestingService, RecommendationService
)
from app.models.publishing_distribution import (
    PublishingStatus, RecommendationType, UserPreferenceCategory
)

# ==================== ROUTERS ====================

router = APIRouter(prefix="/api/v1", tags=["publishing-distribution"])
publishing_router = APIRouter(prefix="/publishing", tags=["publishing"])
distribution_router = APIRouter(prefix="/distribution", tags=["distribution"])
analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])
ab_test_router = APIRouter(prefix="/ab-testing", tags=["ab-testing"])
recommendation_router = APIRouter(prefix="/recommendations", tags=["recommendations"])


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
    user_id: int
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
    org_id: int = Query(...),
    user_id: int = Query(...),
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
            status=job.status.value,
            scheduled_publish_time=job.scheduled_publish_time,
            distribution_channels=job.distribution_channels,
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@publishing_router.get("/jobs/pending")
async def get_pending_jobs(
    org_id: int = Query(...),
    session: AsyncSession = Depends(get_db),
) -> List[PublishingJobResponse]:
    """Get all pending publishing jobs"""
    try:
        jobs = await PublishingService.get_pending_jobs(session, org_id)

        return [
            PublishingJobResponse(
                id=job.id,
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
    org_id: int = Query(...),
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


@distribution_router.post("/syndicate")
async def syndicate_content(
    content_id: int = Query(...),
    profile_id: int = Query(...),
    syndication_url: str = Query(...),
    org_id: int = Query(...),
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
    org_id: int = Query(...),
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
    org_id: int = Query(...),
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@analytics_router.post("/metrics/update")
async def update_engagement_metrics(
    content_id: int = Query(...),
    org_id: int = Query(...),
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

@ab_test_router.post("/campaigns")
async def create_ab_test(
    request: ABTestRequest,
    org_id: int = Query(...),
    user_id: int = Query(...),
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
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Create test variant"""
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
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Record variant performance"""
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
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Analyze A/B test results"""
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

@recommendation_router.post("/generate")
async def generate_recommendations(
    request: RecommendationRequest,
    org_id: int = Query(...),
    engine_id: int = Query(...),
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Generate content recommendations"""
    try:
        log = await RecommendationService.generate_recommendations(
            session=session,
            org_id=org_id,
            user_id=request.user_id,
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
    org_id: int = Query(...),
    user_id: int = Query(...),
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
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Record recommendation click"""
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
