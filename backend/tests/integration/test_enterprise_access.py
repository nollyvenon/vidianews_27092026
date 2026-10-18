"""Route tests for enterprise features: privilege changes are administrator-only, and users act on their own records."""

from app.core.security import create_access_token
from app.models.user import User
from app.services.enterprise_features_service import (
    ModerationService,
    NotificationService,
    ReportingService,
    SecurityService,
)
from app.models.enterprise_features import AccessLevel, NotificationType, ReportFormat

GRANT = {
    "resource_type": "course", "resource_id": 5, "access_level": AccessLevel.PRIVATE.value,
    "permissions": ["read"], "granted_by": 1,
}
ROLE = {"role": "editor", "permissions": ["content:write"], "can_edit_content": True}
NOTICE = {"notification_type": NotificationType.INFO.value, "title": "Hi", "message": "Welcome"}
TEMPLATE = {"name": "Weekly", "report_type": "sales", "sections": ["summary"], "format": ReportFormat.JSON.value}


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


class TestPrivilegeChangesAreAdministratorOnly:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/security/audit-logs")).status_code == 401

    async def test_customers_cannot_grant_access_to_themselves(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post("/api/v1/security/access-control/2", json=GRANT, headers=headers)
        assert response.status_code == 403

    async def test_customers_cannot_assign_roles(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post("/api/v1/security/roles/2", json=ROLE, headers=headers)
        assert response.status_code == 403
        assert (await async_client.get("/api/v1/security/roles/2", headers=headers)).status_code == 404

    async def test_customers_cannot_write_audit_entries(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post(
            "/api/v1/security/audit-logs?user_id=2&action=forged", headers=headers,
        )
        assert response.status_code == 403

    async def test_customers_cannot_send_notifications_to_others(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post("/api/v1/enterprise/notifications/?user_id=1", json=NOTICE, headers=headers)
        assert response.status_code == 403

    async def test_customers_cannot_create_report_templates(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        assert (await async_client.post("/api/v1/reports/templates", json=TEMPLATE, headers=headers)).status_code == 403

    async def test_administrator_grants_and_revokes_access(self, async_client, platform_admin, reference_data, session):
        granted = await async_client.post("/api/v1/security/access-control/2", json=GRANT, headers=platform_admin)
        assert granted.status_code == 201
        assert granted.json()["permissions"] == ["read"]

        check = await async_client.post(
            "/api/v1/security/check-permission?user_id=2&resource_type=course&resource_id=5&permission=read",
            headers=await _headers_for(session, 2),
        )
        assert check.json() == {"has_permission": True}

        revoked = await async_client.delete("/api/v1/security/access-control/2/course/5", headers=platform_admin)
        assert revoked.status_code == 200
        assert (await async_client.delete("/api/v1/security/access-control/2/course/5", headers=platform_admin)).status_code == 404

    async def test_administrator_assigns_a_role(self, async_client, platform_admin, reference_data, session):
        response = await async_client.post("/api/v1/security/roles/2", json=ROLE, headers=platform_admin)
        assert response.status_code == 201
        assert response.json()["can_edit_content"] is True
        fetched = await async_client.get("/api/v1/security/roles/2", headers=await _headers_for(session, 2))
        assert fetched.json()["role"] == "editor"

    async def test_administrator_sends_a_notification(self, async_client, platform_admin, reference_data, session):
        response = await async_client.post("/api/v1/enterprise/notifications/?user_id=2", json=NOTICE, headers=platform_admin)
        assert response.status_code == 201
        assert response.json()["user_id"] == 2


class TestOwnRecords:
    async def test_users_cannot_check_or_read_others_permissions(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        check = await async_client.post(
            "/api/v1/security/check-permission?user_id=1&resource_type=course&resource_id=5&permission=read",
            headers=headers,
        )
        role = await async_client.get("/api/v1/security/roles/1", headers=headers)
        assert check.status_code == 403
        assert role.status_code == 403

    async def test_audit_log_is_limited_to_the_caller(self, async_client, org_member, reference_data, session):
        await SecurityService(session).log_audit_event(1, "other-user-action")
        await SecurityService(session).log_audit_event(2, "my-action")
        headers = await _headers_for(session, 2)
        mine = await async_client.get("/api/v1/security/audit-logs", headers=headers)
        assert [row["action"] for row in mine.json()] == ["my-action"]
        others = await async_client.get("/api/v1/security/audit-logs?user_id=1", headers=headers)
        assert others.status_code == 403

    async def test_users_update_only_their_own_preferences(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        own = await async_client.put(
            "/api/v1/enterprise/notifications/preferences/2", json={"email_enabled": False}, headers=headers,
        )
        assert own.status_code == 200
        assert own.json()["email_enabled"] is False
        theirs = await async_client.put(
            "/api/v1/enterprise/notifications/preferences/1", json={"email_enabled": False}, headers=headers,
        )
        assert theirs.status_code == 403

    async def test_users_cannot_mark_others_notifications_read(self, async_client, org_member, reference_data, session):
        notice = await NotificationService(session).create_notification(1, NotificationType.INFO, "Private", "for user 1")
        headers = await _headers_for(session, 2)
        response = await async_client.post(f"/api/v1/enterprise/notifications/{notice.id}/mark-read", headers=headers)
        assert response.status_code == 404
        still_unread = await NotificationService(session).get_notification(notice.id)
        assert still_unread.read is False

    async def test_owner_marks_their_notification_read(self, async_client, org_member, reference_data, session):
        notice = await NotificationService(session).create_notification(2, NotificationType.INFO, "Mine", "for user 2")
        headers = await _headers_for(session, 2)
        response = await async_client.post(f"/api/v1/enterprise/notifications/{notice.id}/mark-read", headers=headers)
        assert response.json() == {"read": True}
        listed = await async_client.get("/api/v1/enterprise/notifications/?unread_only=true", headers=headers)
        assert listed.json() == []

    async def test_customers_cannot_review_moderation_items(self, async_client, org_member, reference_data, session):
        item = await ModerationService(session).submit_for_moderation(1, "post", "spam")
        headers = await _headers_for(session, 2)
        review = await async_client.post(
            f"/api/v1/moderation/queue/{item.id}/review", json={"status": "approved", "decision": "ok"}, headers=headers,
        )
        assert review.status_code == 403
        assert (await async_client.get("/api/v1/moderation/queue/pending", headers=headers)).status_code == 403

    async def test_moderator_reviews_with_their_own_identity(self, async_client, platform_admin, reference_data, session):
        item = await ModerationService(session).submit_for_moderation(1, "post", "spam")
        review = await async_client.post(
            f"/api/v1/moderation/queue/{item.id}/review", json={"status": "rejected", "decision": "spam"}, headers=platform_admin,
        )
        assert review.status_code == 200
        assert review.json() == {"reviewed": True, "status": "rejected"}
        refreshed = await ModerationService(session).get_pending_items()
        assert refreshed == []

    async def test_export_jobs_are_visible_to_their_owner_only(self, async_client, org_member, reference_data, session):
        job = await ReportingService(session).create_export_job(2, "orders", ReportFormat.CSV)
        owner = await async_client.get(f"/api/v1/reports/exports/{job.id}", headers=await _headers_for(session, 2))
        stranger = await async_client.get(f"/api/v1/reports/exports/{job.id}", headers=org_member)
        assert owner.status_code == 200
        assert owner.json()["status"] == "pending"
        assert stranger.status_code == 404

    async def test_users_export_only_their_own_data(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        own = await async_client.post("/api/v1/reports/exports?user_id=2", json={"export_type": "orders", "format": "csv"}, headers=headers)
        theirs = await async_client.post("/api/v1/reports/exports?user_id=1", json={"export_type": "orders", "format": "csv"}, headers=headers)
        assert own.status_code == 201
        assert theirs.status_code == 403

    async def test_export_progress_is_reported_by_administrators(self, async_client, platform_admin, reference_data, session):
        job = await ReportingService(session).create_export_job(2, "orders", ReportFormat.CSV)
        customer = await async_client.put(f"/api/v1/reports/exports/{job.id}/progress?progress=10", headers=await _headers_for(session, 2))
        worker = await async_client.put(f"/api/v1/reports/exports/{job.id}/progress?progress=100&record_count=9", headers=platform_admin)
        assert customer.status_code == 403
        assert worker.json() == {"progress": 100, "status": "completed"}


class TestRateLimitRoutes:
    async def test_rate_limit_check_without_a_config_is_not_limited(self, async_client, reference_data, session):
        response = await async_client.post("/api/v1/rate-limits/check?endpoint=/search", headers=await _headers_for(session, 2))
        assert response.status_code == 200
        assert response.json()["limited"] is False

    async def test_rate_limit_configuration_is_administrator_only(self, async_client, platform_admin, reference_data, session):
        customer = await _headers_for(session, 2)
        body = {"endpoint": "/search", "requests_per_minute": 5}
        assert (await async_client.post("/api/v1/rate-limits/config?user_id=2", json=body, headers=customer)).status_code == 403
        assert (await async_client.get("/api/v1/rate-limits/configs", headers=customer)).status_code == 403

        created = await async_client.post("/api/v1/rate-limits/config?user_id=2", json=body, headers=platform_admin)
        assert created.status_code == 201
        listed = await async_client.get("/api/v1/rate-limits/configs", headers=platform_admin)
        assert [row["endpoint"] for row in listed.json()] == ["/search"]
