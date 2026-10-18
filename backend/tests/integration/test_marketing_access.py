"""Route tests for marketing: every record is scoped to the signed-in user's organization"""

import pytest
from app.models.organizations import OrganizationMember
from app.services.marketing_service import EmailCampaignService, LoyaltyService, SegmentationService

CAMPAIGN = {
    "name": "Launch",
    "subject": "We launched",
    "html_content": "<p>Hello</p>",
    "email_type": "promotional",
    "from_email": "news@example.com",
}


@pytest.fixture
async def other_org_records(second_organization, session):
    """A campaign, a segment, a loyalty program with a member, all owned by organization 2."""
    campaign = await EmailCampaignService(session).create_campaign(2, dict(CAMPAIGN, name="Other"))
    segment = await SegmentationService(session).create_segment(
        2, {"name": "Other segment", "segmentation_type": "custom"}
    )
    program = await LoyaltyService(session).create_program(2, {"name": "Other rewards", "points_per_dollar": 1.0})
    member = await LoyaltyService(session).enroll_member(program.id, 2)
    return {"campaign": campaign.id, "segment": segment.id, "program": program.id, "member": member.id}


class TestMarketingAccess:
    async def test_campaigns_are_created_for_the_callers_organization(self, async_client, org_member, reference_data):
        response = await async_client.post("/api/v1/campaigns", json=CAMPAIGN, headers=org_member)

        assert response.status_code == 200
        assert response.json()["organization_id"] == 1

    async def test_creating_a_campaign_needs_an_organization(self, async_client, unaffiliated_user):
        response = await async_client.post("/api/v1/campaigns", json=CAMPAIGN, headers=unaffiliated_user)

        assert response.status_code == 422

    async def test_another_organizations_campaign_is_not_found(self, async_client, org_member, other_org_records):
        campaign = other_org_records["campaign"]

        fetched = await async_client.get(f"/api/v1/campaigns/{campaign}", headers=org_member)
        sent = await async_client.post(f"/api/v1/campaigns/{campaign}/send", headers=org_member)

        assert fetched.status_code == 404
        assert sent.status_code == 404

    async def test_own_campaign_is_returned(self, async_client, org_member, reference_data):
        created = await async_client.post("/api/v1/campaigns", json=CAMPAIGN, headers=org_member)

        fetched = await async_client.get(f"/api/v1/campaigns/{created.json()['id']}", headers=org_member)

        assert fetched.status_code == 200
        assert fetched.json()["name"] == "Launch"

    async def test_another_organizations_segment_and_members_are_not_found(self, async_client, org_member, other_org_records):
        segment = other_org_records["segment"]

        fetched = await async_client.get(f"/api/v1/segments/{segment}", headers=org_member)
        members = await async_client.get(f"/api/v1/segments/{segment}/members", headers=org_member)

        assert fetched.status_code == 404
        assert members.status_code == 404

    async def test_own_segment_is_created_and_returned(self, async_client, org_member, reference_data):
        created = await async_client.post(
            "/api/v1/segments",
            json={"name": "Readers", "segmentation_type": "engagement"},
            headers=org_member,
        )

        fetched = await async_client.get(f"/api/v1/segments/{created.json()['id']}", headers=org_member)

        assert created.status_code == 200
        assert fetched.status_code == 200

    async def test_lead_scores_are_open_to_own_person_and_organization_members_only(
        self, async_client, org_member, reference_data, session,
    ):
        session.add(OrganizationMember(organization_id=1, user_id=2, role="member", status="active"))
        await session.commit()

        own = await async_client.get("/api/v1/leads/1/score", headers=org_member)
        colleague = await async_client.get("/api/v1/leads/2/score", headers=org_member)
        colleague_update = await async_client.put("/api/v1/leads/2/score?engagement=5", headers=org_member)
        own_update = await async_client.put("/api/v1/leads/1/score?engagement=5", headers=org_member)

        assert own.status_code == 200
        assert colleague.status_code == 200
        assert colleague_update.status_code == 200
        assert own_update.status_code == 200

    async def test_lead_scores_of_people_outside_the_organization_are_refused(self, async_client, org_member, unaffiliated_user, reference_data):
        response = await async_client.get("/api/v1/leads/2/score", headers=org_member)

        assert response.status_code == 403

    async def test_workflows_are_created_for_the_callers_organization(self, async_client, org_member, reference_data):
        response = await async_client.post(
            "/api/v1/workflows",
            json={"name": "Welcome", "trigger_event": "signup", "workflow_config": {"steps": []}},
            headers=org_member,
        )

        assert response.status_code == 200
        assert response.json()["organization_id"] == 1

    async def test_each_organization_has_one_loyalty_program(self, async_client, org_member, reference_data):
        first = await async_client.post(
            "/api/v1/loyalty-programs", json={"name": "Rewards", "points_per_dollar": 2.0}, headers=org_member
        )
        second = await async_client.post(
            "/api/v1/loyalty-programs", json={"name": "Rewards again", "points_per_dollar": 2.0}, headers=org_member
        )

        assert first.status_code == 200
        assert second.status_code == 409

    async def test_another_organizations_loyalty_program_cannot_be_enrolled_in(self, async_client, org_member, other_org_records):
        response = await async_client.post(
            f"/api/v1/loyalty-programs/{other_org_records['program']}/enroll/1", headers=org_member
        )

        assert response.status_code == 404

    async def test_points_of_another_organizations_member_cannot_be_changed(self, async_client, org_member, other_org_records):
        member = other_org_records["member"]

        added = await async_client.post(
            f"/api/v1/loyalty-members/{member}/add-points?points=5&reason=bonus", headers=org_member
        )
        redeemed = await async_client.post(
            f"/api/v1/loyalty-members/{member}/redeem-points?points=1&reason=gift", headers=org_member
        )

        assert added.status_code == 404
        assert redeemed.status_code == 404

    async def test_points_of_an_own_member_can_be_changed(self, async_client, org_member, reference_data, session):
        program = await LoyaltyService(session).create_program(1, {"name": "Own rewards", "points_per_dollar": 1.0})
        member = await LoyaltyService(session).enroll_member(program.id, 1)

        added = await async_client.post(
            f"/api/v1/loyalty-members/{member.id}/add-points?points=5&reason=bonus", headers=org_member
        )

        assert added.status_code == 200
        assert added.json() == {"status": "points_added"}
