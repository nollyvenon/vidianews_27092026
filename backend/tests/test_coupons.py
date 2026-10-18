"""Coupon service: creation rules, discount calculation, redemption limits and checkout application (async)."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.models.ecommerce import CheckoutSession, Coupon, DiscountType
from app.services.coupon_service import CouponService
from app.services.ecommerce_service import CartService, CheckoutService
from app.utils.exceptions import NotFoundError, ValidationError


def _percent(code: str = "TEN", value: str = "10", **extra) -> dict:
    return {"code": code, "discount_type": DiscountType.PERCENT, "discount_value": Decimal(value), **extra}


def _fixed(code: str = "FIVE", value: str = "5", **extra) -> dict:
    return {"code": code, "discount_type": DiscountType.FIXED, "discount_value": Decimal(value), **extra}


@pytest.fixture
async def checkout(session, reference_data):
    """A checkout for user 1 with a subtotal of 99.99 and tax of 8.00, shipping standard at 5.00."""
    cart = await CartService(session).get_or_create_cart(1)
    session_checkout = CheckoutSession(
        checkout_token="coupon-token",
        user_id=1,
        cart_id=cart.id,
        billing_address={"city": "NY"},
        shipping_address={"city": "NY"},
        email="a@example.com",
        subtotal=Decimal("99.99"),
        tax=Decimal("8.00"),
        shipping_cost=Decimal("5.00"),
        discount=Decimal("0.00"),
        total=Decimal("112.99"),
    )
    session.add(session_checkout)
    await session.commit()
    await session.refresh(session_checkout)
    return session_checkout


class TestCreation:
    async def test_codes_are_stored_upper_case(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent(code="  spring10 "))
        assert coupon.code == "SPRING10"
        assert coupon.is_active is True
        assert coupon.redemption_count == 0

    async def test_duplicate_codes_are_refused(self, session, reference_data):
        await CouponService.create_coupon(session, _percent(code="SAME"))
        with pytest.raises(ValidationError):
            await CouponService.create_coupon(session, _fixed(code="same"))

    async def test_percentage_cannot_exceed_one_hundred(self, session, reference_data):
        with pytest.raises(ValidationError):
            await CouponService.create_coupon(session, _percent(code="BIG", value="150"))

    async def test_validity_window_must_be_ordered(self, session, reference_data):
        now = datetime.now(timezone.utc)
        with pytest.raises(ValidationError):
            await CouponService.create_coupon(session, _percent(code="BACKWARDS", valid_from=now, valid_until=now - timedelta(days=1)))

    async def test_activation_can_be_switched_off_and_on(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent(code="TOGGLE"))
        assert (await CouponService.set_active(session, coupon.id, False)).is_active is False
        assert (await CouponService.set_active(session, coupon.id, True)).is_active is True
        with pytest.raises(NotFoundError):
            await CouponService.set_active(session, 999999, False)

    async def test_listing_returns_every_coupon(self, session, reference_data):
        await CouponService.create_coupon(session, _percent(code="ONE"))
        await CouponService.create_coupon(session, _fixed(code="TWO"))
        assert [c.code for c in await CouponService.list_coupons(session)] == ["ONE", "TWO"]


class TestDiscounts:
    async def test_percentage_is_rounded_to_the_cent(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent(value="12.5"))
        assert CouponService.discount_for(coupon, Decimal("99.99")) == Decimal("12.50")

    async def test_fixed_amount_never_exceeds_the_subtotal(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _fixed(value="50"))
        assert CouponService.discount_for(coupon, Decimal("12.00")) == Decimal("12.00")

    async def test_minimum_subtotal_is_enforced(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _fixed(min_subtotal=Decimal("100")))
        with pytest.raises(ValidationError):
            CouponService.discount_for(coupon, Decimal("99.99"))

    async def test_inactive_coupons_are_refused(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent())
        await CouponService.set_active(session, coupon.id, False)
        with pytest.raises(ValidationError):
            CouponService.discount_for(await CouponService.get_coupon(session, coupon.id), Decimal("50"))

    async def test_expired_and_future_coupons_are_refused(self, session, reference_data):
        now = datetime.now(timezone.utc)
        expired = await CouponService.create_coupon(session, _percent(code="OLD", valid_until=now - timedelta(days=1)))
        future = await CouponService.create_coupon(session, _percent(code="SOON", valid_from=now + timedelta(days=1)))
        with pytest.raises(ValidationError, match="expired"):
            CouponService.discount_for(expired, Decimal("50"))
        with pytest.raises(ValidationError, match="not valid yet"):
            CouponService.discount_for(future, Decimal("50"))

    async def test_a_current_window_is_accepted(self, session, reference_data):
        now = datetime.now(timezone.utc)
        coupon = await CouponService.create_coupon(session, _percent(
            code="NOW", valid_from=now - timedelta(days=1), valid_until=now + timedelta(days=1),
        ))
        assert CouponService.discount_for(coupon, Decimal("100")) == Decimal("10.00")


class TestCheckoutApplication:
    async def test_applying_a_coupon_reprices_the_checkout(self, session, checkout):
        await CouponService.create_coupon(session, _percent(code="TEN"))
        applied = await CheckoutService(session).apply_coupon(checkout.id, "ten")
        assert applied.coupon_code == "TEN"
        assert applied.discount == Decimal("10.00")
        assert applied.total == Decimal("99.99") + Decimal("8.00") + Decimal("5.00") - Decimal("10.00")

    async def test_reapplying_the_same_code_counts_one_redemption(self, session, checkout):
        coupon = await CouponService.create_coupon(session, _percent(code="ONCE", max_redemptions=5))
        await CheckoutService(session).apply_coupon(checkout.id, "ONCE")
        await CheckoutService(session).apply_coupon(checkout.id, "ONCE")
        await session.refresh(coupon)
        assert coupon.redemption_count == 1

    async def test_switching_codes_releases_the_previous_redemption(self, session, checkout):
        first = await CouponService.create_coupon(session, _percent(code="FIRST"))
        second = await CouponService.create_coupon(session, _fixed(code="SECOND"))
        await CheckoutService(session).apply_coupon(checkout.id, "FIRST")
        applied = await CheckoutService(session).apply_coupon(checkout.id, "SECOND")
        await session.refresh(first)
        await session.refresh(second)
        assert (first.redemption_count, second.redemption_count) == (0, 1)
        assert applied.discount == Decimal("5.00")

    async def test_redemption_limit_stops_further_checkouts(self, session, checkout, reference_data):
        await CouponService.create_coupon(session, _percent(code="LIMITED", max_redemptions=1))
        await CheckoutService(session).apply_coupon(checkout.id, "LIMITED")

        other_cart = await CartService(session).get_or_create_cart(2)
        other = CheckoutSession(
            checkout_token="other-token", user_id=2, cart_id=other_cart.id, billing_address={}, shipping_address={},
            email="b@example.com", subtotal=Decimal("50.00"), tax=Decimal("4.00"), shipping_cost=Decimal("5.00"),
            discount=Decimal("0.00"), total=Decimal("59.00"),
        )
        session.add(other)
        await session.commit()
        with pytest.raises(ValidationError, match="redemption limit"):
            await CheckoutService(session).apply_coupon(other.id, "LIMITED")

    async def test_reserve_and_release_adjust_the_count(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent(code="COUNT"))
        await CouponService.reserve(session, coupon)
        await CouponService.reserve(session, coupon)
        await session.refresh(coupon)
        assert coupon.redemption_count == 2
        await CouponService.release(session, coupon)
        await CouponService.release(session, coupon)
        await CouponService.release(session, coupon)
        await session.refresh(coupon)
        assert coupon.redemption_count == 0

    async def test_unknown_checkout_is_not_found(self, session, reference_data):
        with pytest.raises(NotFoundError):
            await CheckoutService(session).apply_coupon(999999, "ANY")

    async def test_stored_coupons_are_plain_rows(self, session, reference_data):
        coupon = await CouponService.create_coupon(session, _percent(code="ROW"))
        assert await session.get(Coupon, coupon.id) is not None
