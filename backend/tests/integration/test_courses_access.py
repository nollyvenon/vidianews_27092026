"""Route tests for courses: who sees drafts, who may change content, grade, and certify."""

from app.models.tenants import TenantMember
from app.services.courses_service import (
    AssignmentService,
    AssignmentSubmissionService,
    EnrollmentService,
    LessonService,
    CourseSectionService,
)

COURSE = {"title": "Python Basics", "description": "Basics", "category": "Programming", "price": 0.0}


async def _make_student_in_tenant(session, user_id: int) -> None:
    session.add(TenantMember(tenant_id=1, user_id=user_id, role="member", status="active"))
    await session.commit()


async def _create_course(async_client, instructor_headers) -> int:
    response = await async_client.post("/api/v1/courses", json=COURSE, headers=instructor_headers)
    assert response.status_code == 201
    return response.json()["id"]


class TestDraftsAndManagement:
    async def test_the_creator_becomes_the_instructor(self, async_client, org_member, reference_data):
        response = await async_client.post("/api/v1/courses", json=COURSE, headers=org_member)
        assert response.status_code == 201
        assert response.json()["instructor_id"] == 1
        assert response.json()["organization_id"] == 1

    async def test_students_cannot_see_draft_courses(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)

        student = {"Authorization": (await _student_headers(session))}
        assert (await async_client.get(f"/api/v1/courses/{course_id}", headers=student)).status_code == 404
        listed = (await async_client.get("/api/v1/courses", headers=student)).json()
        assert all(item["id"] != course_id for item in listed)

    async def test_students_cannot_change_or_publish_a_course(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        student = {"Authorization": (await _student_headers(session))}

        updated = await async_client.put(f"/api/v1/courses/{course_id}", json={"title": "Hijacked"}, headers=student)
        published = await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=student)
        assert updated.status_code == 403
        assert published.status_code == 403

    async def test_instructor_publishes_and_students_then_see_and_enroll(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        assert (await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)).status_code == 200

        student = {"Authorization": (await _student_headers(session))}
        assert (await async_client.get(f"/api/v1/courses/{course_id}", headers=student)).status_code == 200
        assert (await async_client.post(f"/api/v1/courses/{course_id}/enroll", headers=student)).status_code == 201

    async def test_empty_course_update_is_refused(self, async_client, org_member, reference_data):
        course_id = await _create_course(async_client, org_member)
        response = await async_client.put(f"/api/v1/courses/{course_id}", json={}, headers=org_member)
        assert response.status_code == 422

    async def test_a_course_of_another_tenant_is_not_found(self, async_client, org_member, reference_data, session):
        from app.models.courses import Course

        other = Course(organization_id=99, instructor_id=2, title="Elsewhere", status="published")
        session.add(other)
        await session.commit()
        assert (await async_client.get(f"/api/v1/courses/{other.id}", headers=org_member)).status_code == 404


class TestStudentActions:
    async def test_students_mark_only_their_own_progress(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)
        section = await CourseSectionService(session).create_section(course_id, {"title": "S1", "order": 1})
        lesson = await LessonService(session).create_lesson(course_id, section.id, {"title": "L1", "order": 1})
        own = await EnrollmentService(session).enroll_student(2, course_id)
        instructors = await EnrollmentService(session).enroll_student(1, course_id)

        student = {"Authorization": (await _student_headers(session))}
        mine = await async_client.post(f"/api/v1/enrollments/{own.id}/lessons/{lesson.id}/complete", headers=student)
        theirs = await async_client.post(f"/api/v1/enrollments/{instructors.id}/lessons/{lesson.id}/complete", headers=student)
        missing = await async_client.post(f"/api/v1/enrollments/{own.id}/lessons/999999/complete", headers=student)
        assert mine.status_code == 200
        assert theirs.status_code == 403
        assert missing.status_code == 404

    async def test_reviews_are_for_enrolled_students_only(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)
        student = {"Authorization": (await _student_headers(session))}

        before = await async_client.post(f"/api/v1/courses/{course_id}/reviews", json={"rating": 5}, headers=student)
        await EnrollmentService(session).enroll_student(2, course_id)
        after = await async_client.post(f"/api/v1/courses/{course_id}/reviews", json={"rating": 5}, headers=student)

        assert before.status_code == 403
        assert after.status_code == 201

    async def test_students_cannot_certify_someone_elses_enrollment(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)
        other = await EnrollmentService(session).enroll_student(1, course_id)
        await EnrollmentService(session).complete_enrollment(other.id)

        student = {"Authorization": (await _student_headers(session))}
        response = await async_client.post(f"/api/v1/enrollments/{other.id}/certificate", headers=student)
        assert response.status_code == 403

    async def test_students_get_their_certificate_once_completed(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)
        own = await EnrollmentService(session).enroll_student(2, course_id)
        student = {"Authorization": (await _student_headers(session))}

        early = await async_client.post(f"/api/v1/enrollments/{own.id}/certificate", headers=student)
        await EnrollmentService(session).complete_enrollment(own.id)
        done = await async_client.post(f"/api/v1/enrollments/{own.id}/certificate", headers=student)

        assert early.status_code == 403
        assert done.status_code == 201


class TestGrading:
    async def test_only_the_instructor_grades(self, async_client, org_member, reference_data, session):
        await _make_student_in_tenant(session, 2)
        course_id = await _create_course(async_client, org_member)
        await async_client.post(f"/api/v1/courses/{course_id}/publish", headers=org_member)
        await EnrollmentService(session).enroll_student(2, course_id)
        assignment = await AssignmentService(session).create_assignment(course_id, {"title": "A1"})
        submission = await AssignmentSubmissionService(session).submit_assignment(assignment.id, 2, {"content": "x"})

        student = {"Authorization": (await _student_headers(session))}
        refused = await async_client.post(
            f"/api/v1/submissions/{submission.id}/grade?score=90&feedback=ok", headers=student,
        )
        graded = await async_client.post(
            f"/api/v1/submissions/{submission.id}/grade?score=90&feedback=ok", headers=org_member,
        )
        assert refused.status_code == 403
        assert graded.status_code == 200

    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/courses")).status_code == 401


async def _student_headers(session) -> str:
    from app.core.security import create_access_token
    from app.models.user import User

    user = await session.get(User, 2)
    return f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"
