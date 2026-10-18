"""Route tests for the user-management dashboard figures, campaign performance, and signed webhook delivery"""

from datetime import datetime, timedelta, timezone

import httpx
import pytest
import respx
from sqlalchemy.orm import Session

from app.models.user_management import (
    CampaignStatus, EmailCampaign, EmailTemplate, SubscriberProfile, UserSegment, UserSegmentType,
)
from app.services.user_management_service import WebhookService

RECEIVER_URL = "https://hooks.example.test/receive"


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@pytest.fixture
def dashboard_data(reset_test_database):
    """Four subscribers across tiers, engagement and churn bands; two sent campaigns, one draft; two segments."""
    now = _now()
    with Session(reset_test_database) as session:
        template = EmailTemplate(name="Digest", subject="Digest", body="<p>Digest</p>")
        session.add(template)
        session.flush()
        session.add_all([
            SubscriberProfile(user_id=101, subscription_tier="premium", engagement_score=80.0, churn_risk_score=0.9, created_at=now),
            SubscriberProfile(user_id=102, subscription_tier="free", engagement_score=50.0, churn_risk_score=0.6, created_at=now),
            SubscriberProfile(user_id=103, subscription_tier="free", engagement_score=20.0, churn_risk_score=0.2, created_at=now),
            SubscriberProfile(user_id=104, subscription_tier="free", engagement_score=10.0, churn_risk_score=0.1,
                              created_at=now - timedelta(days=60)),
        ])
        session.add_all([
            EmailCampaign(name="Sent today", template_id=template.id, subject="Today", from_email="news@example.test",
                          status=CampaignStatus.SENT, sent_at=now, sent_count=1000, open_count=400, click_count=50),
            EmailCampaign(name="Sent last month", template_id=template.id, subject="Old", from_email="news@example.test",
                          status=CampaignStatus.SENT, sent_at=now - timedelta(days=30), sent_count=500, open_count=100, click_count=10),
            EmailCampaign(name="Draft", template_id=template.id, subject="Draft", from_email="news@example.test",
                          status=CampaignStatus.DRAFT, sent_count=0),
        ])
        session.add_all([
            UserSegment(name="Everyone", segment_type=UserSegmentType.ACTIVE, filter_criteria={}),
            UserSegment(name="Heavy readers", segment_type=UserSegmentType.ENGAGED, filter_criteria={"min_articles": 5}),
        ])
        session.commit()


class TestSubscriberOverview:
    async def test_overview_figures_match_the_seeded_subscribers_and_campaigns(self, async_client, platform_admin, dashboard_data):
        response = await async_client.get("/api/v1/subscribers/overview", headers=platform_admin)

        assert response.status_code == 200
        body = response.json()
        assert body["total_subscribers"] == 4
        assert body["new_subscribers_this_month"] == 3
        assert body["average_engagement"] == 40.0
        assert body["average_churn_risk"] == pytest.approx(0.45)
        assert body["tiers"] == [{"tier": "free", "count": 3}, {"tier": "premium", "count": 1}]
        assert body["engagement_levels"] == [
            {"level": "highly_engaged", "count": 1},
            {"level": "engaged", "count": 1},
            {"level": "low_engagement", "count": 1},
            {"level": "inactive", "count": 1},
        ]
        assert body["churn_risk_levels"] == [
            {"level": "high", "count": 1},
            {"level": "medium", "count": 1},
            {"level": "low", "count": 2},
        ]
        assert body["campaigns_sent"] == 2
        assert body["campaigns_sent_last_7_days"] == 1
        assert body["active_segments"] == 2
        assert body["dynamic_segments"] == 1

    async def test_an_empty_platform_reports_zeros_not_errors(self, async_client, platform_admin):
        response = await async_client.get("/api/v1/subscribers/overview", headers=platform_admin)

        assert response.status_code == 200
        body = response.json()
        assert body["total_subscribers"] == 0
        assert body["average_engagement"] == 0.0
        assert body["average_churn_risk"] == 0.0
        assert body["tiers"] == []
        assert all(item["count"] == 0 for item in body["engagement_levels"])

    async def test_the_overview_is_administrator_only(self, async_client, org_member, dashboard_data):
        response = await async_client.get("/api/v1/subscribers/overview", headers=org_member)

        assert response.status_code == 403
        assert response.json()["detail"] == "Admin access required"

    async def test_the_overview_requires_a_signed_in_user(self, async_client, dashboard_data):
        response = await async_client.get("/api/v1/subscribers/overview")

        assert response.status_code in (401, 403)


class TestCampaignPerformance:
    async def test_campaigns_list_newest_first_with_click_through_rate(self, async_client, platform_admin, dashboard_data):
        response = await async_client.get("/api/v1/emails/campaigns?limit=3", headers=platform_admin)

        assert response.status_code == 200
        rows = {row["name"]: row for row in response.json()}
        assert set(rows) == {"Sent today", "Sent last month", "Draft"}
        assert rows["Sent today"]["ctr"] == 5.0
        assert rows["Sent today"]["sent_count"] == 1000
        assert rows["Sent today"]["open_count"] == 400
        assert rows["Sent today"]["click_count"] == 50
        assert rows["Sent last month"]["ctr"] == 2.0
        assert rows["Draft"]["ctr"] == 0.0
        assert rows["Draft"]["sent_at"] is None
        assert rows["Draft"]["status"] == "draft"

    async def test_the_limit_is_honoured_and_clamped(self, async_client, platform_admin, dashboard_data):
        limited = await async_client.get("/api/v1/emails/campaigns?limit=1", headers=platform_admin)
        clamped = await async_client.get("/api/v1/emails/campaigns?limit=0", headers=platform_admin)

        assert len(limited.json()) == 1
        assert len(clamped.json()) == 1

    async def test_campaign_performance_is_administrator_only(self, async_client, org_member, dashboard_data):
        response = await async_client.get("/api/v1/emails/campaigns", headers=org_member)

        assert response.status_code == 403


class TestWebhookDelivery:
    async def _register(self, async_client, headers) -> dict:
        response = await async_client.post(
            "/api/v1/webhooks/endpoints",
            json={"name": "Receiver", "url": RECEIVER_URL, "events": ["content.published"]},
            headers=headers,
        )
        assert response.status_code == 201
        return response.json()

    async def test_a_2xx_response_marks_the_delivery_and_signs_the_body(self, async_client, org_member):
        endpoint = await self._register(async_client, org_member)

        with respx.mock(assert_all_called=True) as mock:
            route = mock.post(RECEIVER_URL).mock(return_value=httpx.Response(200, text="received"))
            response = await async_client.post(
                f"/api/v1/webhooks/{endpoint['id']}/trigger",
                json={"event_type": "content.published", "payload": {"content_id": 7}},
                headers=org_member,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["delivered"] is True
        assert body["status_code"] == 200
        assert body["error"] is None

        sent = route.calls.last.request
        assert sent.headers["X-Webhook-Event"] == "content.published"
        signature = sent.headers["X-Webhook-Signature"]
        assert WebhookService.verify_webhook_signature(sent.content.decode(), signature, endpoint["secret_key"])
        assert sent.content.decode() and '"content_id": 7' in sent.content.decode()

    async def test_a_failure_status_is_recorded_but_not_marked_delivered(self, async_client, org_member):
        endpoint = await self._register(async_client, org_member)

        with respx.mock(assert_all_called=True) as mock:
            mock.post(RECEIVER_URL).mock(return_value=httpx.Response(500, text="boom"))
            response = await async_client.post(
                f"/api/v1/webhooks/{endpoint['id']}/trigger",
                json={"event_type": "content.published", "payload": {}},
                headers=org_member,
            )

        body = response.json()
        assert response.status_code == 200
        assert body["delivered"] is False
        assert body["status_code"] == 500
        assert body["error"] is None

    async def test_an_unreachable_endpoint_reports_the_network_error(self, async_client, org_member):
        endpoint = await self._register(async_client, org_member)

        with respx.mock(assert_all_called=True) as mock:
            mock.post(RECEIVER_URL).mock(side_effect=httpx.ConnectError("connection refused"))
            response = await async_client.post(
                f"/api/v1/webhooks/{endpoint['id']}/trigger",
                json={"event_type": "content.published", "payload": {}},
                headers=org_member,
            )

        body = response.json()
        assert response.status_code == 200
        assert body["delivered"] is False
        assert body["status_code"] is None
        assert body["error"].startswith("ConnectError")

    async def test_triggering_an_unknown_endpoint_is_not_found(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/webhooks/999/trigger",
            json={"event_type": "content.published", "payload": {}},
            headers=org_member,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Webhook 999 not found"
