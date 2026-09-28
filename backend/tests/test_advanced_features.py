import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.advanced_features import (
    AdvancedPersonalizationProfile,
    ContentEmbedding,
    UserEmbedding,
    ContentRecommendation,
    CollaborativeFilteringModel,
    RetentionMetric,
    RetentionCampaign,
    ABTest,
    ABTestVariant,
    AdvancedAnalyticsInsight,
    UserCohort,
    CohortMembership,
    PredictionModel,
    UserPrediction,
    Base,
    RecommendationType,
    RetentionStatus,
    ABTestStatus,
)
from app.services.advanced_features_service import (
    AdvancedPersonalizationService,
    RecommendationService,
    RetentionService,
    ABTestingService,
    InsightService,
    CohortService,
    PredictionService,
)


@pytest.fixture
async def db():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class TestAdvancedPersonalizationService:
    async def test_create_profile(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        assert profile.user_id == 1
        assert profile.personalization_score == 0.0

    async def test_update_preferences(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        
        updated = await service.update_preferences(
            1,
            {"tech": 0.8, "news": 0.6},
            {"author1": 0.9},
            {"science": 0.7}
        )
        assert updated is not None
        assert updated.content_preferences["tech"] == 0.8
        assert updated.author_preferences["author1"] == 0.9

    async def test_update_reading_preference(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        
        updated = await service.update_reading_preference(1, "short")
        assert updated.reading_time_preference == "short"

    async def test_update_topic_clusters(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        
        clusters = ["cluster1", "cluster2", "cluster3"]
        updated = await service.update_topic_clusters(1, clusters)
        assert updated.topic_clusters == clusters

    async def test_get_profile(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        
        retrieved = await service.get_profile(1)
        assert retrieved.user_id == 1

    async def test_get_nonexistent_profile(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.get_profile(999)
        assert profile is None

    async def test_calculate_personalization_score(self, db):
        service = AdvancedPersonalizationService(db)
        profile = await service.create_profile(1)
        
        await service.update_preferences(
            1,
            {"t1": 0.5, "t2": 0.6},
            {"a1": 0.7},
            {"c1": 0.8, "c2": 0.9}
        )
        await service.update_topic_clusters(1, ["cl1", "cl2"])
        
        result = await service.calculate_personalization_score(1)
        assert result.personalization_score > 0
        assert result.personalization_score <= 1.0


class TestRecommendationService:
    async def test_create_recommendation(self, db):
        service = RecommendationService(db)
        rec = await service.create_recommendation(
            1, 100, RecommendationType.COLLABORATIVE, 0.85, 0.90, 0.95
        )
        assert rec.user_id == 1
        assert rec.content_id == 100
        assert rec.recommendation_type == RecommendationType.COLLABORATIVE

    async def test_get_recommendations(self, db):
        service = RecommendationService(db)
        
        for i in range(5):
            await service.create_recommendation(
                1, 100 + i, RecommendationType.COLLABORATIVE, 0.8, 0.9 - i * 0.1
            )
        
        recs = await service.get_recommendations(1, limit=3)
        assert len(recs) == 3
        assert recs[0].relevance_score >= recs[1].relevance_score

    async def test_get_recommendations_by_type(self, db):
        service = RecommendationService(db)
        
        await service.create_recommendation(1, 100, RecommendationType.COLLABORATIVE, 0.8, 0.9)
        await service.create_recommendation(1, 101, RecommendationType.CONTENT_BASED, 0.7, 0.85)
        
        collab = await service.get_recommendations_by_type(1, RecommendationType.COLLABORATIVE)
        assert len(collab) == 1
        assert collab[0].recommendation_type == RecommendationType.COLLABORATIVE

    async def test_record_click(self, db):
        service = RecommendationService(db)
        rec = await service.create_recommendation(1, 100, RecommendationType.COLLABORATIVE, 0.8, 0.9)
        
        clicked = await service.record_click(rec.id)
        assert clicked.clicked == True
        assert clicked.click_timestamp is not None

    async def test_record_conversion(self, db):
        service = RecommendationService(db)
        rec = await service.create_recommendation(1, 100, RecommendationType.COLLABORATIVE, 0.8, 0.9)
        
        converted = await service.record_conversion(rec.id)
        assert converted.conversion == True

    async def test_get_recommendation_effectiveness(self, db):
        service = RecommendationService(db)
        
        rec1 = await service.create_recommendation(1, 100, RecommendationType.COLLABORATIVE, 0.8, 0.9)
        rec2 = await service.create_recommendation(1, 101, RecommendationType.CONTENT_BASED, 0.7, 0.85)
        
        await service.record_click(rec1.id)
        await service.record_conversion(rec2.id)
        
        effectiveness = await service.get_recommendation_effectiveness(1)
        assert effectiveness["total_recommendations"] == 2
        assert effectiveness["click_through_rate"] > 0

    async def test_calculate_collaborative_filtering(self, db):
        service = RecommendationService(db)
        
        user_emb = UserEmbedding(user_id=1, behavior_embedding=[0.1, 0.2, 0.3], interest_embedding=[0.4, 0.5, 0.6])
        other_emb = UserEmbedding(user_id=2, behavior_embedding=[0.1, 0.2, 0.25], interest_embedding=[0.4, 0.5, 0.6])
        
        db.add(user_emb)
        db.add(other_emb)
        await db.commit()
        
        similar = await service.calculate_collaborative_filtering(1)
        assert 2 in similar


class TestRetentionService:
    async def test_create_retention_metric(self, db):
        service = RetentionService(db)
        metric = await service.create_retention_metric(1)
        assert metric.user_id == 1
        assert metric.churn_probability == 0.0

    async def test_update_churn_probability(self, db):
        service = RetentionService(db)
        metric = await service.create_retention_metric(1)
        
        updated = await service.update_churn_probability(1, 0.75)
        assert updated.churn_probability == 0.75

    async def test_get_at_risk_users(self, db):
        service = RetentionService(db)
        
        await service.create_retention_metric(1)
        await service.create_retention_metric(2)
        
        await service.update_churn_probability(1, 0.8)
        await service.update_churn_probability(2, 0.3)
        
        at_risk = await service.get_at_risk_users(0.6)
        assert len(at_risk) == 1
        assert at_risk[0].user_id == 1

    async def test_create_campaign(self, db):
        service = RetentionService(db)
        campaign = await service.create_campaign(
            "Summer Campaign", "Special offers", "at_risk", "discount", 1000.0
        )
        assert campaign.name == "Summer Campaign"
        assert campaign.status == "draft"

    async def test_update_campaign_metrics(self, db):
        service = RetentionService(db)
        campaign = await service.create_campaign(
            "Summer Campaign", "Special offers", "at_risk", "discount", 1000.0
        )
        
        updated = await service.update_campaign_metrics(campaign.id, sent_count=100, converted_count=25)
        assert updated.sent_count == 100
        assert updated.converted_count == 25
        assert updated.roi > 0

    async def test_get_campaigns(self, db):
        service = RetentionService(db)
        
        c1 = await service.create_campaign("Camp1", "Desc", "active", "email", 500.0)
        c2 = await service.create_campaign("Camp2", "Desc", "at_risk", "sms", 1000.0)
        
        campaigns = await service.get_campaigns()
        assert len(campaigns) == 2


class TestABTestingService:
    async def test_create_test(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate",
            "Current Design",
            "New Design"
        )
        assert test.name == "Homepage Test"
        assert test.status == ABTestStatus.DRAFT

    async def test_start_test(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate"
        )
        
        started = await service.start_test(test.id)
        assert started.status == ABTestStatus.RUNNING
        assert started.start_date is not None

    async def test_assign_user_to_variant(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate"
        )
        await service.start_test(test.id)
        
        variant = await service.assign_user_to_variant(test.id, 1)
        assert variant.user_id == 1
        assert variant.variant in [test.variant_a_name, test.variant_b_name]

    async def test_consistent_user_assignment(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate"
        )
        
        v1 = await service.assign_user_to_variant(test.id, 1)
        v2 = await service.assign_user_to_variant(test.id, 1)
        assert v1.variant == v2.variant

    async def test_record_variant_conversion(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate"
        )
        
        variant = await service.assign_user_to_variant(test.id, 1)
        converted = await service.record_variant_conversion(variant.id, 0.95)
        assert converted.conversion == True
        assert converted.metric_value == 0.95

    async def test_end_test_calculates_significance(self, db):
        service = ABTestingService(db)
        test = await service.create_test(
            "Homepage Test",
            "New header design increases CTR",
            "click_through_rate",
            sample_size=100
        )
        await service.start_test(test.id)
        
        for i in range(50):
            variant = await service.assign_user_to_variant(test.id, 100 + i)
            if i < 30:
                await service.record_variant_conversion(variant.id, 0.9)
        
        ended = await service.end_test(test.id)
        assert ended.status == ABTestStatus.COMPLETED


class TestInsightService:
    async def test_create_insight(self, db):
        service = InsightService(db)
        insight = await service.create_insight(
            "trend", "Increasing engagement", "User engagement is up 15%",
            {"metric": "engagement_score", "value": 15}
        )
        assert insight.type == "trend"
        assert insight.actionable == False

    async def test_create_actionable_insight(self, db):
        service = InsightService(db)
        insight = await service.create_insight(
            "anomaly", "Unusual traffic pattern",
            "Traffic spike detected in region X",
            {"region": "X"},
            confidence_level=0.85
        )
        assert insight.actionable == True

    async def test_get_insights(self, db):
        service = InsightService(db)
        
        for i in range(5):
            await service.create_insight(
                "trend", f"Insight {i}", f"Description {i}", {}
            )
        
        insights = await service.get_insights(limit=3)
        assert len(insights) == 3

    async def test_get_actionable_insights(self, db):
        service = InsightService(db)
        
        await service.create_insight("trend", "Low confidence", "Desc", {}, confidence_level=0.5)
        await service.create_insight("anomaly", "High confidence", "Desc", {}, confidence_level=0.9)
        
        actionable = await service.get_actionable_insights()
        assert len(actionable) == 1

    async def test_get_insights_by_type(self, db):
        service = InsightService(db)
        
        await service.create_insight("trend", "Trend 1", "Desc", {})
        await service.create_insight("anomaly", "Anomaly 1", "Desc", {})
        
        trends = await service.get_insights_by_type("trend")
        assert len(trends) == 1


class TestCohortService:
    async def test_create_cohort(self, db):
        service = CohortService(db)
        cohort = await service.create_cohort(
            "High Value Users", "behavioral",
            {"min_purchases": 5, "min_lifetime_value": 1000}
        )
        assert cohort.name == "High Value Users"
        assert cohort.user_count == 0

    async def test_add_user_to_cohort(self, db):
        service = CohortService(db)
        cohort = await service.create_cohort(
            "High Value Users", "behavioral", {}
        )
        
        membership = await service.add_user_to_cohort(cohort.id, 1)
        assert membership.user_id == 1

    async def test_prevent_duplicate_cohort_membership(self, db):
        service = CohortService(db)
        cohort = await service.create_cohort("High Value Users", "behavioral", {})
        
        m1 = await service.add_user_to_cohort(cohort.id, 1)
        m2 = await service.add_user_to_cohort(cohort.id, 1)
        assert m1.id == m2.id

    async def test_get_cohort_members(self, db):
        service = CohortService(db)
        cohort = await service.create_cohort("High Value Users", "behavioral", {})
        
        for i in range(5):
            await service.add_user_to_cohort(cohort.id, 1 + i)
        
        members = await service.get_cohort_members(cohort.id)
        assert len(members) == 5

    async def test_get_user_cohorts(self, db):
        service = CohortService(db)
        
        c1 = await service.create_cohort("Cohort1", "behavioral", {})
        c2 = await service.create_cohort("Cohort2", "demographic", {})
        
        await service.add_user_to_cohort(c1.id, 1)
        await service.add_user_to_cohort(c2.id, 1)
        
        cohorts = await service.get_user_cohorts(1)
        assert len(cohorts) == 2

    async def test_get_cohorts(self, db):
        service = CohortService(db)
        
        await service.create_cohort("Cohort1", "behavioral", {})
        await service.create_cohort("Cohort2", "demographic", {})
        
        cohorts = await service.get_cohorts()
        assert len(cohorts) == 2


class TestPredictionService:
    async def test_create_model(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability",
            ["session_count", "last_login_days", "purchase_amount"]
        )
        assert model.name == "Churn Prediction"
        assert model.deployed == False

    async def test_deploy_model(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability", []
        )
        
        deployed = await service.deploy_model(model.id)
        assert deployed.deployed == True

    async def test_create_prediction(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability", []
        )
        
        prediction = await service.create_prediction(1, model.id, 0.75, 0.9)
        assert prediction.user_id == 1
        assert prediction.prediction_score == 0.75

    async def test_get_user_predictions(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability", []
        )
        
        for i in range(5):
            await service.create_prediction(1, model.id, 0.5 + i * 0.1)
        
        predictions = await service.get_user_predictions(1, limit=3)
        assert len(predictions) == 3

    async def test_record_prediction_outcome(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability", []
        )
        
        prediction = await service.create_prediction(1, model.id, 0.8)
        outcome = await service.record_prediction_outcome(prediction.id, "churned", True)
        
        assert outcome.actual_behavior == "churned"
        assert outcome.correct == True

    async def test_update_model_metrics(self, db):
        service = PredictionService(db)
        model = await service.create_model(
            "Churn Prediction", "xgboost", "churn_probability", []
        )
        
        updated = await service.update_model_metrics(
            model.id, 0.92, 0.89, 0.91, 0.90, 0.94
        )
        assert updated.accuracy == 0.92
        assert updated.auc_score == 0.94

    async def test_get_deployed_models(self, db):
        service = PredictionService(db)
        
        m1 = await service.create_model("Model1", "xgboost", "target", [])
        m2 = await service.create_model("Model2", "xgboost", "target", [])
        
        await service.deploy_model(m1.id)
        
        deployed = await service.get_deployed_models()
        assert len(deployed) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
