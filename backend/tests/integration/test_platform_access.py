"""Route tests for platform completion: users act only as themselves, and platform operations are for administrators."""

from app.core.security import create_access_token
from app.models.platform_completion import AdminActionType, InteractionType, PushNotificationType, SearchIndexType
from app.models.user import User
from app.services.platform_completion_service import PushNotificationService, SocialService


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


class TestActingAsTheCaller:
    async def test_interactions_are_recorded_for_the_caller(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post(
            "/api/v1/platform/interactions", json={"content_id": 4, "interaction_type": "like"}, headers=headers,
        )
        assert response.status_code == 201
        assert response.json()["user_id"] == 2

    async def test_naming_another_user_is_refused(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        response = await async_client.post(
            "/api/v1/platform/interactions?user_id=1", json={"content_id": 4, "interaction_type": "like"}, headers=headers,
        )
        assert response.status_code == 403

    async def test_users_cannot_read_someone_elses_conversation(self, async_client, org_member, reference_data, session):
        await SocialService.send_message(session, 1, 2, "private hello")
        headers = await _headers_for(session, 2)
        refused = await async_client.get("/api/v1/platform/conversations/1?user_id=1", headers=headers)
        allowed = await async_client.get("/api/v1/platform/conversations/1", headers=headers)
        assert refused.status_code == 403
        assert allowed.status_code == 200
        assert [m["text"] for m in allowed.json()] == ["private hello"]

    async def test_users_cannot_read_someone_elses_devices_or_logs(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        assert (await async_client.get("/api/v1/platform/devices?user_id=1", headers=headers)).status_code == 403
        assert (await async_client.get("/api/v1/platform/notifications/logs?user_id=1", headers=headers)).status_code == 403

    async def test_comment_and_follow_show_their_stored_fields(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        comment = await async_client.post("/api/v1/platform/comments", json={"content_id": 1, "text": "Great"}, headers=headers)
        follow = await async_client.post("/api/v1/platform/follow", json={"following_id": 1}, headers=headers)
        assert comment.status_code == 201
        assert comment.json()["status"] == "published"
        assert follow.status_code == 201
        assert follow.json()["created_at"]

        followers = await async_client.get("/api/v1/platform/followers/1", headers=await _headers_for(session, 1))
        assert followers.status_code == 200
        assert followers.json()[0]["follower_id"] == 2


class TestEnumInputs:
    async def test_unknown_interaction_type_is_refused(self, async_client, reference_data, session):
        response = await async_client.post(
            "/api/v1/platform/interactions", json={"content_id": 1, "interaction_type": "teleport"},
            headers=await _headers_for(session, 2),
        )
        assert response.status_code == 422

    async def test_unknown_notification_type_is_refused(self, async_client, reference_data, session):
        response = await async_client.post(
            "/api/v1/platform/notifications/log",
            json={"notification_type": "spam", "title": "t", "body": "b"},
            headers=await _headers_for(session, 2),
        )
        assert response.status_code == 422


class TestPlatformOperationsAreAdministratorOnly:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/platform/dashboard-summary")).status_code == 401

    async def test_customers_cannot_run_platform_operations(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        requests = [
            ("post", "/api/v1/platform/admin/users", {"user_id": 2, "role": "owner"}),
            ("get", "/api/v1/platform/admin/logs", None),
            ("post", "/api/v1/platform/admin/logs", {"action_type": "audit", "resource_type": "x", "resource_id": 1}),
            ("post", "/api/v1/platform/system/notifications", {"title": "t", "message": "m", "notification_type": "info"}),
            ("post", "/api/v1/platform/statistics", {"metric_name": "m", "metric_value": 1.0}),
            ("get", "/api/v1/platform/statistics", None),
            ("get", "/api/v1/platform/dashboard-summary", None),
            ("post", "/api/v1/platform/search-index", {"content_id": 1, "index_type": "content", "title": "t", "content": "c"}),
            ("put", "/api/v1/platform/notifications/1/status?status=delivered", None),
        ]
        for method, path, body in requests:
            kwargs = {"headers": headers}
            if body is not None:
                kwargs["json"] = body
            response = await getattr(async_client, method)(path, **kwargs)
            assert response.status_code == 403, (method, path)

    async def test_administrator_manages_admins_and_the_action_trail(self, async_client, platform_admin, reference_data, session):
        made = await async_client.post("/api/v1/platform/admin/users", json={"user_id": 2, "role": "support"}, headers=platform_admin)
        assert made.status_code == 201
        assert made.json()["role"] == "support"

        logged = await async_client.post(
            "/api/v1/platform/admin/logs?admin_user_id=1",
            json={"action_type": AdminActionType.CONTENT_MANAGE.value, "resource_type": "course", "resource_id": 5},
            headers=platform_admin,
        )
        assert logged.status_code == 201
        assert logged.json()["resource_type"] == "course"
        assert logged.json()["resource_id"] == 5

        trail = await async_client.get("/api/v1/platform/admin/logs", headers=platform_admin)
        assert [row["resource_type"] for row in trail.json()] == ["course"]

        permissions = await async_client.put(
            "/api/v1/platform/admin/users/2/permissions", json=["content:review"], headers=platform_admin,
        )
        assert permissions.status_code == 200
        assert permissions.json()["permissions"] == ["content:review"]

    async def test_administrator_cannot_log_actions_as_another_admin(self, async_client, platform_admin, reference_data, session):
        response = await async_client.post(
            "/api/v1/platform/admin/logs?admin_user_id=2",
            json={"action_type": AdminActionType.AUDIT.value, "resource_type": "x", "resource_id": 1},
            headers=platform_admin,
        )
        assert response.status_code == 403

    async def test_administrator_publishes_and_reads_system_notices(self, async_client, platform_admin, reference_data, session):
        published = await async_client.post(
            "/api/v1/platform/system/notifications",
            json={"title": "Maintenance", "message": "Tonight", "notification_type": "warning", "target_users": [2]},
            headers=platform_admin,
        )
        assert published.status_code == 201
        listed = await async_client.get("/api/v1/platform/system/notifications", headers=await _headers_for(session, 2))
        assert [n["title"] for n in listed.json()] == ["Maintenance"]

    async def test_administrator_reads_the_dashboard_and_statistics(self, async_client, platform_admin, reference_data, session):
        await SocialService.create_interaction(session, 2, 1, InteractionType.LIKE)
        summary = await async_client.get("/api/v1/platform/dashboard-summary", headers=platform_admin)
        assert summary.status_code == 200
        assert summary.json()["total_interactions"] == 1

        recorded = await async_client.post(
            "/api/v1/platform/statistics", json={"metric_name": "signups", "metric_value": 4.0}, headers=platform_admin,
        )
        assert recorded.status_code == 201
        aggregated = await async_client.get(
            "/api/v1/platform/statistics/aggregated?metric_name=signups", headers=await _headers_for(session, 2),
        )
        assert aggregated.json()["sum"] == 4.0

    async def test_administrator_maintains_the_search_index_and_users_search_it(self, async_client, platform_admin, reference_data, session):
        added = await async_client.post(
            "/api/v1/platform/search-index",
            json={"content_id": 1, "index_type": SearchIndexType.CONTENT.value, "title": "Zebra guide", "content": "stripes"},
            headers=platform_admin,
        )
        assert added.status_code == 201
        assert added.json()["content"] == "stripes"
        found = await async_client.get("/api/v1/platform/search?query=zebra", headers=await _headers_for(session, 2))
        assert [row["title"] for row in found.json()] == ["Zebra guide"]

    async def test_delivery_status_is_recorded_by_administrators(self, async_client, platform_admin, reference_data, session):
        entry = await PushNotificationService.log_notification(session, 2, PushNotificationType.SYSTEM, "T", "B")
        updated = await async_client.put(
            f"/api/v1/platform/notifications/{entry.id}/status?status=delivered", headers=platform_admin,
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "delivered"
