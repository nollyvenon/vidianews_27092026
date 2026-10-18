"""Tests for course services (membership services are covered in test_memberships.py)"""

import pytest
from sqlalchemy.orm import Session, sessionmaker
from app.models.user import User
from app.models.courses import (
    AssignmentSubmission
)
from app.services.courses_service import (
    CourseService, LessonService, CourseSectionService, EnrollmentService,


    StudentLessonProgressService, CourseReviewService, AssignmentService,
    AssignmentSubmissionService, CertificateService
)


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


@pytest.fixture
def db(reset_test_database) -> Session:
    """Blocking session on the per-test database (these services are synchronous)"""
    db_session = sessionmaker(bind=reset_test_database, expire_on_commit=False)()
    yield db_session
    db_session.close()


@pytest.fixture
def instructor(db):
    user = User(email="instructor@example.com", password_hash="hashed", first_name="Ada", last_name="Lovelace")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_course(db, instructor):
    return CourseService.create_course(db, 1, instructor.id, {
        "title": "Python Basics",
        "description": "Learn Python fundamentals",
        "category": "Programming",
        "price": 49.99,
        "difficulty_level": "beginner",
        "language": "en",
        "learning_objectives": ["Learn Python syntax", "Build first program"],
        "prerequisites": []
    })


@pytest.fixture
def test_section(db, test_course):
    return CourseSectionService.create_section(db, test_course.id, {
        "title": "Introduction",
        "description": "Getting started",
        "order": 1
    })


@pytest.fixture
def test_lesson(db, test_course, test_section):
    return LessonService.create_lesson(db, test_course.id, test_section.id, {
        "title": "Variables and Types",
        "description": "Learn about variables",
        "video_url": "https://example.com/video1",
        "video_duration": 600,
        "content": "Variables lesson content",
        "order": 1
    })


class TestCourseService:
    def test_create_course(self, db, test_course):
        assert test_course.id is not None
        assert test_course.title == "Python Basics"
        assert test_course.status == "draft"

    def test_get_course(self, db, test_course):
        retrieved = CourseService.get_course(db, test_course.id)
        assert retrieved.id == test_course.id
        assert retrieved.title == "Python Basics"

    def test_publish_course(self, db, test_course):
        CourseService.publish_course(db, test_course.id)
        published = CourseService.get_course(db, test_course.id)
        assert published.status == "published"

    def test_search_courses(self, db, test_course):
        CourseService.publish_course(db, test_course.id)
        results = CourseService.search_courses(db, 1, "Python")
        assert len(results) > 0

    def test_update_course(self, db, test_course):
        updated = CourseService.update_course(db, test_course.id, {"title": "Advanced Python"})
        assert updated.title == "Advanced Python"


class TestEnrollmentService:
    def test_enroll_student(self, db, test_course):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        assert enrollment.id is not None
        assert enrollment.user_id == 1
        assert enrollment.course_id == test_course.id
        assert enrollment.status == "active"

    def test_get_user_enrollments(self, db, test_course):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        enrollments = EnrollmentService.get_user_enrollments(db, 1)
        assert len(enrollments) > 0

    def test_complete_enrollment(self, db, test_course):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        EnrollmentService.complete_enrollment(db, enrollment.id)

        completed = EnrollmentService.get_enrollment(db, enrollment.id)
        assert completed.status == "completed"
        assert completed.completed_date is not None

    def test_drop_course(self, db, test_course):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        EnrollmentService.drop_course(db, enrollment.id)

        dropped = EnrollmentService.get_enrollment(db, enrollment.id)
        assert dropped.status == "dropped"


class TestStudentLessonProgressService:
    def test_mark_lesson_complete(self, db, test_course, test_lesson):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        StudentLessonProgressService.mark_lesson_complete(db, enrollment.id, test_lesson.id)

        progress = StudentLessonProgressService.get_lesson_progress(db, enrollment.id, test_lesson.id)
        assert progress.is_completed is True
        assert progress.completion_percentage == 100.0

    def test_update_watch_time(self, db, test_course, test_lesson):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        StudentLessonProgressService.mark_lesson_complete(db, enrollment.id, test_lesson.id)
        StudentLessonProgressService.update_watch_time(db, enrollment.id, test_lesson.id, 300)

        progress = StudentLessonProgressService.get_lesson_progress(db, enrollment.id, test_lesson.id)
        assert progress.video_watch_time == 300


class TestCourseReviewService:
    def test_create_review(self, db, test_course):
        review = CourseReviewService.create_review(db, test_course.id, 1, {
            "rating": 5,
            "title": "Great course",
            "content": "Really helped me learn",
            "verified_purchase": True
        })

        assert review.id is not None
        assert review.rating == 5
        assert test_course.total_reviews > 0

    def test_get_course_reviews(self, db, test_course):
        review = CourseReviewService.create_review(db, test_course.id, 1, {
            "rating": 4,
            "title": "Good course"
        })

        reviews = CourseReviewService.get_course_reviews(db, test_course.id)
        assert len(reviews) > 0


class TestAssignmentService:
    def test_create_assignment(self, db, test_course):
        assignment = AssignmentService.create_assignment(db, test_course.id, {
            "title": "Python Assignment 1",
            "description": "Complete the assignment",
            "instructions": "Follow these steps",
            "max_score": 100.0
        })

        assert assignment.id is not None
        assert assignment.title == "Python Assignment 1"

    def test_publish_assignment(self, db, test_course):
        assignment = AssignmentService.create_assignment(db, test_course.id, {
            "title": "Python Assignment 1"
        })

        AssignmentService.publish_assignment(db, assignment.id)
        published = AssignmentService.get_assignment(db, assignment.id)
        assert published.status == "assigned"


class TestAssignmentSubmissionService:
    def test_submit_assignment(self, db, test_course):
        assignment = AssignmentService.create_assignment(db, test_course.id, {
            "title": "Python Assignment 1"
        })

        submission = AssignmentSubmissionService.submit_assignment(db, assignment.id, 1, {
            "content": "My submission",
            "file_urls": ["https://example.com/solution.py"]
        })

        assert submission.id is not None
        assert submission.status == "submitted"

    def test_grade_submission(self, db, test_course):
        assignment = AssignmentService.create_assignment(db, test_course.id, {
            "title": "Python Assignment 1"
        })
        submission = AssignmentSubmissionService.submit_assignment(db, assignment.id, 1, {
            "content": "My submission"
        })

        AssignmentSubmissionService.grade_submission(db, submission.id, 95.0, "Excellent work", 2)

        graded = db.query(AssignmentSubmission).filter_by(id=submission.id).first()
        assert graded.status == "graded"
        assert graded.score == 95.0


class TestCertificateService:
    def test_issue_certificate(self, db, test_course):
        enrollment = EnrollmentService.enroll_student(db, 1, test_course.id)
        certificate = CertificateService.issue_certificate(db, test_course.id, 1)

        assert certificate.id is not None
        assert certificate.certificate_number is not None
        assert certificate.is_valid is True
