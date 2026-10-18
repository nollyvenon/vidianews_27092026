"""Route tests for discount codes: administrators manage them, customers apply them at checkout."""

from decimal import Decimal

from app.core.security import create_access_token
from app.models.ecommerce import CheckoutSession, DiscountType
from app.models.user import User
from app.services.coupon_service import CouponService
from app.services.ecommerce_service import CartService

NEW_CODE = {"code": "save10", "discount_type": DiscountType.PERCENT.value, "discount_value": 10, "min_subtotal": 0}


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


async def _checkout_for(session, user_id: int) -> CheckoutSession:
    cart = await CartService(session).get_or_create_cart(user_id)
    checkout = CheckoutSession(
        checkout_token=f"route-token-{user_id}", user_id=user_id, cart_id=cart.id,
        billing_address={"city": "NY"}, shipping_address={"city": "NY"}, email="a@example.com",
        subtotal=Decimal("100.00"), tax=Decimal("8.00"), shipping_cost=Decimal("5.00"),
        discount=Decimal("0.00"), total=Decimal("113.00"),
    )
    session.add(checkout)
    await session.commit()
    await session.refresh(checkout)
    return checkout


class TestCouponAdministration:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/coupons")).status_code == 401

    async def test_customers_cannot_manage_codes(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        assert (await async_client.get("/api/v1/coupons", headers=headers)).status_code == 403
        assert (await async_client.post("/api/v1/coupons", json=NEW_CODE, headers=headers)).status_code == 403

    async def test_administrator_creates_lists_and_disables_a_code(self, async_client, platform_admin, reference_data):
        created = await async_client.post("/api/v1/coupons", json=NEW_CODE, headers=platform_admin)
        assert created.status_code == 201
        assert created.json()["code"] == "SAVE10"
        assert created.json()["redemption_count"] == 0

        listed = await async_client.get("/api/v1/coupons", headers=platform_admin)
        assert [row["code"] for row in listed.json()] == ["SAVE10"]

        disabled = await async_client.patch(
            f"/api/v1/coupons/{created.json()['id']}", json={"is_active": False}, headers=platform_admin,
        )
        assert disabled.status_code == 200
        assert disabled.json()["is_active"] is False

    async def test_invalid_codes_are_refused(self, async_client, platform_admin, reference_data):
        too_big = await async_client.post(
            "/api/v1/coupons", json={**NEW_CODE, "discount_value": 150}, headers=platform_admin,
        )
        assert too_big.status_code == 422

    async def test_unknown_coupon_status_is_not_found(self, async_client, platform_admin, reference_data):
        response = await async_client.patch("/api/v1/coupons/999999", json={"is_active": True}, headers=platform_admin)
        assert response.status_code == 404


class TestCouponAtCheckout:
    async def test_customer_applies_a_valid_code(self, async_client, reference_data, session):
        await CouponService.create_coupon(session, {
            "code": "SAVE10", "discount_type": DiscountType.PERCENT, "discount_value": Decimal("10"),
        })
        checkout = await _checkout_for(session, 2)
        response = await async_client.post(
            f"/api/v1/checkout/{checkout.id}/coupon?coupon_code=save10", headers=await _headers_for(session, 2),
        )
        assert response.status_code == 200
        body = response.json()
        assert body["coupon_code"] == "SAVE10"
        assert Decimal(str(body["discount"])) == Decimal("10.00")
        assert Decimal(str(body["total"])) == Decimal("103.00")

    async def test_disabled_codes_are_refused_at_checkout(self, async_client, reference_data, session):
        coupon = await CouponService.create_coupon(session, {
            "code": "OFF", "discount_type": DiscountType.FIXED, "discount_value": Decimal("5"),
        })
        await CouponService.set_active(session, coupon.id, False)
        checkout = await _checkout_for(session, 2)
        response = await async_client.post(
            f"/api/v1/checkout/{checkout.id}/coupon?coupon_code=OFF", headers=await _headers_for(session, 2),
        )
        assert response.status_code == 422

    async def test_customers_cannot_apply_codes_to_someone_elses_checkout(self, async_client, org_member, reference_data, session):
        await CouponService.create_coupon(session, {
            "code": "SAVE10", "discount_type": DiscountType.PERCENT, "discount_value": Decimal("10"),
        })
        checkout = await _checkout_for(session, 2)
        response = await async_client.post(
            f"/api/v1/checkout/{checkout.id}/coupon?coupon_code=SAVE10", headers=org_member,
        )
        assert response.status_code == 404
