"""Memberships: async services and the membership API, including who may manage what."""

from datetime import timedelta

import httpx
import pytest

from app.core.security import create_access_token, hash_password
from app.db.session import get_db, get_session
from app.main import app
from app.models.memberships import MembershipInvoice, MembershipSubscription, SubscriptionStatus
from app.models.organizations import Organization, OrganizationMember
from app.models.tenants import Tenant
from app.models.user import User
from app.services.memberships_service import (
    MembershipInvoiceService,
    MembershipPaymentMethodService,
    MembershipSubscriptionService,
    MembershipTypeService,
    active_subscriber_counts,
)
from app.utils.exceptions import NotFoundError


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
    await session.flush()
    return user


async def _org(session, slug):
    tenant = Tenant(name=f"Tenant {slug}", slug=f"tenant-{slug}")
    session.add(tenant)
    await session.flush()
    org = Organization(tenant_id=tenant.id, name=f"Org {slug}", slug=slug, status="active")
    session.add(org)
    await session.flush()
    return org


async def _member(session, user, org, role="member", is_lead=False):
    session.add(OrganizationMember(organization_id=org.id, user_id=user.id, role=role, status="active", is_lead=is_lead))
    await session.flush()


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


PLAN = {
    "name": "Premium",
    "tier": "premium",
    "description": "Premium membership",
    "price": 29.99,
    "billing_cycle": "monthly",
    "max_courses": 100,
    "max_students": 1000,
    "features": {"ad_free": True},
}


@pytest.fixture
async def world(session):
    """Two organizations; a manager, a plain member and a stranger in the first one."""
    org = await _org(session, "alpha")
    other_org = await _org(session, "beta")
    manager = await _user(session, "manager@example.com")
    member = await _user(session, "member@example.com")
    stranger = await _user(session, "stranger@example.com")
    await _member(session, manager, org, role="admin")
    await _member(session, member, org)
    await _member(session, stranger, other_org)
    await session.commit()
    return {"org": org, "other_org": other_org, "manager": manager, "member": member, "stranger": stranger}


@pytest.fixture
async def plan(session, world):
    membership = await MembershipTypeService(session).create_membership_type(world["org"].id, dict(PLAN))
    return membership


class TestMembershipTypeService:
    @pytest.mark.asyncio
    async def test_create_and_get(self, session, world):
        created = await MembershipTypeService(session).create_membership_type(world["org"].id, dict(PLAN))
        assert created.id is not None and created.price == 29.99
        fetched = await MembershipTypeService(session).get_membership_type(created.id)
        assert fetched.name == "Premium"

    @pytest.mark.asyncio
    async def test_list_returns_only_active_types_of_the_organization(self, session, world, plan):
        service = MembershipTypeService(session)
        await service.create_membership_type(world["other_org"].id, {**PLAN, "name": "Elsewhere"})
        retired = await service.create_membership_type(world["org"].id, {**PLAN, "name": "Retired"})
        await service.update_membership_type(retired.id, {"is_active": False})

        listed = await service.list_membership_types(world["org"].id)
        assert [item.name for item in listed] == ["Premium"]

    @pytest.mark.asyncio
    async def test_update_changes_fields(self, session, world, plan):
        updated = await MembershipTypeService(session).update_membership_type(
            plan.id, {"price": 39.99, "name": "Premium Plus"},
        )
        assert updated.price == 39.99 and updated.name == "Premium Plus"

    @pytest.mark.asyncio
    async def test_update_of_a_missing_type_is_not_found(self, session, world):
        with pytest.raises(NotFoundError):
            await MembershipTypeService(session).update_membership_type(999999, {"price": 1})


class TestSubscriptionService:
    @pytest.mark.asyncio
    async def test_subscribe_sets_an_active_subscription_with_renewal(self, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        assert sub.status == SubscriptionStatus.ACTIVE
        assert sub.renewal_date - sub.start_date == timedelta(days=30)

    @pytest.mark.asyncio
    async def test_subscribing_to_a_missing_or_retired_type_is_not_found(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        with pytest.raises(NotFoundError):
            await service.subscribe_user(world["member"].id, 999999)
        await MembershipTypeService(session).update_membership_type(plan.id, {"is_active": False})
        with pytest.raises(NotFoundError):
            await service.subscribe_user(world["member"].id, plan.id)

    @pytest.mark.asyncio
    async def test_active_subscription_is_the_newest_active_one(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        first = await service.subscribe_user(world["member"].id, plan.id)
        second = await service.subscribe_user(world["member"].id, plan.id)
        active = await service.get_active_subscription(world["member"].id)
        assert active.id == second.id != first.id

    @pytest.mark.asyncio
    async def test_cancel_marks_cancelled_and_sets_end_date(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        sub = await service.subscribe_user(world["member"].id, plan.id)
        await service.cancel_subscription(sub.id)
        row = await session.get(MembershipSubscription, sub.id)
        await session.refresh(row)
        assert row.status == SubscriptionStatus.CANCELLED and row.end_date is not None

    @pytest.mark.asyncio
    async def test_pause_marks_paused(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        sub = await service.subscribe_user(world["member"].id, plan.id)
        await service.pause_subscription(sub.id)
        row = await session.get(MembershipSubscription, sub.id)
        await session.refresh(row)
        assert row.status == SubscriptionStatus.PAUSED

    @pytest.mark.asyncio
    async def test_renew_moves_the_renewal_date_forward(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        sub = await service.subscribe_user(world["member"].id, plan.id)
        old_renewal = sub.renewal_date
        await service.renew_subscription(sub.id)
        row = await session.get(MembershipSubscription, sub.id)
        await session.refresh(row)
        assert row.status == SubscriptionStatus.ACTIVE and row.renewal_date > old_renewal

    @pytest.mark.asyncio
    async def test_missing_subscription_is_not_found(self, session, world):
        with pytest.raises(NotFoundError):
            await MembershipSubscriptionService(session).cancel_subscription(999999)

    @pytest.mark.asyncio
    async def test_subscriber_counts_count_only_active_subscriptions(self, session, world, plan):
        service = MembershipSubscriptionService(session)
        await service.subscribe_user(world["member"].id, plan.id)
        cancelled = await service.subscribe_user(world["stranger"].id, plan.id)
        await service.cancel_subscription(cancelled.id)
        assert await active_subscriber_counts(session, [plan.id]) == {plan.id: 1}


class TestInvoiceAndPaymentMethodServices:
    @pytest.mark.asyncio
    async def test_invoice_lifecycle(self, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        service = MembershipInvoiceService(session)
        first = await service.create_invoice(sub.id, 29.99)
        second = await service.create_invoice(sub.id, 29.99)
        assert first.total_amount > 29.99 and first.status == "pending"
        assert first.invoice_number != second.invoice_number

        await service.mark_invoice_paid(first.id)
        paid = await session.get(MembershipInvoice, first.id)
        await session.refresh(paid)
        assert paid.status == "paid" and paid.paid_date is not None

        listed = await service.get_subscription_invoices(sub.id)
        assert len(listed) == 2

    @pytest.mark.asyncio
    async def test_invoice_for_missing_subscription_is_not_found(self, session, world):
        with pytest.raises(NotFoundError):
            await MembershipInvoiceService(session).create_invoice(999999, 10)

    @pytest.mark.asyncio
    async def test_the_newest_payment_method_becomes_the_default(self, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        service = MembershipPaymentMethodService(session)
        visa = await service.add_payment_method(sub.id, "visa", "4242", "pm_1")
        mastercard = await service.add_payment_method(sub.id, "mastercard", "5555", "pm_2")
        assert mastercard.is_default is True
        await session.refresh(visa)
        assert visa.is_default is False

        await service.set_default_payment_method(visa.id)
        methods = {m.id: m for m in await service.get_payment_methods(sub.id)}
        assert methods[visa.id].is_default is True and methods[mastercard.id].is_default is False

    @pytest.mark.asyncio
    async def test_default_for_missing_method_is_not_found(self, session, world):
        with pytest.raises(NotFoundError):
            await MembershipPaymentMethodService(session).set_default_payment_method(999999)


class TestMembershipTypeEndpoints:
    @pytest.mark.asyncio
    async def test_manager_creates_a_plan_for_their_organization(self, client, world):
        response = await client.post("/api/v1/membership-types", json=PLAN, headers=_headers(world["manager"]))
        assert response.status_code == 201
        assert response.json()["subscriber_count"] == 0 and response.json()["tier"] == "premium"

    @pytest.mark.asyncio
    async def test_plain_member_cannot_create_plans(self, client, world):
        response = await client.post("/api/v1/membership-types", json=PLAN, headers=_headers(world["member"]))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_account_without_an_organization_is_refused(self, client, session):
        lone = await _user(session, "lone@example.com")
        await session.commit()
        response = await client.get("/api/v1/membership-types", headers=_headers(lone))
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_members_see_their_organizations_plans_with_subscriber_counts(self, client, session, world, plan):
        await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        response = await client.get("/api/v1/membership-types", headers=_headers(world["member"]))
        assert response.status_code == 200
        assert [(item["name"], item["subscriber_count"]) for item in response.json()] == [("Premium", 1)]

    @pytest.mark.asyncio
    async def test_a_plan_from_another_organization_is_not_found(self, client, session, world):
        other_plan = await MembershipTypeService(session).create_membership_type(world["other_org"].id, dict(PLAN))
        response = await client.get(f"/api/v1/membership-types/{other_plan.id}", headers=_headers(world["member"]))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_plan_is_rejected(self, client, world):
        response = await client.post(
            "/api/v1/membership-types", json={**PLAN, "price": -1}, headers=_headers(world["manager"]),
        )
        assert response.status_code == 422


class TestSubscriptionEndpoints:
    @pytest.mark.asyncio
    async def test_subscribe_then_read_the_active_subscription(self, client, world, plan):
        created = await client.post("/api/v1/subscriptions", json={"membership_type_id": plan.id}, headers=_headers(world["member"]))
        assert created.status_code == 201
        active = await client.get("/api/v1/subscriptions/me/active", headers=_headers(world["member"]))
        assert active.status_code == 200 and active.json()["id"] == created.json()["id"]

    @pytest.mark.asyncio
    async def test_no_active_subscription_is_not_found(self, client, world):
        response = await client.get("/api/v1/subscriptions/me/active", headers=_headers(world["member"]))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_subscribing_to_a_missing_plan_is_not_found(self, client, world):
        response = await client.post("/api/v1/subscriptions", json={"membership_type_id": 999999}, headers=_headers(world["member"]))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_subscriber_can_cancel_their_own_subscription(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        response = await client.post(f"/api/v1/subscriptions/{sub.id}/cancel", headers=_headers(world["member"]))
        assert response.status_code == 200 and response.json() == {"status": "cancelled"}

    @pytest.mark.asyncio
    async def test_organization_manager_can_pause_a_members_subscription(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        response = await client.post(f"/api/v1/subscriptions/{sub.id}/pause", headers=_headers(world["manager"]))
        assert response.status_code == 200 and response.json() == {"status": "paused"}

    @pytest.mark.asyncio
    async def test_stranger_cannot_cancel_someone_elses_subscription(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        response = await client.post(f"/api/v1/subscriptions/{sub.id}/cancel", headers=_headers(world["stranger"]))
        assert response.status_code == 403
        row = await session.get(MembershipSubscription, sub.id)
        await session.refresh(row)
        assert row.status == SubscriptionStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_plain_member_of_the_organization_cannot_manage_others(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["stranger"].id, plan.id)
        response = await client.post(f"/api/v1/subscriptions/{sub.id}/cancel", headers=_headers(world["member"]))
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_cancelling_a_missing_subscription_is_not_found(self, client, world):
        response = await client.post("/api/v1/subscriptions/999999/cancel", headers=_headers(world["member"]))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invoices_are_visible_to_the_subscriber_only(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        await MembershipInvoiceService(session).create_invoice(sub.id, 29.99)

        mine = await client.get(f"/api/v1/subscriptions/{sub.id}/invoices", headers=_headers(world["member"]))
        assert mine.status_code == 200 and len(mine.json()) == 1
        assert mine.json()[0]["status"] == "pending"

        theirs = await client.get(f"/api/v1/subscriptions/{sub.id}/invoices", headers=_headers(world["stranger"]))
        assert theirs.status_code == 403

    @pytest.mark.asyncio
    async def test_payment_methods_round_trip_and_validate_the_card(self, client, session, world, plan):
        sub = await MembershipSubscriptionService(session).subscribe_user(world["member"].id, plan.id)
        body = {"card_brand": "visa", "card_last_four": "4242", "stripe_payment_method_id": "pm_api_1"}

        created = await client.post(f"/api/v1/subscriptions/{sub.id}/payment-methods", json=body, headers=_headers(world["member"]))
        assert created.status_code == 201 and created.json()["is_default"] is True

        listed = await client.get(f"/api/v1/subscriptions/{sub.id}/payment-methods", headers=_headers(world["member"]))
        assert [item["card_last_four"] for item in listed.json()] == ["4242"]

        bad = await client.post(
            f"/api/v1/subscriptions/{sub.id}/payment-methods",
            json={**body, "card_last_four": "42"},
            headers=_headers(world["member"]),
        )
        assert bad.status_code == 422

    @pytest.mark.asyncio
    async def test_anonymous_requests_are_rejected(self, client, world, plan):
        assert (await client.get("/api/v1/subscriptions/me/active")).status_code == 401
