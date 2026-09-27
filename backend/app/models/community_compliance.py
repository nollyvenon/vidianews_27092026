"""Community, Gamification & Compliance models: Modules 61-65"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class ForumCategory(str, enum.Enum):
    GENERAL = "general"
    TUTORIALS = "tutorials"
    FEEDBACK = "feedback"
    BUG_REPORTS = "bug_reports"


class BadgeType(str, enum.Enum):
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    CONTRIBUTOR = "contributor"
    INFLUENCER = "influencer"


class ReportType(str, enum.Enum):
    VIEWS = "views"
    REVENUE = "revenue"
    ENGAGEMENT = "engagement"
    GROWTH = "growth"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    REVIEW = "review"
    NON_COMPLIANT = "non_compliant"


# ==================== MODULE 61: COMMUNITY & FORUMS ====================

class ForumThread(Base):
    __tablename__ = "forum_threads"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(SQLEnum(ForumCategory), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    views = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)

    creator = relationship("User", backref="forum_threads")


class ForumReply(Base):
    __tablename__ = "forum_replies"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("forum_threads.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    upvotes = Column(Integer, default=0)

    thread = relationship("ForumThread", backref="replies")
    author = relationship("User", backref="forum_replies")


# ==================== MODULE 62: GAMIFICATION ====================

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    badge_type = Column(SQLEnum(BadgeType), nullable=False)
    icon_url = Column(String(500))
    criteria = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_id = Column(Integer, ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    earned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="badges")
    badge = relationship("Badge", backref="users")


class Leaderboard(Base):
    __tablename__ = "leaderboards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    rank = Column(Integer, index=True)
    points = Column(Integer, default=0)
    views = Column(Integer, default=0)
    engagement = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="leaderboard_entry")


# ==================== MODULE 63: REPORTS & EXPORTS ====================

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    data = Column(JSON)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    download_count = Column(Integer, default=0)

    creator = relationship("User", backref="reports")


class DataExport(Base):
    __tablename__ = "data_exports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    export_type = Column(String(100), nullable=False)
    file_path = Column(String(500))
    status = Column(String(50), default="processing")
    requested_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="data_exports")


# ==================== MODULE 64: COMPLIANCE ====================

class CompliancePolicy(Base):
    __tablename__ = "compliance_policies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    requirements = Column(JSON)
    status = Column(SQLEnum(ComplianceStatus), default=ComplianceStatus.REVIEW)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UserCompliance(Base):
    __tablename__ = "user_compliance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    gdpr_compliant = Column(Boolean, default=True)
    ccpa_compliant = Column(Boolean, default=True)
    terms_accepted = Column(Boolean, default=False)
    privacy_accepted = Column(Boolean, default=False)
    last_updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="compliance")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255))
    changes = Column(JSON)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="audit_logs")


# ==================== MODULE 65: INTERNATIONALIZATION ====================

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    native_name = Column(String(100))
    is_active = Column(Boolean, default=True)


class Translation(Base):
    __tablename__ = "translations"
    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(500), nullable=False)
    value = Column(Text, nullable=False)
    context = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    language = relationship("Language", backref="translations")


class UserLocalization(Base):
    __tablename__ = "user_localization"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="SET NULL"), nullable=True)
    timezone = Column(String(100))
    date_format = Column(String(50))
    currency = Column(String(10))

    user = relationship("User", backref="localization")
    language = relationship("Language")
