"""Coupon management: creation, validation, discount calculation and redemption counting (async).

A coupon is reserved (its redemption counted) when a checkout applies it, so the usage limit holds under
concurrent checkouts. Applying a different code releases the reservation of the previous one.
"""

from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ecommerce import CheckoutSession, Coupon, DiscountType
from app.utils.exceptions import NotFoundError, ValidationError

CENT = Decimal("0.01")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def normalise_code(code: str) -> str:
    return code.strip().upper()


class CouponService:
    @staticmethod
    async def create_coupon(session: AsyncSession, data: dict) -> Coupon:
        code = normalise_code(data["code"])
        if await CouponService.get_by_code(session, code) is not None:
            raise ValidationError("A coupon with this code already exists")
        if data["discount_type"] == DiscountType.PERCENT and data["discount_value"] > Decimal("100"):
            raise ValidationError("A percentage discount cannot exceed 100")
        valid_from, valid_until = data.get("valid_from"), data.get("valid_until")
        if valid_from and valid_until and valid_until <= valid_from:
            raise ValidationError("valid_until must be after valid_from")

        coupon = Coupon(
            code=code,
            discount_type=data["discount_type"],
            discount_value=data["discount_value"],
            min_subtotal=data.get("min_subtotal") or Decimal("0.00"),
            max_redemptions=data.get("max_redemptions"),
            valid_from=valid_from,
            valid_until=valid_until,
            is_active=True,
            redemption_count=0,
        )
        session.add(coupon)
        await session.commit()
        await session.refresh(coupon)
        return coupon

    @staticmethod
    async def list_coupons(session: AsyncSession) -> List[Coupon]:
        result = await session.execute(select(Coupon).order_by(Coupon.id))
        return list(result.scalars().all())

    @staticmethod
    async def get_coupon(session: AsyncSession, coupon_id: int) -> Optional[Coupon]:
        return await session.get(Coupon, coupon_id)

    @staticmethod
    async def get_by_code(session: AsyncSession, code: str) -> Optional[Coupon]:
        return (await session.execute(
            select(Coupon).where(Coupon.code == normalise_code(code))
        )).scalar_one_or_none()

    @staticmethod
    async def set_active(session: AsyncSession, coupon_id: int, is_active: bool) -> Coupon:
        coupon = await session.get(Coupon, coupon_id)
        if coupon is None:
            raise NotFoundError("Coupon")
        coupon.is_active = is_active
        coupon.updated_at = _now()
        await session.commit()
        await session.refresh(coupon)
        return coupon

    @staticmethod
    def discount_for(coupon: Coupon, subtotal: Decimal, now: Optional[datetime] = None) -> Decimal:
        """The amount `coupon` takes off `subtotal`. Raises ValidationError when the coupon cannot be used."""
        now = now or _now()
        if not coupon.is_active:
            raise ValidationError("Coupon code is not valid")
        if coupon.valid_from and now < coupon.valid_from:
            raise ValidationError("Coupon is not valid yet")
        if coupon.valid_until and now >= coupon.valid_until:
            raise ValidationError("Coupon has expired")
        if subtotal < coupon.min_subtotal:
            raise ValidationError(f"Coupon requires a subtotal of at least {coupon.min_subtotal}")
        if coupon.discount_type == DiscountType.PERCENT:
            discount = (subtotal * coupon.discount_value / Decimal("100")).quantize(CENT, rounding=ROUND_HALF_UP)
        else:
            discount = coupon.discount_value
        return min(discount, subtotal).quantize(CENT, rounding=ROUND_HALF_UP)

    @staticmethod
    async def reserve(session: AsyncSession, coupon: Coupon) -> None:
        """Count one redemption, refusing when the limit is already reached. Atomic in the database."""
        result = await session.execute(
            update(Coupon)
            .where(
                Coupon.id == coupon.id,
                or_(Coupon.max_redemptions.is_(None), Coupon.redemption_count < Coupon.max_redemptions),
            )
            .values(redemption_count=Coupon.redemption_count + 1)
            .execution_options(synchronize_session=False)
        )
        if result.rowcount != 1:
            raise ValidationError("Coupon has reached its redemption limit")

    @staticmethod
    async def release(session: AsyncSession, coupon: Coupon) -> None:
        await session.execute(
            update(Coupon)
            .where(Coupon.id == coupon.id, Coupon.redemption_count > 0)
            .values(redemption_count=Coupon.redemption_count - 1)
            .execution_options(synchronize_session=False)
        )

    @staticmethod
    async def apply_to_checkout(session: AsyncSession, checkout: CheckoutSession, code: str) -> CheckoutSession:
        coupon = await CouponService.get_by_code(session, code)
        if coupon is None:
            raise ValidationError("Coupon code is not valid")

        discount = CouponService.discount_for(coupon, checkout.subtotal)
        if checkout.coupon_code != coupon.code:
            await CouponService.reserve(session, coupon)
            previous = await CouponService.get_by_code(session, checkout.coupon_code) if checkout.coupon_code else None
            if previous is not None:
                await CouponService.release(session, previous)
            checkout.coupon_code = coupon.code

        checkout.discount = discount
        checkout.total = checkout.subtotal + checkout.tax + checkout.shipping_cost - discount
        await session.commit()
        await session.refresh(checkout)
        return checkout
