"""Course models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum
from app.db.base import Base


class CourseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DISCONTINUED = "discontinued"


class LessonStatus(str, Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    COMPLETED = "completed"


class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class AssignmentStatus(str, Enum):
    DRAFT = "draft"
    ASSIGNED = "assigned"
    SUBMITTED = "submitted"
    GRADED = "graded"
    ARCHIVED = "archived"


class SubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    REVISION_REQUESTED = "revision_requested"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    instructor_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), index=True)
    thumbnail_url = Column(String(500))
    price = Column(Float, default=0.0)
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT)
    difficulty_level = Column(String(50), default="beginner")
    duration_hours = Column(Float)
    language = Column(String(50), default="en")
    total_enrollments = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    prerequisites = Column(JSON, default=[])
    learning_objectives = Column(JSON, default=[])
    requirements = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    instructor = relationship("User")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    reviews = relationship("CourseReview", back_populates="course", cascade="all, delete-orphan")
    bundles = relationship("CourseBundle", secondary="course_bundle_items", back_populates="courses")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("course_sections.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    video_url = Column(String(500))
    video_duration = Column(Integer)
    content = Column(Text)
    resources = Column(JSON, default=[])
    order = Column(Integer)
    is_preview = Column(Boolean, default=False)
    status = Column(SQLEnum(LessonStatus), default=LessonStatus.LOCKED)
    release_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="lessons")
    section = relationship("CourseSection", back_populates="lessons")
    progress_records = relationship("StudentLessonProgress", back_populates="lesson")


class CourseSection(Base):
    __tablename__ = "course_sections"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    course = relationship("Course")
    lessons = relationship("Lesson", back_populates="section")


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    status = Column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    enrolled_date = Column(DateTime, default=datetime.now(timezone.utc))
    completed_date = Column(DateTime)
    progress_percentage = Column(Float, default=0.0)
    lessons_completed = Column(Integer, default=0)
    total_lessons = Column(Integer)
    certificate_issued = Column(Boolean, default=False)
    certificate_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User")
    course = relationship("Course", back_populates="enrollments")
    progress_records = relationship("StudentLessonProgress", back_populates="enrollment")


class StudentLessonProgress(Base):
    __tablename__ = "student_lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    video_watch_time = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    completed_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    enrollment = relationship("CourseEnrollment", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")


class CourseReview(Base):
    __tablename__ = "course_reviews"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    title = Column(String(255))
    content = Column(Text)
    verified_purchase = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="reviews")
    user = relationship("User")


class CourseBundle(Base):
    __tablename__ = "course_bundles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    thumbnail_url = Column(String(500))
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    courses = relationship("Course", secondary="course_bundle_items", back_populates="bundles")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.DRAFT)
    due_date = Column(DateTime)
    max_score = Column(Float, default=100.0)
    is_graded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    status = Column(SQLEnum(SubmissionStatus), default=SubmissionStatus.DRAFT)
    content = Column(Text)
    file_urls = Column(JSON, default=[])
    submitted_date = Column(DateTime)
    score = Column(Float)
    feedback = Column(Text)
    graded_date = Column(DateTime)
    graded_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", foreign_keys=[user_id])
    grader = relationship("User", foreign_keys=[graded_by])


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    certificate_number = Column(String(255), unique=True, nullable=False)
    certificate_url = Column(String(500))
    issue_date = Column(DateTime, default=datetime.now(timezone.utc))
    expiry_date = Column(DateTime)
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    course = relationship("Course")
    user = relationship("User")
