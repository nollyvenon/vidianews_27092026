"""Memberships API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from app.models.memberships import MembershipSubscription, MembershipType, SubscriptionStatus
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.services.memberships_service import (
    MembershipTypeService, MembershipSubscriptionService, MembershipInvoiceService,
    MembershipPaymentMethodService
)
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class MembershipTypeRequest(BaseModel):
    name: str
    tier: str
    description: Optional[str] = None
    price: float = 0.0
    billing_cycle: str = "monthly"
    max_courses: int = -1
    max_students: int = -1
    features: dict = {}


class SubscriptionRequest(BaseModel):
    membership_type_id: int
    stripe_subscription_id: Optional[str] = None


class PaymentMethodRequest(BaseModel):
    card_brand: str
    card_last_four: str
    stripe_payment_method_id: str


def _organization_id(current_user: User) -> int:
    if current_user.organization_id is None:
        raise HTTPException(status_code=422, detail="Your account has no organization yet. Create one under Organizations first.")
    return current_user.organization_id


def _membership_payload(membership, subscriber_count: int) -> dict:
    return {
        "id": membership.id,
        "name": membership.name,
        "tier": membership.tier.value if hasattr(membership.tier, "value") else membership.tier,
        "description": membership.description,
        "price": membership.price,
        "billing_cycle": membership.billing_cycle.value if hasattr(membership.billing_cycle, "value") else membership.billing_cycle,
        "max_courses": membership.max_courses,
        "max_students": membership.max_students,
        "is_active": membership.is_active,
        "subscriber_count": subscriber_count,
    }


def _active_subscriber_counts(db: Session, membership_ids: list) -> dict:
    if not membership_ids:
        return {}
    rows = db.query(MembershipSubscription.membership_type_id, func.count(MembershipSubscription.id)).filter(
        MembershipSubscription.membership_type_id.in_(membership_ids),
        MembershipSubscription.status == SubscriptionStatus.ACTIVE,
    ).group_by(MembershipSubscription.membership_type_id).all()
    return dict(rows)


@router.post("/membership-types")
def create_membership_type(
    req: MembershipTypeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create membership type in the caller's organization"""
    return MembershipTypeService.create_membership_type(db, _organization_id(current_user), req.dict())


@router.get("/membership-types/{membership_id}")
def get_membership_type(
    membership_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get membership type of the caller's organization, with its active subscriber count"""
    membership = db.query(MembershipType).filter(
        MembershipType.id == membership_id,
        MembershipType.organization_id == _organization_id(current_user),
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership type not found")
    return _membership_payload(membership, _active_subscriber_counts(db, [membership.id]).get(membership.id, 0))


@router.get("/membership-types")
def list_membership_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List the organization's active membership types with their active subscriber counts"""
    memberships = MembershipTypeService.list_membership_types(db, _organization_id(current_user))
    counts = _active_subscriber_counts(db, [m.id for m in memberships])
    return [_membership_payload(m, counts.get(m.id, 0)) for m in memberships]


@router.post("/subscriptions")
def create_subscription(
    req: SubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Subscribe to membership"""
    return MembershipSubscriptionService.subscribe_user(
        db, current_user.id, req.membership_type_id, req.stripe_subscription_id
    )


@router.get("/subscriptions/me/active")
def get_active_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active subscription"""
    subscription = MembershipSubscriptionService.get_active_subscription(db, current_user.id)
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    return subscription


@router.post("/subscriptions/{subscription_id}/cancel")
def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel subscription"""
    MembershipSubscriptionService.cancel_subscription(db, subscription_id)
    return {"status": "cancelled"}


@router.post("/subscriptions/{subscription_id}/pause")
def pause_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pause subscription"""
    MembershipSubscriptionService.pause_subscription(db, subscription_id)
    return {"status": "paused"}


@router.get("/subscriptions/{subscription_id}/invoices")
def get_invoices(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get subscription invoices"""
    return MembershipInvoiceService.get_subscription_invoices(db, subscription_id)


@router.post("/subscriptions/{subscription_id}/payment-methods")
def add_payment_method(
    subscription_id: int,
    req: PaymentMethodRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add payment method"""
    return MembershipPaymentMethodService.add_payment_method(
        db, subscription_id, req.card_brand, req.card_last_four, req.stripe_payment_method_id
    )


@router.get("/subscriptions/{subscription_id}/payment-methods")
def get_payment_methods(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payment methods"""
    return MembershipPaymentMethodService.get_payment_methods(db, subscription_id)
