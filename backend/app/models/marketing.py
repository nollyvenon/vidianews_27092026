"""Marketing models for email campaigns, SMS, automation, social, analytics"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text,
    Enum as SQLEnum, Float, Index, Table, DECIMAL
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


# ============================================================================
# ENUMS
# ============================================================================

class CampaignStatus(str, enum.Enum):
    """Campaign status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    SENDING = "sending"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class EmailType(str, enum.Enum):
    """Email types"""
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"
    TRANSACTIONAL = "transactional"
    WELCOME = "welcome"
    ABANDONED_CART = "abandoned_cart"
    WIN_BACK = "win_back"


class SegmentationType(str, enum.Enum):
    """Segmentation types"""
    BEHAVIORAL = "behavioral"
    DEMOGRAPHIC = "demographic"
    GEOGRAPHIC = "geographic"
    PURCHASE_HISTORY = "purchase_history"
    ENGAGEMENT = "engagement"
    CUSTOM = "custom"


class LeadScoreStatus(str, enum.Enum):
    """Lead score status"""
    COLD = "cold"
    WARM = "warm"
    HOT = "hot"
    QUALIFIED = "qualified"


# ============================================================================
# MODULE 111-112: EMAIL CAMPAIGNS & AUTOMATION
# ============================================================================

class EmailCampaign(Base):
    """Email marketing campaigns"""
    __tablename__ = "email_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    # Campaign details
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    preview_text = Column(String(500))
    email_type = Column(SQLEnum(EmailType), nullable=False)

    # Content
    html_content = Column(Text, nullable=False)
    plain_text_content = Column(Text)

    # Targeting
    segment_id = Column(Integer, ForeignKey("segments.id"), index=True)
    recipient_count = Column(Integer, default=0)

    # Scheduling
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    scheduled_time = Column(DateTime(timezone=True))

    # Performance
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    bounced_count = Column(Integer, default=0)

    # Rates
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)

    # Metadata
    from_name = Column(String(255))
    from_email = Column(String(255), nullable=False)
    reply_to_email = Column(String(255))

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    sent_at = Column(DateTime(timezone=True))

    # Relationships
    template = relationship("EmailTemplate", uselist=False)
    metrics = relationship("EmailMetric", back_populates="campaign", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_campaign_org", "organization_id"),
        Index("idx_campaign_status", "status"),
        Index("idx_campaign_created", "created_at"),
    )


class EmailTemplate(Base):
    """Email templates"""
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id", ondelete="CASCADE"), unique=True, index=True)

    # Template details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    html_content = Column(Text, nullable=False)
    preview_image_url = Column(String(500))

    # Metadata
    is_reusable = Column(Boolean, default=False)
    category = Column(String(100))

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_email_template_org", "organization_id"),
    )


class AutomationWorkflow(Base):
    """Email automation workflows"""
    __tablename__ = "automation_workflows"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    # Workflow details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    trigger_event = Column(String(100), nullable=False)

    # Configuration
    workflow_config = Column(JSON)  # Steps, conditions, actions
    is_active = Column(Boolean, default=False, index=True)

    # Engagement
    contacts_enrolled = Column(Integer, default=0)
    contacts_completed = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_automation_org", "organization_id"),
        Index("idx_automation_active", "is_active"),
    )


# ============================================================================
# MODULE 113: SMS MARKETING
# ============================================================================

class SMSCampaign(Base):
    """SMS marketing campaigns"""
    __tablename__ = "sms_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    # Campaign details
    name = Column(String(255), nullable=False)
    message = Column(String(160), nullable=False)

    # Targeting
    segment_id = Column(Integer, ForeignKey("segments.id"), index=True)
    recipient_count = Column(Integer, default=0)

    # Scheduling
    status = Column(String(50), default="draft", index=True)
    scheduled_time = Column(DateTime(timezone=True))

    # Performance
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    sent_at = Column(DateTime(timezone=True))


# ============================================================================
# MODULE 114: CUSTOMER SEGMENTATION
# ============================================================================

class Segment(Base):
    """Customer segments"""
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    # Segment details
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    segmentation_type = Column(SQLEnum(SegmentationType), nullable=False)

    # Configuration
    segment_config = Column(JSON)  # Conditions for membership
    is_dynamic = Column(Boolean, default=True)

    # Membership
    contact_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    campaigns = relationship("EmailCampaign")

    __table_args__ = (
        Index("idx_segment_org", "organization_id"),
        Index("idx_segment_type", "segmentation_type"),
    )


class SegmentMembership(Base):
    """Segment membership"""
    __tablename__ = "segment_memberships"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("segments.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Membership details
    added_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_segment_membership_segment", "segment_id"),
        Index("idx_segment_membership_contact", "contact_id"),
    )


# ============================================================================
# MODULE 115: LEAD SCORING
# ============================================================================

class LeadScore(Base):
    """Lead scoring"""
    __tablename__ = "lead_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Scoring
    total_score = Column(Integer, default=0)
    engagement_score = Column(Integer, default=0)
    purchase_score = Column(Integer, default=0)
    behavior_score = Column(Integer, default=0)

    # Status
    status = Column(SQLEnum(LeadScoreStatus), default=LeadScoreStatus.COLD, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_lead_score_user", "user_id"),
        Index("idx_lead_score_status", "status"),
    )


# ============================================================================
# MODULE 120: MARKETING ANALYTICS
# ============================================================================

class EmailMetric(Base):
    """Email campaign metrics"""
    __tablename__ = "email_metrics"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id", ondelete="CASCADE"), nullable=False, index=True)

    # Metrics by time
    metric_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Engagement
    sends = Column(Integer, default=0)
    deliveries = Column(Integer, default=0)
    opens = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    bounces = Column(Integer, default=0)
    complaints = Column(Integer, default=0)

    # Rates
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)

    # Relationships
    campaign = relationship("EmailCampaign", back_populates="metrics")

    __table_args__ = (
        Index("idx_email_metric_campaign", "campaign_id"),
        Index("idx_email_metric_date", "metric_date"),
    )


# ============================================================================
# MODULE 121: A/B TESTING
# ============================================================================

class ABTest(Base):
    """A/B testing campaigns"""
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    # Test details
    name = Column(String(255), nullable=False)
    test_type = Column(String(50), nullable=False)  # subject, sender, content

    # Variants
    variant_a_id = Column(Integer, ForeignKey("email_campaigns.id"), nullable=False)
    variant_b_id = Column(Integer, ForeignKey("email_campaigns.id"), nullable=False)

    # Configuration
    split_ratio = Column(Float, default=0.5)
    test_duration = Column(Integer)  # hours

    # Results
    winner = Column(String(1))  # A or B
    winning_metric = Column(String(50))  # opens, clicks

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_ab_test_org", "organization_id"),
    )


# ============================================================================
# MODULE 123: LOYALTY PROGRAM
# ============================================================================

class LoyaltyProgram(Base):
    """Loyalty programs"""
    __tablename__ = "loyalty_programs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, unique=True, index=True)

    # Program details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="active", index=True)

    # Configuration
    points_per_dollar = Column(Float, default=1.0)
    redemption_rate = Column(Float)  # dollars per point
    tier_config = Column(JSON)  # Bronze, Silver, Gold, Platinum

    # Engagement
    total_members = Column(Integer, default=0)
    total_points_distributed = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    members = relationship("LoyaltyMember", back_populates="program", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_loyalty_program_org", "organization_id"),
    )


class LoyaltyMember(Base):
    """Loyalty program members"""
    __tablename__ = "loyalty_members"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("loyalty_programs.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Membership
    member_id = Column(String(50), unique=True, index=True)
    tier = Column(String(50), default="bronze")

    # Points
    total_points = Column(Integer, default=0)
    available_points = Column(Integer, default=0)
    redeemed_points = Column(Integer, default=0)

    # Engagement
    lifetime_purchases = Column(DECIMAL(12, 2), default=0)
    last_purchase_date = Column(DateTime(timezone=True))

    # Timestamps
    enrolled_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    program = relationship("LoyaltyProgram", back_populates="members")

    __table_args__ = (
        Index("idx_loyalty_member_program", "program_id"),
        Index("idx_loyalty_member_user", "user_id"),
    )


class LoyaltyTransaction(Base):
    """Loyalty points transactions"""
    __tablename__ = "loyalty_transactions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("loyalty_members.id", ondelete="CASCADE"), nullable=False, index=True)

    # Transaction details
    transaction_type = Column(String(50), nullable=False)  # earn, redeem
    points = Column(Integer, nullable=False)
    reason = Column(String(255))

    # Reference
    reference_type = Column(String(50))
    reference_id = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_loyalty_transaction_member", "member_id"),
        Index("idx_loyalty_transaction_type", "transaction_type"),
    )
