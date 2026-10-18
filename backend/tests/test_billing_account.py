"""The signed-in account's own subscription, invoices and payments."""

from datetime import datetime, timedelta, timezone

import httpx
import pytest

from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.monetization import BillingCycle, Invoice, Payment, PaymentStatus, Subscription, SubscriptionTier
from app.models.organizations import Organization
from app.models.tenants import Tenant
from app.models.user import User

NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


@pytest.fixture
async def client(test_session):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as http:
        yield http
    app.dependency_overrides.clear()


async def _user(session, email):
    user = User(email=email, password_hash=hash_password("Passw0rd!long"), first_name="T", last_name="U", status="active")
    session.add(user)
    await session.commit()
    return user


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


async def _org(session):
    tenant = Tenant(name=f"Tenant {datetime.now(timezone.utc).timestamp()}", slug=f"t-{datetime.now(timezone.utc).timestamp()}")
    session.add(tenant)
    await session.flush()
    org = Organization(tenant_id=tenant.id, name="Org", slug=f"o-{tenant.id}", status="active")
    session.add(org)
    await session.flush()
    return org


async def _subscription(session, user, org, *, tier, active, started_days_ago):
    sub = Subscription(
        user_id=user.id,
        organization_id=org.id,
        tier=tier,
        billing_cycle=BillingCycle.MONTHLY,
        amount=49.0 if tier == SubscriptionTier.PRO else 9.0,
        is_active=active,
        started_at=NOW - timedelta(days=started_days_ago),
        canceled_at=None if active else NOW,
    )
    session.add(sub)
    await session.flush()
    return sub


@pytest.fixture
async def customer(session):
    return await _user(session, "customer@example.com")


@pytest.fixture
async def other(session):
    return await _user(session, "other@example.com")


class TestSubscription:
    @pytest.mark.asyncio
    async def test_active_subscription_is_preferred_over_an_older_canceled_one(self, client, session, customer):
        org = await _org(session)
        await _subscription(session, customer, org, tier=SubscriptionTier.STARTER, active=False, started_days_ago=1)
        await _subscription(session, customer, org, tier=SubscriptionTier.PRO, active=True, started_days_ago=90)
        await session.commit()

        response = await client.get("/api/v1/billing/subscription", headers=_headers(customer))
        assert response.status_code == 200
        body = response.json()
        assert body["tier"] == "pro" and body["is_active"] is True
        assert body["billing_cycle"] == "monthly" and body["amount"] == 49.0

    @pytest.mark.asyncio
    async def test_most_recent_canceled_subscription_is_returned_when_none_is_active(self, client, session, customer):
        org = await _org(session)
        await _subscription(session, customer, org, tier=SubscriptionTier.PRO, active=False, started_days_ago=60)
        await _subscription(session, customer, org, tier=SubscriptionTier.STARTER, active=False, started_days_ago=5)
        await session.commit()

        body = (await client.get("/api/v1/billing/subscription", headers=_headers(customer))).json()
        assert body["tier"] == "starter" and body["is_active"] is False

    @pytest.mark.asyncio
    async def test_account_without_a_subscription_is_not_found(self, client, customer):
        response = await client.get("/api/v1/billing/subscription", headers=_headers(customer))
        assert response.status_code == 404
        assert response.json()["detail"] == "No subscription on this account"

    @pytest.mark.asyncio
    async def test_anonymous_request_is_rejected(self, client):
        assert (await client.get("/api/v1/billing/subscription")).status_code == 401


class TestInvoicesAndPayments:
    @pytest.mark.asyncio
    async def test_invoices_are_only_the_accounts_own_newest_first(self, client, session, customer, other):
        org = await _org(session)
        mine = await _subscription(session, customer, org, tier=SubscriptionTier.PRO, active=True, started_days_ago=60)
        theirs = await _subscription(session, other, org, tier=SubscriptionTier.PRO, active=True, started_days_ago=60)
        session.add_all([
            Invoice(subscription_id=mine.id, amount=49.0, status=PaymentStatus.COMPLETED, created_at=NOW - timedelta(days=30)),
            Invoice(subscription_id=mine.id, amount=49.0, status=PaymentStatus.PENDING, created_at=NOW),
            Invoice(subscription_id=theirs.id, amount=99.0, status=PaymentStatus.PENDING, created_at=NOW),
        ])
        await session.commit()

        invoices = (await client.get("/api/v1/billing/invoices", headers=_headers(customer))).json()
        assert [item["status"] for item in invoices] == ["pending", "completed"]
        assert all(item["subscription_id"] == mine.id for item in invoices)

    @pytest.mark.asyncio
    async def test_payments_are_only_the_accounts_own(self, client, session, customer, other):
        org = await _org(session)
        mine = await _subscription(session, customer, org, tier=SubscriptionTier.PRO, active=True, started_days_ago=60)
        theirs = await _subscription(session, other, org, tier=SubscriptionTier.PRO, active=True, started_days_ago=60)
        my_invoice = Invoice(subscription_id=mine.id, amount=49.0, status=PaymentStatus.COMPLETED)
        their_invoice = Invoice(subscription_id=theirs.id, amount=49.0, status=PaymentStatus.COMPLETED)
        session.add_all([my_invoice, their_invoice])
        await session.flush()
        session.add_all([
            Payment(user_id=customer.id, invoice_id=my_invoice.id, amount=49.0, status=PaymentStatus.COMPLETED, payment_method="card"),
            Payment(user_id=other.id, invoice_id=their_invoice.id, amount=49.0, status=PaymentStatus.FAILED, payment_method="card"),
        ])
        await session.commit()

        payments = (await client.get("/api/v1/billing/payments", headers=_headers(customer))).json()
        assert len(payments) == 1
        assert payments[0]["status"] == "completed" and payments[0]["payment_method"] == "card"

    @pytest.mark.asyncio
    async def test_no_invoices_gives_an_empty_list(self, client, customer):
        assert (await client.get("/api/v1/billing/invoices", headers=_headers(customer))).json() == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize("path", ["/api/v1/billing/invoices?limit=0", "/api/v1/billing/payments?limit=500"])
    async def test_paging_limits_are_enforced(self, client, customer, path):
        assert (await client.get(path, headers=_headers(customer))).status_code == 422
