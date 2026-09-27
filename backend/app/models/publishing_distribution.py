"""Publishing, Distribution & Optimization Models: Modules 66-70"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


# ==================== ENUMS ====================

class PublishingStatus(str, enum.Enum):
    """Publishing status"""
    SCHEDULED = "scheduled"
    QUEUED = "queued"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DistributionChannel(str, enum.Enum):
    """Distribution channels"""
    WEBSITE = "website"
    EMAIL = "email"
    SOCIAL_TWITTER = "social_twitter"
    SOCIAL_FACEBOOK = "social_facebook"
    SOCIAL_LINKEDIN = "social_linkedin"
    SOCIAL_INSTAGRAM = "social_instagram"
    RSS = "rss"
    PUSH_NOTIFICATION = "push_notification"
    WEBHOOKS = "webhooks"


class ABTestStatus(str, enum.Enum):
    """A/B test status"""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RecommendationType(str, enum.Enum):
    """Recommendation types"""
    COLLABORATIVE = "collaborative"
    CONTENT_BASED = "content_based"
    HYBRID = "hybrid"
    TRENDING = "trending"
    PERSONALIZED = "personalized"


class UserPreferenceCategory(str, enum.Enum):
    """User preference categories"""
    TOPIC = "topic"
    AUTHOR = "author"
    CONTENT_TYPE = "content_type"
    PUBLICATION_FREQUENCY = "publication_frequency"
    ENGAGEMENT_LEVEL = "engagement_level"


# ==================== MODULE 66: CONTENT PUBLISHING & SCHEDULING ====================

class PublishingJob(Base):
    """Content publishing jobs with scheduling and distribution"""
    __tablename__ = "publishing_jobs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    status = Column(SQLEnum(PublishingStatus), default=PublishingStatus.SCHEDULED, index=True)

    # Publishing details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    scheduled_publish_time = Column(DateTime(timezone=True), nullable=False, index=True)
    actual_publish_time = Column(DateTime(timezone=True))

    # Distribution settings
    distribution_channels = Column(JSON, default=[])
    target_audience_segments = Column(JSON, default=[])
    priority = Column(Integer, default=5)

    # Publishing options
    auto_promote = Column(Boolean, default=False)
    schedule_reruns = Column(Boolean, default=False)
    rerun_schedule = Column(JSON)

    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    error_message = Column(Text)

    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_publishing_job_org", "organization_id"),
        Index("idx_publishing_job_content", "content_id"),
        Index("idx_publishing_job_status", "status"),
        Index("idx_publishing_job_scheduled", "scheduled_publish_time"),
    )


class PublishingSchedule(Base):
    """Publishing schedule templates and recurring patterns"""
    __tablename__ = "publishing_schedules"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Recurrence pattern
    frequency = Column(String(50), nullable=False)  # daily, weekly, monthly
    day_of_week = Column(String(20))  # Monday-Sunday
    time_of_day = Column(String(10))  # HH:MM format
    timezone = Column(String(50), default="UTC")

    # Distribution settings
    default_channels = Column(JSON, default=[])
    default_audience_segments = Column(JSON, default=[])

    # Settings
    is_active = Column(Boolean, default=True)
    is_template = Column(Boolean, default=False)
    max_scheduled_ahead = Column(Integer, default=30)  # days

    # Statistics
    total_publishes = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_publishing_schedule_org", "organization_id"),
        Index("idx_publishing_schedule_active", "is_active"),
    )


class PublishingLog(Base):
    """Publishing event logs for auditing and analytics"""
    __tablename__ = "publishing_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    publishing_job_id = Column(Integer, ForeignKey("publishing_jobs.id", ondelete="SET NULL"), nullable=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="SET NULL"), nullable=True)

    event_type = Column(String(50), nullable=False, index=True)  # published, scheduled, failed, etc.
    status = Column(String(50), nullable=False)

    # Publishing details
    published_url = Column(String(2048))
    publishing_duration_ms = Column(Integer)

    # Distribution info
    channels_used = Column(JSON, default=[])
    audience_reached = Column(Integer, default=0)

    # Error handling
    error_code = Column(String(100))
    error_message = Column(Text)

    # Metadata
    metadata = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_publishing_log_org", "organization_id"),
        Index("idx_publishing_log_job", "publishing_job_id"),
        Index("idx_publishing_log_event", "event_type"),
    )


# ==================== MODULE 67: DISTRIBUTION & SYNDICATION ====================

class SyndicationProfile(Base):
    """Syndication partner profiles and settings"""
    __tablename__ = "syndication_profiles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    partner_name = Column(String(255), nullable=False)
    partner_type = Column(String(100), nullable=False)  # news_agency, platform, blog_network

    # API Configuration
    api_endpoint = Column(String(2048))
    api_key = Column(String(500))
    auth_type = Column(String(50))  # api_key, oauth2, basic

    # Syndication settings
    auto_syndicate = Column(Boolean, default=False)
    content_categories = Column(JSON, default=[])
    content_types = Column(JSON, default=[])
    min_quality_score = Column(Float, default=0.7)

    # Reach & impact
    estimated_reach = Column(Integer, default=0)
    avg_syndication_rate = Column(Float, default=0.0)

    # Status
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime(timezone=True))
    total_articles_syndicated = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_syndication_profile_org", "organization_id"),
        Index("idx_syndication_profile_active", "is_active"),
    )


class DistributionChannel(Base):
    """Distribution channels configuration and management"""
    __tablename__ = "distribution_channels"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    channel_type = Column(SQLEnum(DistributionChannel), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)

    # Configuration
    api_credentials = Column(JSON, default={})
    settings = Column(JSON, default={})

    # Performance metrics
    message_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_delivery_time_ms = Column(Integer, default=0)

    # Status & scheduling
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=5)
    rate_limit = Column(Integer)  # messages per hour

    # Metadata
    tags = Column(JSON, default=[])
    last_used = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_distribution_channel_org", "organization_id"),
        Index("idx_distribution_channel_type", "channel_type"),
        Index("idx_distribution_channel_active", "is_active"),
    )


class SyndicationLog(Base):
    """Syndication activity logs"""
    __tablename__ = "syndication_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    syndication_profile_id = Column(Integer, ForeignKey("syndication_profiles.id", ondelete="SET NULL"), nullable=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="SET NULL"), nullable=True)

    status = Column(String(50), nullable=False, index=True)  # success, failed, pending
    syndicated_url = Column(String(2048))

    # Performance data
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)

    # Error handling
    error_message = Column(Text)

    # Metadata
    metadata = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_syndication_log_org", "organization_id"),
        Index("idx_syndication_log_profile", "syndication_profile_id"),
        Index("idx_syndication_log_status", "status"),
    )


# ==================== MODULE 68: PERFORMANCE ANALYTICS & ENGAGEMENT ====================

class EngagementMetric(Base):
    """Real-time engagement metrics for published content"""
    __tablename__ = "engagement_metrics"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)

    # View metrics
    total_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    avg_time_on_page = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)

    # Interaction metrics
    total_clicks = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_reactions = Column(Integer, default=0)

    # Conversion metrics
    conversion_count = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)

    # Engagement score
    engagement_score = Column(Float, default=0.0)
    engagement_trend = Column(String(20))  # increasing, stable, decreasing

    # Demographics
    top_demographics = Column(JSON, default=[])
    top_referrers = Column(JSON, default=[])

    # Time period
    metric_date = Column(DateTime(timezone=True), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_engagement_metric_org", "organization_id"),
        Index("idx_engagement_metric_content", "content_id"),
        Index("idx_engagement_metric_date", "metric_date"),
    )


class PerformanceAnalytics(Base):
    """Aggregated performance analytics and trends"""
    __tablename__ = "performance_analytics"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # Aggregated metrics
    total_content_published = Column(Integer, default=0)
    avg_engagement_score = Column(Float, default=0.0)
    total_views_all_content = Column(Integer, default=0)
    total_unique_visitors = Column(Integer, default=0)

    # Performance indicators
    top_performing_content = Column(JSON, default=[])
    low_performing_content = Column(JSON, default=[])
    trending_topics = Column(JSON, default=[])
    audience_growth_rate = Column(Float, default=0.0)

    # Insights
    key_insights = Column(JSON, default=[])
    recommendations = Column(JSON, default=[])

    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    period_type = Column(String(20))  # daily, weekly, monthly

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_performance_analytics_org", "organization_id"),
        Index("idx_performance_analytics_period", "period_start", "period_end"),
    )


class EngagementTracker(Base):
    """User engagement tracking and interaction logs"""
    __tablename__ = "engagement_trackers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Engagement actions
    action_type = Column(String(50), nullable=False, index=True)  # view, click, share, comment, reaction
    action_count = Column(Integer, default=1)

    # Device & source info
    device_type = Column(String(50))  # desktop, mobile, tablet
    referrer_url = Column(String(2048))
    user_agent = Column(String(500))

    # Session info
    session_duration_seconds = Column(Integer)
    is_returning_user = Column(Boolean, default=False)

    # Location
    country = Column(String(100))
    city = Column(String(100))

    # Metadata
    metadata = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_engagement_tracker_org", "organization_id"),
        Index("idx_engagement_tracker_content", "content_id"),
        Index("idx_engagement_tracker_action", "action_type"),
        Index("idx_engagement_tracker_user", "user_id"),
    )


# ==================== MODULE 69: A/B TESTING & OPTIMIZATION ====================

class ABTestCampaign(Base):
    """A/B testing campaigns for content optimization"""
    __tablename__ = "ab_test_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    status = Column(SQLEnum(ABTestStatus), default=ABTestStatus.DRAFT, index=True)

    # Test parameters
    test_metric = Column(String(100), nullable=False)  # engagement, clicks, conversion, dwell_time
    hypothesis = Column(Text)

    # Sample size
    sample_size_percent = Column(Float, default=50.0)
    minimum_sample_size = Column(Integer, default=100)

    # Duration
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    expected_duration_days = Column(Integer, default=14)

    # Results
    winner = Column(String(10))  # A, B, or null if inconclusive
    confidence_level = Column(Float)  # 0.90, 0.95, 0.99
    is_statistically_significant = Column(Boolean, default=False)

    # Metadata
    tags = Column(JSON, default=[])
    notes = Column(Text)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_ab_test_campaign_org", "organization_id"),
        Index("idx_ab_test_campaign_content", "content_id"),
        Index("idx_ab_test_campaign_status", "status"),
    )


class ABTestVariant(Base):
    """A/B test variants (control and treatment groups)"""
    __tablename__ = "ab_test_variants"

    id = Column(Integer, primary_key=True, index=True)
    ab_test_campaign_id = Column(Integer, ForeignKey("ab_test_campaigns.id", ondelete="CASCADE"), nullable=False, index=True)

    variant_name = Column(String(100), nullable=False)  # A, B, etc.
    variant_type = Column(String(50), nullable=False)  # control or treatment

    # Content variations
    title_variant = Column(String(500))
    description_variant = Column(Text)
    thumbnail_variant = Column(String(2048))
    headline_variant = Column(String(500))
    cta_text_variant = Column(String(255))

    # Statistics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)

    # Calculated metrics
    ctr = Column(Float, default=0.0)  # Click-through rate
    conversion_rate = Column(Float, default=0.0)
    avg_engagement_time = Column(Float, default=0.0)

    # Performance
    performance_score = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_ab_test_variant_campaign", "ab_test_campaign_id"),
    )


class ABTestResult(Base):
    """A/B test results and analysis"""
    __tablename__ = "ab_test_results"

    id = Column(Integer, primary_key=True, index=True)
    ab_test_campaign_id = Column(Integer, ForeignKey("ab_test_campaigns.id", ondelete="CASCADE"), nullable=False, index=True)

    # Statistical analysis
    chi_square_statistic = Column(Float)
    p_value = Column(Float)
    effect_size = Column(Float)

    # Comparison
    variant_a_metric_value = Column(Float)
    variant_b_metric_value = Column(Float)
    improvement_percent = Column(Float)

    # Conclusion
    is_significant = Column(Boolean, default=False)
    recommended_action = Column(String(100))  # deploy_a, deploy_b, continue_testing, inconclusive
    explanation = Column(Text)

    # Metadata
    analyzed_at = Column(DateTime(timezone=True), nullable=False)
    analyzed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_ab_test_result_campaign", "ab_test_campaign_id"),
    )


# ==================== MODULE 70: CONTENT RECOMMENDATIONS ====================

class RecommendationEngine(Base):
    """Recommendation engine configuration and settings"""
    __tablename__ = "recommendation_engines"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Algorithm configuration
    recommendation_type = Column(SQLEnum(RecommendationType), nullable=False)

    # Weighting
    collaborative_weight = Column(Float, default=0.4)
    content_weight = Column(Float, default=0.3)
    trending_weight = Column(Float, default=0.2)
    personalization_weight = Column(Float, default=0.1)

    # Parameters
    num_recommendations = Column(Integer, default=5)
    min_confidence_score = Column(Float, default=0.5)
    diversity_factor = Column(Float, default=0.3)  # favor diverse recommendations
    freshness_weight = Column(Float, default=0.2)

    # Performance
    avg_relevance_score = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)

    # Status
    is_active = Column(Boolean, default=True)
    last_trained = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_recommendation_engine_org", "organization_id"),
    )


class UserPreference(Base):
    """User content preferences and interests"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Preference type and value
    preference_category = Column(SQLEnum(UserPreferenceCategory), nullable=False, index=True)
    preference_value = Column(String(255), nullable=False)

    # Scoring
    preference_weight = Column(Float, default=1.0)  # 0.0-2.0
    confidence_score = Column(Float, default=0.5)

    # Engagement history
    total_interactions = Column(Integer, default=0)
    positive_interactions = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True)
    last_interacted_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_user_preference_org", "organization_id"),
        Index("idx_user_preference_user", "user_id"),
        Index("idx_user_preference_category", "preference_category"),
    )


class RecommendationLog(Base):
    """Recommendation delivery and performance logs"""
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_engine_id = Column(Integer, ForeignKey("recommendation_engines.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Recommended content
    recommended_content_ids = Column(JSON, default=[])
    recommendation_scores = Column(JSON, default=[])

    # Performance tracking
    was_clicked = Column(Boolean, default=False)
    clicked_content_id = Column(Integer, ForeignKey("contents.id", ondelete="SET NULL"), nullable=True)

    # User interaction
    interaction_type = Column(String(50))  # view, click, share, save, dismiss
    time_to_interaction = Column(Integer)  # seconds

    # Context
    recommendation_context = Column(String(100))  # email, website, app, push
    device_type = Column(String(50))

    # Quality metrics
    relevance_rating = Column(Integer)  # 1-5 star rating from user
    was_helpful = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_recommendation_log_org", "organization_id"),
        Index("idx_recommendation_log_engine", "recommendation_engine_id"),
        Index("idx_recommendation_log_user", "user_id"),
        Index("idx_recommendation_log_clicked", "was_clicked"),
    )
