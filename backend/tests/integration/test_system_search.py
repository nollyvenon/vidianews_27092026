"""Route tests for system search: results are the caller's organization's indexed resources, matched by title."""

from app.core.security import create_access_token
from app.models.user import User
from app.services.integrations_service import SearchService


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


class TestSystemSearch:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/system/search?q=launch")).status_code == 401

    async def test_matching_resources_of_the_callers_organization_are_returned(
        self, async_client, org_member, reference_data, session,
    ):
        await SearchService(session).index_resource(1, "video", 5, "Launch Video", "The launch recap")
        await SearchService(session).index_resource(1, "article", 6, "Quarterly Report", "Numbers")

        response = await async_client.get("/api/v1/system/search?q=launch", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert [(row["resource_type"], row["resource_id"], row["title"]) for row in rows] == [("video", 5, "Launch Video")]
        assert rows[0]["content"] == "The launch recap"

    async def test_resources_of_another_organization_are_not_returned(
        self, async_client, org_member, second_organization, reference_data, session,
    ):
        await SearchService(session).index_resource(2, "video", 9, "Launch Elsewhere", "Other org")

        response = await async_client.get("/api/v1/system/search?q=launch", headers=org_member)

        assert response.status_code == 200
        assert response.json() == []
