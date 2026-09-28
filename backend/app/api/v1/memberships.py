"""Memberships API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.memberships_service import (
    MembershipTypeService, MembershipSubscriptionService, MembershipInvoiceService,
    MembershipPaymentMethodService
)
from app.models.auth import User
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


@router.post("/membership-types")
def create_membership_type(
    req: MembershipTypeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create membership type"""
    return MembershipTypeService.create_membership_type(db, 1, req.dict())


@router.get("/membership-types/{membership_id}")
def get_membership_type(
    membership_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get membership type"""
    membership = MembershipTypeService.get_membership_type(db, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership type not found")
    return membership


@router.get("/membership-types")
def list_membership_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all membership types"""
    return MembershipTypeService.list_membership_types(db, 1)


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
