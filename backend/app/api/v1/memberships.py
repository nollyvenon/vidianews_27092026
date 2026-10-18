"""Memberships API: membership types for an organization, and users' subscriptions.

Organization scope comes from the caller's active organization membership. Subscription
actions are limited to the subscriber and to managers (lead, admin or owner) of the
organization that sells the membership.
"""

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.memberships import BillingCycle, MembershipSubscription, MembershipTier, MembershipType
from app.models.organizations import OrganizationMember
from app.models.user import User
from app.services.memberships_service import (
    MembershipInvoiceService,
    MembershipPaymentMethodService,
    MembershipSubscriptionService,
    MembershipTypeService,
    active_subscriber_counts,
)

router = APIRouter()

MANAGER_ROLES = {"admin", "owner"}


class MembershipTypeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    tier: MembershipTier
    description: Optional[str] = Field(None, max_length=5000)
    price: float = Field(0.0, ge=0)
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    max_courses: int = Field(-1, ge=-1)
    max_students: int = Field(-1, ge=-1)
    features: Dict[str, object] = Field(default_factory=dict)


class MembershipTypeOut(BaseModel):
    id: int
    name: str
    tier: str
    description: Optional[str]
    price: float
    billing_cycle: str
    max_courses: int
    max_students: int
    is_active: bool
    subscriber_count: int


class SubscriptionRequest(BaseModel):
    membership_type_id: int = Field(..., ge=1)
    stripe_subscription_id: Optional[str] = Field(None, max_length=255)


class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    membership_type_id: int
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    renewal_date: Optional[datetime]
    auto_renew: bool


class InvoiceOut(BaseModel):
    id: int
    subscription_id: int
    invoice_number: str
    amount: float
    tax_amount: float
    total_amount: float
    status: str
    due_date: Optional[datetime]
    paid_date: Optional[datetime]
    created_at: Optional[datetime]


class PaymentMethodRequest(BaseModel):
    card_brand: str = Field(..., min_length=1, max_length=50)
    card_last_four: str = Field(..., pattern=r"^\d{4}$")
    stripe_payment_method_id: str = Field(..., min_length=1, max_length=255)


class PaymentMethodOut(BaseModel):
    id: int
    subscription_id: int
    card_brand: Optional[str]
    card_last_four: Optional[str]
    is_default: bool
    created_at: Optional[datetime]


async def _membership_row(session: AsyncSession, user: User) -> Optional[OrganizationMember]:
    """The caller's active organization membership (lead first, then the oldest)."""
    return (await session.execute(
        select(OrganizationMember)
        .where(OrganizationMember.user_id == user.id, OrganizationMember.status == "active")
        .order_by(OrganizationMember.is_lead.desc(), OrganizationMember.id)
        .limit(1)
    )).scalar_one_or_none()


async def _organization_id(session: AsyncSession, user: User) -> int:
    row = await _membership_row(session, user)
    if row is None:
        raise HTTPException(status_code=422, detail="Your account is not a member of an organization yet.")
    return row.organization_id


async def _is_manager_of(session: AsyncSession, user: User, organization_id: int) -> bool:
    row = (await session.execute(
        select(OrganizationMember).where(
            OrganizationMember.user_id == user.id,
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.status == "active",
        )
    )).scalar_one_or_none()
    return row is not None and (bool(row.is_lead) or row.role in MANAGER_ROLES)


async def _require_subscription_access(session: AsyncSession, subscription: MembershipSubscription, user: User) -> None:
    if subscription.user_id == user.id:
        return
    membership = await session.get(MembershipType, subscription.membership_type_id)
    if membership is not None and membership.organization_id and await _is_manager_of(session, user, membership.organization_id):
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot manage this subscription")


async def _subscription_or_404(session: AsyncSession, subscription_id: int) -> MembershipSubscription:
    subscription = await session.get(MembershipSubscription, subscription_id)
    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription


def _membership_out(membership: MembershipType, subscriber_count: int) -> dict:
    return {
        "id": membership.id,
        "name": membership.name,
        "tier": membership.tier.value if membership.tier else None,
        "description": membership.description,
        "price": membership.price or 0.0,
        "billing_cycle": membership.billing_cycle.value if membership.billing_cycle else BillingCycle.MONTHLY.value,
        "max_courses": membership.max_courses,
        "max_students": membership.max_students,
        "is_active": bool(membership.is_active),
        "subscriber_count": subscriber_count,
    }


def _subscription_out(sub: MembershipSubscription) -> dict:
    return {
        "id": sub.id,
        "user_id": sub.user_id,
        "membership_type_id": sub.membership_type_id,
        "status": sub.status.value if sub.status else None,
        "start_date": sub.start_date,
        "end_date": sub.end_date,
        "renewal_date": sub.renewal_date,
        "auto_renew": bool(sub.auto_renew),
    }


@router.post("/membership-types", response_model=MembershipTypeOut, status_code=status.HTTP_201_CREATED)
async def create_membership_type(
    req: MembershipTypeRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create a membership type for the caller's organization (organization managers only)."""
    org_id = await _organization_id(session, current_user)
    if not await _is_manager_of(session, current_user, org_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only organization managers can create membership types")
    membership = await MembershipTypeService(session).create_membership_type(org_id, req.model_dump())
    return _membership_out(membership, 0)


@router.get("/membership-types/{membership_id}", response_model=MembershipTypeOut)
async def get_membership_type(
    membership_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """A membership type of the caller's organization, with its active subscriber count."""
    org_id = await _organization_id(session, current_user)
    membership = await MembershipTypeService(session).get_membership_type(membership_id)
    if membership is None or membership.organization_id != org_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership type not found")
    counts = await active_subscriber_counts(session, [membership.id])
    return _membership_out(membership, counts.get(membership.id, 0))


@router.get("/membership-types", response_model=List[MembershipTypeOut])
async def list_membership_types(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """The caller's organization's active membership types with their active subscriber counts."""
    org_id = await _organization_id(session, current_user)
    memberships = await MembershipTypeService(session).list_membership_types(org_id)
    counts = await active_subscriber_counts(session, [m.id for m in memberships])
    return [_membership_out(m, counts.get(m.id, 0)) for m in memberships]


@router.post("/subscriptions", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    req: SubscriptionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Subscribe the caller to an active membership type."""
    sub = await MembershipSubscriptionService(session).subscribe_user(
        current_user.id, req.membership_type_id, req.stripe_subscription_id,
    )
    return _subscription_out(sub)


@router.get("/subscriptions/me/active", response_model=SubscriptionOut)
async def get_active_subscription(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    sub = await MembershipSubscriptionService(session).get_active_subscription(current_user.id)
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active subscription")
    return _subscription_out(sub)


@router.post("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    subscription = await _subscription_or_404(session, subscription_id)
    await _require_subscription_access(session, subscription, current_user)
    await MembershipSubscriptionService(session).cancel_subscription(subscription_id)
    return {"status": "cancelled"}


@router.post("/subscriptions/{subscription_id}/pause")
async def pause_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    subscription = await _subscription_or_404(session, subscription_id)
    await _require_subscription_access(session, subscription, current_user)
    await MembershipSubscriptionService(session).pause_subscription(subscription_id)
    return {"status": "paused"}


@router.get("/subscriptions/{subscription_id}/invoices", response_model=List[InvoiceOut])
async def get_invoices(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    subscription = await _subscription_or_404(session, subscription_id)
    await _require_subscription_access(session, subscription, current_user)
    invoices = await MembershipInvoiceService(session).get_subscription_invoices(subscription_id)
    return [
        {
            "id": inv.id,
            "subscription_id": inv.subscription_id,
            "invoice_number": inv.invoice_number,
            "amount": inv.amount,
            "tax_amount": inv.tax_amount or 0.0,
            "total_amount": inv.total_amount,
            "status": inv.status,
            "due_date": inv.due_date,
            "paid_date": inv.paid_date,
            "created_at": inv.created_at,
        }
        for inv in invoices
    ]


@router.post("/subscriptions/{subscription_id}/payment-methods", response_model=PaymentMethodOut, status_code=status.HTTP_201_CREATED)
async def add_payment_method(
    subscription_id: int,
    req: PaymentMethodRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    subscription = await _subscription_or_404(session, subscription_id)
    await _require_subscription_access(session, subscription, current_user)
    method = await MembershipPaymentMethodService(session).add_payment_method(
        subscription_id, req.card_brand, req.card_last_four, req.stripe_payment_method_id,
    )
    return _payment_method_out(method)


@router.get("/subscriptions/{subscription_id}/payment-methods", response_model=List[PaymentMethodOut])
async def get_payment_methods(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    subscription = await _subscription_or_404(session, subscription_id)
    await _require_subscription_access(session, subscription, current_user)
    methods = await MembershipPaymentMethodService(session).get_payment_methods(subscription_id)
    return [_payment_method_out(method) for method in methods]


def _payment_method_out(method) -> dict:
    return {
        "id": method.id,
        "subscription_id": method.subscription_id,
        "card_brand": method.card_brand,
        "card_last_four": method.card_last_four,
        "is_default": bool(method.is_default),
        "created_at": method.created_at,
    }
