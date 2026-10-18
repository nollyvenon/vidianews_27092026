"""Membership types, subscriptions, invoices and payment methods (async)."""

import uuid
from datetime import timedelta
from typing import List, Optional

from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memberships import (
    utc_now_naive,
    MembershipInvoice,
    MembershipPaymentMethod,
    MembershipSubscription,
    MembershipType,
    SubscriptionStatus,
)
from app.utils.exceptions import NotFoundError

RENEWAL_DAYS = {"monthly": 30, "quarterly": 90}
DEFAULT_RENEWAL_DAYS = 365


def _renewal_delta(membership_type: MembershipType) -> timedelta:
    cycle = membership_type.billing_cycle.value if membership_type.billing_cycle else "monthly"
    return timedelta(days=RENEWAL_DAYS.get(cycle, DEFAULT_RENEWAL_DAYS))


class MembershipTypeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_membership_type(self, org_id: int, type_data: dict) -> MembershipType:
        membership = MembershipType(organization_id=org_id, **type_data)
        self.session.add(membership)
        await self.session.commit()
        await self.session.refresh(membership)
        return membership

    async def get_membership_type(self, membership_id: int) -> Optional[MembershipType]:
        return await self.session.get(MembershipType, membership_id)

    async def list_membership_types(self, org_id: int) -> List[MembershipType]:
        result = await self.session.execute(
            select(MembershipType).where(
                and_(MembershipType.organization_id == org_id, MembershipType.is_active.is_(True))
            ).order_by(MembershipType.id)
        )
        return list(result.scalars().all())

    async def update_membership_type(self, membership_id: int, update_data: dict) -> MembershipType:
        membership = await self.get_membership_type(membership_id)
        if membership is None:
            raise NotFoundError("Membership type")
        for key, value in update_data.items():
            setattr(membership, key, value)
        membership.updated_at = utc_now_naive()
        await self.session.commit()
        await self.session.refresh(membership)
        return membership


class MembershipSubscriptionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get(self, subscription_id: int) -> MembershipSubscription:
        subscription = await self.session.get(MembershipSubscription, subscription_id)
        if subscription is None:
            raise NotFoundError("Subscription")
        return subscription

    async def subscribe_user(
        self,
        user_id: int,
        membership_type_id: int,
        stripe_subscription_id: Optional[str] = None,
    ) -> MembershipSubscription:
        membership_type = await self.session.get(MembershipType, membership_type_id)
        if membership_type is None or not membership_type.is_active:
            raise NotFoundError("Membership type")
        start_date = utc_now_naive()
        subscription = MembershipSubscription(
            user_id=user_id,
            membership_type_id=membership_type_id,
            start_date=start_date,
            renewal_date=start_date + _renewal_delta(membership_type),
            stripe_subscription_id=stripe_subscription_id,
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def get_active_subscription(self, user_id: int) -> Optional[MembershipSubscription]:
        result = await self.session.execute(
            select(MembershipSubscription)
            .where(
                and_(
                    MembershipSubscription.user_id == user_id,
                    MembershipSubscription.status == SubscriptionStatus.ACTIVE,
                )
            )
            .order_by(MembershipSubscription.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_subscription(self, subscription_id: int) -> MembershipSubscription:
        return await self._get(subscription_id)

    async def cancel_subscription(self, subscription_id: int) -> None:
        subscription = await self._get(subscription_id)
        subscription.status = SubscriptionStatus.CANCELLED
        subscription.end_date = utc_now_naive()
        await self.session.commit()

    async def renew_subscription(self, subscription_id: int) -> None:
        subscription = await self._get(subscription_id)
        membership_type = await self.session.get(MembershipType, subscription.membership_type_id)
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.start_date = subscription.renewal_date
        subscription.renewal_date = subscription.renewal_date + _renewal_delta(membership_type)
        await self.session.commit()

    async def pause_subscription(self, subscription_id: int) -> None:
        subscription = await self._get(subscription_id)
        subscription.status = SubscriptionStatus.PAUSED
        await self.session.commit()


class MembershipInvoiceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_invoice(
        self,
        subscription_id: int,
        amount: float,
        stripe_invoice_id: Optional[str] = None,
    ) -> MembershipInvoice:
        if await self.session.get(MembershipSubscription, subscription_id) is None:
            raise NotFoundError("Subscription")
        # The random suffix keeps invoice numbers unique when several are created in the same second.
        invoice_number = f"INV-{int(utc_now_naive().timestamp())}-{uuid.uuid4().hex[:8].upper()}"
        tax_amount = amount * 0.1
        invoice = MembershipInvoice(
            subscription_id=subscription_id,
            invoice_number=invoice_number,
            amount=amount,
            tax_amount=tax_amount,
            total_amount=amount + tax_amount,
            due_date=utc_now_naive() + timedelta(days=30),
            stripe_invoice_id=stripe_invoice_id,
        )
        self.session.add(invoice)
        await self.session.commit()
        await self.session.refresh(invoice)
        return invoice

    async def mark_invoice_paid(self, invoice_id: int) -> None:
        invoice = await self.session.get(MembershipInvoice, invoice_id)
        if invoice is None:
            raise NotFoundError("Invoice")
        invoice.status = "paid"
        invoice.paid_date = utc_now_naive()
        await self.session.commit()

    async def get_subscription_invoices(self, subscription_id: int) -> List[MembershipInvoice]:
        result = await self.session.execute(
            select(MembershipInvoice)
            .where(MembershipInvoice.subscription_id == subscription_id)
            .order_by(MembershipInvoice.created_at.desc(), MembershipInvoice.id.desc())
        )
        return list(result.scalars().all())


class MembershipPaymentMethodService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_payment_method(
        self,
        subscription_id: int,
        card_brand: str,
        card_last_four: str,
        stripe_payment_method_id: str,
    ) -> MembershipPaymentMethod:
        if await self.session.get(MembershipSubscription, subscription_id) is None:
            raise NotFoundError("Subscription")
        payment_method = MembershipPaymentMethod(
            subscription_id=subscription_id,
            card_brand=card_brand,
            card_last_four=card_last_four,
            stripe_payment_method_id=stripe_payment_method_id,
            is_default=True,
        )
        self.session.add(payment_method)
        # Flush so the new row has an id; without it the update below would also clear the new row's default.
        await self.session.flush()
        await self.session.execute(
            update(MembershipPaymentMethod)
            .where(
                and_(
                    MembershipPaymentMethod.subscription_id == subscription_id,
                    MembershipPaymentMethod.id != payment_method.id,
                )
            )
            .values(is_default=False)
        )
        await self.session.commit()
        await self.session.refresh(payment_method)
        return payment_method

    async def get_payment_methods(self, subscription_id: int) -> List[MembershipPaymentMethod]:
        result = await self.session.execute(
            select(MembershipPaymentMethod)
            .where(MembershipPaymentMethod.subscription_id == subscription_id)
            .order_by(MembershipPaymentMethod.id)
        )
        return list(result.scalars().all())

    async def set_default_payment_method(self, payment_method_id: int) -> None:
        payment_method = await self.session.get(MembershipPaymentMethod, payment_method_id)
        if payment_method is None:
            raise NotFoundError("Payment method")
        await self.session.execute(
            update(MembershipPaymentMethod)
            .where(MembershipPaymentMethod.subscription_id == payment_method.subscription_id)
            .values(is_default=False)
        )
        payment_method.is_default = True
        await self.session.commit()


async def active_subscriber_counts(session: AsyncSession, membership_ids: List[int]) -> dict:
    if not membership_ids:
        return {}
    result = await session.execute(
        select(MembershipSubscription.membership_type_id, func.count(MembershipSubscription.id))
        .where(
            MembershipSubscription.membership_type_id.in_(membership_ids),
            MembershipSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .group_by(MembershipSubscription.membership_type_id)
    )
    return dict(result.all())
