from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_, or_, desc
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import json
import hashlib
import math
from typing import List, Optional, Dict, Any
from scipy import stats
import numpy as np

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
    RecommendationType,
    RetentionStatus,
    ABTestStatus,
)


class AdvancedPersonalizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, user_id: int) -> AdvancedPersonalizationProfile:
        profile = AdvancedPersonalizationProfile(user_id=user_id)
        self.db.add(profile)
        await self.db.commit()
        return profile

    async def update_preferences(
        self,
        user_id: int,
        content_preferences: Dict[str, float],
        author_preferences: Dict[str, float],
        category_weights: Dict[str, float],
    ) -> Optional[AdvancedPersonalizationProfile]:
        result = await self.db.execute(
            select(AdvancedPersonalizationProfile).where(
                AdvancedPersonalizationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        if profile:
            profile.content_preferences = content_preferences
            profile.author_preferences = author_preferences
            profile.category_weights = category_weights
            profile.last_updated = datetime.utcnow()
            await self.db.commit()
        return profile

    async def update_reading_preference(
        self, user_id: int, preference: str
    ) -> Optional[AdvancedPersonalizationProfile]:
        result = await self.db.execute(
            select(AdvancedPersonalizationProfile).where(
                AdvancedPersonalizationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        if profile:
            profile.reading_time_preference = preference
            await self.db.commit()
        return profile

    async def update_topic_clusters(
        self, user_id: int, clusters: List[str]
    ) -> Optional[AdvancedPersonalizationProfile]:
        result = await self.db.execute(
            select(AdvancedPersonalizationProfile).where(
                AdvancedPersonalizationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        if profile:
            profile.topic_clusters = clusters
            await self.db.commit()
        return profile

    async def get_profile(self, user_id: int) -> Optional[AdvancedPersonalizationProfile]:
        result = await self.db.execute(
            select(AdvancedPersonalizationProfile).where(
                AdvancedPersonalizationProfile.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def calculate_personalization_score(
        self, user_id: int
    ) -> Optional[AdvancedPersonalizationProfile]:
        result = await self.db.execute(
            select(AdvancedPersonalizationProfile).where(
                AdvancedPersonalizationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        if profile:
            score = 0.0
            if profile.content_preferences:
                score += len(profile.content_preferences) * 0.1
            if profile.author_preferences:
                score += len(profile.author_preferences) * 0.15
            if profile.category_weights:
                score += len(profile.category_weights) * 0.2
            if profile.topic_clusters:
                score += len(profile.topic_clusters) * 0.25
            score = min(score, 1.0)
            profile.personalization_score = score
            await self.db.commit()
        return profile


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_recommendation(
        self,
        user_id: int,
        content_id: int,
        recommendation_type: RecommendationType,
        similarity_score: float,
        relevance_score: float,
        confidence: float = 0.0,
        rank: int = 0,
    ) -> ContentRecommendation:
        rec = ContentRecommendation(
            user_id=user_id,
            content_id=content_id,
            recommendation_type=recommendation_type,
            similarity_score=similarity_score,
            relevance_score=relevance_score,
            confidence=confidence,
            rank=rank,
        )
        self.db.add(rec)
        await self.db.commit()
        return rec

    async def get_recommendations(
        self, user_id: int, limit: int = 10
    ) -> List[ContentRecommendation]:
        result = await self.db.execute(
            select(ContentRecommendation)
            .where(ContentRecommendation.user_id == user_id)
            .order_by(desc(ContentRecommendation.relevance_score))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recommendations_by_type(
        self,
        user_id: int,
        recommendation_type: RecommendationType,
        limit: int = 10,
    ) -> List[ContentRecommendation]:
        result = await self.db.execute(
            select(ContentRecommendation)
            .where(
                and_(
                    ContentRecommendation.user_id == user_id,
                    ContentRecommendation.recommendation_type == recommendation_type,
                )
            )
            .order_by(desc(ContentRecommendation.relevance_score))
            .limit(limit)
        )
        return result.scalars().all()

    async def record_click(self, recommendation_id: int) -> Optional[ContentRecommendation]:
        result = await self.db.execute(
            select(ContentRecommendation).where(ContentRecommendation.id == recommendation_id)
        )
        rec = result.scalar_one_or_none()
        if rec:
            rec.clicked = True
            rec.click_timestamp = datetime.utcnow()
            await self.db.commit()
        return rec

    async def record_conversion(
        self, recommendation_id: int
    ) -> Optional[ContentRecommendation]:
        result = await self.db.execute(
            select(ContentRecommendation).where(ContentRecommendation.id == recommendation_id)
        )
        rec = result.scalar_one_or_none()
        if rec:
            rec.conversion = True
            await self.db.commit()
        return rec

    async def get_recommendation_effectiveness(self, user_id: int) -> Dict[str, Any]:
        result = await self.db.execute(
            select(ContentRecommendation).where(ContentRecommendation.user_id == user_id)
        )
        recommendations = result.scalars().all()

        if not recommendations:
            return {
                "total_recommendations": 0,
                "click_through_rate": 0.0,
                "conversion_rate": 0.0,
            }

        clicks = sum(1 for r in recommendations if r.clicked)
        conversions = sum(1 for r in recommendations if r.conversion)

        return {
            "total_recommendations": len(recommendations),
            "clicks": clicks,
            "conversions": conversions,
            "click_through_rate": clicks / len(recommendations),
            "conversion_rate": conversions / len(recommendations),
        }

    async def calculate_collaborative_filtering(self, user_id: int) -> List[int]:
        result = await self.db.execute(
            select(UserEmbedding).where(UserEmbedding.user_id == user_id)
        )
        user_embedding = result.scalar_one_or_none()
        if not user_embedding:
            return []

        all_embeddings = await self.db.execute(select(UserEmbedding))
        all_users = all_embeddings.scalars().all()

        similarities = []
        for other_user in all_users:
            if other_user.user_id != user_id:
                similarity = self._cosine_similarity(
                    user_embedding.behavior_embedding,
                    other_user.behavior_embedding,
                )
                similarities.append((other_user.user_id, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return [user_id for user_id, _ in similarities[:10]]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)


class RetentionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_retention_metric(self, user_id: int) -> RetentionMetric:
        metric = RetentionMetric(user_id=user_id)
        self.db.add(metric)
        await self.db.commit()
        return metric

    async def update_churn_probability(
        self, user_id: int, probability: float, engagement_trend: str = None
    ) -> Optional[RetentionMetric]:
        result = await self.db.execute(
            select(RetentionMetric).where(RetentionMetric.user_id == user_id)
        )
        metric = result.scalar_one_or_none()
        if metric:
            metric.churn_probability = probability
            if engagement_trend:
                metric.engagement_trend = engagement_trend
            metric.updated_at = datetime.utcnow()
            await self.db.commit()
        return metric

    async def get_at_risk_users(self, churn_threshold: float = 0.6) -> List[RetentionMetric]:
        result = await self.db.execute(
            select(RetentionMetric).where(
                RetentionMetric.churn_probability >= churn_threshold
            )
        )
        return result.scalars().all()

    async def update_retention_segment(
        self, user_id: int, segment: str, recommended_action: str = None
    ) -> Optional[RetentionMetric]:
        result = await self.db.execute(
            select(RetentionMetric).where(RetentionMetric.user_id == user_id)
        )
        metric = result.scalar_one_or_none()
        if metric:
            metric.retention_segment = segment
            if recommended_action:
                metric.recommended_action = recommended_action
            await self.db.commit()
        return metric

    async def create_campaign(
        self,
        name: str,
        description: str,
        target_segment: str,
        campaign_type: str,
        budget: float,
    ) -> RetentionCampaign:
        campaign = RetentionCampaign(
            name=name,
            description=description,
            target_segment=target_segment,
            campaign_type=campaign_type,
            budget=budget,
            status="draft",
        )
        self.db.add(campaign)
        await self.db.commit()
        return campaign

    async def get_campaign(self, campaign_id: int) -> Optional[RetentionCampaign]:
        result = await self.db.execute(
            select(RetentionCampaign).where(RetentionCampaign.id == campaign_id)
        )
        return result.scalar_one_or_none()

    async def update_campaign_metrics(
        self, campaign_id: int, sent_count: int = 0, converted_count: int = 0
    ) -> Optional[RetentionCampaign]:
        result = await self.db.execute(
            select(RetentionCampaign).where(RetentionCampaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        if campaign:
            campaign.sent_count += sent_count
            campaign.converted_count += converted_count
            if campaign.sent_count > 0:
                campaign.roi = (campaign.converted_count / campaign.sent_count) * 100
            await self.db.commit()
        return campaign

    async def get_campaigns(self, status: str = None) -> List[RetentionCampaign]:
        query = select(RetentionCampaign)
        if status:
            query = query.where(RetentionCampaign.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()


class ABTestingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_test(
        self,
        name: str,
        hypothesis: str,
        metric_to_optimize: str,
        variant_a_name: str = "Control",
        variant_b_name: str = "Treatment",
        traffic_allocation_a: int = 50,
        traffic_allocation_b: int = 50,
        sample_size: int = 1000,
    ) -> ABTest:
        test = ABTest(
            name=name,
            hypothesis=hypothesis,
            metric_to_optimize=metric_to_optimize,
            variant_a_name=variant_a_name,
            variant_b_name=variant_b_name,
            traffic_allocation_a=traffic_allocation_a,
            traffic_allocation_b=traffic_allocation_b,
            sample_size=sample_size,
        )
        self.db.add(test)
        await self.db.commit()
        return test

    async def get_test(self, test_id: int) -> Optional[ABTest]:
        result = await self.db.execute(
            select(ABTest).where(ABTest.id == test_id)
        )
        return result.scalar_one_or_none()

    async def start_test(self, test_id: int) -> Optional[ABTest]:
        result = await self.db.execute(
            select(ABTest).where(ABTest.id == test_id)
        )
        test = result.scalar_one_or_none()
        if test:
            test.status = ABTestStatus.RUNNING
            test.start_date = datetime.utcnow()
            await self.db.commit()
        return test

    async def end_test(self, test_id: int) -> Optional[ABTest]:
        result = await self.db.execute(
            select(ABTest).where(ABTest.id == test_id)
        )
        test = result.scalar_one_or_none()
        if test:
            test.status = ABTestStatus.COMPLETED
            test.end_date = datetime.utcnow()
            await self._calculate_statistical_significance(test)
            await self.db.commit()
        return test

    async def assign_user_to_variant(
        self, test_id: int, user_id: int
    ) -> Optional[ABTestVariant]:
        hash_input = f"{test_id}-{user_id}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)

        test_result = await self.db.execute(
            select(ABTest).where(ABTest.id == test_id)
        )
        test = test_result.scalar_one_or_none()
        if not test:
            return None

        allocation = hash_value % 100
        variant = (
            test.variant_a_name
            if allocation < test.traffic_allocation_a
            else test.variant_b_name
        )

        check_result = await self.db.execute(
            select(ABTestVariant).where(
                and_(ABTestVariant.ab_test_id == test_id, ABTestVariant.user_id == user_id)
            )
        )
        existing = check_result.scalar_one_or_none()
        if existing:
            return existing

        variant_obj = ABTestVariant(
            ab_test_id=test_id,
            user_id=user_id,
            variant=variant,
        )
        self.db.add(variant_obj)
        await self.db.commit()
        return variant_obj

    async def record_variant_conversion(
        self, variant_id: int, metric_value: float = 0.0
    ) -> Optional[ABTestVariant]:
        result = await self.db.execute(
            select(ABTestVariant).where(ABTestVariant.id == variant_id)
        )
        variant = result.scalar_one_or_none()
        if variant:
            variant.conversion = True
            variant.metric_value = metric_value
            await self.db.commit()
        return variant

    async def _calculate_statistical_significance(self, test: ABTest) -> None:
        variants_result = await self.db.execute(
            select(ABTestVariant).where(ABTestVariant.ab_test_id == test.id)
        )
        variants = variants_result.scalars().all()

        a_conversions = sum(
            1 for v in variants if v.variant == test.variant_a_name and v.conversion
        )
        b_conversions = sum(
            1 for v in variants if v.variant == test.variant_b_name and v.conversion
        )
        a_total = sum(1 for v in variants if v.variant == test.variant_a_name)
        b_total = sum(1 for v in variants if v.variant == test.variant_b_name)

        if a_total > 0 and b_total > 0:
            a_rate = a_conversions / a_total
            b_rate = b_conversions / b_total

            test.metric_a = a_rate
            test.metric_b = b_rate

            # Chi-square test
            contingency_table = [
                [a_conversions, a_total - a_conversions],
                [b_conversions, b_total - b_conversions],
            ]
            chi2 = (
                (a_conversions * (b_total - b_conversions) - b_conversions * (a_total - a_conversions)) ** 2
                * (a_total + b_total)
                / (a_total * b_total * (a_conversions + b_conversions) * (a_total + b_total - a_conversions - b_conversions))
            )
            p_value = 1 - stats.chi2.cdf(chi2, 1)
            confidence = (1 - p_value) * 100

            test.confidence = confidence
            if confidence >= 95:
                test.winner = (
                    test.variant_b_name if b_rate > a_rate else test.variant_a_name
                )


class InsightService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_insight(
        self,
        insight_type: str,
        title: str,
        description: str,
        data: Dict[str, Any],
        metric_name: str = None,
        metric_value: float = None,
        confidence_level: float = 0.0,
    ) -> AdvancedAnalyticsInsight:
        insight = AdvancedAnalyticsInsight(
            type=insight_type,
            title=title,
            description=description,
            data=data,
            metric_name=metric_name,
            metric_value=metric_value,
            confidence_level=confidence_level,
            actionable=confidence_level >= 0.75,
        )
        self.db.add(insight)
        await self.db.commit()
        return insight

    async def get_insights(self, limit: int = 10) -> List[AdvancedAnalyticsInsight]:
        result = await self.db.execute(
            select(AdvancedAnalyticsInsight)
            .order_by(desc(AdvancedAnalyticsInsight.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_actionable_insights(self, limit: int = 10) -> List[AdvancedAnalyticsInsight]:
        result = await self.db.execute(
            select(AdvancedAnalyticsInsight)
            .where(AdvancedAnalyticsInsight.actionable == True)
            .order_by(desc(AdvancedAnalyticsInsight.confidence_level))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_insights_by_type(
        self, insight_type: str, limit: int = 10
    ) -> List[AdvancedAnalyticsInsight]:
        result = await self.db.execute(
            select(AdvancedAnalyticsInsight)
            .where(AdvancedAnalyticsInsight.type == insight_type)
            .order_by(desc(AdvancedAnalyticsInsight.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def update_recommended_action(
        self, insight_id: int, action: str
    ) -> Optional[AdvancedAnalyticsInsight]:
        result = await self.db.execute(
            select(AdvancedAnalyticsInsight).where(AdvancedAnalyticsInsight.id == insight_id)
        )
        insight = result.scalar_one_or_none()
        if insight:
            insight.recommended_action = action
            await self.db.commit()
        return insight


class CohortService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cohort(
        self,
        name: str,
        cohort_type: str,
        criteria: Dict[str, Any],
        description: str = None,
    ) -> UserCohort:
        cohort = UserCohort(
            name=name,
            cohort_type=cohort_type,
            criteria=criteria,
            description=description,
            created_date=datetime.utcnow(),
        )
        self.db.add(cohort)
        await self.db.commit()
        return cohort

    async def get_cohort(self, cohort_id: int) -> Optional[UserCohort]:
        result = await self.db.execute(
            select(UserCohort).where(UserCohort.id == cohort_id)
        )
        return result.scalar_one_or_none()

    async def add_user_to_cohort(self, cohort_id: int, user_id: int) -> Optional[CohortMembership]:
        check_result = await self.db.execute(
            select(CohortMembership).where(
                and_(
                    CohortMembership.cohort_id == cohort_id,
                    CohortMembership.user_id == user_id,
                )
            )
        )
        existing = check_result.scalar_one_or_none()
        if existing:
            return existing

        membership = CohortMembership(cohort_id=cohort_id, user_id=user_id)
        self.db.add(membership)

        cohort = await self.get_cohort(cohort_id)
        if cohort:
            cohort.user_count += 1

        await self.db.commit()
        return membership

    async def get_cohort_members(self, cohort_id: int, limit: int = 100) -> List[int]:
        result = await self.db.execute(
            select(CohortMembership)
            .where(CohortMembership.cohort_id == cohort_id)
            .limit(limit)
        )
        memberships = result.scalars().all()
        return [m.user_id for m in memberships]

    async def get_user_cohorts(self, user_id: int) -> List[UserCohort]:
        result = await self.db.execute(
            select(UserCohort)
            .join(CohortMembership, UserCohort.id == CohortMembership.cohort_id)
            .where(CohortMembership.user_id == user_id)
        )
        return result.scalars().all()

    async def get_cohorts(self, cohort_type: str = None) -> List[UserCohort]:
        query = select(UserCohort)
        if cohort_type:
            query = query.where(UserCohort.cohort_type == cohort_type)
        result = await self.db.execute(query)
        return result.scalars().all()


class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_model(
        self,
        name: str,
        model_type: str,
        target_metric: str,
        features_used: List[str],
        training_data_size: int = 0,
    ) -> PredictionModel:
        model = PredictionModel(
            name=name,
            model_type=model_type,
            target_metric=target_metric,
            features_used=features_used,
            training_data_size=training_data_size,
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def get_model(self, model_id: int) -> Optional[PredictionModel]:
        result = await self.db.execute(
            select(PredictionModel).where(PredictionModel.id == model_id)
        )
        return result.scalar_one_or_none()

    async def deploy_model(self, model_id: int) -> Optional[PredictionModel]:
        result = await self.db.execute(
            select(PredictionModel).where(PredictionModel.id == model_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.deployed = True
            await self.db.commit()
        return model

    async def create_prediction(
        self,
        user_id: int,
        model_id: int,
        prediction_score: float,
        confidence: float = 0.0,
        predicted_behavior: str = None,
    ) -> UserPrediction:
        prediction = UserPrediction(
            user_id=user_id,
            model_id=model_id,
            prediction_score=prediction_score,
            confidence=confidence,
            predicted_behavior=predicted_behavior,
        )
        self.db.add(prediction)
        await self.db.commit()
        return prediction

    async def get_user_predictions(self, user_id: int, limit: int = 10) -> List[UserPrediction]:
        result = await self.db.execute(
            select(UserPrediction)
            .where(UserPrediction.user_id == user_id)
            .order_by(desc(UserPrediction.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def record_prediction_outcome(
        self, prediction_id: int, actual_behavior: str, correct: bool
    ) -> Optional[UserPrediction]:
        result = await self.db.execute(
            select(UserPrediction).where(UserPrediction.id == prediction_id)
        )
        prediction = result.scalar_one_or_none()
        if prediction:
            prediction.actual_behavior = actual_behavior
            prediction.correct = correct
            await self.db.commit()
        return prediction

    async def update_model_metrics(
        self,
        model_id: int,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: float,
        auc_score: float,
    ) -> Optional[PredictionModel]:
        result = await self.db.execute(
            select(PredictionModel).where(PredictionModel.id == model_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.accuracy = accuracy
            model.precision = precision
            model.recall = recall
            model.f1_score = f1_score
            model.auc_score = auc_score
            model.last_trained = datetime.utcnow()
            await self.db.commit()
        return model

    async def get_deployed_models(self) -> List[PredictionModel]:
        result = await self.db.execute(
            select(PredictionModel).where(PredictionModel.deployed == True)
        )
        return result.scalars().all()
