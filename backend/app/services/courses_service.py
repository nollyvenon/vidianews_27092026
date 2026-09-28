"""Course and enrollment services"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.courses import (
    Course, Lesson, CourseSection, CourseEnrollment, StudentLessonProgress,
    CourseReview, CourseBundle, Assignment, AssignmentSubmission, Certificate
)
from datetime import datetime, timezone
import uuid


class CourseService:
    @staticmethod
    def create_course(db: Session, org_id: int, instructor_id: int, course_data: dict) -> Course:
        course = Course(organization_id=org_id, instructor_id=instructor_id, **course_data)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def get_course(db: Session, course_id: int) -> Course:
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def list_courses(db: Session, org_id: int, status: str = None):
        query = db.query(Course).filter(Course.organization_id == org_id)
        if status:
            query = query.filter(Course.status == status)
        return query.all()

    @staticmethod
    def update_course(db: Session, course_id: int, update_data: dict) -> Course:
        course = CourseService.get_course(db, course_id)
        for key, value in update_data.items():
            setattr(course, key, value)
        course.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def publish_course(db: Session, course_id: int):
        course = CourseService.get_course(db, course_id)
        course.status = "published"
        db.commit()

    @staticmethod
    def search_courses(db: Session, org_id: int, search_term: str):
        return db.query(Course).filter(
            and_(
                Course.organization_id == org_id,
                Course.status == "published",
                Course.title.ilike(f"%{search_term}%")
            )
        ).all()


class LessonService:
    @staticmethod
    def create_lesson(db: Session, course_id: int, section_id: int, lesson_data: dict) -> Lesson:
        lesson = Lesson(course_id=course_id, section_id=section_id, **lesson_data)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def get_lesson(db: Session, lesson_id: int) -> Lesson:
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()

    @staticmethod
    def update_lesson(db: Session, lesson_id: int, update_data: dict) -> Lesson:
        lesson = LessonService.get_lesson(db, lesson_id)
        for key, value in update_data.items():
            setattr(lesson, key, value)
        lesson.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(lesson)
        return lesson


class CourseSectionService:
    @staticmethod
    def create_section(db: Session, course_id: int, section_data: dict) -> CourseSection:
        section = CourseSection(course_id=course_id, **section_data)
        db.add(section)
        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def get_section(db: Session, section_id: int) -> CourseSection:
        return db.query(CourseSection).filter(CourseSection.id == section_id).first()

    @staticmethod
    def get_course_sections(db: Session, course_id: int):
        return db.query(CourseSection).filter(CourseSection.course_id == course_id).order_by(
            CourseSection.order
        ).all()


class EnrollmentService:
    @staticmethod
    def enroll_student(db: Session, user_id: int, course_id: int) -> CourseEnrollment:
        course = db.query(Course).filter(Course.id == course_id).first()
        total_lessons = db.query(Lesson).filter(Lesson.course_id == course_id).count()

        enrollment = CourseEnrollment(
            user_id=user_id,
            course_id=course_id,
            total_lessons=total_lessons
        )
        db.add(enrollment)

        course.total_enrollments += 1

        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def get_enrollment(db: Session, enrollment_id: int) -> CourseEnrollment:
        return db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()

    @staticmethod
    def get_user_enrollments(db: Session, user_id: int):
        return db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user_id).all()

    @staticmethod
    def complete_enrollment(db: Session, enrollment_id: int):
        enrollment = EnrollmentService.get_enrollment(db, enrollment_id)
        enrollment.status = "completed"
        enrollment.completed_date = datetime.now(timezone.utc)
        enrollment.progress_percentage = 100.0
        db.commit()

    @staticmethod
    def drop_course(db: Session, enrollment_id: int):
        enrollment = EnrollmentService.get_enrollment(db, enrollment_id)
        enrollment.status = "dropped"
        db.commit()

    @staticmethod
    def update_progress(db: Session, enrollment_id: int):
        enrollment = EnrollmentService.get_enrollment(db, enrollment_id)
        completed = db.query(StudentLessonProgress).filter(
            and_(
                StudentLessonProgress.enrollment_id == enrollment_id,
                StudentLessonProgress.is_completed == True
            )
        ).count()

        if enrollment.total_lessons > 0:
            enrollment.progress_percentage = (completed / enrollment.total_lessons) * 100
            enrollment.lessons_completed = completed

        db.commit()


class StudentLessonProgressService:
    @staticmethod
    def mark_lesson_complete(db: Session, enrollment_id: int, lesson_id: int):
        progress = db.query(StudentLessonProgress).filter(
            and_(
                StudentLessonProgress.enrollment_id == enrollment_id,
                StudentLessonProgress.lesson_id == lesson_id
            )
        ).first()

        if not progress:
            progress = StudentLessonProgress(
                enrollment_id=enrollment_id,
                lesson_id=lesson_id
            )
            db.add(progress)

        progress.is_completed = True
        progress.completion_percentage = 100.0
        progress.completed_date = datetime.now(timezone.utc)
        db.commit()

        EnrollmentService.update_progress(db, enrollment_id)

    @staticmethod
    def get_lesson_progress(db: Session, enrollment_id: int, lesson_id: int):
        return db.query(StudentLessonProgress).filter(
            and_(
                StudentLessonProgress.enrollment_id == enrollment_id,
                StudentLessonProgress.lesson_id == lesson_id
            )
        ).first()

    @staticmethod
    def update_watch_time(db: Session, enrollment_id: int, lesson_id: int, watch_time: int):
        progress = StudentLessonProgressService.get_lesson_progress(db, enrollment_id, lesson_id)
        if progress:
            progress.video_watch_time = watch_time
            db.commit()


class CourseReviewService:
    @staticmethod
    def create_review(db: Session, course_id: int, user_id: int, review_data: dict) -> CourseReview:
        review = CourseReview(course_id=course_id, user_id=user_id, **review_data)
        db.add(review)

        course = db.query(Course).filter(Course.id == course_id).first()
        course.total_reviews += 1
        all_reviews = db.query(CourseReview).filter(CourseReview.course_id == course_id).all()
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else 0
        course.average_rating = avg_rating

        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_course_reviews(db: Session, course_id: int):
        return db.query(CourseReview).filter(CourseReview.course_id == course_id).order_by(
            CourseReview.created_at.desc()
        ).all()


class AssignmentService:
    @staticmethod
    def create_assignment(db: Session, course_id: int, assignment_data: dict) -> Assignment:
        assignment = Assignment(course_id=course_id, **assignment_data)
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def get_assignment(db: Session, assignment_id: int) -> Assignment:
        return db.query(Assignment).filter(Assignment.id == assignment_id).first()

    @staticmethod
    def publish_assignment(db: Session, assignment_id: int):
        assignment = AssignmentService.get_assignment(db, assignment_id)
        assignment.status = "assigned"
        db.commit()


class AssignmentSubmissionService:
    @staticmethod
    def submit_assignment(db: Session, assignment_id: int, user_id: int,
                         submission_data: dict) -> AssignmentSubmission:
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            user_id=user_id,
            status="submitted",
            submitted_date=datetime.now(timezone.utc),
            **submission_data
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def grade_submission(db: Session, submission_id: int, score: float, feedback: str, graded_by: int):
        submission = db.query(AssignmentSubmission).filter(
            AssignmentSubmission.id == submission_id
        ).first()
        submission.status = "graded"
        submission.score = score
        submission.feedback = feedback
        submission.graded_by = graded_by
        submission.graded_date = datetime.now(timezone.utc)
        db.commit()


class CertificateService:
    @staticmethod
    def issue_certificate(db: Session, course_id: int, user_id: int) -> Certificate:
        certificate_number = str(uuid.uuid4())
        certificate = Certificate(
            course_id=course_id,
            user_id=user_id,
            certificate_number=certificate_number,
            issue_date=datetime.now(timezone.utc)
        )
        db.add(certificate)

        enrollment = db.query(CourseEnrollment).filter(
            and_(
                CourseEnrollment.user_id == user_id,
                CourseEnrollment.course_id == course_id
            )
        ).first()
        if enrollment:
            enrollment.certificate_issued = True
            enrollment.certificate_url = f"/certificates/{certificate_number}"

        db.commit()
        db.refresh(certificate)
        return certificate
