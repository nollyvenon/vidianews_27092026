"""Route tests for extended ecommerce: who may see and change shipments, returns, wishlists and stock."""

import uuid
from decimal import Decimal


from app.core.security import create_access_token
from app.models.ecommerce import Order, PaymentMethod, Product, ProductCategory, ProductStatus
from app.models.ecommerce_extended import ReturnReason, ShippingCarrier
from app.models.user import User
from app.services.ecommerce_extended_service import (
    InventoryService,
    ReturnService,
    ShippingService,
    WishlistService,
)

SHIPMENT = {"carrier": "ups", "tracking_number": "1Z-ROUTE-1", "base_rate": 5, "total_cost": 6}
ADDRESS = {
    "first_name": "Grace", "last_name": "Hopper", "street_address": "2 Harbor Rd", "city": "Arlington",
    "postal_code": "22201", "country": "US",
}


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


async def _stranger_headers(session) -> dict:
    """A signed-in user with no roles, so they are neither the owner nor an administrator."""
    user = User(email="stranger@example.com", password_hash="hash")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return await _headers_for(session, user.id)


async def _product(session, sku: str = "ROUTE-001") -> Product:
    product = Product(
        sku=sku, name="Route Product", price=Decimal("30.00"), category=ProductCategory.ELECTRONICS,
        status=ProductStatus.PUBLISHED,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def _order(session, user_id: int) -> Order:
    order = Order(
        order_number=f"ORD-ROUTE-{uuid.uuid4().hex[:10].upper()}", user_id=user_id,
        billing_address={"city": "NY"}, shipping_address={"city": "NY"}, email="x@example.com",
        subtotal=Decimal("30.00"), total=Decimal("30.00"), payment_method=PaymentMethod.STRIPE,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


class TestShippingAccess:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/shipping-addresses")).status_code == 401

    async def test_customers_manage_their_own_addresses(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        created = await async_client.post("/api/v1/shipping-addresses", json=ADDRESS, headers=headers)
        listed = await async_client.get("/api/v1/shipping-addresses", headers=headers)
        other = await async_client.get("/api/v1/shipping-addresses", headers=org_member)
        assert created.status_code == 201
        assert [a["city"] for a in listed.json()] == ["Arlington"]
        assert other.json() == []

    async def test_customers_cannot_create_shipments(self, async_client, org_member, reference_data, session):
        order = await _order(session, 2)
        response = await async_client.post(f"/api/v1/orders/{order.id}/shipment", json=SHIPMENT, headers=await _headers_for(session, 2))
        assert response.status_code == 403

    async def test_administrator_creates_a_shipment_and_tracking(self, async_client, platform_admin, reference_data, session):
        order = await _order(session, 2)
        admin = platform_admin
        created = await async_client.post(f"/api/v1/orders/{order.id}/shipment", json=SHIPMENT, headers=admin)
        assert created.status_code == 201
        assert created.json()["carrier"] == ShippingCarrier.UPS.value
        shipment_id = created.json()["id"]

        event = await async_client.post(
            f"/api/v1/shipments/{shipment_id}/tracking", json={"status": "in_transit", "location": "Dallas"}, headers=admin,
        )
        assert event.status_code == 201
        assert event.json()["timestamp"]

    async def test_shipment_for_an_unknown_order_is_not_found(self, async_client, platform_admin, reference_data):
        response = await async_client.post(
            "/api/v1/orders/999999/shipment", json=SHIPMENT, headers=platform_admin,
        )
        assert response.status_code == 404

    async def test_tracking_is_visible_to_the_owner_and_administrators_only(
        self, async_client, org_member, platform_admin, reference_data, session,
    ):
        order = await _order(session, 2)
        shipment = await ShippingService.create_shipment(session, order.id, {
            "carrier": ShippingCarrier.FEDEX, "tracking_number": "FX-1", "base_rate": Decimal("4"), "total_cost": Decimal("5"),
        })
        await ShippingService.add_tracking_event(session, shipment.id, {"status": "picked_up"})

        owner = await async_client.get(f"/api/v1/shipments/{shipment.id}/tracking", headers=await _headers_for(session, 2))
        admin = await async_client.get(f"/api/v1/shipments/{shipment.id}/tracking", headers=platform_admin)
        stranger = await async_client.get(
            f"/api/v1/shipments/{shipment.id}/tracking", headers=await _stranger_headers(session),
        )
        assert owner.status_code == 200 and owner.json()[0]["status"] == "picked_up"
        assert admin.status_code == 200
        assert stranger.status_code == 404


class TestInventoryAccess:
    async def test_stock_level_is_readable_by_signed_in_users(self, async_client, org_member, reference_data, session):
        product = await _product(session)
        response = await async_client.get(f"/api/v1/products/{product.id}/inventory", headers=org_member)
        assert response.status_code == 200
        assert response.json()["quantity_on_hand"] == 0

    async def test_unknown_product_stock_is_not_found(self, async_client, org_member, reference_data):
        assert (await async_client.get("/api/v1/products/999999/inventory", headers=org_member)).status_code == 404

    async def test_stock_reports_are_for_administrators(self, async_client, platform_admin, reference_data, session):
        product = await _product(session)
        await InventoryService.update_stock(session, product.id, 2, "restock")
        for path in ("/api/v1/inventory/low-stock", "/api/v1/inventory/out-of-stock"):
            assert (await async_client.get(path, headers=await _headers_for(session, 2))).status_code == 403
        low = await async_client.get("/api/v1/inventory/low-stock", headers=platform_admin)
        assert low.status_code == 200
        assert [row["product_id"] for row in low.json()] == [product.id]


class TestWishlistAccess:
    async def test_wishlist_items_belong_to_their_owner(self, async_client, org_member, reference_data, session):
        product = await _product(session)
        owner_headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Gifts"}, headers=owner_headers)).json()
        added = await async_client.post(f"/api/v1/wishlists/{wishlist['id']}/items/{product.id}", headers=owner_headers)
        assert added.status_code == 201
        item_id = added.json()["id"]

        stolen = await async_client.delete(f"/api/v1/wishlist-items/{item_id}", headers=org_member)
        assert stolen.status_code == 404
        listed = await async_client.get(f"/api/v1/wishlists/{wishlist['id']}/items", headers=org_member)
        assert listed.status_code == 404

        removed = await async_client.delete(f"/api/v1/wishlist-items/{item_id}", headers=owner_headers)
        assert removed.status_code == 200

    async def test_adding_an_unknown_product_is_not_found(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Gifts"}, headers=headers)).json()
        response = await async_client.post(f"/api/v1/wishlists/{wishlist['id']}/items/999999", headers=headers)
        assert response.status_code == 404

    async def test_adding_the_same_product_twice_is_refused(self, async_client, reference_data, session):
        product = await _product(session)
        headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Gifts"}, headers=headers)).json()
        first = await async_client.post(f"/api/v1/wishlists/{wishlist['id']}/items/{product.id}", headers=headers)
        second = await async_client.post(f"/api/v1/wishlists/{wishlist['id']}/items/{product.id}", headers=headers)
        assert first.status_code == 201
        assert second.status_code == 422

    async def test_public_wishlists_are_shared_by_token(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        public = (await async_client.post("/api/v1/wishlists", json={"name": "Open", "is_public": True}, headers=headers)).json()
        private = (await async_client.post("/api/v1/wishlists", json={"name": "Closed"}, headers=headers)).json()
        assert (await async_client.get(f"/api/v1/wishlists/share/{public['share_token']}")).status_code == 200
        assert (await async_client.get(f"/api/v1/wishlists/share/{private['share_token']}")).status_code == 404

    async def test_another_users_wishlist_is_not_found(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Private"}, headers=headers)).json()
        assert (await async_client.get(f"/api/v1/wishlists/{wishlist['id']}", headers=org_member)).status_code == 404

    async def test_in_wishlist_check_is_for_the_caller(self, async_client, org_member, reference_data, session):
        product = await _product(session)
        headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Gifts"}, headers=headers)).json()
        await WishlistService.add_to_wishlist(session, wishlist["id"], product.id)
        mine = await async_client.get(f"/api/v1/products/{product.id}/in-wishlist", headers=headers)
        theirs = await async_client.get(f"/api/v1/products/{product.id}/in-wishlist", headers=org_member)
        assert mine.json()["in_wishlist"] is True
        assert theirs.json()["in_wishlist"] is False


class TestReturnAccess:
    async def test_customers_request_returns_only_for_their_orders(self, async_client, org_member, reference_data, session):
        order = await _order(session, 2)
        body = {"reason": ReturnReason.DAMAGED.value, "quantity_requested": 1}
        own = await async_client.post(f"/api/v1/orders/{order.id}/return", json=body, headers=await _headers_for(session, 2))
        stranger = await async_client.post(f"/api/v1/orders/{order.id}/return", json=body, headers=org_member)
        assert own.status_code == 201
        assert own.json()["rma_number"].startswith("RMA-")
        assert stranger.status_code == 404

    async def test_returns_are_visible_to_the_owner_and_administrators(
        self, async_client, org_member, platform_admin, reference_data, session,
    ):
        order = await _order(session, 2)
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": 1,
        })
        owner = await _headers_for(session, 2)
        assert (await async_client.get(f"/api/v1/returns/{request.id}", headers=owner)).status_code == 200
        assert (await async_client.get(f"/api/v1/returns/{request.id}", headers=platform_admin)).status_code == 200
        stranger = await _stranger_headers(session)
        assert (await async_client.get(f"/api/v1/returns/{request.id}", headers=stranger)).status_code == 404
        assert (await async_client.get(f"/api/v1/orders/{order.id}/returns", headers=owner)).status_code == 200
        assert (await async_client.get(f"/api/v1/orders/{order.id}/returns", headers=stranger)).status_code == 404

    async def test_return_decisions_are_for_administrators(self, async_client, org_member, platform_admin, reference_data, session):
        order = await _order(session, 2)
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": 1,
        })
        customer = await _headers_for(session, 2)
        assert (await async_client.get("/api/v1/returns/pending", headers=customer)).status_code == 403
        assert (await async_client.post(f"/api/v1/returns/{request.id}/approve", headers=customer)).status_code == 403
        assert (await async_client.post(f"/api/v1/returns/{request.id}/refund", headers=customer)).status_code == 403

        approved = await async_client.post(f"/api/v1/returns/{request.id}/approve", headers=platform_admin)
        assert approved.status_code == 200
        refused_again = await async_client.post(f"/api/v1/returns/{request.id}/approve", headers=platform_admin)
        assert refused_again.status_code == 422

        pending = await async_client.get("/api/v1/returns/pending", headers=platform_admin)
        assert [row["id"] for row in pending.json()] == [request.id]

    async def test_full_return_flow_through_the_routes(self, async_client, platform_admin, reference_data, session):
        order = await _order(session, 2)
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.WRONG_ITEM, "quantity_requested": 1,
        })
        admin = platform_admin
        assert (await async_client.post(f"/api/v1/returns/{request.id}/approve?refund_amount=30", headers=admin)).status_code == 200
        assert (await async_client.post(f"/api/v1/returns/{request.id}/receive?quantity_received=1", headers=admin)).status_code == 200
        assert (await async_client.post(f"/api/v1/returns/{request.id}/refund", headers=admin)).status_code == 200
        done = await async_client.get(f"/api/v1/returns/{request.id}", headers=admin)
        assert done.json()["status"] == "refunded"
        assert Decimal(done.json()["refund_amount"]) == Decimal("30")

    async def test_rejection_is_recorded_on_the_request(self, async_client, platform_admin, reference_data, session):
        order = await _order(session, 2)
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "reason_details": "Wrong size", "quantity_requested": 1,
        })
        response = await async_client.post(
            f"/api/v1/returns/{request.id}/reject?reason=Past%20the%20window", headers=platform_admin,
        )
        assert response.status_code == 200
        detail = (await async_client.get(f"/api/v1/returns/{request.id}", headers=platform_admin)).json()
        assert detail["status"] == "rejected"
        assert "Past the window" in detail["reason_details"]


class TestMissingRecordsAndListings:
    async def test_unknown_shipment_tracking_is_not_found(self, async_client, reference_data, session):
        response = await async_client.get("/api/v1/shipments/999999/tracking", headers=await _headers_for(session, 2))
        assert response.status_code == 404

    async def test_out_of_stock_report_lists_empty_stock_for_administrators(self, async_client, platform_admin, reference_data, session):
        product = await _product(session)
        await InventoryService.update_stock(session, product.id, 1, "restock")
        await InventoryService.update_stock(session, product.id, -1, "sale")
        response = await async_client.get("/api/v1/inventory/out-of-stock", headers=platform_admin)
        assert response.status_code == 200
        assert [row["product_id"] for row in response.json()] == [product.id]

    async def test_customers_list_their_own_wishlists(self, async_client, org_member, reference_data, session):
        headers = await _headers_for(session, 2)
        await async_client.post("/api/v1/wishlists", json={"name": "Mine"}, headers=headers)
        mine = await async_client.get("/api/v1/wishlists", headers=headers)
        theirs = await async_client.get("/api/v1/wishlists", headers=org_member)
        assert [row["name"] for row in mine.json()] == ["Mine"]
        assert theirs.json() == []

    async def test_unknown_wishlist_routes_are_not_found(self, async_client, reference_data, session):
        headers = await _headers_for(session, 2)
        product = await _product(session)
        assert (await async_client.get("/api/v1/wishlists/share/no-such-token")).status_code == 404
        assert (await async_client.get("/api/v1/wishlists/999999", headers=headers)).status_code == 404
        assert (await async_client.get("/api/v1/wishlists/999999/items", headers=headers)).status_code == 404
        assert (await async_client.post(f"/api/v1/wishlists/999999/items/{product.id}", headers=headers)).status_code == 404
        assert (await async_client.delete("/api/v1/wishlist-items/999999", headers=headers)).status_code == 404

    async def test_owner_lists_items_of_their_wishlist(self, async_client, reference_data, session):
        product = await _product(session)
        headers = await _headers_for(session, 2)
        wishlist = (await async_client.post("/api/v1/wishlists", json={"name": "Gifts"}, headers=headers)).json()
        await async_client.post(f"/api/v1/wishlists/{wishlist['id']}/items/{product.id}?priority=3", headers=headers)
        items = await async_client.get(f"/api/v1/wishlists/{wishlist['id']}/items", headers=headers)
        assert items.status_code == 200
        assert [row["product_id"] for row in items.json()] == [product.id]

    async def test_unknown_return_and_order_routes_are_not_found(self, async_client, platform_admin, reference_data, session):
        headers = await _headers_for(session, 2)
        body = {"reason": ReturnReason.OTHER.value, "quantity_requested": 1}
        assert (await async_client.post("/api/v1/orders/999999/return", json=body, headers=headers)).status_code == 404
        assert (await async_client.get("/api/v1/returns/999999", headers=platform_admin)).status_code == 404
        assert (await async_client.get("/api/v1/orders/999999/returns", headers=platform_admin)).status_code == 404
        assert (await async_client.post("/api/v1/returns/999999/approve", headers=platform_admin)).status_code == 404
        assert (await async_client.post("/api/v1/returns/999999/reject", headers=platform_admin)).status_code == 404
        assert (await async_client.post("/api/v1/returns/999999/receive?quantity_received=0", headers=platform_admin)).status_code == 404
        assert (await async_client.post("/api/v1/returns/999999/refund", headers=platform_admin)).status_code == 404

    async def test_customer_lists_returns_for_their_order(self, async_client, reference_data, session):
        order = await _order(session, 2)
        await ReturnService.create_return_request(session, order.id, {"reason": ReturnReason.OTHER, "quantity_requested": 1})
        response = await async_client.get(f"/api/v1/orders/{order.id}/returns", headers=await _headers_for(session, 2))
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestOrderShipments:
    async def test_owner_and_administrators_list_an_orders_shipments(
        self, async_client, platform_admin, reference_data, session,
    ):
        order = await _order(session, 2)
        await ShippingService.create_shipment(session, order.id, {
            "carrier": ShippingCarrier.DHL, "tracking_number": "DHL-LIST-1", "base_rate": Decimal("3"), "total_cost": Decimal("4"),
        })
        owner = await async_client.get(f"/api/v1/orders/{order.id}/shipments", headers=await _headers_for(session, 2))
        admin = await async_client.get(f"/api/v1/orders/{order.id}/shipments", headers=platform_admin)
        assert owner.status_code == 200
        assert [row["tracking_number"] for row in owner.json()] == ["DHL-LIST-1"]
        assert admin.status_code == 200

    async def test_other_customers_cannot_see_an_orders_shipments(self, async_client, reference_data, session):
        order = await _order(session, 2)
        stranger = await async_client.get(f"/api/v1/orders/{order.id}/shipments", headers=await _stranger_headers(session))
        missing = await async_client.get("/api/v1/orders/999999/shipments", headers=await _headers_for(session, 2))
        assert stranger.status_code == 404
        assert missing.status_code == 404
