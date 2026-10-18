from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey,
    Enum, UniqueConstraint, Index, JSON, ARRAY, func, Numeric, DECIMAL
)
from sqlalchemy.orm import relationship, synonym
from datetime import datetime
import enum

from app.db.base import Base


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
        Index("idx_user_id_user_embeddings", "user_id"),
        Index("idx_embedding_version", "embedding_version"),
    )


class ContentRecommendation(Base):
    __tablename__ = "content_recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content_id = Column(Integer, nullable=False)
    recommendation_type = Column(Enum(RecommendationType, name="advanced_features_recommendation_type"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    confidence = Column(Float, default=0.0)
    rank = Column(Integer, default=0)
    clicked = Column(Boolean, default=False)
    conversion = Column(Boolean, default=False)
    click_timestamp = Column(DateTime)
    reason = Column(Text, nullable=True)  # Why this item was recommended, shown to the user
    created_at = Column(DateTime, server_default=func.now())
    score = synonym("relevance_score")

    __table_args__ = (
        Index("idx_user_id_content_recommendations", "user_id"),
        Index("idx_content_id_content_recommendations", "content_id"),
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
        Index("idx_user_id_collaborative_filtering_models", "user_id"),
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
        Index("idx_user_id_retention_metrics", "user_id"),
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
        Index("idx_status_retention_campaigns", "status"),
        Index("idx_target_segment", "target_segment"),
    )


class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    status = Column(Enum(ABTestStatus, name="advanced_features_a_b_test_status"), default=ABTestStatus.DRAFT)
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
        Index("idx_status_ab_tests", "status"),
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
        Index("idx_user_id_ab_test_variants", "user_id"),
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
        Index("idx_name_user_cohorts", "name"),
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
        Index("idx_user_id_cohort_memberships", "user_id"),
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
        Index("idx_name_prediction_models", "name"),
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
        Index("idx_user_id_user_predictions", "user_id"),
        Index("idx_model_id", "model_id"),
        Index("idx_prediction_score", "prediction_score"),
    )


# ==================== SHARING, STORAGE, MEDIA & ENGAGEMENT ====================


class PermissionLevel(str, enum.Enum):
    NONE = "none"
    READ = "read"
    COMMENT = "comment"
    EDIT = "edit"
    ADMIN = "admin"


class ShareLink(Base):
    """Shareable access link for a content resource"""
    __tablename__ = "share_links"

    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    token = Column(String(64), unique=True, nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_level = Column(Enum(PermissionLevel, native_enum=False, length=20), nullable=False, default=PermissionLevel.READ)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    access_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StorageProvider(str, enum.Enum):
    LOCAL = "local"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"


class StorageFile(Base):
    """A stored file owned by a user"""
    __tablename__ = "storage_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(1000), nullable=False)
    storage_provider = Column(Enum(StorageProvider, native_enum=False, length=20), nullable=False, default=StorageProvider.LOCAL)
    mime_type = Column(String(255), nullable=True)
    size_bytes = Column(Integer, nullable=False, default=0)
    checksum_sha256 = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True, index=True)


class CDNUrl(Base):
    """Signed CDN URL for a stored file"""
    __tablename__ = "cdn_urls"

    id = Column(Integer, primary_key=True, index=True)
    storage_file_id = Column(Integer, ForeignKey("storage_files.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    region = Column(String(50), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class VideoQualityLevel(str, enum.Enum):
    Q_480P = "480p"
    Q_720P = "720p"
    Q_1080P = "1080p"
    Q_2160P = "2160p"


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoProcess(Base):
    """Transcoding job for one quality level of a video"""
    __tablename__ = "video_processes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    quality = Column(Enum(VideoQualityLevel, native_enum=False, length=20), nullable=False)
    status = Column(Enum(ProcessingStatus, native_enum=False, length=20), nullable=False, default=ProcessingStatus.PENDING)
    output_url = Column(String(1000), nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Thumbnail(Base):
    """Thumbnail image generated for a video"""
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Comment(Base):
    """Threaded comment on a content item"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, index=True)
    body = Column(Text, nullable=False)
    is_edited = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ReactionType(str, enum.Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


class Reaction(Base):
    """One reaction per user per content item"""
    __tablename__ = "reactions"
    __table_args__ = (UniqueConstraint("user_id", "content_id", name="uq_reactions_user_content"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    reaction_type = Column(Enum(ReactionType, native_enum=False, length=20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CommentReaction(Base):
    """One reaction per user per comment"""
    __tablename__ = "comment_reactions"
    __table_args__ = (UniqueConstraint("comment_id", "user_id", name="uq_comment_reactions_comment_user"),)

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reaction_type = Column(Enum(ReactionType, native_enum=False, length=20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
