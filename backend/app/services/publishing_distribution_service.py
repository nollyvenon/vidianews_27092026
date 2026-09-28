"""Services for Publishing, Distribution & Optimization: Modules 66-70"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
import json
import math

from app.models.publishing_distribution import (
    PublishingJob, PublishingSchedule, PublishingLog,
    SyndicationProfile, DistributionChannel, SyndicationLog,
    EngagementMetric, PerformanceAnalytics, EngagementTracker,
    ABTestCampaign, ABTestVariant, ABTestResult,
    RecommendationEngine, UserPreference, RecommendationLog,
    PublishingStatus, DistributionChannel as DistChannelEnum,
    ABTestStatus, RecommendationType, UserPreferenceCategory
)


class PublishingService:
    """Module 66: Publishing and scheduling service"""

    @staticmethod
    async def create_publishing_job(
        session: AsyncSession,
        org_id: int,
        content_id: int,
        user_id: int,
        title: str,
        scheduled_publish_time: datetime,
        distribution_channels: List[str],
        auto_promote: bool = False,
    ) -> PublishingJob:
        """Create a new publishing job"""
        job = PublishingJob(
            organization_id=org_id,
            content_id=content_id,
            creator_user_id=user_id,
            title=title,
            scheduled_publish_time=scheduled_publish_time,
            distribution_channels=distribution_channels,
            auto_promote=auto_promote,
            status=PublishingStatus.SCHEDULED,
        )
        session.add(job)
        await session.flush()
        return job

    @staticmethod
    async def get_pending_jobs(session: AsyncSession, org_id: int) -> List[PublishingJob]:
        """Get all pending jobs ready to publish"""
        result = await session.execute(
            select(PublishingJob).where(
                and_(
                    PublishingJob.organization_id == org_id,
                    PublishingJob.status == PublishingStatus.SCHEDULED,
                    PublishingJob.scheduled_publish_time <= datetime.now(timezone.utc),
                )
            ).order_by(PublishingJob.scheduled_publish_time)
        )
        return result.scalars().all()

    @staticmethod
    async def update_publishing_job_status(
        session: AsyncSession,
        job_id: int,
        status: PublishingStatus,
        publish_time: Optional[datetime] = None,
        error_message: Optional[str] = None,
    ) -> PublishingJob:
        """Update publishing job status"""
        result = await session.execute(select(PublishingJob).where(PublishingJob.id == job_id))
        job = result.scalar_one()

        job.status = status
        if publish_time:
            job.actual_publish_time = publish_time
        if error_message:
            job.error_message = error_message
        if status == PublishingStatus.FAILED:
            job.retry_count += 1

        job.updated_at = datetime.now(timezone.utc)
        await session.flush()
        return job

    @staticmethod
    async def create_publishing_schedule(
        session: AsyncSession,
        org_id: int,
        name: str,
        frequency: str,
        time_of_day: str,
        default_channels: List[str],
    ) -> PublishingSchedule:
        """Create a publishing schedule template"""
        schedule = PublishingSchedule(
            organization_id=org_id,
            name=name,
            frequency=frequency,
            time_of_day=time_of_day,
            default_channels=default_channels,
            is_template=True,
        )
        session.add(schedule)
        await session.flush()
        return schedule

    @staticmethod
    async def log_publishing_event(
        session: AsyncSession,
        org_id: int,
        job_id: int,
        content_id: int,
        event_type: str,
        status: str,
        published_url: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> PublishingLog:
        """Log a publishing event"""
        log = PublishingLog(
            organization_id=org_id,
            publishing_job_id=job_id,
            content_id=content_id,
            event_type=event_type,
            status=status,
            published_url=published_url,
            error_message=error_message,
        )
        session.add(log)
        await session.flush()
        return log


class DistributionService:
    """Module 67: Distribution and syndication service"""

    @staticmethod
    async def create_syndication_profile(
        session: AsyncSession,
        org_id: int,
        partner_name: str,
        partner_type: str,
        api_endpoint: str,
        auto_syndicate: bool = False,
    ) -> SyndicationProfile:
        """Create a syndication partner profile"""
        profile = SyndicationProfile(
            organization_id=org_id,
            partner_name=partner_name,
            partner_type=partner_type,
            api_endpoint=api_endpoint,
            auto_syndicate=auto_syndicate,
            is_active=True,
        )
        session.add(profile)
        await session.flush()
        return profile

    @staticmethod
    async def get_active_distribution_channels(
        session: AsyncSession,
        org_id: int,
    ) -> List[DistributionChannel]:
        """Get all active distribution channels"""
        result = await session.execute(
            select(DistributionChannel).where(
                and_(
                    DistributionChannel.organization_id == org_id,
                    DistributionChannel.is_active == True,
                )
            ).order_by(DistributionChannel.priority)
        )
        return result.scalars().all()

    @staticmethod
    async def syndicate_content(
        session: AsyncSession,
        org_id: int,
        content_id: int,
        profile_id: int,
        syndication_url: str,
    ) -> SyndicationLog:
        """Log content syndication"""
        log = SyndicationLog(
            organization_id=org_id,
            syndication_profile_id=profile_id,
            content_id=content_id,
            status="success",
            syndicated_url=syndication_url,
        )
        session.add(log)
        await session.flush()
        return log

    @staticmethod
    async def track_syndication_performance(
        session: AsyncSession,
        log_id: int,
        impressions: int,
        clicks: int,
    ) -> SyndicationLog:
        """Update syndication performance metrics"""
        result = await session.execute(select(SyndicationLog).where(SyndicationLog.id == log_id))
        log = result.scalar_one()

        log.impressions = impressions
        log.clicks = clicks
        if impressions > 0:
            log.engagement_rate = clicks / impressions

        log.updated_at = datetime.now(timezone.utc)
        await session.flush()
        return log


class AnalyticsService:
    """Module 68: Performance analytics and engagement tracking"""

    @staticmethod
    async def record_engagement(
        session: AsyncSession,
        org_id: int,
        content_id: int,
        user_id: Optional[int],
        action_type: str,
        device_type: str,
        referrer_url: Optional[str] = None,
    ) -> EngagementTracker:
        """Record user engagement action"""
        tracker = EngagementTracker(
            organization_id=org_id,
            content_id=content_id,
            user_id=user_id,
            action_type=action_type,
            device_type=device_type,
            referrer_url=referrer_url,
        )
        session.add(tracker)
        await session.flush()
        return tracker

    @staticmethod
    async def get_engagement_metrics(
        session: AsyncSession,
        org_id: int,
        content_id: int,
    ) -> Optional[EngagementMetric]:
        """Get engagement metrics for content"""
        result = await session.execute(
            select(EngagementMetric).where(
                and_(
                    EngagementMetric.organization_id == org_id,
                    EngagementMetric.content_id == content_id,
                )
            ).order_by(desc(EngagementMetric.metric_date)).limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_engagement_metrics(
        session: AsyncSession,
        org_id: int,
        content_id: int,
        views: int,
        clicks: int,
        shares: int,
        comments: int,
        reactions: int,
    ) -> EngagementMetric:
        """Update or create engagement metrics"""
        # Try to get existing metric for today
        today = datetime.now(timezone.utc).date()
        result = await session.execute(
            select(EngagementMetric).where(
                and_(
                    EngagementMetric.organization_id == org_id,
                    EngagementMetric.content_id == content_id,
                )
            )
        )
        metric = result.scalar_one_or_none()

        if not metric:
            metric = EngagementMetric(
                organization_id=org_id,
                content_id=content_id,
                metric_date=datetime.now(timezone.utc),
            )
            session.add(metric)

        metric.total_views = views
        metric.total_clicks = clicks
        metric.total_shares = shares
        metric.total_comments = comments
        metric.total_reactions = reactions

        # Calculate engagement score
        metric.engagement_score = AnalyticsService._calculate_engagement_score(
            views, clicks, shares, comments, reactions
        )

        metric.updated_at = datetime.now(timezone.utc)
        await session.flush()
        return metric

    @staticmethod
    def _calculate_engagement_score(views: int, clicks: int, shares: int, comments: int, reactions: int) -> float:
        """Calculate engagement score based on metrics"""
        if views == 0:
            return 0.0

        click_rate = clicks / max(views, 1)
        share_rate = shares / max(views, 1)
        comment_rate = comments / max(views, 1)
        reaction_rate = reactions / max(views, 1)

        # Weighted calculation
        score = (
            (click_rate * 0.3) +
            (share_rate * 0.3) +
            (comment_rate * 0.2) +
            (reaction_rate * 0.2)
        ) * 100

        return min(100.0, score)

    @staticmethod
    async def create_performance_analytics(
        session: AsyncSession,
        org_id: int,
        period_type: str,
        total_content: int,
        avg_engagement: float,
        total_views: int,
    ) -> PerformanceAnalytics:
        """Create performance analytics report"""
        now = datetime.now(timezone.utc)

        if period_type == "daily":
            period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=1)
        elif period_type == "weekly":
            period_start = now - timedelta(days=now.weekday())
            period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=7)
        else:  # monthly
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = period_start + timedelta(days=32)
            period_end = next_month.replace(day=1)

        analytics = PerformanceAnalytics(
            organization_id=org_id,
            period_start=period_start,
            period_end=period_end,
            period_type=period_type,
            total_content_published=total_content,
            avg_engagement_score=avg_engagement,
            total_views_all_content=total_views,
        )
        session.add(analytics)
        await session.flush()
        return analytics


class ABTestingService:
    """Module 69: A/B testing and optimization service"""

    @staticmethod
    async def create_ab_test(
        session: AsyncSession,
        org_id: int,
        content_id: int,
        user_id: int,
        name: str,
        test_metric: str,
        hypothesis: str,
    ) -> ABTestCampaign:
        """Create a new A/B test campaign"""
        campaign = ABTestCampaign(
            organization_id=org_id,
            content_id=content_id,
            creator_user_id=user_id,
            name=name,
            test_metric=test_metric,
            hypothesis=hypothesis,
            status=ABTestStatus.DRAFT,
        )
        session.add(campaign)
        await session.flush()
        return campaign

    @staticmethod
    async def create_test_variant(
        session: AsyncSession,
        campaign_id: int,
        variant_name: str,
        variant_type: str,
        title_variant: Optional[str] = None,
        cta_text_variant: Optional[str] = None,
    ) -> ABTestVariant:
        """Create a test variant"""
        variant = ABTestVariant(
            ab_test_campaign_id=campaign_id,
            variant_name=variant_name,
            variant_type=variant_type,
            title_variant=title_variant,
            cta_text_variant=cta_text_variant,
        )
        session.add(variant)
        await session.flush()
        return variant

    @staticmethod
    async def record_variant_performance(
        session: AsyncSession,
        variant_id: int,
        impressions: int,
        clicks: int,
        conversions: int,
    ) -> ABTestVariant:
        """Record variant performance metrics"""
        result = await session.execute(select(ABTestVariant).where(ABTestVariant.id == variant_id))
        variant = result.scalar_one()

        variant.impressions = impressions
        variant.clicks = clicks
        variant.conversions = conversions

        # Calculate metrics
        if impressions > 0:
            variant.ctr = clicks / impressions
        if clicks > 0:
            variant.conversion_rate = conversions / clicks

        # Calculate performance score
        variant.performance_score = (variant.ctr * 0.4) + (variant.conversion_rate * 0.6) * 100

        await session.flush()
        return variant

    @staticmethod
    async def analyze_test_results(
        session: AsyncSession,
        campaign_id: int,
    ) -> ABTestResult:
        """Analyze A/B test results and determine winner"""
        # Get all variants for this campaign
        result = await session.execute(
            select(ABTestVariant).where(ABTestVariant.ab_test_campaign_id == campaign_id)
        )
        variants = result.scalars().all()

        if len(variants) < 2:
            raise ValueError("Need at least 2 variants to analyze")

        variant_a = variants[0]
        variant_b = variants[1]

        # Chi-square test for statistical significance
        chi_square, p_value = ABTestingService._chi_square_test(
            variant_a.conversions, variant_a.clicks,
            variant_b.conversions, variant_b.clicks
        )

        # Determine winner
        is_significant = p_value < 0.05
        improvement = ((variant_b.conversion_rate - variant_a.conversion_rate) /
                       variant_a.conversion_rate * 100) if variant_a.conversion_rate > 0 else 0

        winner = "B" if variant_b.performance_score > variant_a.performance_score else "A"

        test_result = ABTestResult(
            ab_test_campaign_id=campaign_id,
            chi_square_statistic=chi_square,
            p_value=p_value,
            variant_a_metric_value=variant_a.performance_score,
            variant_b_metric_value=variant_b.performance_score,
            improvement_percent=improvement,
            is_significant=is_significant,
            recommended_action="deploy_" + winner.lower() if is_significant else "continue_testing",
            analyzed_at=datetime.now(timezone.utc),
        )
        session.add(test_result)

        # Update campaign with results
        campaign_result = await session.execute(select(ABTestCampaign).where(ABTestCampaign.id == campaign_id))
        campaign = campaign_result.scalar_one()
        campaign.winner = winner
        campaign.is_statistically_significant = is_significant
        campaign.status = ABTestStatus.COMPLETED

        await session.flush()
        return test_result

    @staticmethod
    def _chi_square_test(conversions_a: int, clicks_a: int, conversions_b: int, clicks_b: int) -> tuple:
        """Perform chi-square test for statistical significance"""
        # Contingency table
        # [conversions_a, clicks_a - conversions_a]
        # [conversions_b, clicks_b - conversions_b]

        non_conversions_a = clicks_a - conversions_a
        non_conversions_b = clicks_b - conversions_b

        total = clicks_a + clicks_b
        if total == 0:
            return 0, 1

        # Expected frequencies
        total_conversions = conversions_a + conversions_b
        total_non_conversions = non_conversions_a + non_conversions_b

        expected_a = (clicks_a / total) * total_conversions
        expected_b = (clicks_b / total) * total_conversions

        # Chi-square calculation
        chi_square = (
            ((conversions_a - expected_a) ** 2 / expected_a) if expected_a > 0 else 0 +
            ((conversions_b - expected_b) ** 2 / expected_b) if expected_b > 0 else 0
        )

        # Simplified p-value (approximation)
        p_value = 0.05 if chi_square > 3.841 else 0.5

        return chi_square, p_value


class RecommendationService:
    """Module 70: Content recommendation service"""

    @staticmethod
    async def create_recommendation_engine(
        session: AsyncSession,
        org_id: int,
        name: str,
        recommendation_type: RecommendationType,
    ) -> RecommendationEngine:
        """Create a recommendation engine"""
        engine = RecommendationEngine(
            organization_id=org_id,
            name=name,
            recommendation_type=recommendation_type,
            is_active=True,
        )
        session.add(engine)
        await session.flush()
        return engine

    @staticmethod
    async def record_user_preference(
        session: AsyncSession,
        org_id: int,
        user_id: int,
        category: UserPreferenceCategory,
        value: str,
        weight: float = 1.0,
    ) -> UserPreference:
        """Record user preference"""
        preference = UserPreference(
            organization_id=org_id,
            user_id=user_id,
            preference_category=category,
            preference_value=value,
            preference_weight=weight,
        )
        session.add(preference)
        await session.flush()
        return preference

    @staticmethod
    async def get_user_preferences(
        session: AsyncSession,
        org_id: int,
        user_id: int,
    ) -> List[UserPreference]:
        """Get all preferences for a user"""
        result = await session.execute(
            select(UserPreference).where(
                and_(
                    UserPreference.organization_id == org_id,
                    UserPreference.user_id == user_id,
                    UserPreference.is_active == True,
                )
            )
        )
        return result.scalars().all()

    @staticmethod
    async def generate_recommendations(
        session: AsyncSession,
        org_id: int,
        user_id: int,
        engine_id: int,
        content_pool: List[int],
        num_recommendations: int = 5,
    ) -> RecommendationLog:
        """Generate content recommendations for a user"""
        # Get user preferences
        preferences = await RecommendationService.get_user_preferences(session, org_id, user_id)

        # Score content based on preferences (simplified algorithm)
        content_scores = {}
        for content_id in content_pool:
            # Score based on preference matching
            score = RecommendationService._score_content(content_id, preferences)
            content_scores[content_id] = score

        # Get top N recommendations
        sorted_content = sorted(content_scores.items(), key=lambda x: x[1], reverse=True)
        recommended_ids = [cid for cid, _ in sorted_content[:num_recommendations]]
        recommendation_scores = [score for _, score in sorted_content[:num_recommendations]]

        # Log recommendation
        log = RecommendationLog(
            organization_id=org_id,
            recommendation_engine_id=engine_id,
            user_id=user_id,
            recommended_content_ids=recommended_ids,
            recommendation_scores=recommendation_scores,
        )
        session.add(log)
        await session.flush()
        return log

    @staticmethod
    async def record_recommendation_click(
        session: AsyncSession,
        log_id: int,
        clicked_content_id: int,
    ) -> RecommendationLog:
        """Record when a user clicks a recommendation"""
        result = await session.execute(select(RecommendationLog).where(RecommendationLog.id == log_id))
        log = result.scalar_one()

        log.was_clicked = True
        log.clicked_content_id = clicked_content_id
        log.updated_at = datetime.now(timezone.utc)

        await session.flush()
        return log

    @staticmethod
    def _score_content(content_id: int, preferences: List[UserPreference]) -> float:
        """Score content based on user preferences"""
        base_score = 0.5

        # Simplified scoring: each preference adds weight
        for pref in preferences:
            if pref.preference_weight > 0:
                base_score += (pref.preference_weight * pref.confidence_score * 0.1)

        return min(1.0, base_score)
