"""Content Quality Models: Modules 61-65"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class CalendarEventType(str, enum.Enum):
    """Content calendar event types"""
    SCHEDULED_POST = "scheduled_post"
    DRAFT_REMINDER = "draft_reminder"
    PUBLICATION_DUE = "publication_due"
    REVIEW_DEADLINE = "review_deadline"
    OPTIMIZATION_WINDOW = "optimization_window"


class ProofreadingIssueType(str, enum.Enum):
    """Types of proofreading issues"""
    GRAMMAR = "grammar"
    SPELLING = "spelling"
    PUNCTUATION = "punctuation"
    STYLE = "style"
    TONE = "tone"
    CLARITY = "clarity"
    CONSISTENCY = "consistency"


class IssueSeverity(str, enum.Enum):
    """Issue severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ReadabilityMetricType(str, enum.Enum):
    """Types of readability metrics"""
    FLESCH_KINCAID = "flesch_kincaid"
    FLESCH_READING_EASE = "flesch_reading_ease"
    GUNNING_FOG = "gunning_fog"
    SMOG_INDEX = "smog_index"
    DALE_CHALL = "dale_chall"
    AUTOMATED_READABILITY = "automated_readability"


class PlagiarismCheckStatus(str, enum.Enum):
    """Plagiarism check status"""
    PENDING = "pending"
    CHECKING = "checking"
    COMPLETED = "completed"
    FAILED = "failed"


class BrandVoiceCheckResult(str, enum.Enum):
    """Brand voice check result"""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NEEDS_REVIEW = "needs_review"


# ==================== MODULE 61: CONTENT CALENDAR INTEGRATION ====================

class ContentCalendarEvent(Base):
    """Content calendar events with AI scheduling recommendations"""
    __tablename__ = "content_calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    event_type = Column(SQLEnum(CalendarEventType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    scheduled_for = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes = Column(Integer, default=60)

    # AI Recommendations
    ai_recommended_time = Column(DateTime(timezone=True))
    ai_confidence_score = Column(Float, default=0.0)
    ai_reasoning = Column(Text)
    audience_segment = Column(String(255))
    expected_engagement = Column(Float)

    # Status and metadata
    is_tentative = Column(Boolean, default=False)
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_calendar_org", "organization_id"),
        Index("idx_calendar_content", "content_id"),
        Index("idx_calendar_scheduled", "scheduled_for"),
        Index("idx_calendar_type", "event_type"),
    )

    organization = relationship("Organization", backref="calendar_events")
    content = relationship("Content", backref="calendar_events")
    creator = relationship("User", backref="calendar_events")


class ContentCalendarRecommendation(Base):
    """AI-powered content scheduling recommendations"""
    __tablename__ = "calendar_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)

    # Time recommendations
    optimal_publish_time = Column(DateTime(timezone=True))
    confidence_score = Column(Float, default=0.0)  # 0-1
    predicted_reach = Column(Integer, default=0)
    predicted_engagement = Column(Integer, default=0)

    # Reasoning
    basis = Column(JSON, default={})  # {historical_data, audience_timezone, trending_topics, etc}
    alternative_times = Column(JSON, default=[])  # Array of alternative times with scores

    accepted = Column(Boolean, default=False)
    accepted_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_rec_org", "organization_id"),
        Index("idx_rec_content", "content_id"),
        Index("idx_rec_confidence", "confidence_score"),
    )

    organization = relationship("Organization", backref="calendar_recommendations")
    content = relationship("Content", backref="calendar_recommendations")


# ==================== MODULE 62: AI PROOFREADING ====================

class ProofreadingCheck(Base):
    """AI proofreading results"""
    __tablename__ = "proofreading_checks"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # Text analysis
    original_text = Column(Text, nullable=False)
    total_word_count = Column(Integer, default=0)

    # Issue counts
    grammar_issues = Column(Integer, default=0)
    spelling_issues = Column(Integer, default=0)
    punctuation_issues = Column(Integer, default=0)
    style_issues = Column(Integer, default=0)
    tone_issues = Column(Integer, default=0)
    clarity_issues = Column(Integer, default=0)
    consistency_issues = Column(Integer, default=0)
    total_issues = Column(Integer, default=0)

    # Scoring
    quality_score = Column(Float, default=0.0)  # 0-100
    overall_rating = Column(String(20))  # Excellent, Good, Fair, Poor

    # Configuration
    check_grammar = Column(Boolean, default=True)
    check_spelling = Column(Boolean, default=True)
    check_punctuation = Column(Boolean, default=True)
    check_style = Column(Boolean, default=True)
    check_tone = Column(Boolean, default=True)
    check_clarity = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_proofread_content", "content_id"),
        Index("idx_proofread_org", "organization_id"),
        Index("idx_proofread_score", "quality_score"),
    )

    content = relationship("Content", backref="proofreading_checks")
    organization = relationship("Organization", backref="proofreading_checks")
    issues = relationship("ProofreadingIssue", back_populates="check", cascade="all, delete-orphan")


class ProofreadingIssue(Base):
    """Individual proofreading issues"""
    __tablename__ = "proofreading_issues"

    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(Integer, ForeignKey("proofreading_checks.id", ondelete="CASCADE"), nullable=False, index=True)

    issue_type = Column(SQLEnum(ProofreadingIssueType), nullable=False, index=True)
    severity = Column(SQLEnum(IssueSeverity), nullable=False, index=True)

    position = Column(Integer)  # Character position in text
    length = Column(Integer)
    text = Column(String(500))
    suggestion = Column(String(500))
    explanation = Column(Text)

    is_ignored = Column(Boolean, default=False)
    is_fixed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_issue_check", "check_id"),
        Index("idx_issue_type", "issue_type"),
        Index("idx_issue_severity", "severity"),
    )

    check = relationship("ProofreadingCheck", back_populates="issues")


# ==================== MODULE 63: PLAGIARISM DETECTION ====================

class PlagiarismCheck(Base):
    """Plagiarism detection results"""
    __tablename__ = "plagiarism_checks"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # Analysis
    text_analyzed = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)

    # Results
    similarity_percentage = Column(Float, default=0.0)  # 0-100
    originality_percentage = Column(Float, default=0.0)  # 0-100
    status = Column(SQLEnum(PlagiarismCheckStatus), default=PlagiarismCheckStatus.PENDING, index=True)

    # Detailed findings
    total_sources_found = Column(Integer, default=0)
    ai_content_percentage = Column(Float, default=0.0)
    human_content_percentage = Column(Float, default=0.0)

    # Scoring
    plagiarism_risk = Column(String(50))  # Low, Medium, High, Critical
    confidence_score = Column(Float, default=0.0)  # 0-1

    # Source data
    detected_sources = Column(JSON, default=[])  # Array of {url, title, similarity_percent, matched_text}
    ai_source_data = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    check_completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_plagiarism_content", "content_id"),
        Index("idx_plagiarism_org", "organization_id"),
        Index("idx_plagiarism_status", "status"),
        Index("idx_plagiarism_similarity", "similarity_percentage"),
    )

    content = relationship("Content", backref="plagiarism_checks")
    organization = relationship("Organization", backref="plagiarism_checks")


# ==================== MODULE 64: CONTENT READABILITY ====================

class ReadabilityScore(Base):
    """Content readability analysis"""
    __tablename__ = "readability_scores"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # Text analysis
    text_analyzed = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    sentence_count = Column(Integer, default=0)
    paragraph_count = Column(Integer, default=0)

    # Readability metrics
    flesch_kincaid_grade = Column(Float, default=0.0)
    flesch_reading_ease = Column(Float, default=0.0)  # 0-100, higher = easier
    gunning_fog_index = Column(Float, default=0.0)
    smog_index = Column(Float, default=0.0)
    dale_chall_score = Column(Float, default=0.0)
    automated_readability_index = Column(Float, default=0.0)

    # Derived readability level
    target_audience_grade_level = Column(String(50))  # e.g., "8-9 grade level"
    readability_level = Column(String(50))  # Easy, Moderate, Difficult, Very Difficult
    avg_word_length = Column(Float, default=0.0)
    avg_sentence_length = Column(Float, default=0.0)

    # Recommendations
    complexity_score = Column(Float, default=0.0)  # 0-100, 100 = very complex
    recommendations = Column(JSON, default=[])  # Array of improvement suggestions

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_readability_content", "content_id"),
        Index("idx_readability_org", "organization_id"),
        Index("idx_readability_level", "readability_level"),
        Index("idx_flesch_ease", "flesch_reading_ease"),
    )

    content = relationship("Content", backref="readability_scores")
    organization = relationship("Organization", backref="readability_scores")


# ==================== MODULE 65: BRAND VOICE CONSISTENCY ====================

class BrandVoiceGuide(Base):
    """Brand voice and style guidelines"""
    __tablename__ = "brand_voice_guides"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Voice characteristics
    tone = Column(JSON, default={})  # {primary, secondary, avoid} - e.g., {professional, friendly, approachable}
    personality_traits = Column(JSON, default=[])  # e.g., [confident, helpful, innovative]
    values = Column(JSON, default=[])  # Brand values

    # Writing style guidelines
    vocabulary_level = Column(String(50))  # Simple, Moderate, Advanced
    sentence_structure = Column(String(255))  # e.g., "Short and punchy"
    paragraph_length = Column(String(100))  # e.g., "2-4 sentences"
    active_voice_preference = Column(Float, default=0.8)  # 0-1, preference for active voice

    # Terminology
    preferred_terminology = Column(JSON, default={})  # {term: preferred_variant}
    forbidden_terms = Column(JSON, default=[])
    style_guide_url = Column(String(500))  # Link to full style guide

    # Examples
    dos_and_donts = Column(JSON, default={})  # {dos: [...], donts: [...]}
    example_content = Column(JSON, default=[])  # Array of exemplary content

    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_brandvoice_org", "organization_id"),
        Index("idx_brandvoice_active", "is_active"),
    )

    organization = relationship("Organization", backref="brand_voice_guides")
    creator = relationship("User", backref="created_brand_voice_guides")


class BrandVoiceCheck(Base):
    """Brand voice consistency check results"""
    __tablename__ = "brand_voice_checks"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    guide_id = Column(Integer, ForeignKey("brand_voice_guides.id", ondelete="SET NULL"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # Analysis
    text_analyzed = Column(Text, nullable=False)
    check_result = Column(SQLEnum(BrandVoiceCheckResult), nullable=False, index=True)

    # Scoring
    compliance_score = Column(Float, default=0.0)  # 0-100
    tone_match_score = Column(Float, default=0.0)  # 0-100
    consistency_score = Column(Float, default=0.0)  # 0-100
    overall_score = Column(Float, default=0.0)  # 0-100

    # Detailed findings
    tone_analysis = Column(JSON, default={})  # Detected tones vs expected
    tone_matches = Column(Integer, default=0)
    tone_mismatches = Column(Integer, default=0)

    # Terminology check
    forbidden_terms_found = Column(Integer, default=0)
    preferred_terms_missed = Column(Integer, default=0)
    terminology_issues = Column(JSON, default=[])  # Array of issues

    # Style compliance
    style_compliance_issues = Column(JSON, default=[])  # Array of style issues
    active_voice_percentage = Column(Float, default=0.0)

    # Recommendations
    recommendations = Column(JSON, default=[])  # Array of improvement suggestions
    suggested_revisions = Column(JSON, default={})  # Suggested text changes

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_brandcheck_content", "content_id"),
        Index("idx_brandcheck_guide", "guide_id"),
        Index("idx_brandcheck_org", "organization_id"),
        Index("idx_brandcheck_result", "check_result"),
        Index("idx_brandcheck_score", "overall_score"),
    )

    content = relationship("Content", backref="brand_voice_checks")
    guide = relationship("BrandVoiceGuide", backref="checks")
    organization = relationship("Organization", backref="brand_voice_checks")
