"""Route tests for discovery: a user's recommended content and the platform's trending topics"""

import pytest
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.social_messaging import DiscoveryRecommendation, SearchQuery
from app.models.user import User


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


def _seed(engine, *, creator_id=1, views=42):
    with Session(engine) as session:
        seed_user = session.get(User, 1)
        seed_user.first_name = "Seed"
        seed_user.last_name = "Creator"
        content = session.get(Content, 1)
        content.creator_user_id = creator_id
        content.views_count = views
        session.add_all([
            DiscoveryRecommendation(user_id=1, content_id=1, recommendation_score=0.9, reason="Matches your interests"),
            DiscoveryRecommendation(user_id=2, content_id=1, recommendation_score=0.99, reason="Someone else's"),
            *[SearchQuery(user_id=1, query="Python ") for _ in range(3)],
            SearchQuery(user_id=2, query="webdesign"),
            SearchQuery(user_id=2, query="old topic", searched_at=datetime.now(timezone.utc) - timedelta(days=30)),
        ])
        session.commit()


class TestRecommendations:
    async def test_recommendations_carry_the_content_title_creator_views_and_reason(self, async_client, org_member, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/recommendations", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert len(rows) == 1
        assert rows[0]["content_id"] == 1
        assert rows[0]["title"] == "Seed Content"
        assert rows[0]["creator"] == "Seed Creator"
        assert rows[0]["views"] == 42
        assert rows[0]["reason"] == "Matches your interests"
        assert rows[0]["score"] == 0.9

    async def test_recommendations_are_only_the_signed_in_users(self, async_client, unaffiliated_user, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/recommendations", headers=unaffiliated_user)

        assert response.status_code == 200
        assert [row["reason"] for row in response.json()] == ["Someone else's"]

    async def test_a_recommended_item_without_a_creator_has_no_creator_name(self, async_client, org_member, reset_test_database):
        _seed(reset_test_database, creator_id=None)

        response = await async_client.get("/api/v1/recommendations", headers=org_member)

        assert response.json()[0]["creator"] is None

    async def test_the_limit_is_clamped_to_a_sane_range(self, async_client, org_member, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/recommendations?limit=0", headers=org_member)

        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_recommendations_require_a_signed_in_user(self, async_client, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/recommendations")

        assert response.status_code in (401, 403)


class TestTrendingTopics:
    async def test_topics_are_ranked_by_trend_score_with_their_mention_counts(self, async_client, org_member, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/trending?limit=5", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert [row["topic"] for row in rows] == ["python", "webdesign"]
        assert rows[0]["mention_count"] == 3
        assert rows[0]["score"] == 3.0
        assert "old topic" not in [row["topic"] for row in rows]

    async def test_trending_requires_a_signed_in_user(self, async_client, reset_test_database):
        _seed(reset_test_database)

        response = await async_client.get("/api/v1/trending")

        assert response.status_code in (401, 403)
