"""Tests for memberships and courses services"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.memberships import (
    MembershipType, MembershipSubscription, MembershipInvoice, MembershipPaymentMethod,
    MembershipTier, SubscriptionStatus, BillingCycle
)
from app.models.courses import (
    Course, Lesson, CourseSection, CourseEnrollment, StudentLessonProgress,
    CourseReview, Assignment, AssignmentSubmission, Certificate,
    CourseStatus, LessonStatus, EnrollmentStatus, AssignmentStatus, SubmissionStatus
)
from app.services.memberships_service import (
    MembershipTypeService, MembershipSubscriptionService, MembershipInvoiceService,
    MembershipPaymentMethodService
)
from app.services.courses_service import (
    CourseService, LessonService, CourseSectionService, EnrollmentService,
    StudentLessonProgressService, CourseReviewService, AssignmentService,
    AssignmentSubmissionService, CertificateService
)


@pytest.fixture
def test_membership_type(db):
    return MembershipTypeService.create_membership_type(db, 1, {
        "name": "Premium",
        "tier": "premium",
        "description": "Premium membership",
        "price": 29.99,
        "billing_cycle": "monthly",
        "max_courses": 100,
        "max_students": 1000,
        "features": {"ad_free": True, "priority_support": True}
    })


@pytest.fixture
def test_course(db):
    return CourseService.create_course(db, 1, 1, {
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


class TestMembershipTypeService:
    def test_create_membership_type(self, db, test_membership_type):
        assert test_membership_type.id is not None
        assert test_membership_type.name == "Premium"
        assert test_membership_type.tier == "premium"
        assert test_membership_type.price == 29.99

    def test_get_membership_type(self, db, test_membership_type):
        retrieved = MembershipTypeService.get_membership_type(db, test_membership_type.id)
        assert retrieved.id == test_membership_type.id
        assert retrieved.name == "Premium"

    def test_list_membership_types(self, db, test_membership_type):
        types = MembershipTypeService.list_membership_types(db, 1)
        assert len(types) > 0
        assert any(t.id == test_membership_type.id for t in types)

    def test_update_membership_type(self, db, test_membership_type):
        updated = MembershipTypeService.update_membership_type(db, test_membership_type.id, {
            "price": 39.99,
            "name": "Premium Plus"
        })
        assert updated.price == 39.99
        assert updated.name == "Premium Plus"


class TestMembershipSubscriptionService:
    def test_subscribe_user(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        assert subscription.id is not None
        assert subscription.user_id == 1
        assert subscription.membership_type_id == test_membership_type.id
        assert subscription.status == "active"

    def test_get_active_subscription(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        active = MembershipSubscriptionService.get_active_subscription(db, 1)
        assert active is not None
        assert active.id == subscription.id

    def test_cancel_subscription(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        MembershipSubscriptionService.cancel_subscription(db, subscription.id)

        cancelled = db.query(MembershipSubscription).filter_by(id=subscription.id).first()
        assert cancelled.status == "cancelled"
        assert cancelled.end_date is not None

    def test_pause_subscription(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        MembershipSubscriptionService.pause_subscription(db, subscription.id)

        paused = db.query(MembershipSubscription).filter_by(id=subscription.id).first()
        assert paused.status == "paused"

    def test_renew_subscription(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        old_renewal = subscription.renewal_date

        MembershipSubscriptionService.renew_subscription(db, subscription.id)

        renewed = db.query(MembershipSubscription).filter_by(id=subscription.id).first()
        assert renewed.status == "active"
        assert renewed.renewal_date > old_renewal


class TestMembershipInvoiceService:
    def test_create_invoice(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        invoice = MembershipInvoiceService.create_invoice(db, subscription.id, 29.99)

        assert invoice.id is not None
        assert invoice.subscription_id == subscription.id
        assert invoice.amount == 29.99
        assert invoice.total_amount > 29.99  # includes tax
        assert invoice.status == "pending"

    def test_mark_invoice_paid(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        invoice = MembershipInvoiceService.create_invoice(db, subscription.id, 29.99)

        MembershipInvoiceService.mark_invoice_paid(db, invoice.id)

        paid = db.query(MembershipInvoice).filter_by(id=invoice.id).first()
        assert paid.status == "paid"
        assert paid.paid_date is not None

    def test_get_subscription_invoices(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        invoice1 = MembershipInvoiceService.create_invoice(db, subscription.id, 29.99)
        invoice2 = MembershipInvoiceService.create_invoice(db, subscription.id, 29.99)

        invoices = MembershipInvoiceService.get_subscription_invoices(db, subscription.id)
        assert len(invoices) == 2


class TestMembershipPaymentMethodService:
    def test_add_payment_method(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        payment = MembershipPaymentMethodService.add_payment_method(
            db, subscription.id, "visa", "4242", "pm_test_123"
        )

        assert payment.id is not None
        assert payment.card_brand == "visa"
        assert payment.card_last_four == "4242"
        assert payment.is_default is True

    def test_get_payment_methods(self, db, test_membership_type):
        subscription = MembershipSubscriptionService.subscribe_user(db, 1, test_membership_type.id)
        payment1 = MembershipPaymentMethodService.add_payment_method(
            db, subscription.id, "visa", "4242", "pm_test_123"
        )
        payment2 = MembershipPaymentMethodService.add_payment_method(
            db, subscription.id, "mastercard", "5555", "pm_test_456"
        )

        methods = MembershipPaymentMethodService.get_payment_methods(db, subscription.id)
        assert len(methods) == 2


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
