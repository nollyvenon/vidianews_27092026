"""Administrative management of subscriptions and transactions (subscription payments and checkout payments)."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ecommerce import CheckoutSession, PaymentDetail, PaymentStatus as EcommercePaymentStatus
from app.models.monetization import Payment, PaymentStatus, Subscription, SubscriptionTier
from app.models.user import User
from app.utils.logger import logger

TRANSACTION_SOURCES = ("subscription", "checkout")


class BillingAdminError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _subscription_view(sub: Subscription, email: Optional[str]) -> Dict[str, Any]:
    return {
        "id": sub.id,
        "user_id": sub.user_id,
        "user_email": email,
        "organization_id": sub.organization_id,
        "tier": sub.tier.value if sub.tier else None,
        "billing_cycle": sub.billing_cycle.value if sub.billing_cycle else None,
        "amount": sub.amount,
        "is_active": bool(sub.is_active),
        "started_at": sub.started_at,
        "renews_at": sub.renews_at,
        "canceled_at": sub.canceled_at,
    }


def _subscription_payment_view(payment: Payment, email: Optional[str]) -> Dict[str, Any]:
    return {
        "source": "subscription",
        "id": payment.id,
        "user_id": payment.user_id,
        "user_email": email,
        "amount": float(payment.amount),
        "currency": "USD",
        "status": payment.status.value if payment.status else None,
        "payment_method": payment.payment_method,
        "reference": payment.stripe_payment_id,
        "created_at": payment.created_at,
    }


def _checkout_payment_view(detail: PaymentDetail, email: Optional[str]) -> Dict[str, Any]:
    return {
        "source": "checkout",
        "id": detail.id,
        "user_id": None,
        "user_email": email,
        "amount": float(detail.amount),
        "currency": detail.currency or "USD",
        "status": detail.status.value if detail.status else None,
        "payment_method": detail.payment_method.value if detail.payment_method else None,
        "reference": detail.transaction_id,
        "created_at": detail.created_at,
    }


def _enum_or_none(enum_cls, value: Optional[str]):
    if value is None:
        return None
    try:
        return enum_cls(value)
    except ValueError as exc:
        raise BillingAdminError(f"Unknown payment status: {value}", 422) from exc


class BillingAdminService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ----- subscriptions ----------------------------------------------------------

    async def list_subscriptions(
        self,
        *,
        is_active: Optional[bool] = None,
        tier: Optional[SubscriptionTier] = None,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Dict[str, Any]], int]:
        filters = []
        if is_active is not None:
            filters.append(Subscription.is_active.is_(is_active))
        if tier is not None:
            filters.append(Subscription.tier == tier)
        if user_id is not None:
            filters.append(Subscription.user_id == user_id)

        total = (await self.session.execute(
            select(func.count(Subscription.id)).where(*filters)
        )).scalar_one()
        stmt = (
            select(Subscription, User.email)
            .outerjoin(User, User.id == Subscription.user_id)
            .where(*filters)
            .order_by(Subscription.started_at.desc(), Subscription.id.desc())
            .offset(skip)
            .limit(limit)
        )
        rows = (await self.session.execute(stmt)).all()
        return [_subscription_view(sub, email) for sub, email in rows], total

    async def update_subscription(
        self,
        subscription_id: int,
        *,
        actor_user_id: int,
        tier: Optional[SubscriptionTier] = None,
        renews_at: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        sub, email = await self._get_subscription(subscription_id)
        if tier is not None:
            sub.tier = tier
        if renews_at is not None:
            sub.renews_at = renews_at
        await self.session.commit()
        logger.info(f"Subscription {subscription_id} updated by user {actor_user_id} (tier={tier}, renews_at={renews_at})")
        return _subscription_view(sub, email)

    async def cancel_subscription(self, subscription_id: int, *, actor_user_id: int) -> Dict[str, Any]:
        sub, email = await self._get_subscription(subscription_id)
        if sub.is_active:
            sub.is_active = False
            sub.canceled_at = datetime.now(timezone.utc)
            await self.session.commit()
            logger.info(f"Subscription {subscription_id} canceled by user {actor_user_id}")
        return _subscription_view(sub, email)

    async def _get_subscription(self, subscription_id: int) -> Tuple[Subscription, Optional[str]]:
        row = (await self.session.execute(
            select(Subscription, User.email)
            .outerjoin(User, User.id == Subscription.user_id)
            .where(Subscription.id == subscription_id)
        )).first()
        if row is None:
            raise BillingAdminError("Subscription not found", 404)
        return row[0], row[1]

    # ----- transactions -----------------------------------------------------------

    async def list_transactions(
        self,
        *,
        source: str = "all",
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Newest-first transactions across subscription payments and checkout payments.

        Each side is fetched up to ``skip + limit`` rows, merged, then sliced, which keeps
        offset paging correct across the two tables.
        """
        if source not in ("all", *TRANSACTION_SOURCES):
            raise BillingAdminError(f"Unknown transaction source: {source}", 422)
        window = skip + limit
        merged: List[Dict[str, Any]] = []
        total = 0
        subscription_status = _enum_or_none(PaymentStatus, status)
        checkout_status = _enum_or_none(EcommercePaymentStatus, status)

        if source in ("all", "subscription"):
            filters = [Payment.status == subscription_status] if subscription_status is not None else []
            total += (await self.session.execute(select(func.count(Payment.id)).where(*filters))).scalar_one()
            rows = (await self.session.execute(
                select(Payment, User.email)
                .outerjoin(User, User.id == Payment.user_id)
                .where(*filters)
                .order_by(Payment.created_at.desc(), Payment.id.desc())
                .limit(window)
            )).all()
            merged.extend(_subscription_payment_view(payment, email) for payment, email in rows)

        if source in ("all", "checkout"):
            filters = [PaymentDetail.status == checkout_status] if checkout_status is not None else []
            total += (await self.session.execute(
                select(func.count(PaymentDetail.id)).where(*filters)
            )).scalar_one()
            rows = (await self.session.execute(
                select(PaymentDetail, User.email)
                .join(CheckoutSession, CheckoutSession.id == PaymentDetail.checkout_id)
                .outerjoin(User, User.id == CheckoutSession.user_id)
                .where(*filters)
                .order_by(PaymentDetail.created_at.desc(), PaymentDetail.id.desc())
                .limit(window)
            )).all()
            merged.extend(_checkout_payment_view(detail, email) for detail, email in rows)

        merged.sort(key=lambda item: item["created_at"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        return merged[skip:window], total
