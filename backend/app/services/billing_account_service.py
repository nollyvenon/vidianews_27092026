"""The signed-in account's own subscription, invoices and payments."""

from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monetization import Invoice, Payment, Subscription


def subscription_view(sub: Subscription) -> Dict[str, Any]:
    return {
        "id": sub.id,
        "tier": sub.tier.value if sub.tier else None,
        "billing_cycle": sub.billing_cycle.value if sub.billing_cycle else None,
        "amount": float(sub.amount or 0),
        "is_active": bool(sub.is_active),
        "started_at": sub.started_at,
        "renews_at": sub.renews_at,
        "canceled_at": sub.canceled_at,
    }


def invoice_view(invoice: Invoice) -> Dict[str, Any]:
    return {
        "id": invoice.id,
        "subscription_id": invoice.subscription_id,
        "amount": float(invoice.amount or 0),
        "status": invoice.status.value if invoice.status else None,
        "due_date": invoice.due_date,
        "paid_date": invoice.paid_date,
        "created_at": invoice.created_at,
    }


def payment_view(payment: Payment) -> Dict[str, Any]:
    return {
        "id": payment.id,
        "invoice_id": payment.invoice_id,
        "amount": float(payment.amount or 0),
        "status": payment.status.value if payment.status else None,
        "payment_method": payment.payment_method,
        "created_at": payment.created_at,
    }


class BillingAccountService:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def current_subscription(self) -> Optional[Subscription]:
        """The active subscription if there is one, otherwise the most recent one."""
        result = await self.session.execute(
            select(Subscription)
            .where(Subscription.user_id == self.user_id)
            .order_by(Subscription.is_active.desc(), Subscription.started_at.desc(), Subscription.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def invoices(self, limit: int = 100) -> List[Invoice]:
        result = await self.session.execute(
            select(Invoice)
            .join(Subscription, Subscription.id == Invoice.subscription_id)
            .where(Subscription.user_id == self.user_id)
            .order_by(Invoice.created_at.desc(), Invoice.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def payments(self, limit: int = 100) -> List[Payment]:
        result = await self.session.execute(
            select(Payment)
            .where(Payment.user_id == self.user_id)
            .order_by(Payment.created_at.desc(), Payment.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
