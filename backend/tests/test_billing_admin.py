"""Admin management of subscriptions and transactions."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import httpx
import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.ecommerce import CheckoutSession, PaymentDetail, PaymentMethod, PaymentStatus as EcommercePaymentStatus
from app.models.monetization import (
    BillingCycle,
    Invoice,
    Payment,
    PaymentStatus,
    Subscription,
    SubscriptionTier,
)
from app.models.organizations import Organization
from app.models.tenants import Tenant
from app.models.user import Role, User

NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


async def _make_user(session, email, roles=()):
    user = User(email=email, password_hash=hash_password("Passw0rd!long"), first_name="T", last_name="U", status="active")
    user.roles = list(roles)
    session.add(user)
    await session.commit()
    return user


def _auth_header(user):
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


@pytest.fixture
async def social_client(test_session):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def admin(session):
    return await _make_user(session, "billing-admin@example.com", roles=[Role(name="admin", description="Administrator")])


@pytest.fixture
async def customer(session):
    return await _make_user(session, "customer@example.com")


@pytest.fixture
async def billing_data(session, customer):
    """One subscription with a subscription payment, and one checkout with a checkout payment."""
    tenant = Tenant(name="Acme", slug="acme")
    session.add(tenant)
    await session.flush()
    org = Organization(tenant_id=tenant.id, name="Acme News", slug="acme-news", status="active")
    session.add(org)
    await session.flush()

    sub = Subscription(
        user_id=customer.id,
        organization_id=org.id,
        tier=SubscriptionTier.PRO,
        billing_cycle=BillingCycle.MONTHLY,
        amount=49.0,
        is_active=True,
        started_at=NOW - timedelta(days=30),
        renews_at=NOW + timedelta(days=1),
    )
    session.add(sub)
    await session.flush()

    invoice = Invoice(subscription_id=sub.id, amount=49.0, status=PaymentStatus.COMPLETED, created_at=NOW - timedelta(days=1))
    session.add(invoice)
    await session.flush()
    payment = Payment(
        user_id=customer.id,
        invoice_id=invoice.id,
        amount=49.0,
        status=PaymentStatus.COMPLETED,
        payment_method="card",
        stripe_payment_id="pay_sub_1",
        created_at=NOW - timedelta(days=1),
    )
    session.add(payment)

    checkout = CheckoutSession(
        checkout_token="chk-token-1",
        user_id=customer.id,
        billing_address={"line1": "1 Road"},
        shipping_address={"line1": "1 Road"},
        email=customer.email,
        subtotal=Decimal("20.00"),
        total=Decimal("20.00"),
    )
    session.add(checkout)
    await session.flush()
    session.add(PaymentDetail(
        checkout_id=checkout.id,
        payment_method=PaymentMethod.CREDIT_CARD,
        status=EcommercePaymentStatus.FAILED,
        transaction_id="txn-checkout-1",
        amount=Decimal("20.00"),
        currency="USD",
        created_at=NOW,
    ))
    await session.commit()
    return {"subscription_id": sub.id}


class TestAccess:
    @pytest.mark.asyncio
    async def test_anonymous_is_rejected(self, social_client):
        assert (await social_client.get("/api/v1/admin/subscriptions")).status_code == 401

    @pytest.mark.asyncio
    async def test_customer_is_forbidden(self, social_client, customer, billing_data):
        headers = _auth_header(customer)
        assert (await social_client.get("/api/v1/admin/subscriptions", headers=headers)).status_code == 403
        assert (await social_client.get("/api/v1/admin/transactions", headers=headers)).status_code == 403
        assert (await social_client.post(
            f"/api/v1/admin/subscriptions/{billing_data['subscription_id']}/cancel", headers=headers,
        )).status_code == 403


class TestSubscriptions:
    @pytest.mark.asyncio
    async def test_lists_subscriptions_with_account_email(self, social_client, admin, billing_data):
        response = await social_client.get("/api/v1/admin/subscriptions", headers=_auth_header(admin))
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        item = body["items"][0]
        assert item["user_email"] == "customer@example.com"
        assert item["tier"] == "pro" and item["billing_cycle"] == "monthly"
        assert item["is_active"] is True

    @pytest.mark.asyncio
    async def test_filters_by_active_state_and_tier(self, social_client, admin, billing_data):
        headers = _auth_header(admin)
        active = await social_client.get("/api/v1/admin/subscriptions?is_active=true", headers=headers)
        canceled = await social_client.get("/api/v1/admin/subscriptions?is_active=false", headers=headers)
        pro = await social_client.get("/api/v1/admin/subscriptions?tier=pro", headers=headers)
        starter = await social_client.get("/api/v1/admin/subscriptions?tier=starter", headers=headers)
        assert active.json()["total"] == 1
        assert canceled.json()["total"] == 0
        assert pro.json()["total"] == 1
        assert starter.json()["total"] == 0

    @pytest.mark.asyncio
    async def test_changes_tier_and_renewal_date(self, social_client, admin, billing_data):
        sub_id = billing_data["subscription_id"]
        renews = (NOW + timedelta(days=30)).isoformat()
        response = await social_client.patch(
            f"/api/v1/admin/subscriptions/{sub_id}",
            json={"tier": "enterprise", "renews_at": renews},
            headers=_auth_header(admin),
        )
        assert response.status_code == 200
        assert response.json()["tier"] == "enterprise"
        assert response.json()["renews_at"].startswith((NOW + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M"))

    @pytest.mark.asyncio
    async def test_update_requires_a_field(self, social_client, admin, billing_data):
        response = await social_client.patch(
            f"/api/v1/admin/subscriptions/{billing_data['subscription_id']}", json={}, headers=_auth_header(admin),
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_rejects_unknown_tier(self, social_client, admin, billing_data):
        response = await social_client.patch(
            f"/api/v1/admin/subscriptions/{billing_data['subscription_id']}",
            json={"tier": "platinum"},
            headers=_auth_header(admin),
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_unknown_subscription_is_not_found(self, social_client, admin):
        response = await social_client.patch(
            "/api/v1/admin/subscriptions/999999", json={"tier": "free"}, headers=_auth_header(admin),
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_cancel_deactivates_and_records_time(self, social_client, admin, billing_data, session):
        sub_id = billing_data["subscription_id"]
        response = await social_client.post(f"/api/v1/admin/subscriptions/{sub_id}/cancel", headers=_auth_header(admin))
        assert response.status_code == 200
        assert response.json()["is_active"] is False
        assert response.json()["canceled_at"] is not None
        row = (await session.execute(select(Subscription).where(Subscription.id == sub_id))).scalar_one()
        assert row.is_active is False

    @pytest.mark.asyncio
    async def test_cancel_is_idempotent(self, social_client, admin, billing_data):
        sub_id = billing_data["subscription_id"]
        headers = _auth_header(admin)
        first = (await social_client.post(f"/api/v1/admin/subscriptions/{sub_id}/cancel", headers=headers)).json()
        second = (await social_client.post(f"/api/v1/admin/subscriptions/{sub_id}/cancel", headers=headers)).json()
        assert first["canceled_at"] == second["canceled_at"]

    @pytest.mark.asyncio
    async def test_cancel_unknown_subscription_is_not_found(self, social_client, admin):
        response = await social_client.post("/api/v1/admin/subscriptions/999999/cancel", headers=_auth_header(admin))
        assert response.status_code == 404


class TestTransactions:
    @pytest.mark.asyncio
    async def test_merges_both_sources_newest_first(self, social_client, admin, billing_data):
        response = await social_client.get("/api/v1/admin/transactions", headers=_auth_header(admin))
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 2
        assert [item["source"] for item in body["items"]] == ["checkout", "subscription"]
        assert body["items"][0]["reference"] == "txn-checkout-1"
        assert body["items"][0]["user_email"] == "customer@example.com"
        assert body["items"][1]["reference"] == "pay_sub_1"

    @pytest.mark.asyncio
    async def test_source_filter_limits_to_one_side(self, social_client, admin, billing_data):
        headers = _auth_header(admin)
        subs = (await social_client.get("/api/v1/admin/transactions?source=subscription", headers=headers)).json()
        checkouts = (await social_client.get("/api/v1/admin/transactions?source=checkout", headers=headers)).json()
        assert [item["source"] for item in subs["items"]] == ["subscription"] and subs["total"] == 1
        assert [item["source"] for item in checkouts["items"]] == ["checkout"] and checkouts["total"] == 1

    @pytest.mark.asyncio
    async def test_status_filter_uses_each_sides_statuses(self, social_client, admin, billing_data):
        headers = _auth_header(admin)
        failed = (await social_client.get("/api/v1/admin/transactions?status=failed", headers=headers)).json()
        completed = (await social_client.get("/api/v1/admin/transactions?status=completed", headers=headers)).json()
        assert [item["source"] for item in failed["items"]] == ["checkout"]
        assert [item["source"] for item in completed["items"]] == ["subscription"]

    @pytest.mark.asyncio
    async def test_unknown_status_is_unprocessable(self, social_client, admin, billing_data):
        response = await social_client.get("/api/v1/admin/transactions?status=bogus", headers=_auth_header(admin))
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_paging_is_correct_across_both_tables(self, social_client, admin, billing_data):
        headers = _auth_header(admin)
        second = (await social_client.get("/api/v1/admin/transactions?skip=1&limit=1", headers=headers)).json()
        assert second["total"] == 2
        assert [item["source"] for item in second["items"]] == ["subscription"]

    @pytest.mark.asyncio
    async def test_unknown_source_is_rejected(self, social_client, admin, billing_data):
        response = await social_client.get("/api/v1/admin/transactions?source=cash", headers=_auth_header(admin))
        assert response.status_code == 422
