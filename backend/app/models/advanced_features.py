from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class RecommendationType(str, enum.Enum):
    COLLABORATIVE = "collaborative"
    CONTENT_BASED = "content_based"
    HYBRID = "hybrid"
    TRENDING = "trending"
    PERSONALIZED = "personalized"


class RetentionStatus(str, enum.Enum):
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"
    RECOVERED = "recovered"
    VIP = "vip"


class ABTestStatus(str, enum.Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class AdvancedPersonalizationProfile(Base):
    __tablename__ = "advanced_personalization_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    content_preferences = Column(JSON, default={})
    author_preferences = Column(JSON, default={})
    category_weights = Column(JSON, default={})
    reading_time_preference = Column(String(50))
    engagement_pattern = Column(JSON, default={})
    topic_clusters = Column(ARRAY(String), default=[])
    semantic_interests = Column(ARRAY(String), default=[])
    personalization_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_personalization_score", "personalization_score"),
    )


class ContentEmbedding(Base):
    __tablename__ = "content_embeddings"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False, unique=True)
    embedding_vector = Column(ARRAY(Float), nullable=False)
    embedding_model = Column(String(100), default="bert-base")
    content_type = Column(String(50), nullable=False)
    category = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_content_id", "content_id"),
        Index("idx_embedding_model", "embedding_model"),
    )


class UserEmbedding(Base):
    __tablename__ = "user_embeddings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    behavior_embedding = Column(ARRAY(Float), nullable=False)
    interest_embedding = Column(ARRAY(Float), nullable=False)
    embedding_model = Column(String(100), default="bert-base")
    embedding_version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_embedding_version", "embedding_version"),
    )


class ContentRecommendation(Base):
    __tablename__ = "content_recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content_id = Column(Integer, nullable=False)
    recommendation_type = Column(Enum(RecommendationType), nullable=False)
    similarity_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    confidence = Column(Float, default=0.0)
    rank = Column(Integer, default=0)
    clicked = Column(Boolean, default=False)
    conversion = Column(Boolean, default=False)
    click_timestamp = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_content_id", "content_id"),
        Index("idx_recommendation_type", "recommendation_type"),
        Index("idx_similarity_score", "similarity_score"),
        UniqueConstraint("user_id", "content_id", "recommendation_type", name="uq_recommendation"),
    )


class CollaborativeFilteringModel(Base):
    __tablename__ = "collaborative_filtering_models"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    similar_users = Column(JSON, default={})
    user_similarity_scores = Column(JSON, default={})
    shared_interests = Column(ARRAY(String), default=[])
    model_version = Column(Integer, default=1)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_model_version", "model_version"),
    )


class RetentionMetric(Base):
    __tablename__ = "retention_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Enum(RetentionStatus), default=RetentionStatus.ACTIVE)
    churn_probability = Column(Float, default=0.0)
    days_since_active = Column(Integer, default=0)
    engagement_trend = Column(String(50))
    retention_segment = Column(String(100))
    recommended_action = Column(String(255))
    last_engagement = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_status", "status"),
        Index("idx_churn_probability", "churn_probability"),
    )


class RetentionCampaign(Base):
    __tablename__ = "retention_campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="draft")
    target_segment = Column(String(100), nullable=False)
    campaign_type = Column(String(50))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Numeric(10, 2), default=0.0)
    sent_count = Column(Integer, default=0)
    converted_count = Column(Integer, default=0)
    roi = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_status", "status"),
        Index("idx_target_segment", "target_segment"),
    )


class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    status = Column(Enum(ABTestStatus), default=ABTestStatus.DRAFT)
    hypothesis = Column(Text)
    metric_to_optimize = Column(String(100), nullable=False)
    variant_a_name = Column(String(100), default="Control")
    variant_b_name = Column(String(100), default="Treatment")
    traffic_allocation_a = Column(Integer, default=50)
    traffic_allocation_b = Column(Integer, default=50)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    sample_size = Column(Integer, default=0)
    metric_a = Column(Float, default=0.0)
    metric_b = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    winner = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_status", "status"),
        Index("idx_name", "name"),
    )


class ABTestVariant(Base):
    __tablename__ = "ab_test_variants"

    id = Column(Integer, primary_key=True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    variant = Column(String(50), nullable=False)
    conversion = Column(Boolean, default=False)
    metric_value = Column(Float, default=0.0)
    session_duration = Column(Integer, default=0)
    assigned_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_ab_test_id", "ab_test_id"),
        Index("idx_user_id", "user_id"),
        Index("idx_variant", "variant"),
    )


class AdvancedAnalyticsInsight(Base):
    __tablename__ = "advanced_analytics_insights"

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    data = Column(JSON, default={})
    metric_name = Column(String(100))
    metric_value = Column(Float)
    trend = Column(String(50))
    confidence_level = Column(Float, default=0.0)
    actionable = Column(Boolean, default=False)
    recommended_action = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_type", "type"),
        Index("idx_metric_name", "metric_name"),
        Index("idx_created_at", "created_at"),
    )


class UserCohort(Base):
    __tablename__ = "user_cohorts"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    cohort_type = Column(String(50), nullable=False)
    criteria = Column(JSON, default={})
    user_count = Column(Integer, default=0)
    created_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_cohort_type", "cohort_type"),
    )


class CohortMembership(Base):
    __tablename__ = "cohort_memberships"

    id = Column(Integer, primary_key=True)
    cohort_id = Column(Integer, ForeignKey("user_cohorts.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    joined_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("cohort_id", "user_id", name="uq_cohort_user"),
        Index("idx_cohort_id", "cohort_id"),
        Index("idx_user_id", "user_id"),
    )


class PredictionModel(Base):
    __tablename__ = "prediction_models"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    model_type = Column(String(50), nullable=False)
    target_metric = Column(String(100), nullable=False)
    version = Column(Integer, default=1)
    accuracy = Column(Float, default=0.0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    auc_score = Column(Float, default=0.0)
    features_used = Column(ARRAY(String), default=[])
    training_data_size = Column(Integer, default=0)
    last_trained = Column(DateTime)
    deployed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_model_type", "model_type"),
        Index("idx_deployed", "deployed"),
    )


class UserPrediction(Base):
    __tablename__ = "user_predictions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=False)
    prediction_score = Column(Float, nullable=False)
    confidence = Column(Float, default=0.0)
    predicted_behavior = Column(String(255))
    actual_behavior = Column(String(255))
    correct = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_model_id", "model_id"),
        Index("idx_prediction_score", "prediction_score"),
    )
