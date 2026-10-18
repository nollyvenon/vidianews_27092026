"""The signed-in account's subscription, invoices and payments (read-only)."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.billing_account_service import (
    BillingAccountService,
    invoice_view,
    payment_view,
    subscription_view,
)

router = APIRouter(prefix="/billing", tags=["billing"])


class SubscriptionOut(BaseModel):
    id: int
    tier: Optional[str]
    billing_cycle: Optional[str]
    amount: float
    is_active: bool
    started_at: Optional[datetime]
    renews_at: Optional[datetime]
    canceled_at: Optional[datetime]


class InvoiceOut(BaseModel):
    id: int
    subscription_id: int
    amount: float
    status: Optional[str]
    due_date: Optional[datetime]
    paid_date: Optional[datetime]
    created_at: Optional[datetime]


class PaymentOut(BaseModel):
    id: int
    invoice_id: int
    amount: float
    status: Optional[str]
    payment_method: Optional[str]
    created_at: Optional[datetime]


@router.get("/subscription", response_model=SubscriptionOut)
async def get_my_subscription(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """The active subscription, or the most recent one if none is active."""
    sub = await BillingAccountService(session, user.id).current_subscription()
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription on this account")
    return subscription_view(sub)


@router.get("/invoices", response_model=List[InvoiceOut])
async def list_my_invoices(
    limit: int = Query(100, ge=1, le=200),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    invoices = await BillingAccountService(session, user.id).invoices(limit)
    return [invoice_view(invoice) for invoice in invoices]


@router.get("/payments", response_model=List[PaymentOut])
async def list_my_payments(
    limit: int = Query(100, ge=1, le=200),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    payments = await BillingAccountService(session, user.id).payments(limit)
    return [payment_view(payment) for payment in payments]
