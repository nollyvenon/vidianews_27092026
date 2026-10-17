"""Admin management of subscriptions and transactions."""

from app.core.security import get_current_user
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import require_admin
from app.db.session import get_db
from app.models.monetization import SubscriptionTier
from app.models.user import User
from app.services.billing_admin_service import BillingAdminError, BillingAdminService

router = APIRouter(prefix="/admin", tags=["billing-admin"])

require_billing_admin = require_admin("billing")


class SubscriptionAdminView(BaseModel):
    id: int
    user_id: int
    user_email: Optional[str]
    organization_id: int
    tier: Optional[str]
    billing_cycle: Optional[str]
    amount: float
    is_active: bool
    started_at: Optional[datetime]
    renews_at: Optional[datetime]
    canceled_at: Optional[datetime]


class SubscriptionPage(BaseModel):
    items: List[SubscriptionAdminView]
    total: int
    skip: int
    limit: int


class SubscriptionUpdate(BaseModel):
    tier: Optional[SubscriptionTier] = None
    renews_at: Optional[datetime] = None


class TransactionView(BaseModel):
    source: str
    id: int
    user_id: Optional[int]
    user_email: Optional[str]
    amount: float
    currency: str
    status: Optional[str]
    payment_method: Optional[str]
    reference: Optional[str]
    created_at: Optional[datetime]


class TransactionPage(BaseModel):
    items: List[TransactionView]
    total: int
    skip: int
    limit: int


def _raise(error: BillingAdminError) -> None:
    raise HTTPException(status_code=error.status_code, detail=error.message)


@router.get("/subscriptions", response_model=SubscriptionPage)
async def list_subscriptions(
    is_active: Optional[bool] = Query(None, description="Filter by active (true) or canceled (false)"),
    tier: Optional[SubscriptionTier] = None,
    user_id: Optional[int] = Query(None, ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _admin: User = Depends(require_billing_admin),
    session: AsyncSession = Depends(get_db),
):
    """Every subscription with the account email, newest first."""
    items, total = await BillingAdminService(session).list_subscriptions(
        is_active=is_active, tier=tier, user_id=user_id, skip=skip, limit=limit,
    )
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.patch("/subscriptions/{subscription_id}", response_model=SubscriptionAdminView)
async def update_subscription(
    subscription_id: int,
    payload: SubscriptionUpdate,
    admin: User = Depends(require_billing_admin),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Change a subscription's tier or next renewal date."""
    if payload.tier is None and payload.renews_at is None:
        raise HTTPException(status_code=422, detail="Provide tier and/or renews_at")
    try:
        return await BillingAdminService(session).update_subscription(
            subscription_id,
            actor_user_id=admin.id,
            tier=payload.tier,
            renews_at=payload.renews_at,
        )
    except BillingAdminError as error:
        _raise(error)


@router.post("/subscriptions/{subscription_id}/cancel", response_model=SubscriptionAdminView)
async def cancel_subscription(
    subscription_id: int,
    admin: User = Depends(require_billing_admin),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancel a subscription. Canceling an already canceled subscription returns it unchanged."""
    try:
        return await BillingAdminService(session).cancel_subscription(subscription_id, actor_user_id=admin.id)
    except BillingAdminError as error:
        _raise(error)


@router.get("/transactions", response_model=TransactionPage)
async def list_transactions(
    source: str = Query("all", pattern="^(all|subscription|checkout)$"),
    status: Optional[str] = Query(None, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _admin: User = Depends(require_billing_admin),
    session: AsyncSession = Depends(get_db),
):
    """Subscription payments and checkout payments, newest first.

    ``source`` selects one side or both (``all``). ``status`` is matched against each
    side's own status values (for example ``completed``, ``failed``, ``refunded``).
    """
    try:
        items, total = await BillingAdminService(session).list_transactions(
            source=source, status=status, skip=skip, limit=limit,
        )
    except BillingAdminError as error:
        _raise(error)
    return {"items": items, "total": total, "skip": skip, "limit": limit}
