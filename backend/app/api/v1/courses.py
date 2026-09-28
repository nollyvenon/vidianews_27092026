"""Courses API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.courses_service import (
    CourseService, LessonService, CourseSectionService, EnrollmentService,
    StudentLessonProgressService, CourseReviewService, AssignmentService,
    AssignmentSubmissionService, CertificateService
)
from app.models.auth import User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class CourseRequest(BaseModel):
    title: str
    description: Optional[str] = None
    category: str = "general"
    price: float = 0.0
    difficulty_level: str = "beginner"
    language: str = "en"
    prerequisites: List[str] = []
    learning_objectives: List[str] = []


class SectionRequest(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 1


class LessonRequest(BaseModel):
    title: str
    section_id: int
    description: Optional[str] = None
    video_url: Optional[str] = None
    video_duration: Optional[int] = None
    content: Optional[str] = None
    order: int = 1


class ReviewRequest(BaseModel):
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None


class AssignmentRequest(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    due_date: Optional[str] = None
    max_score: float = 100.0


class AssignmentSubmissionRequest(BaseModel):
    content: Optional[str] = None
    file_urls: List[str] = []


@router.post("/courses")
def create_course(
    req: CourseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create course"""
    return CourseService.create_course(db, 1, current_user.id, req.dict())


@router.get("/courses/{course_id}")
def get_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get course"""
    course = CourseService.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/courses")
def list_courses(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List courses"""
    return CourseService.list_courses(db, 1, status)


@router.put("/courses/{course_id}")
def update_course(
    course_id: int,
    req: CourseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update course"""
    return CourseService.update_course(db, course_id, req.dict(exclude_unset=True))


@router.post("/courses/{course_id}/publish")
def publish_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish course"""
    CourseService.publish_course(db, course_id)
    return {"status": "published"}


@router.get("/courses/search/{search_term}")
def search_courses(
    search_term: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search courses"""
    return CourseService.search_courses(db, 1, search_term)


@router.post("/courses/{course_id}/sections")
def create_section(
    course_id: int,
    req: SectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create course section"""
    return CourseSectionService.create_section(db, course_id, req.dict())


@router.get("/courses/{course_id}/sections")
def get_sections(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get course sections"""
    return CourseSectionService.get_course_sections(db, course_id)


@router.post("/sections/{section_id}/lessons")
def create_lesson(
    section_id: int,
    req: LessonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create lesson"""
    section = db.query(__import__('app.models.courses', fromlist=['CourseSection']).CourseSection).filter_by(id=section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return LessonService.create_lesson(db, section.course_id, section_id, req.dict())


@router.get("/lessons/{lesson_id}")
def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get lesson"""
    lesson = LessonService.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/courses/{course_id}/enroll")
def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in course"""
    return EnrollmentService.enroll_student(db, current_user.id, course_id)


@router.get("/enrollments/me")
def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get my enrollments"""
    return EnrollmentService.get_user_enrollments(db, current_user.id)


@router.post("/enrollments/{enrollment_id}/lessons/{lesson_id}/complete")
def mark_lesson_complete(
    enrollment_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark lesson as complete"""
    StudentLessonProgressService.mark_lesson_complete(db, enrollment_id, lesson_id)
    return {"status": "completed"}


@router.post("/courses/{course_id}/reviews")
def create_review(
    course_id: int,
    req: ReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create course review"""
    return CourseReviewService.create_review(db, course_id, current_user.id, req.dict())


@router.get("/courses/{course_id}/reviews")
def get_reviews(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get course reviews"""
    return CourseReviewService.get_course_reviews(db, course_id)


@router.post("/courses/{course_id}/assignments")
def create_assignment(
    course_id: int,
    req: AssignmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create assignment"""
    return AssignmentService.create_assignment(db, course_id, req.dict())


@router.post("/assignments/{assignment_id}/submissions")
def submit_assignment(
    assignment_id: int,
    req: AssignmentSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit assignment"""
    return AssignmentSubmissionService.submit_assignment(db, assignment_id, current_user.id, req.dict())


@router.post("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: int,
    score: float,
    feedback: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Grade submission"""
    AssignmentSubmissionService.grade_submission(db, submission_id, score, feedback, current_user.id)
    return {"status": "graded"}


@router.post("/enrollments/{enrollment_id}/certificate")
def issue_certificate(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Issue certificate"""
    enrollment = db.query(__import__('app.models.courses', fromlist=['CourseEnrollment']).CourseEnrollment).filter_by(id=enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return CertificateService.issue_certificate(db, enrollment.course_id, enrollment.user_id)
