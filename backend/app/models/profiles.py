"""User profile models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class UserProfile(Base):
    """Extended user profile information"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Personal info
    bio = Column(Text)
    avatar_url = Column(String(500))
    cover_url = Column(String(500))
    title = Column(String(255))
    department = Column(String(255))
    location = Column(String(255))
    phone = Column(String(20))

    # Social links
    website = Column(String(500))
    twitter = Column(String(255))
    linkedin = Column(String(255))
    github = Column(String(255))

    # Preferences
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    notification_preferences = Column(JSON, default={})
    privacy_settings = Column(JSON, default={})

    # Additional custom fields (JSON)
    custom_fields = Column(JSON, default={})
    metadata = Column(JSON, default={})

    # Visibility
    is_public = Column(Boolean, default=False)
    show_email = Column(Boolean, default=False)
    show_phone = Column(Boolean, default=False)

    # Activity tracking
    last_profile_update = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", backref="profile")
    skills = relationship("UserSkill", back_populates="profile", cascade="all, delete-orphan")
    experiences = relationship("UserExperience", back_populates="profile", cascade="all, delete-orphan")
    educations = relationship("UserEducation", back_populates="profile", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="profile", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_is_public", "is_public"),
    )


class UserSkill(Base):
    """User skills/competencies"""
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    category = Column(String(100))  # e.g., "backend", "frontend", "devops"
    proficiency = Column(String(50), default="intermediate")  # beginner, intermediate, expert
    years_experience = Column(Integer, default=0)
    endorsed_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("UserProfile", back_populates="skills")

    __table_args__ = (
        Index("idx_profile_skill", "profile_id", "name"),
    )


class UserExperience(Base):
    """User work experience"""
    __tablename__ = "user_experiences"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    company = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    employment_type = Column(String(50))  # full-time, part-time, contract, etc.
    location = Column(String(255))

    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    current = Column(Boolean, default=False)

    skills = Column(JSON, default=[])  # List of skill tags

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("UserProfile", back_populates="experiences")


class UserEducation(Base):
    """User education history"""
    __tablename__ = "user_educations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    school = Column(String(255), nullable=False)
    degree = Column(String(255))
    field = Column(String(255))
    description = Column(Text)

    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    grade = Column(String(10))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("UserProfile", back_populates="educations")


class UserBadge(Base):
    """Achievements/badges earned by users"""
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    badge_name = Column(String(255), nullable=False)
    badge_type = Column(String(50))  # achievement, certification, milestone
    description = Column(Text)
    icon_url = Column(String(500))

    earned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=True)

    metadata = Column(JSON, default={})

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("UserProfile", back_populates="badges")

    __table_args__ = (
        Index("idx_profile_badge", "profile_id", "badge_name"),
    )
