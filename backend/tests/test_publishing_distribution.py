"""Tests for Publishing, Distribution & Optimization: Modules 66-70"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.services.publishing_distribution_service import (
    PublishingService, DistributionService, AnalyticsService,
    ABTestingService, RecommendationService
)
from app.models.publishing_distribution import (
    PublishingStatus, ABTestStatus, RecommendationType,
    UserPreferenceCategory
)


@pytest.fixture
async def async_session():
    """Create async test database session"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session

    await engine.dispose()


class TestPublishingService:
    """Tests for Module 66: Publishing Service"""

    @pytest.mark.asyncio
    async def test_create_publishing_job(self, async_session):
        """Test creating a publishing job"""
        job = await PublishingService.create_publishing_job(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            title="Test Article",
            scheduled_publish_time=datetime.now(timezone.utc),
            distribution_channels=["website", "email"],
            auto_promote=True,
        )

        assert job.id is not None
        assert job.title == "Test Article"
        assert job.status == PublishingStatus.SCHEDULED
        assert job.auto_promote == True

    @pytest.mark.asyncio
    async def test_update_publishing_job_status(self, async_session):
        """Test updating publishing job status"""
        job = await PublishingService.create_publishing_job(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            title="Test",
            scheduled_publish_time=datetime.now(timezone.utc),
            distribution_channels=["website"],
        )

        updated_job = await PublishingService.update_publishing_job_status(
            session=async_session,
            job_id=job.id,
            status=PublishingStatus.PUBLISHED,
            publish_time=datetime.now(timezone.utc),
        )

        assert updated_job.status == PublishingStatus.PUBLISHED
        assert updated_job.actual_publish_time is not None

    @pytest.mark.asyncio
    async def test_create_publishing_schedule(self, async_session):
        """Test creating publishing schedule"""
        schedule = await PublishingService.create_publishing_schedule(
            session=async_session,
            org_id=1,
            name="Daily Schedule",
            frequency="daily",
            time_of_day="09:00",
            default_channels=["website", "email"],
        )

        assert schedule.name == "Daily Schedule"
        assert schedule.frequency == "daily"
        assert schedule.is_template == True


class TestDistributionService:
    """Tests for Module 67: Distribution Service"""

    @pytest.mark.asyncio
    async def test_create_syndication_profile(self, async_session):
        """Test creating syndication profile"""
        profile = await DistributionService.create_syndication_profile(
            session=async_session,
            org_id=1,
            partner_name="News Agency",
            partner_type="news_agency",
            api_endpoint="https://api.newsagency.com",
            auto_syndicate=True,
        )

        assert profile.partner_name == "News Agency"
        assert profile.auto_syndicate == True
        assert profile.is_active == True

    @pytest.mark.asyncio
    async def test_syndicate_content(self, async_session):
        """Test content syndication logging"""
        await DistributionService.create_syndication_profile(
            session=async_session,
            org_id=1,
            partner_name="News Agency",
            partner_type="news_agency",
            api_endpoint="https://api.newsagency.com",
        )

        log = await DistributionService.syndicate_content(
            session=async_session,
            org_id=1,
            content_id=1,
            profile_id=1,
            syndication_url="https://newsagency.com/article",
        )

        assert log.syndicated_url == "https://newsagency.com/article"
        assert log.status == "success"

    @pytest.mark.asyncio
    async def test_track_syndication_performance(self, async_session):
        """Test tracking syndication performance"""
        await DistributionService.create_syndication_profile(
            session=async_session,
            org_id=1,
            partner_name="News Agency",
            partner_type="news_agency",
            api_endpoint="https://api.newsagency.com",
        )

        log = await DistributionService.syndicate_content(
            session=async_session,
            org_id=1,
            content_id=1,
            profile_id=1,
            syndication_url="https://newsagency.com/article",
        )

        updated_log = await DistributionService.track_syndication_performance(
            session=async_session,
            log_id=log.id,
            impressions=1000,
            clicks=50,
        )

        assert updated_log.impressions == 1000
        assert updated_log.engagement_rate == 0.05


class TestAnalyticsService:
    """Tests for Module 68: Analytics Service"""

    @pytest.mark.asyncio
    async def test_record_engagement(self, async_session):
        """Test recording engagement"""
        tracker = await AnalyticsService.record_engagement(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            action_type="view",
            device_type="mobile",
        )

        assert tracker.action_type == "view"
        assert tracker.device_type == "mobile"

    @pytest.mark.asyncio
    async def test_update_engagement_metrics(self, async_session):
        """Test updating engagement metrics"""
        metrics = await AnalyticsService.update_engagement_metrics(
            session=async_session,
            org_id=1,
            content_id=1,
            views=1000,
            clicks=100,
            shares=50,
            comments=25,
            reactions=200,
        )

        assert metrics.total_views == 1000
        assert metrics.total_clicks == 100
        assert metrics.engagement_score > 0

    @pytest.mark.asyncio
    async def test_calculate_engagement_score(self):
        """Test engagement score calculation"""
        score = AnalyticsService._calculate_engagement_score(
            views=1000,
            clicks=100,
            shares=50,
            comments=25,
            reactions=200,
        )

        assert 0 <= score <= 100
        assert score > 0

    @pytest.mark.asyncio
    async def test_create_performance_analytics(self, async_session):
        """Test creating performance analytics"""
        analytics = await AnalyticsService.create_performance_analytics(
            session=async_session,
            org_id=1,
            period_type="daily",
            total_content=50,
            avg_engagement=75.5,
            total_views=50000,
        )

        assert analytics.total_content_published == 50
        assert analytics.period_type == "daily"


class TestABTestingService:
    """Tests for Module 69: A/B Testing Service"""

    @pytest.mark.asyncio
    async def test_create_ab_test(self, async_session):
        """Test creating A/B test"""
        campaign = await ABTestingService.create_ab_test(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            name="Title Test",
            test_metric="clicks",
            hypothesis="Shorter titles get more clicks",
        )

        assert campaign.name == "Title Test"
        assert campaign.status == ABTestStatus.DRAFT
        assert campaign.test_metric == "clicks"

    @pytest.mark.asyncio
    async def test_create_test_variant(self, async_session):
        """Test creating test variant"""
        campaign = await ABTestingService.create_ab_test(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            name="Title Test",
            test_metric="clicks",
            hypothesis="Test",
        )

        variant_a = await ABTestingService.create_test_variant(
            session=async_session,
            campaign_id=campaign.id,
            variant_name="A",
            variant_type="control",
            title_variant="Original Title",
        )

        assert variant_a.variant_name == "A"
        assert variant_a.variant_type == "control"

    @pytest.mark.asyncio
    async def test_record_variant_performance(self, async_session):
        """Test recording variant performance"""
        campaign = await ABTestingService.create_ab_test(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            name="Title Test",
            test_metric="clicks",
            hypothesis="Test",
        )

        variant = await ABTestingService.create_test_variant(
            session=async_session,
            campaign_id=campaign.id,
            variant_name="A",
            variant_type="control",
        )

        updated = await ABTestingService.record_variant_performance(
            session=async_session,
            variant_id=variant.id,
            impressions=1000,
            clicks=100,
            conversions=10,
        )

        assert updated.impressions == 1000
        assert updated.ctr == 0.1
        assert updated.performance_score > 0

    @pytest.mark.asyncio
    async def test_chi_square_test(self):
        """Test chi-square calculation"""
        chi_square, p_value = ABTestingService._chi_square_test(
            conversions_a=10,
            clicks_a=100,
            conversions_b=15,
            clicks_b=100,
        )

        assert chi_square >= 0
        assert 0 <= p_value <= 1


class TestRecommendationService:
    """Tests for Module 70: Recommendation Service"""

    @pytest.mark.asyncio
    async def test_create_recommendation_engine(self, async_session):
        """Test creating recommendation engine"""
        engine = await RecommendationService.create_recommendation_engine(
            session=async_session,
            org_id=1,
            name="Collaborative Engine",
            recommendation_type=RecommendationType.COLLABORATIVE,
        )

        assert engine.name == "Collaborative Engine"
        assert engine.is_active == True

    @pytest.mark.asyncio
    async def test_record_user_preference(self, async_session):
        """Test recording user preference"""
        preference = await RecommendationService.record_user_preference(
            session=async_session,
            org_id=1,
            user_id=1,
            category=UserPreferenceCategory.TOPIC,
            value="technology",
            weight=1.5,
        )

        assert preference.preference_value == "technology"
        assert preference.preference_weight == 1.5

    @pytest.mark.asyncio
    async def test_score_content(self):
        """Test content scoring"""
        score = RecommendationService._score_content(1, [])

        assert 0 <= score <= 1
        assert score > 0  # Base score is 0.5

    @pytest.mark.asyncio
    async def test_generate_recommendations(self, async_session):
        """Test generating recommendations"""
        engine = await RecommendationService.create_recommendation_engine(
            session=async_session,
            org_id=1,
            name="Test Engine",
            recommendation_type=RecommendationType.HYBRID,
        )

        log = await RecommendationService.generate_recommendations(
            session=async_session,
            org_id=1,
            user_id=1,
            engine_id=engine.id,
            content_pool=[1, 2, 3, 4, 5],
            num_recommendations=3,
        )

        assert len(log.recommended_content_ids) <= 3
        assert len(log.recommendation_scores) == len(log.recommended_content_ids)

    @pytest.mark.asyncio
    async def test_record_recommendation_click(self, async_session):
        """Test recording recommendation click"""
        engine = await RecommendationService.create_recommendation_engine(
            session=async_session,
            org_id=1,
            name="Test Engine",
            recommendation_type=RecommendationType.HYBRID,
        )

        log = await RecommendationService.generate_recommendations(
            session=async_session,
            org_id=1,
            user_id=1,
            engine_id=engine.id,
            content_pool=[1, 2, 3],
            num_recommendations=3,
        )

        updated = await RecommendationService.record_recommendation_click(
            session=async_session,
            log_id=log.id,
            clicked_content_id=1,
        )

        assert updated.was_clicked == True
        assert updated.clicked_content_id == 1


class TestIntegrationScenarios:
    """Integration tests combining multiple modules"""

    @pytest.mark.asyncio
    async def test_full_publishing_workflow(self, async_session):
        """Test complete publishing workflow"""
        # 1. Create publishing job
        job = await PublishingService.create_publishing_job(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            title="New Article",
            scheduled_publish_time=datetime.now(timezone.utc),
            distribution_channels=["website", "email"],
        )

        # 2. Record engagement
        tracker = await AnalyticsService.record_engagement(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            action_type="view",
            device_type="desktop",
        )

        # 3. Update metrics
        metrics = await AnalyticsService.update_engagement_metrics(
            session=async_session,
            org_id=1,
            content_id=1,
            views=100,
            clicks=10,
            shares=5,
            comments=3,
            reactions=25,
        )

        assert job.status == PublishingStatus.SCHEDULED
        assert tracker.action_type == "view"
        assert metrics.engagement_score > 0

    @pytest.mark.asyncio
    async def test_ab_test_to_recommendation_workflow(self, async_session):
        """Test A/B testing leading to recommendations"""
        # 1. Create and run A/B test
        campaign = await ABTestingService.create_ab_test(
            session=async_session,
            org_id=1,
            content_id=1,
            user_id=1,
            name="Content Test",
            test_metric="engagement",
            hypothesis="Test hypothesis",
        )

        # 2. Create variants
        variant_a = await ABTestingService.create_test_variant(
            session=async_session,
            campaign_id=campaign.id,
            variant_name="A",
            variant_type="control",
        )

        variant_b = await ABTestingService.create_test_variant(
            session=async_session,
            campaign_id=campaign.id,
            variant_name="B",
            variant_type="treatment",
        )

        # 3. Record performance
        await ABTestingService.record_variant_performance(
            session=async_session,
            variant_id=variant_a.id,
            impressions=1000,
            clicks=80,
            conversions=8,
        )

        await ABTestingService.record_variant_performance(
            session=async_session,
            variant_id=variant_b.id,
            impressions=1000,
            clicks=120,
            conversions=15,
        )

        # 4. Analyze results
        result = await ABTestingService.analyze_test_results(
            session=async_session,
            campaign_id=campaign.id,
        )

        # 5. Use results for recommendations
        engine = await RecommendationService.create_recommendation_engine(
            session=async_session,
            org_id=1,
            name="Optimized Engine",
            recommendation_type=RecommendationType.CONTENT_BASED,
        )

        recommendations = await RecommendationService.generate_recommendations(
            session=async_session,
            org_id=1,
            user_id=1,
            engine_id=engine.id,
            content_pool=[1, 2, 3, 4, 5],
        )

        assert result.is_significant is not None
        assert len(recommendations.recommended_content_ids) > 0
