"""Course and enrollment services (async).

Timestamps are naive UTC to match the courses columns. Missing records raise NotFoundError.
"""

import uuid
from typing import List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.courses import (
    Assignment,
    AssignmentSubmission,
    Certificate,
    Course,
    CourseEnrollment,
    CourseReview,
    CourseSection,
    Lesson,
    StudentLessonProgress,
    utc_now_naive,
)
from app.utils.exceptions import NotFoundError


class CourseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_course(self, org_id: int, instructor_id: int, course_data: dict) -> Course:
        course = Course(organization_id=org_id, instructor_id=instructor_id, **course_data)
        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def get_course(self, course_id: int) -> Optional[Course]:
        return await self.session.get(Course, course_id)

    async def list_courses(self, org_id: int, status: Optional[str] = None) -> List[Course]:
        stmt = select(Course).where(Course.organization_id == org_id)
        if status:
            stmt = stmt.where(Course.status == status)
        return list((await self.session.execute(stmt.order_by(Course.id))).scalars().all())

    async def update_course(self, course_id: int, update_data: dict) -> Course:
        course = await self.get_course(course_id)
        if course is None:
            raise NotFoundError("Course")
        for key, value in update_data.items():
            setattr(course, key, value)
        course.updated_at = utc_now_naive()
        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def publish_course(self, course_id: int) -> None:
        course = await self.get_course(course_id)
        if course is None:
            raise NotFoundError("Course")
        course.status = "published"
        await self.session.commit()

    async def search_courses(self, org_id: int, search_term: str) -> List[Course]:
        result = await self.session.execute(
            select(Course).where(and_(
                Course.organization_id == org_id,
                Course.status == "published",
                Course.title.ilike(f"%{search_term}%"),
            )).order_by(Course.id)
        )
        return list(result.scalars().all())


class LessonService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_lesson(self, course_id: int, section_id: int, lesson_data: dict) -> Lesson:
        lesson = Lesson(course_id=course_id, section_id=section_id, **lesson_data)
        self.session.add(lesson)
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson

    async def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        return await self.session.get(Lesson, lesson_id)

    async def update_lesson(self, lesson_id: int, update_data: dict) -> Lesson:
        lesson = await self.get_lesson(lesson_id)
        if lesson is None:
            raise NotFoundError("Lesson")
        for key, value in update_data.items():
            setattr(lesson, key, value)
        lesson.updated_at = utc_now_naive()
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson


class CourseSectionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_section(self, course_id: int, section_data: dict) -> CourseSection:
        section = CourseSection(course_id=course_id, **section_data)
        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)
        return section

    async def get_section(self, section_id: int) -> Optional[CourseSection]:
        return await self.session.get(CourseSection, section_id)

    async def get_course_sections(self, course_id: int) -> List[CourseSection]:
        result = await self.session.execute(
            select(CourseSection).where(CourseSection.course_id == course_id).order_by(CourseSection.order)
        )
        return list(result.scalars().all())


class EnrollmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def enroll_student(self, user_id: int, course_id: int) -> CourseEnrollment:
        course = await self.session.get(Course, course_id)
        if course is None:
            raise NotFoundError("Course")
        total_lessons = (await self.session.execute(
            select(func.count(Lesson.id)).where(Lesson.course_id == course_id)
        )).scalar_one()
        enrollment = CourseEnrollment(user_id=user_id, course_id=course_id, total_lessons=total_lessons)
        self.session.add(enrollment)
        course.total_enrollments += 1
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment

    async def get_enrollment(self, enrollment_id: int) -> Optional[CourseEnrollment]:
        return await self.session.get(CourseEnrollment, enrollment_id)

    async def _enrollment(self, enrollment_id: int) -> CourseEnrollment:
        enrollment = await self.get_enrollment(enrollment_id)
        if enrollment is None:
            raise NotFoundError("Enrollment")
        return enrollment

    async def get_user_enrollments(self, user_id: int) -> List[CourseEnrollment]:
        result = await self.session.execute(
            select(CourseEnrollment).where(CourseEnrollment.user_id == user_id).order_by(CourseEnrollment.id)
        )
        return list(result.scalars().all())

    async def complete_enrollment(self, enrollment_id: int) -> None:
        enrollment = await self._enrollment(enrollment_id)
        enrollment.status = "completed"
        enrollment.completed_date = utc_now_naive()
        enrollment.progress_percentage = 100.0
        await self.session.commit()

    async def drop_course(self, enrollment_id: int) -> None:
        enrollment = await self._enrollment(enrollment_id)
        enrollment.status = "dropped"
        await self.session.commit()

    async def update_progress(self, enrollment_id: int) -> None:
        enrollment = await self._enrollment(enrollment_id)
        completed = (await self.session.execute(
            select(func.count(StudentLessonProgress.id)).where(and_(
                StudentLessonProgress.enrollment_id == enrollment_id,
                StudentLessonProgress.is_completed == True,  # noqa: E712 - SQL comparison
            ))
        )).scalar_one()
        if enrollment.total_lessons > 0:
            enrollment.progress_percentage = (completed / enrollment.total_lessons) * 100
            enrollment.lessons_completed = completed
        await self.session.commit()


class StudentLessonProgressService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def mark_lesson_complete(self, enrollment_id: int, lesson_id: int) -> None:
        enrollment = await self.session.get(CourseEnrollment, enrollment_id)
        if enrollment is None:
            raise NotFoundError("Enrollment")
        lesson = await self.session.get(Lesson, lesson_id)
        if lesson is None or lesson.course_id != enrollment.course_id:
            raise NotFoundError("Lesson")
        progress = await self.get_lesson_progress(enrollment_id, lesson_id)
        if progress is None:
            progress = StudentLessonProgress(enrollment_id=enrollment_id, lesson_id=lesson_id)
            self.session.add(progress)
        progress.is_completed = True
        progress.completion_percentage = 100.0
        progress.completed_date = utc_now_naive()
        await self.session.commit()
        await EnrollmentService(self.session).update_progress(enrollment_id)

    async def get_lesson_progress(self, enrollment_id: int, lesson_id: int) -> Optional[StudentLessonProgress]:
        return (await self.session.execute(
            select(StudentLessonProgress).where(and_(
                StudentLessonProgress.enrollment_id == enrollment_id,
                StudentLessonProgress.lesson_id == lesson_id,
            ))
        )).scalar_one_or_none()

    async def update_watch_time(self, enrollment_id: int, lesson_id: int, watch_time: int) -> None:
        progress = await self.get_lesson_progress(enrollment_id, lesson_id)
        if progress is not None:
            progress.video_watch_time = watch_time
            await self.session.commit()


class CourseReviewService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, course_id: int, user_id: int, review_data: dict) -> CourseReview:
        course = await self.session.get(Course, course_id)
        if course is None:
            raise NotFoundError("Course")
        review = CourseReview(course_id=course_id, user_id=user_id, **review_data)
        self.session.add(review)
        await self.session.flush()
        course.total_reviews += 1
        ratings = (await self.session.execute(
            select(CourseReview.rating).where(CourseReview.course_id == course_id)
        )).scalars().all()
        course.average_rating = sum(ratings) / len(ratings) if ratings else 0
        await self.session.commit()
        await self.session.refresh(review)
        return review

    async def get_course_reviews(self, course_id: int) -> List[CourseReview]:
        result = await self.session.execute(
            select(CourseReview).where(CourseReview.course_id == course_id).order_by(CourseReview.created_at.desc())
        )
        return list(result.scalars().all())


class AssignmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_assignment(self, course_id: int, assignment_data: dict) -> Assignment:
        assignment = Assignment(course_id=course_id, **assignment_data)
        self.session.add(assignment)
        await self.session.commit()
        await self.session.refresh(assignment)
        return assignment

    async def get_assignment(self, assignment_id: int) -> Optional[Assignment]:
        return await self.session.get(Assignment, assignment_id)

    async def publish_assignment(self, assignment_id: int) -> None:
        assignment = await self.get_assignment(assignment_id)
        if assignment is None:
            raise NotFoundError("Assignment")
        assignment.status = "assigned"
        await self.session.commit()


class AssignmentSubmissionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def submit_assignment(self, assignment_id: int, user_id: int, submission_data: dict) -> AssignmentSubmission:
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            user_id=user_id,
            status="submitted",
            submitted_date=utc_now_naive(),
            **submission_data,
        )
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        return submission

    async def grade_submission(self, submission_id: int, score: float, feedback: str, graded_by: int) -> None:
        submission = await self.session.get(AssignmentSubmission, submission_id)
        if submission is None:
            raise NotFoundError("Submission")
        submission.status = "graded"
        submission.score = score
        submission.feedback = feedback
        submission.graded_by = graded_by
        submission.graded_date = utc_now_naive()
        await self.session.commit()


class CertificateService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def issue_certificate(self, course_id: int, user_id: int) -> Certificate:
        certificate_number = str(uuid.uuid4())
        certificate = Certificate(
            course_id=course_id,
            user_id=user_id,
            certificate_number=certificate_number,
            issue_date=utc_now_naive(),
        )
        self.session.add(certificate)
        enrollment = (await self.session.execute(
            select(CourseEnrollment).where(and_(
                CourseEnrollment.user_id == user_id,
                CourseEnrollment.course_id == course_id,
            ))
        )).scalar_one_or_none()
        if enrollment is not None:
            enrollment.certificate_issued = True
            enrollment.certificate_url = f"/certificates/{certificate_number}"
        await self.session.commit()
        await self.session.refresh(certificate)
        return certificate
