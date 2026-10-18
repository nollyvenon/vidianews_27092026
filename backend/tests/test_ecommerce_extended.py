"""Service tests for shipping, inventory, wishlists and returns (async)."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from sqlalchemy import select

from app.models.ecommerce import Order, OrderItem, PaymentMethod, Product, ProductCategory, ProductStatus
from app.models.ecommerce_extended import InventoryStatus, Return, ReturnReason, ReturnStatus, ShippingCarrier
from app.models.user import User
from app.services.ecommerce_extended_service import (
    InventoryService,
    ReturnService,
    ShippingService,
    WishlistService,
    order_owner_id,
    return_order_owner_id,
    shipment_order_owner_id,
)
from app.utils.exceptions import NotFoundError, ValidationError

ADDRESS = {
    "first_name": "Ada", "last_name": "Lovelace", "street_address": "1 Main St", "city": "London",
    "postal_code": "W1", "country": "UK",
}
SHIPMENT = {"carrier": ShippingCarrier.UPS, "tracking_number": "1Z999", "base_rate": Decimal("5.00"), "total_cost": Decimal("6.00")}


@pytest.fixture
async def owner(session) -> User:
    user = User(email="owner@example.com", password_hash="hash")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def product(session) -> Product:
    item = Product(
        sku="EXT-001", name="Extended Product", price=Decimal("20.00"), category=ProductCategory.ELECTRONICS,
        status=ProductStatus.PUBLISHED, stock_quantity=0,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@pytest.fixture
async def order(session, owner) -> Order:
    placed = Order(
        order_number="ORD-EXT-1", user_id=owner.id, billing_address={"city": "London"},
        shipping_address={"city": "London"}, email="owner@example.com", subtotal=Decimal("20.00"),
        total=Decimal("20.00"), payment_method=PaymentMethod.STRIPE,
    )
    session.add(placed)
    await session.commit()
    await session.refresh(placed)
    return placed


@pytest.fixture
async def order_item(session, order, product) -> OrderItem:
    item = OrderItem(
        order_id=order.id, product_id=product.id, product_name=product.name, product_sku=product.sku,
        quantity=2, unit_price=Decimal("20.00"), line_total=Decimal("40.00"),
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@pytest.fixture
async def shipment(session, order):
    return await ShippingService.create_shipment(session, order.id, dict(SHIPMENT))


class TestShipping:
    async def test_addresses_are_listed_per_user(self, session, owner):
        await ShippingService.create_shipping_address(session, owner.id, dict(ADDRESS))
        addresses = await ShippingService.get_user_shipping_addresses(session, owner.id)
        assert len(addresses) == 1 and addresses[0].city == "London"
        assert await ShippingService.get_user_shipping_addresses(session, owner.id + 999) == []

    async def test_shipment_needs_an_existing_order(self, session):
        with pytest.raises(NotFoundError):
            await ShippingService.create_shipment(session, 999999, dict(SHIPMENT))

    async def test_shipment_is_created_for_the_order(self, session, shipment, order):
        assert shipment.order_id == order.id
        assert shipment.carrier == ShippingCarrier.UPS

    async def test_tracking_event_defaults_its_timestamp(self, session, shipment):
        event = await ShippingService.add_tracking_event(session, shipment.id, {"status": "picked_up"})
        assert event.timestamp is not None
        assert event.timestamp.tzinfo is not None

    async def test_tracking_event_for_an_unknown_shipment_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await ShippingService.add_tracking_event(session, 999999, {"status": "lost"})

    async def test_tracking_history_is_newest_first(self, session, shipment):
        now = datetime.now(timezone.utc)
        await ShippingService.add_tracking_event(session, shipment.id, {"status": "first", "timestamp": now - timedelta(hours=2)})
        await ShippingService.add_tracking_event(session, shipment.id, {"status": "second", "timestamp": now})
        history = await ShippingService.get_shipment_tracking(session, shipment.id)
        assert [event.status for event in history] == ["second", "first"]

    async def test_tracking_for_an_unknown_shipment_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await ShippingService.get_shipment_tracking(session, 999999)

    async def test_delivered_and_shipped_status_set_their_dates(self, session, shipment):
        await ShippingService.update_shipment_status(session, shipment.id, "shipped")
        await session.refresh(shipment)
        assert shipment.shipped_at is not None and shipment.delivered_at is None
        await ShippingService.update_shipment_status(session, shipment.id, "delivered")
        await session.refresh(shipment)
        assert shipment.delivered_at is not None

    async def test_status_update_for_an_unknown_shipment_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await ShippingService.update_shipment_status(session, 999999, "shipped")

    async def test_order_owner_lookups(self, session, owner, order, shipment):
        assert await order_owner_id(session, order.id) == owner.id
        assert await order_owner_id(session, 999999) is None
        assert await shipment_order_owner_id(session, shipment.id) == owner.id
        assert await shipment_order_owner_id(session, 999999) is None


class TestInventory:
    async def test_inventory_is_created_empty_on_first_read(self, session, product):
        inventory = await InventoryService.get_or_create_inventory_level(session, product.id)
        assert inventory.quantity_on_hand == 0
        assert (await InventoryService.get_or_create_inventory_level(session, product.id)).id == inventory.id

    async def test_stock_adjustments_move_the_status(self, session, product):
        await InventoryService.update_stock(session, product.id, 50, "restock")
        inventory = await InventoryService.get_or_create_inventory_level(session, product.id)
        assert inventory.status == InventoryStatus.IN_STOCK
        assert inventory.quantity_available == 50

        await InventoryService.update_stock(session, product.id, -45, "sale")
        await session.refresh(inventory)
        assert inventory.status == InventoryStatus.LOW_STOCK

        await InventoryService.update_stock(session, product.id, -5, "sale")
        await session.refresh(inventory)
        assert inventory.status == InventoryStatus.OUT_OF_STOCK

    async def test_stock_cannot_go_negative(self, session, product):
        with pytest.raises(ValidationError):
            await InventoryService.update_stock(session, product.id, -1, "sale")

    async def test_stock_update_for_an_unknown_product_is_not_found(self, session):
        with pytest.raises(NotFoundError):
            await InventoryService.update_stock(session, 999999, 1, "restock")

    async def test_reservations_are_limited_to_available_stock(self, session, product):
        await InventoryService.update_stock(session, product.id, 10, "restock")
        await InventoryService.reserve_stock(session, product.id, 4)
        inventory = await InventoryService.get_or_create_inventory_level(session, product.id)
        assert inventory.quantity_reserved == 4 and inventory.quantity_available == 6

        with pytest.raises(ValidationError):
            await InventoryService.reserve_stock(session, product.id, 7)
        with pytest.raises(ValidationError):
            await InventoryService.reserve_stock(session, product.id, 0)

    async def test_release_never_goes_below_zero(self, session, product):
        await InventoryService.update_stock(session, product.id, 10, "restock")
        await InventoryService.release_stock(session, product.id, 3)
        inventory = await InventoryService.get_or_create_inventory_level(session, product.id)
        assert inventory.quantity_reserved == 0
        with pytest.raises(ValidationError):
            await InventoryService.release_stock(session, product.id, -1)

    async def test_low_and_out_of_stock_lists(self, session, product):
        await InventoryService.update_stock(session, product.id, 5, "restock")
        assert [i.product_id for i in await InventoryService.get_low_stock_products(session)] == [product.id]
        assert await InventoryService.get_out_of_stock_products(session) == []

    async def test_stock_alert_needs_a_product(self, session, product):
        alert = await InventoryService.create_stock_alert(
            session, product.id, {"alert_type": "low_stock", "threshold": 5},
        )
        assert alert.product_id == product.id
        with pytest.raises(NotFoundError):
            await InventoryService.create_stock_alert(session, 999999, {"alert_type": "low_stock", "threshold": 5})


class TestWishlists:
    async def test_wishlist_gets_a_share_token(self, session, owner):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Gifts", "is_public": True})
        assert wishlist.share_token
        found = await WishlistService.get_wishlist_by_share_token(session, wishlist.share_token)
        assert found.id == wishlist.id

    async def test_private_wishlists_are_not_shared(self, session, owner):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Private", "is_public": False})
        assert await WishlistService.get_wishlist_by_share_token(session, wishlist.share_token) is None

    async def test_product_is_added_once(self, session, owner, product):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Gifts"})
        await WishlistService.add_to_wishlist(session, wishlist.id, product.id, 2)
        with pytest.raises(ValidationError):
            await WishlistService.add_to_wishlist(session, wishlist.id, product.id)
        assert await WishlistService.check_item_in_wishlist(session, owner.id, product.id) is True
        assert await WishlistService.check_item_in_wishlist(session, owner.id + 999, product.id) is False

    async def test_unknown_product_cannot_be_added(self, session, owner):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Gifts"})
        with pytest.raises(NotFoundError):
            await WishlistService.add_to_wishlist(session, wishlist.id, 999999)

    async def test_items_are_ordered_by_priority(self, session, owner, product):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Gifts"})
        other = Product(sku="EXT-002", name="Other", price=Decimal("1.00"), category=ProductCategory.ELECTRONICS, status=ProductStatus.PUBLISHED)
        session.add(other)
        await session.commit()
        await WishlistService.add_to_wishlist(session, wishlist.id, product.id, 1)
        await WishlistService.add_to_wishlist(session, wishlist.id, other.id, 5)
        items = await WishlistService.get_wishlist_items(session, wishlist.id)
        assert [item.product_id for item in items] == [other.id, product.id]

    async def test_item_carries_its_wishlist_and_can_be_removed(self, session, owner, product):
        wishlist = await WishlistService.create_wishlist(session, owner.id, {"name": "Gifts"})
        item = await WishlistService.add_to_wishlist(session, wishlist.id, product.id)
        loaded = await WishlistService.get_wishlist_item(session, item.id)
        assert loaded.wishlist.user_id == owner.id
        await WishlistService.remove_from_wishlist(session, item.id)
        assert await WishlistService.get_wishlist_item(session, item.id) is None
        with pytest.raises(NotFoundError):
            await WishlistService.remove_from_wishlist(session, item.id)


class TestReturns:
    async def test_return_is_created_with_an_rma_number(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DAMAGED, "quantity_requested": 1,
        })
        assert request.rma_number.startswith("RMA-")
        assert request.status == ReturnStatus.INITIATED

    async def test_return_needs_an_existing_order(self, session):
        with pytest.raises(NotFoundError):
            await ReturnService.create_return_request(session, 999999, {
                "reason": ReturnReason.DAMAGED, "quantity_requested": 1,
            })

    async def test_order_item_must_belong_to_the_order(self, session, order, order_item):
        other_order = Order(
            order_number="ORD-EXT-2", user_id=order.user_id, billing_address={}, shipping_address={},
            email="owner@example.com", subtotal=Decimal("1"), total=Decimal("1"), payment_method=PaymentMethod.STRIPE,
        )
        session.add(other_order)
        await session.commit()
        with pytest.raises(ValidationError):
            await ReturnService.create_return_request(session, other_order.id, {
                "reason": ReturnReason.WRONG_ITEM, "quantity_requested": 1, "order_item_id": order_item.id,
            })
        accepted = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.WRONG_ITEM, "quantity_requested": 1, "order_item_id": order_item.id,
        })
        assert accepted.order_item_id == order_item.id

    async def test_full_return_lifecycle(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": 2,
        })
        await ReturnService.approve_return(session, request.id, Decimal("15.00"))
        await ReturnService.create_return_shipment(session, request.id, {"carrier": ShippingCarrier.USPS, "tracking_number": "RS-1"})
        await ReturnService.receive_return(session, request.id, 2)
        await ReturnService.process_refund(session, request.id)
        refreshed = await ReturnService.get_return_request(session, request.id)
        assert refreshed.status == ReturnStatus.REFUNDED
        assert refreshed.refund_amount == Decimal("15.00")
        assert refreshed.approved_at and refreshed.received_at and refreshed.refunded_at

    async def test_moves_out_of_order_are_refused(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": 1,
        })
        with pytest.raises(ValidationError):
            await ReturnService.receive_return(session, request.id, 1)
        with pytest.raises(ValidationError):
            await ReturnService.process_refund(session, request.id)
        await ReturnService.approve_return(session, request.id)
        with pytest.raises(ValidationError):
            await ReturnService.approve_return(session, request.id)

    async def test_received_quantity_cannot_exceed_the_request(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": 1,
        })
        await ReturnService.approve_return(session, request.id)
        with pytest.raises(ValidationError):
            await ReturnService.receive_return(session, request.id, 2)

    async def test_rejection_keeps_the_reason_with_the_request(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "reason_details": "Changed my mind", "quantity_requested": 1,
        })
        await ReturnService.reject_return(session, request.id, "Outside the return window")
        refreshed = await ReturnService.get_return_request(session, request.id)
        assert refreshed.status == ReturnStatus.REJECTED
        assert "Changed my mind" in refreshed.reason_details
        assert "Outside the return window" in refreshed.reason_details

    async def test_rejected_return_cannot_be_received(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "quantity_requested": 1,
        })
        await ReturnService.reject_return(session, request.id)
        with pytest.raises(ValidationError):
            await ReturnService.receive_return(session, request.id, 1)

    async def test_unknown_return_is_not_found(self, session):
        for action in (
            lambda: ReturnService.approve_return(session, 999999),
            lambda: ReturnService.reject_return(session, 999999),
            lambda: ReturnService.receive_return(session, 999999, 1),
            lambda: ReturnService.process_refund(session, 999999),
            lambda: ReturnService.create_return_shipment(session, 999999, {"carrier": ShippingCarrier.DHL}),
        ):
            with pytest.raises(NotFoundError):
                await action()

    async def test_pending_and_order_returns(self, session, order):
        open_request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "quantity_requested": 1,
        })
        closed = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "quantity_requested": 1,
        })
        await ReturnService.reject_return(session, closed.id)
        pending = await ReturnService.get_pending_returns(session)
        assert [r.id for r in pending] == [open_request.id]
        assert {r.id for r in await ReturnService.get_order_returns(session, order.id)} == {open_request.id, closed.id}

    async def test_return_owner_lookup(self, session, owner, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "quantity_requested": 1,
        })
        assert await return_order_owner_id(session, request.id) == owner.id
        assert await return_order_owner_id(session, 999999) is None
        assert isinstance(await ReturnService.get_return_request(session, request.id), Return)


class TestReturnRefunds:
    async def _received_return(self, session, order, order_item, quantity: int = 1, approved_amount=None):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.DEFECTIVE, "quantity_requested": quantity, "order_item_id": order_item.id,
        })
        await ReturnService.approve_return(session, request.id, approved_amount)
        await ReturnService.receive_return(session, request.id, quantity)
        return request

    async def test_stripe_paid_return_is_refunded_through_stripe(self, session, order, order_item, monkeypatch):
        import stripe
        from types import SimpleNamespace

        from app.models.ecommerce import CheckoutSession, PaymentDetail, PaymentMethod, PaymentStatus, Refund
        from app.services.ecommerce_service import CartService

        order.payment_id = "pi_refund_1"
        cart = await CartService(session).get_or_create_cart(order.user_id)
        checkout = CheckoutSession(
            checkout_token="refund-checkout", user_id=order.user_id, cart_id=cart.id, billing_address={},
            shipping_address={}, email="owner@example.com", subtotal=Decimal("20.00"), total=Decimal("20.00"),
        )
        session.add(checkout)
        await session.commit()
        session.add(PaymentDetail(
            checkout_id=checkout.id, payment_method=PaymentMethod.STRIPE, amount=Decimal("20.00"), currency="USD",
            status=PaymentStatus.COMPLETED, transaction_id="pi_refund_1", stripe_payment_intent_id="pi_refund_1",
        ))
        await session.commit()
        calls = []

        def fake_refund(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(id="re_test_1")

        monkeypatch.setattr(stripe.Refund, "create", fake_refund)

        request = await self._received_return(session, order, order_item)
        await ReturnService.process_refund(session, request.id)

        refreshed = await ReturnService.get_return_request(session, request.id)
        assert refreshed.status == ReturnStatus.REFUNDED
        assert refreshed.refund_method == "stripe"
        assert refreshed.refund_amount == Decimal("20.00")
        assert calls == [{"payment_intent": "pi_refund_1", "amount": 2000}]
        assert (await session.execute(select(Refund))).scalars().one().refund_transaction_id == "re_test_1"

    async def test_orders_paid_another_way_are_refunded_manually(self, session, order, order_item):
        request = await self._received_return(session, order, order_item)
        await ReturnService.process_refund(session, request.id)
        refreshed = await ReturnService.get_return_request(session, request.id)
        assert refreshed.refund_method == "manual"
        assert refreshed.refund_amount == Decimal("20.00")

    async def test_refund_cannot_exceed_the_order_total(self, session, order, order_item):
        request = await self._received_return(session, order, order_item, approved_amount=Decimal("999.00"))
        with pytest.raises(ValidationError):
            await ReturnService.process_refund(session, request.id)
        refreshed = await ReturnService.get_return_request(session, request.id)
        assert refreshed.status == ReturnStatus.RECEIVED

    async def test_return_without_an_amount_or_item_is_refused(self, session, order):
        request = await ReturnService.create_return_request(session, order.id, {
            "reason": ReturnReason.OTHER, "quantity_requested": 1,
        })
        await ReturnService.approve_return(session, request.id)
        await ReturnService.receive_return(session, request.id, 1)
        with pytest.raises(ValidationError):
            await ReturnService.process_refund(session, request.id)
