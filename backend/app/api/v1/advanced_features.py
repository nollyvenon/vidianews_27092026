from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.services.advanced_features_service import (
    AdvancedPersonalizationService,
    RecommendationService,
    RetentionService,
    ABTestingService,
    InsightService,
    CohortService,
    PredictionService,
)

router = APIRouter(prefix="/api/v1", tags=["advanced_features"])


# Pydantic schemas
class PersonalizationProfileRequest(BaseModel):
    content_preferences: Dict[str, float] = {}
    author_preferences: Dict[str, float] = {}
    category_weights: Dict[str, float] = {}
    reading_time_preference: Optional[str] = None


class RecommendationRequest(BaseModel):
    content_id: int
    recommendation_type: str
    similarity_score: float
    relevance_score: float
    confidence: Optional[float] = 0.0


class ContentRecommendationResponse(BaseModel):
    id: int
    user_id: int
    content_id: int
    recommendation_type: str
    similarity_score: float
    relevance_score: float
    clicked: bool
    conversion: bool


class RetentionCampaignRequest(BaseModel):
    name: str
    description: Optional[str] = None
    target_segment: str
    campaign_type: str
    budget: float


class ABTestRequest(BaseModel):
    name: str
    hypothesis: str
    metric_to_optimize: str
    variant_a_name: Optional[str] = "Control"
    variant_b_name: Optional[str] = "Treatment"
    traffic_allocation_a: Optional[int] = 50
    traffic_allocation_b: Optional[int] = 50
    sample_size: Optional[int] = 1000


class ABTestResponse(BaseModel):
    id: int
    name: str
    status: str
    metric_a: float
    metric_b: float
    confidence: float
    winner: Optional[str]


class InsightRequest(BaseModel):
    insight_type: str
    title: str
    description: str
    data: Dict[str, Any] = {}
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None


class UserCohortRequest(BaseModel):
    name: str
    cohort_type: str
    criteria: Dict[str, Any]
    description: Optional[str] = None


class PredictionModelRequest(BaseModel):
    name: str
    model_type: str
    target_metric: str
    features_used: List[str]
    training_data_size: Optional[int] = 0


# Personalization endpoints
@router.post("/personalization/profile/{user_id}", tags=["personalization"])
async def create_personalization_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    service = AdvancedPersonalizationService(db)
    profile = await service.create_profile(user_id)
    return {"id": profile.id, "user_id": user_id, "personalization_score": profile.personalization_score}


@router.put("/personalization/profile/{user_id}", tags=["personalization"])
async def update_personalization_preferences(
    user_id: int, request: PersonalizationProfileRequest, db: AsyncSession = Depends(get_db)
):
    service = AdvancedPersonalizationService(db)
    profile = await service.update_preferences(
        user_id, request.content_preferences, request.author_preferences, request.category_weights
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"id": profile.id, "user_id": user_id, "personalization_score": profile.personalization_score}


@router.get("/personalization/profile/{user_id}", tags=["personalization"])
async def get_personalization_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    service = AdvancedPersonalizationService(db)
    profile = await service.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "id": profile.id,
        "user_id": user_id,
        "content_preferences": profile.content_preferences,
        "author_preferences": profile.author_preferences,
        "category_weights": profile.category_weights,
        "personalization_score": profile.personalization_score,
    }


@router.post("/personalization/profile/{user_id}/calculate-score", tags=["personalization"])
async def calculate_personalization_score(user_id: int, db: AsyncSession = Depends(get_db)):
    service = AdvancedPersonalizationService(db)
    profile = await service.calculate_personalization_score(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"user_id": user_id, "personalization_score": profile.personalization_score}


# Recommendation endpoints
@router.post("/recommendations/{user_id}", tags=["recommendations"])
async def create_recommendation(
    user_id: int, request: RecommendationRequest, db: AsyncSession = Depends(get_db)
):
    service = RecommendationService(db)
    rec = await service.create_recommendation(
        user_id,
        request.content_id,
        request.recommendation_type,
        request.similarity_score,
        request.relevance_score,
        request.confidence,
    )
    return {"id": rec.id, "user_id": user_id, "content_id": rec.content_id}


@router.get("/recommendations/{user_id}", tags=["recommendations"])
async def get_recommendations(user_id: int, limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = RecommendationService(db)
    recs = await service.get_recommendations(user_id, limit)
    return [
        {
            "id": r.id,
            "content_id": r.content_id,
            "type": r.recommendation_type,
            "relevance_score": r.relevance_score,
            "clicked": r.clicked,
            "conversion": r.conversion,
        }
        for r in recs
    ]


@router.get("/recommendations/{user_id}/type/{rec_type}", tags=["recommendations"])
async def get_recommendations_by_type(
    user_id: int, rec_type: str, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    service = RecommendationService(db)
    recs = await service.get_recommendations_by_type(user_id, rec_type, limit)
    return [
        {
            "id": r.id,
            "content_id": r.content_id,
            "type": r.recommendation_type,
            "relevance_score": r.relevance_score,
        }
        for r in recs
    ]


@router.post("/recommendations/{recommendation_id}/click", tags=["recommendations"])
async def record_recommendation_click(recommendation_id: int, db: AsyncSession = Depends(get_db)):
    service = RecommendationService(db)
    rec = await service.record_click(recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"id": rec.id, "clicked": rec.clicked}


@router.get("/recommendations/{user_id}/effectiveness", tags=["recommendations"])
async def get_recommendation_effectiveness(user_id: int, db: AsyncSession = Depends(get_db)):
    service = RecommendationService(db)
    stats = await service.get_recommendation_effectiveness(user_id)
    return stats


# Retention endpoints
@router.post("/retention/metrics/{user_id}", tags=["retention"])
async def create_retention_metric(user_id: int, db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    metric = await service.create_retention_metric(user_id)
    return {"id": metric.id, "user_id": user_id, "status": metric.status}


@router.put("/retention/metrics/{user_id}/churn", tags=["retention"])
async def update_churn_probability(
    user_id: int, probability: float, db: AsyncSession = Depends(get_db)
):
    service = RetentionService(db)
    metric = await service.update_churn_probability(user_id, probability)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"user_id": user_id, "churn_probability": metric.churn_probability}


@router.get("/retention/at-risk", tags=["retention"])
async def get_at_risk_users(churn_threshold: float = 0.6, db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    users = await service.get_at_risk_users(churn_threshold)
    return [{"user_id": u.user_id, "churn_probability": u.churn_probability} for u in users]


@router.post("/retention/campaigns", tags=["retention"])
async def create_retention_campaign(request: RetentionCampaignRequest, db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    campaign = await service.create_campaign(
        request.name, request.description, request.target_segment, request.campaign_type, request.budget
    )
    return {"id": campaign.id, "name": campaign.name, "status": campaign.status}


@router.get("/retention/campaigns/{campaign_id}", tags=["retention"])
async def get_retention_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    campaign = await service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {
        "id": campaign.id,
        "name": campaign.name,
        "status": campaign.status,
        "sent_count": campaign.sent_count,
        "converted_count": campaign.converted_count,
        "roi": campaign.roi,
    }


@router.get("/retention/campaigns", tags=["retention"])
async def get_retention_campaigns(status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    campaigns = await service.get_campaigns(status)
    return [
        {"id": c.id, "name": c.name, "status": c.status, "roi": c.roi} for c in campaigns
    ]


# A/B Testing endpoints
@router.post("/ab-tests", tags=["ab_testing"])
async def create_ab_test(request: ABTestRequest, db: AsyncSession = Depends(get_db)):
    service = ABTestingService(db)
    test = await service.create_test(
        request.name,
        request.hypothesis,
        request.metric_to_optimize,
        request.variant_a_name,
        request.variant_b_name,
        request.traffic_allocation_a,
        request.traffic_allocation_b,
        request.sample_size,
    )
    return {"id": test.id, "name": test.name, "status": test.status}


@router.get("/ab-tests/{test_id}", tags=["ab_testing"])
async def get_ab_test(test_id: int, db: AsyncSession = Depends(get_db)):
    service = ABTestingService(db)
    test = await service.get_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return ABTestResponse(
        id=test.id,
        name=test.name,
        status=test.status,
        metric_a=test.metric_a,
        metric_b=test.metric_b,
        confidence=test.confidence,
        winner=test.winner,
    )


@router.post("/ab-tests/{test_id}/start", tags=["ab_testing"])
async def start_ab_test(test_id: int, db: AsyncSession = Depends(get_db)):
    service = ABTestingService(db)
    test = await service.start_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"id": test.id, "status": test.status}


@router.post("/ab-tests/{test_id}/end", tags=["ab_testing"])
async def end_ab_test(test_id: int, db: AsyncSession = Depends(get_db)):
    service = ABTestingService(db)
    test = await service.end_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return ABTestResponse(
        id=test.id,
        name=test.name,
        status=test.status,
        metric_a=test.metric_a,
        metric_b=test.metric_b,
        confidence=test.confidence,
        winner=test.winner,
    )


@router.post("/ab-tests/{test_id}/assign-user/{user_id}", tags=["ab_testing"])
async def assign_user_to_variant(test_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    service = ABTestingService(db)
    variant = await service.assign_user_to_variant(test_id, user_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"variant_id": variant.id, "variant": variant.variant}


# Insights endpoints
@router.post("/insights", tags=["insights"])
async def create_insight(request: InsightRequest, db: AsyncSession = Depends(get_db)):
    service = InsightService(db)
    insight = await service.create_insight(
        request.insight_type,
        request.title,
        request.description,
        request.data,
        request.metric_name,
        request.metric_value,
    )
    return {"id": insight.id, "type": insight.type, "actionable": insight.actionable}


@router.get("/insights", tags=["insights"])
async def get_insights(limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = InsightService(db)
    insights = await service.get_insights(limit)
    return [
        {"id": i.id, "type": i.type, "title": i.title, "confidence_level": i.confidence_level}
        for i in insights
    ]


@router.get("/insights/actionable", tags=["insights"])
async def get_actionable_insights(limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = InsightService(db)
    insights = await service.get_actionable_insights(limit)
    return [
        {"id": i.id, "type": i.type, "title": i.title, "recommended_action": i.recommended_action}
        for i in insights
    ]


@router.get("/insights/type/{insight_type}", tags=["insights"])
async def get_insights_by_type(insight_type: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = InsightService(db)
    insights = await service.get_insights_by_type(insight_type, limit)
    return [{"id": i.id, "title": i.title, "confidence_level": i.confidence_level} for i in insights]


# Cohort endpoints
@router.post("/cohorts", tags=["cohorts"])
async def create_cohort(request: UserCohortRequest, db: AsyncSession = Depends(get_db)):
    service = CohortService(db)
    cohort = await service.create_cohort(request.name, request.cohort_type, request.criteria, request.description)
    return {"id": cohort.id, "name": cohort.name, "user_count": cohort.user_count}


@router.get("/cohorts/{cohort_id}", tags=["cohorts"])
async def get_cohort(cohort_id: int, db: AsyncSession = Depends(get_db)):
    service = CohortService(db)
    cohort = await service.get_cohort(cohort_id)
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return {"id": cohort.id, "name": cohort.name, "cohort_type": cohort.cohort_type, "user_count": cohort.user_count}


@router.post("/cohorts/{cohort_id}/add-user/{user_id}", tags=["cohorts"])
async def add_user_to_cohort(cohort_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    service = CohortService(db)
    membership = await service.add_user_to_cohort(cohort_id, user_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return {"cohort_id": cohort_id, "user_id": user_id}


@router.get("/cohorts/{cohort_id}/members", tags=["cohorts"])
async def get_cohort_members(cohort_id: int, limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = CohortService(db)
    members = await service.get_cohort_members(cohort_id, limit)
    return {"cohort_id": cohort_id, "member_count": len(members), "members": members}


@router.get("/cohorts", tags=["cohorts"])
async def get_cohorts(cohort_type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    service = CohortService(db)
    cohorts = await service.get_cohorts(cohort_type)
    return [{"id": c.id, "name": c.name, "user_count": c.user_count} for c in cohorts]


# Prediction endpoints
@router.post("/predictions/models", tags=["predictions"])
async def create_prediction_model(request: PredictionModelRequest, db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    model = await service.create_model(
        request.name, request.model_type, request.target_metric, request.features_used, request.training_data_size
    )
    return {"id": model.id, "name": model.name, "deployed": model.deployed}


@router.get("/predictions/models/{model_id}", tags=["predictions"])
async def get_prediction_model(model_id: int, db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return {
        "id": model.id,
        "name": model.name,
        "accuracy": model.accuracy,
        "precision": model.precision,
        "recall": model.recall,
        "f1_score": model.f1_score,
        "auc_score": model.auc_score,
        "deployed": model.deployed,
    }


@router.post("/predictions/models/{model_id}/deploy", tags=["predictions"])
async def deploy_prediction_model(model_id: int, db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    model = await service.deploy_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"id": model.id, "deployed": model.deployed}


@router.post("/predictions/user/{user_id}", tags=["predictions"])
async def create_user_prediction(
    user_id: int, model_id: int, prediction_score: float, db: AsyncSession = Depends(get_db)
):
    service = PredictionService(db)
    prediction = await service.create_prediction(user_id, model_id, prediction_score)
    return {"id": prediction.id, "prediction_score": prediction.prediction_score}


@router.get("/predictions/user/{user_id}", tags=["predictions"])
async def get_user_predictions(user_id: int, limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    predictions = await service.get_user_predictions(user_id, limit)
    return [{"id": p.id, "prediction_score": p.prediction_score, "confidence": p.confidence} for p in predictions]


@router.get("/predictions/models/deployed", tags=["predictions"])
async def get_deployed_models(db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    models = await service.get_deployed_models()
    return [{"id": m.id, "name": m.name, "model_type": m.model_type} for m in models]
