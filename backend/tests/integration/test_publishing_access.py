"""Route tests for A/B testing and recommendations: organization scoping and the signed-in user"""

import pytest
from sqlalchemy.orm import Session

from app.models.publishing_distribution import (
    ABTestCampaign, ABTestVariant, RecommendationEngine, RecommendationLog, RecommendationType, SyndicationLog,
)


@pytest.fixture
def other_org_records(second_organization, reset_test_database):
    """A campaign with a variant, an engine and a recommendation log that belong to organization 2."""
    with Session(reset_test_database) as session:
        campaign = ABTestCampaign(
            organization_id=2, content_id=1, name="Other campaign", test_metric="clicks", hypothesis="Other",
        )
        session.add(campaign)
        session.flush()
        variant = ABTestVariant(ab_test_campaign_id=campaign.id, variant_name="A", variant_type="control")
        engine = RecommendationEngine(
            organization_id=2, name="Other engine", recommendation_type=RecommendationType.HYBRID, is_active=True,
        )
        log = RecommendationLog(organization_id=2, recommended_content_ids=[1], recommendation_scores=[0.5])
        session.add_all([variant, engine, log])
        session.flush()
        ids = {"campaign": campaign.id, "variant": variant.id, "engine": engine.id, "log": log.id}
        session.commit()
    return ids


class TestABTestingAccess:
    async def test_campaign_list_contains_only_the_callers_organization(self, async_client, org_member, other_org_records):
        created = await async_client.post(
            "/api/v1/ab-testing/campaigns",
            json={"content_id": 1, "name": "Subject line", "test_metric": "clicks", "hypothesis": "Shorter wins"},
            headers=org_member,
        )
        assert created.status_code == 200

        listed = await async_client.get("/api/v1/ab-testing/campaigns", headers=org_member)

        assert listed.status_code == 200
        names = [campaign["name"] for campaign in listed.json()]
        assert names == ["Subject line"]

    async def test_variants_and_results_of_another_organization_are_not_found(self, async_client, org_member, other_org_records):
        campaign = other_org_records["campaign"]
        variant = other_org_records["variant"]

        add = await async_client.post(
            f"/api/v1/ab-testing/campaigns/{campaign}/variants",
            json={"variant_name": "B", "variant_type": "treatment"},
            headers=org_member,
        )
        record = await async_client.patch(
            f"/api/v1/ab-testing/variants/{variant}/performance?impressions=1&clicks=1&conversions=1",
            headers=org_member,
        )
        analyze = await async_client.post(f"/api/v1/ab-testing/campaigns/{campaign}/analyze", headers=org_member)

        assert add.status_code == 404
        assert record.status_code == 404
        assert analyze.status_code == 404

    async def test_own_campaign_can_be_built_measured_and_analyzed(self, async_client, org_member):
        created = await async_client.post(
            "/api/v1/ab-testing/campaigns",
            json={"content_id": 1, "name": "CTA", "test_metric": "conversion", "hypothesis": "Green converts"},
            headers=org_member,
        )
        campaign_id = created.json()["id"]
        variant_ids = []
        for name, variant_type in (("Blue", "control"), ("Green", "treatment")):
            added = await async_client.post(
                f"/api/v1/ab-testing/campaigns/{campaign_id}/variants",
                json={"variant_name": name, "variant_type": variant_type},
                headers=org_member,
            )
            assert added.status_code == 200
            variant_ids.append(added.json()["id"])
        await async_client.patch(
            f"/api/v1/ab-testing/variants/{variant_ids[0]}/performance?impressions=100&clicks=20&conversions=5",
            headers=org_member,
        )
        await async_client.patch(
            f"/api/v1/ab-testing/variants/{variant_ids[1]}/performance?impressions=100&clicks=30&conversions=12",
            headers=org_member,
        )

        analyzed = await async_client.post(f"/api/v1/ab-testing/campaigns/{campaign_id}/analyze", headers=org_member)

        assert analyzed.status_code == 200
        body = analyzed.json()
        assert set(body) == {"id", "p_value", "is_significant", "improvement_percent", "recommended_action"}
        listed = (await async_client.get("/api/v1/ab-testing/campaigns", headers=org_member)).json()
        assert [variant["variant_name"] for variant in listed[0]["variants"]] == ["Blue", "Green"]
        assert listed[0]["variants"][1]["clicks"] == 30
        assert listed[0]["variants"][1]["ctr"] == pytest.approx(30.0)

    async def test_campaign_creation_needs_an_organization(self, async_client, unaffiliated_user):
        response = await async_client.post(
            "/api/v1/ab-testing/campaigns",
            json={"content_id": 1, "name": "CTA", "test_metric": "clicks", "hypothesis": "Green"},
            headers=unaffiliated_user,
        )

        assert response.status_code == 422


class TestRecommendationAccess:
    async def test_engines_are_created_and_listed_for_the_callers_organization(self, async_client, org_member, other_org_records):
        created = await async_client.post(
            "/api/v1/content-recommendations/engines",
            json={"name": "Main engine", "recommendation_type": "hybrid"},
            headers=org_member,
        )
        listed = await async_client.get("/api/v1/content-recommendations/engines", headers=org_member)

        assert created.status_code == 201, created.text
        assert created.json()["recommendation_type"] == "hybrid"
        assert [engine["name"] for engine in listed.json()] == ["Main engine"]

    async def test_engine_creation_rejects_an_unknown_type(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/content-recommendations/engines",
            json={"name": "Magic", "recommendation_type": "magic"},
            headers=org_member,
        )

        assert response.status_code == 422

    async def test_recommendations_are_generated_for_the_signed_in_user(self, async_client, org_member):
        engine = await async_client.post(
            "/api/v1/content-recommendations/engines",
            json={"name": "Main engine", "recommendation_type": "hybrid"},
            headers=org_member,
        )
        response = await async_client.post(
            f"/api/v1/content-recommendations/generate?engine_id={engine.json()['id']}",
            json={"content_pool": [1], "num_recommendations": 1},
            headers=org_member,
        )

        assert response.status_code == 200, response.text
        assert set(response.json()) == {"id", "recommended_content_ids", "recommendation_scores"}

    async def test_recommendations_cannot_be_generated_for_another_user(self, async_client, org_member):
        engine = await async_client.post(
            "/api/v1/content-recommendations/engines",
            json={"name": "Main engine", "recommendation_type": "hybrid"},
            headers=org_member,
        )
        response = await async_client.post(
            f"/api/v1/content-recommendations/generate?engine_id={engine.json()['id']}",
            json={"user_id": 2, "content_pool": [1], "num_recommendations": 1},
            headers=org_member,
        )

        assert response.status_code == 403

    async def test_another_organizations_engine_is_not_found(self, async_client, org_member, other_org_records):
        response = await async_client.post(
            f"/api/v1/content-recommendations/generate?engine_id={other_org_records['engine']}",
            json={"content_pool": [1], "num_recommendations": 1},
            headers=org_member,
        )

        assert response.status_code == 404, response.text

    async def test_clicks_on_another_organizations_recommendation_are_not_found(self, async_client, org_member, other_org_records):
        response = await async_client.post(
            f"/api/v1/content-recommendations/logs/{other_org_records['log']}/click?clicked_content_id=1",
            headers=org_member,
        )

        assert response.status_code == 404


class TestRouteReachability:
    async def test_engagement_metrics_route_reaches_the_publishing_handler(self, async_client, org_member):
        """Without a recorded metric the publishing handler answers 404 'Metrics not found'; a shadowing route would not."""
        response = await async_client.get("/api/v1/analytics/metrics/1", headers=org_member)

        assert response.status_code == 404
        assert response.json()["detail"] == "Metrics not found"

    async def test_publishing_channels_route_is_reachable(self, async_client, org_member):
        response = await async_client.get("/api/v1/distribution/channels", headers=org_member)

        assert response.status_code == 200
        assert response.json() == []


class TestSyndicationPartners:
    async def test_partners_list_the_articles_and_reach_each_partner_produced(self, async_client, org_member, reset_test_database):
        created = await async_client.post(
            "/api/v1/distribution/syndication-profiles",
            json={"partner_name": "Partner News", "partner_type": "newsletter", "api_endpoint": "https://partner.example.test/api"},
            headers=org_member,
        )
        assert created.status_code == 201
        profile_id = created.json()["id"]

        with Session(reset_test_database) as session:
            session.add_all([
                SyndicationLog(organization_id=1, syndication_profile_id=profile_id, content_id=1, status="success", impressions=120),
                SyndicationLog(organization_id=1, syndication_profile_id=profile_id, content_id=1, status="success", impressions=30),
            ])
            session.commit()

        response = await async_client.get("/api/v1/distribution/syndication-profiles", headers=org_member)

        assert response.status_code == 200
        assert response.json() == [{
            "id": profile_id,
            "partner_name": "Partner News",
            "partner_type": "newsletter",
            "articles_syndicated": 2,
            "reach": 150,
        }]

    async def test_a_partner_with_no_deliveries_reports_zero(self, async_client, org_member):
        await async_client.post(
            "/api/v1/distribution/syndication-profiles",
            json={"partner_name": "Quiet Partner", "partner_type": "rss"},
            headers=org_member,
        )

        rows = (await async_client.get("/api/v1/distribution/syndication-profiles", headers=org_member)).json()

        assert rows[0]["articles_syndicated"] == 0
        assert rows[0]["reach"] == 0
