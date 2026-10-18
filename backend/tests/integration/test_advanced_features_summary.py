"""Route tests for the advanced features summary: recommendation performance, retention, personalization, predictions and performance"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models.advanced_features import (
    AdvancedPersonalizationProfile, ContentRecommendation, PredictionModel, RecommendationType, UserPrediction,
)
from app.models.advanced_platform import APIUsageMetrics
from app.models.user_management import SubscriberProfile


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


def _seed(engine):
    with Session(engine) as session:
        session.add_all([
            ContentRecommendation(user_id=1, content_id=1, recommendation_type=RecommendationType.COLLABORATIVE,
                                  similarity_score=0.8, relevance_score=0.7, clicked=True, conversion=False),
            ContentRecommendation(user_id=2, content_id=1, recommendation_type=RecommendationType.COLLABORATIVE,
                                  similarity_score=0.6, relevance_score=0.5, clicked=False, conversion=False),
            ContentRecommendation(user_id=1, content_id=1, recommendation_type=RecommendationType.CONTENT_BASED,
                                  similarity_score=0.9, relevance_score=0.9, clicked=True, conversion=True),
            ContentRecommendation(user_id=2, content_id=1, recommendation_type=RecommendationType.HYBRID,
                                  similarity_score=0.4, relevance_score=0.4, clicked=False, conversion=False),
            AdvancedPersonalizationProfile(user_id=1, personalization_score=0.5),
            AdvancedPersonalizationProfile(user_id=2, personalization_score=0.9),
            SubscriberProfile(user_id=101, churn_risk_score=0.9),
            SubscriberProfile(user_id=102, churn_risk_score=0.2),
            APIUsageMetrics(endpoint="/a", method="GET", call_count=10, error_count=0, average_response_time_ms=20.0),
            APIUsageMetrics(endpoint="/b", method="POST", call_count=30, error_count=1, average_response_time_ms=40.0),
        ])
        session.flush()
        deployed = PredictionModel(name="Churn", model_type="classification", target_metric="churn", accuracy=0.9, deployed=True)
        candidate = PredictionModel(name="Draft", model_type="classification", target_metric="clicks", accuracy=0.5, deployed=False)
        session.add_all([deployed, candidate])
        session.flush()
        session.add(UserPrediction(user_id=1, model_id=deployed.id, prediction_score=0.7, created_at=datetime.utcnow()))
        session.commit()


class TestAdvancedSummary:
    async def test_the_summary_aggregates_every_section_from_the_recorded_data(self, async_client, org_member, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/advanced/summary", headers=org_member)

        assert response.status_code == 200
        body = response.json()

        recommendations = body["recommendations"]
        assert recommendations["total"] == 4
        assert recommendations["click_through_rate"] == 50.0
        assert recommendations["conversion_rate"] == 25.0
        by_type = {row["type"]: row for row in recommendations["by_type"]}
        assert by_type["collaborative"]["count"] == 2
        assert by_type["collaborative"]["click_through_rate"] == 50.0
        assert by_type["content_based"]["click_through_rate"] == 100.0
        assert by_type["content_based"]["conversion_rate"] == 100.0
        assert by_type["hybrid"]["conversion_rate"] == 0.0

        assert body["retention"] == {"subscribers": 2, "at_risk": 1, "average_churn_risk": 0.55}
        assert body["personalization"] == {"profiles": 2, "average_score": 0.7}
        assert body["predictions"] == {"deployed_models": 1, "average_accuracy": 0.9, "predictions_this_month": 1}
        assert body["performance"] == {"measured_endpoints": 2, "total_calls": 40, "average_response_time_ms": 35.0}

    async def test_an_empty_platform_reports_zeros(self, async_client, org_member):
        response = await async_client.get("/api/v1/advanced/summary", headers=org_member)

        assert response.status_code == 200
        body = response.json()
        assert body["recommendations"] == {"total": 0, "click_through_rate": 0.0, "conversion_rate": 0.0, "by_type": []}
        assert body["performance"]["average_response_time_ms"] == 0.0
        assert body["predictions"]["average_accuracy"] == 0.0

    async def test_the_summary_requires_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/advanced/summary")

        assert response.status_code in (401, 403)
