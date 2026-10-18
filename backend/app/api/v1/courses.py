"""Courses API endpoints.

Access rules:
- Courses belong to a tenant. Members of the tenant see its published courses; drafts are
  visible only to the course's managers.
- A course manager is its instructor or an administrator of the courses area. Managers edit
  content, grade submissions, and issue certificates for any enrollment.
- Students act only on their own enrollments: they mark lessons complete, submit assignments,
  review courses they are enrolled in, and receive their own certificate once completed.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import is_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.courses import Assignment, AssignmentSubmission, Course, CourseEnrollment, CourseSection
from app.models.user import User
from app.services.courses_service import (
    AssignmentService,
    AssignmentSubmissionService,
    CertificateService,
    CourseReviewService,
    CourseSectionService,
    CourseService,
    EnrollmentService,
    LessonService,
    StudentLessonProgressService,
)

router = APIRouter()


class CourseRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = "general"
    price: float = Field(0.0, ge=0)
    difficulty_level: str = "beginner"
    language: str = "en"
    prerequisites: List[str] = []
    learning_objectives: List[str] = []


class CourseUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    difficulty_level: Optional[str] = None
    language: Optional[str] = None
    prerequisites: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None


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
    rating: int = Field(..., ge=1, le=5)
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


def _tenant(current_user: User) -> int:
    if current_user.tenant_id is None:
        raise HTTPException(status_code=422, detail="Your account has no workspace yet. Create a tenant first.")
    return current_user.tenant_id


async def _is_course_manager(session: AsyncSession, user: User, course: Course) -> bool:
    return course.instructor_id == user.id or await is_admin(session, user.id, "courses")


async def _course_for_read(session: AsyncSession, user: User, course_id: int) -> Course:
    """A course the caller may see: in their tenant, and published unless they manage it."""
    course = await session.get(Course, course_id)
    if course is None or course.organization_id != _tenant(user):
        raise HTTPException(status_code=404, detail="Course not found")
    if course.status != "published" and not await _is_course_manager(session, user, course):
        raise HTTPException(status_code=404, detail="Course not found")
    return course


async def _course_for_manage(session: AsyncSession, user: User, course_id: int) -> Course:
    course = await session.get(Course, course_id)
    if course is None or course.organization_id != _tenant(user):
        raise HTTPException(status_code=404, detail="Course not found")
    if not await _is_course_manager(session, user, course):
        raise HTTPException(status_code=403, detail="Only the course instructor or an administrator can change this course")
    return course


async def _enrollment_of(session: AsyncSession, enrollment_id: int) -> CourseEnrollment:
    enrollment = await session.get(CourseEnrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


async def _enrolled(session: AsyncSession, user: User, course_id: int) -> bool:
    return (await session.execute(
        select(CourseEnrollment.id).where(
            CourseEnrollment.user_id == user.id, CourseEnrollment.course_id == course_id,
        ).limit(1)
    )).first() is not None


@router.post("/courses", status_code=201)
async def create_course(
    req: CourseRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create a course in the caller's tenant; the caller becomes its instructor"""
    return await CourseService(session).create_course(_tenant(current_user), current_user.id, req.model_dump())


@router.get("/courses/{course_id}")
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await _course_for_read(session, current_user, course_id)


@router.get("/courses")
async def list_courses(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Courses of the caller's tenant: published ones for everyone, drafts for their managers"""
    courses = await CourseService(session).list_courses(_tenant(current_user), status)
    visible = []
    for course in courses:
        if course.status == "published" or await _is_course_manager(session, current_user, course):
            visible.append(course)
    return visible


@router.put("/courses/{course_id}")
async def update_course(
    course_id: int,
    req: CourseUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_manage(session, current_user, course_id)
    changes = req.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="Provide at least one field to change")
    return await CourseService(session).update_course(course_id, changes)


@router.post("/courses/{course_id}/publish")
async def publish_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_manage(session, current_user, course_id)
    await CourseService(session).publish_course(course_id)
    return {"status": "published"}


@router.get("/courses/search/{search_term}")
async def search_courses(
    search_term: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Published courses of the caller's tenant whose title matches"""
    return await CourseService(session).search_courses(_tenant(current_user), search_term)


@router.post("/courses/{course_id}/sections", status_code=201)
async def create_section(
    course_id: int,
    req: SectionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_manage(session, current_user, course_id)
    return await CourseSectionService(session).create_section(course_id, req.model_dump())


@router.get("/courses/{course_id}/sections")
async def get_sections(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_read(session, current_user, course_id)
    return await CourseSectionService(session).get_course_sections(course_id)


@router.post("/sections/{section_id}/lessons", status_code=201)
async def create_lesson(
    section_id: int,
    req: LessonRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    section = await session.get(CourseSection, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    await _course_for_manage(session, current_user, section.course_id)
    return await LessonService(session).create_lesson(section.course_id, section_id, req.model_dump())


@router.get("/lessons/{lesson_id}")
async def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    lesson = await LessonService(session).get_lesson(lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    await _course_for_read(session, current_user, lesson.course_id)
    return lesson


@router.post("/courses/{course_id}/enroll", status_code=201)
async def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    course = await _course_for_read(session, current_user, course_id)
    if course.status != "published":
        raise HTTPException(status_code=404, detail="Course not found")
    return await EnrollmentService(session).enroll_student(current_user.id, course_id)


@router.get("/enrollments/me")
async def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await EnrollmentService(session).get_user_enrollments(current_user.id)


@router.post("/enrollments/{enrollment_id}/lessons/{lesson_id}/complete")
async def mark_lesson_complete(
    enrollment_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    enrollment = await _enrollment_of(session, enrollment_id)
    if enrollment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only record progress on your own enrollment")
    await StudentLessonProgressService(session).mark_lesson_complete(enrollment_id, lesson_id)
    return {"status": "completed"}


@router.post("/courses/{course_id}/reviews", status_code=201)
async def create_review(
    course_id: int,
    req: ReviewRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Review a course you are enrolled in"""
    await _course_for_read(session, current_user, course_id)
    if not await _enrolled(session, current_user, course_id):
        raise HTTPException(status_code=403, detail="Only enrolled students can review this course")
    return await CourseReviewService(session).create_review(course_id, current_user.id, req.model_dump())


@router.get("/courses/{course_id}/reviews")
async def get_reviews(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_read(session, current_user, course_id)
    return await CourseReviewService(session).get_course_reviews(course_id)


async def _assignment_course(session: AsyncSession, assignment_id: int) -> Assignment:
    assignment = await AssignmentService(session).get_assignment(assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.post("/courses/{course_id}/assignments", status_code=201)
async def create_assignment(
    course_id: int,
    req: AssignmentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _course_for_manage(session, current_user, course_id)
    return await AssignmentService(session).create_assignment(course_id, req.model_dump())


@router.post("/assignments/{assignment_id}/submissions", status_code=201)
async def submit_assignment(
    assignment_id: int,
    req: AssignmentSubmissionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    assignment = await _assignment_course(session, assignment_id)
    await _course_for_read(session, current_user, assignment.course_id)
    if not await _enrolled(session, current_user, assignment.course_id):
        raise HTTPException(status_code=403, detail="Only enrolled students can submit this assignment")
    return await AssignmentSubmissionService(session).submit_assignment(assignment_id, current_user.id, req.model_dump())


@router.post("/submissions/{submission_id}/grade")
async def grade_submission(
    submission_id: int,
    score: float,
    feedback: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    submission = await session.get(AssignmentSubmission, submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    assignment = await _assignment_course(session, submission.assignment_id)
    await _course_for_manage(session, current_user, assignment.course_id)
    await AssignmentSubmissionService(session).grade_submission(submission_id, score, feedback, current_user.id)
    return {"status": "graded"}


@router.post("/enrollments/{enrollment_id}/certificate", status_code=201)
async def issue_certificate(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Certificate for an enrollment: its student once completed, or a manager of the course"""
    enrollment = await _enrollment_of(session, enrollment_id)
    course = await session.get(Course, enrollment.course_id)
    is_owner_completed = enrollment.user_id == current_user.id and enrollment.status == "completed"
    if not is_owner_completed and not await _is_course_manager(session, current_user, course):
        raise HTTPException(status_code=403, detail="Certificates are issued to students who completed the course")
    return await CertificateService(session).issue_certificate(enrollment.course_id, enrollment.user_id)
