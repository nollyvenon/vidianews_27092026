"""Course services (async): courses, sections, lessons, enrollments, progress, reviews, assignments, certificates."""

import pytest

from app.models.courses import AssignmentSubmission
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
from app.utils.exceptions import NotFoundError


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


@pytest.fixture
async def test_course(session):
    return await CourseService(session).create_course(1, 1, {
        "title": "Python Basics",
        "description": "Learn Python fundamentals",
        "category": "Programming",
        "price": 49.99,
        "difficulty_level": "beginner",
        "language": "en",
        "learning_objectives": ["Learn Python syntax", "Build first program"],
        "prerequisites": [],
    })


@pytest.fixture
async def test_section(session, test_course):
    return await CourseSectionService(session).create_section(test_course.id, {
        "title": "Introduction", "description": "Getting started", "order": 1,
    })


@pytest.fixture
async def test_lesson(session, test_course, test_section):
    return await LessonService(session).create_lesson(test_course.id, test_section.id, {
        "title": "Variables and Types",
        "description": "Learn about variables",
        "video_url": "https://example.com/video1",
        "video_duration": 600,
        "content": "Variables lesson content",
        "order": 1,
    })


class TestCourseService:
    async def test_create_course(self, test_course):
        assert test_course.id is not None
        assert test_course.title == "Python Basics"
        assert test_course.status == "draft"

    async def test_get_course(self, session, test_course):
        retrieved = await CourseService(session).get_course(test_course.id)
        assert retrieved.id == test_course.id

    async def test_publish_course(self, session, test_course):
        service = CourseService(session)
        await service.publish_course(test_course.id)
        assert (await service.get_course(test_course.id)).status == "published"

    async def test_search_courses_returns_published_matches_only(self, session, test_course):
        service = CourseService(session)
        assert await service.search_courses(1, "Python") == []
        await service.publish_course(test_course.id)
        assert len(await service.search_courses(1, "Python")) == 1

    async def test_update_course(self, session, test_course):
        updated = await CourseService(session).update_course(test_course.id, {"title": "Advanced Python"})
        assert updated.title == "Advanced Python"

    async def test_missing_course_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await CourseService(session).update_course(999999, {"title": "x"})
        with pytest.raises(NotFoundError):
            await CourseService(session).publish_course(999999)


class TestEnrollmentService:
    async def test_enroll_student(self, session, test_course):
        enrollment = await EnrollmentService(session).enroll_student(2, test_course.id)
        assert enrollment.user_id == 2
        assert enrollment.course_id == test_course.id
        assert enrollment.status == "active"

    async def test_enrolling_in_a_missing_course_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await EnrollmentService(session).enroll_student(2, 999999)

    async def test_get_user_enrollments(self, session, test_course):
        service = EnrollmentService(session)
        await service.enroll_student(2, test_course.id)
        assert len(await service.get_user_enrollments(2)) == 1

    async def test_complete_enrollment(self, session, test_course):
        service = EnrollmentService(session)
        enrollment = await service.enroll_student(2, test_course.id)
        await service.complete_enrollment(enrollment.id)
        completed = await service.get_enrollment(enrollment.id)
        assert completed.status == "completed"
        assert completed.completed_date is not None

    async def test_drop_course(self, session, test_course):
        service = EnrollmentService(session)
        enrollment = await service.enroll_student(2, test_course.id)
        await service.drop_course(enrollment.id)
        assert (await service.get_enrollment(enrollment.id)).status == "dropped"


class TestStudentLessonProgressService:
    async def test_mark_lesson_complete_updates_the_enrollment(self, session, test_course, test_lesson):
        enrollment = await EnrollmentService(session).enroll_student(2, test_course.id)
        progress_service = StudentLessonProgressService(session)
        await progress_service.mark_lesson_complete(enrollment.id, test_lesson.id)

        progress = await progress_service.get_lesson_progress(enrollment.id, test_lesson.id)
        assert progress.is_completed is True
        assert progress.completion_percentage == 100.0
        refreshed = await EnrollmentService(session).get_enrollment(enrollment.id)
        assert refreshed.lessons_completed == 1

    async def test_update_watch_time(self, session, test_course, test_lesson):
        enrollment = await EnrollmentService(session).enroll_student(2, test_course.id)
        progress_service = StudentLessonProgressService(session)
        await progress_service.mark_lesson_complete(enrollment.id, test_lesson.id)
        await progress_service.update_watch_time(enrollment.id, test_lesson.id, 300)

        progress = await progress_service.get_lesson_progress(enrollment.id, test_lesson.id)
        assert progress.video_watch_time == 300


class TestCourseReviewService:
    async def test_create_review_updates_the_course_rating(self, session, test_course):
        review = await CourseReviewService(session).create_review(test_course.id, 2, {
            "rating": 5, "title": "Great course", "content": "Really helped me learn",
        })
        assert review.rating == 5
        await session.refresh(test_course)
        assert test_course.total_reviews == 1
        assert test_course.average_rating == 5

    async def test_get_course_reviews(self, session, test_course):
        service = CourseReviewService(session)
        await service.create_review(test_course.id, 2, {"rating": 4, "title": "Good course"})
        assert len(await service.get_course_reviews(test_course.id)) == 1


class TestAssignmentServices:
    async def test_create_and_publish_assignment(self, session, test_course):
        service = AssignmentService(session)
        assignment = await service.create_assignment(test_course.id, {"title": "Python Assignment 1", "max_score": 100.0})
        assert assignment.title == "Python Assignment 1"
        await service.publish_assignment(assignment.id)
        assert (await service.get_assignment(assignment.id)).status == "assigned"

    async def test_submit_and_grade(self, session, test_course):
        assignment = await AssignmentService(session).create_assignment(test_course.id, {"title": "Python Assignment 1"})
        service = AssignmentSubmissionService(session)
        submission = await service.submit_assignment(assignment.id, 2, {
            "content": "My submission", "file_urls": ["https://example.com/solution.py"],
        })
        assert submission.status == "submitted"

        await service.grade_submission(submission.id, 95.0, "Excellent work", 1)
        graded = await session.get(AssignmentSubmission, submission.id)
        await session.refresh(graded)
        assert graded.status == "graded"
        assert graded.score == 95.0

    async def test_grading_a_missing_submission_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await AssignmentSubmissionService(session).grade_submission(999999, 1.0, "x", 1)


class TestCertificateService:
    async def test_issue_certificate_marks_the_enrollment(self, session, test_course):
        enrollment = await EnrollmentService(session).enroll_student(2, test_course.id)
        certificate = await CertificateService(session).issue_certificate(test_course.id, 2)

        assert certificate.id is not None
        assert certificate.certificate_number is not None
        await session.refresh(enrollment)
        assert enrollment.certificate_issued is True
