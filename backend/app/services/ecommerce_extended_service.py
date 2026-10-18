"""Extended ecommerce services for shipping, inventory, wishlists, and returns (async).

Timestamps are timezone-aware, matching the ``DateTime(timezone=True)`` columns in
``app.models.ecommerce_extended``. Missing records raise NotFoundError and invalid
state changes raise ValidationError so the API answers with a client error, not a 500.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.ecommerce import Order, OrderItem, Product
from app.models.ecommerce_extended import (
    InventoryLevel,
    InventoryStatus,
    InventoryTransaction,
    Return,
    ReturnShipment,
    ReturnStatus,
    Shipment,
    ShippingAddress,
    StockAlert,
    TrackingEvent,
    Wishlist,
    WishlistItem,
)
from app.utils.exceptions import NotFoundError, ValidationError


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def order_owner_id(session: AsyncSession, order_id: int) -> Optional[int]:
    """User id that placed the order, or None when the order does not exist."""
    return (await session.execute(select(Order.user_id).where(Order.id == order_id))).scalar_one_or_none()


async def shipment_order_owner_id(session: AsyncSession, shipment_id: int) -> Optional[int]:
    """User id that placed the order a shipment belongs to, or None when the shipment does not exist."""
    return (await session.execute(
        select(Order.user_id).join(Shipment, Shipment.order_id == Order.id).where(Shipment.id == shipment_id)
    )).scalar_one_or_none()


async def return_order_owner_id(session: AsyncSession, return_id: int) -> Optional[int]:
    """User id that placed the order a return belongs to, or None when the return does not exist."""
    return (await session.execute(
        select(Order.user_id).join(Return, Return.order_id == Order.id).where(Return.id == return_id)
    )).scalar_one_or_none()


class ShippingService:
    """Shipping and fulfillment service"""

    @staticmethod
    async def create_shipping_address(db: AsyncSession, user_id: int, address_data: dict) -> ShippingAddress:
        address = ShippingAddress(user_id=user_id, **address_data)
        db.add(address)
        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def get_user_shipping_addresses(db: AsyncSession, user_id: int) -> List[ShippingAddress]:
        result = await db.execute(
            select(ShippingAddress).where(ShippingAddress.user_id == user_id).order_by(ShippingAddress.id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def create_shipment(db: AsyncSession, order_id: int, shipment_data: dict) -> Shipment:
        if await order_owner_id(db, order_id) is None:
            raise NotFoundError("Order")
        shipment = Shipment(order_id=order_id, **shipment_data)
        db.add(shipment)
        await db.commit()
        await db.refresh(shipment)
        return shipment

    @staticmethod
    async def get_shipment(db: AsyncSession, shipment_id: int) -> Optional[Shipment]:
        return await db.get(Shipment, shipment_id)

    @staticmethod
    async def add_tracking_event(db: AsyncSession, shipment_id: int, event_data: dict) -> TrackingEvent:
        if await db.get(Shipment, shipment_id) is None:
            raise NotFoundError("Shipment")
        event = TrackingEvent(shipment_id=shipment_id, **{**event_data, "timestamp": event_data.get("timestamp") or _now()})
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def get_shipment_tracking(db: AsyncSession, shipment_id: int) -> List[TrackingEvent]:
        if await db.get(Shipment, shipment_id) is None:
            raise NotFoundError("Shipment")
        result = await db.execute(
            select(TrackingEvent)
            .where(TrackingEvent.shipment_id == shipment_id)
            .order_by(TrackingEvent.timestamp.desc(), TrackingEvent.id.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def update_shipment_status(db: AsyncSession, shipment_id: int, status: str) -> None:
        shipment = await db.get(Shipment, shipment_id)
        if shipment is None:
            raise NotFoundError("Shipment")
        shipment.status = status
        if status == "shipped" and shipment.shipped_at is None:
            shipment.shipped_at = _now()
        if status == "delivered":
            shipment.delivered_at = _now()
        await db.commit()


class InventoryService:
    """Inventory management service"""

    @staticmethod
    async def get_or_create_inventory_level(db: AsyncSession, product_id: int) -> InventoryLevel:
        inventory = (await db.execute(
            select(InventoryLevel).where(InventoryLevel.product_id == product_id)
        )).scalar_one_or_none()

        if inventory is None:
            inventory = InventoryLevel(product_id=product_id)
            db.add(inventory)
            await db.commit()
            await db.refresh(inventory)

        return inventory

    @staticmethod
    def _apply_status(inventory: InventoryLevel) -> None:
        """Out of stock is checked first: a zero balance is also at or below the reorder level."""
        inventory.quantity_available = max(0, inventory.quantity_on_hand - inventory.quantity_reserved)
        if inventory.quantity_on_hand <= 0:
            inventory.status = InventoryStatus.OUT_OF_STOCK
        elif inventory.quantity_on_hand <= inventory.reorder_level:
            inventory.status = InventoryStatus.LOW_STOCK
        else:
            inventory.status = InventoryStatus.IN_STOCK

    @staticmethod
    async def update_stock(
        db: AsyncSession,
        product_id: int,
        quantity: int,
        reason: str,
        reference_type: Optional[str] = None,
        reference_id: Optional[int] = None,
    ) -> None:
        if await db.get(Product, product_id) is None:
            raise NotFoundError("Product")
        inventory = await InventoryService.get_or_create_inventory_level(db, product_id)
        if inventory.quantity_on_hand + quantity < 0:
            raise ValidationError("Stock adjustment would make on-hand quantity negative")
        inventory.quantity_on_hand += quantity
        InventoryService._apply_status(inventory)

        db.add(InventoryTransaction(
            product_id=product_id,
            transaction_type="adjustment",
            quantity=quantity,
            reason=reason,
            reference_type=reference_type,
            reference_id=reference_id,
        ))
        await db.commit()

    @staticmethod
    async def reserve_stock(db: AsyncSession, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("Reserved quantity must be positive")
        inventory = await InventoryService.get_or_create_inventory_level(db, product_id)
        if quantity > inventory.quantity_available:
            raise ValidationError("Insufficient stock to reserve")
        inventory.quantity_reserved += quantity
        InventoryService._apply_status(inventory)
        await db.commit()

    @staticmethod
    async def release_stock(db: AsyncSession, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("Released quantity must be positive")
        inventory = await InventoryService.get_or_create_inventory_level(db, product_id)
        inventory.quantity_reserved = max(0, inventory.quantity_reserved - quantity)
        InventoryService._apply_status(inventory)
        await db.commit()

    @staticmethod
    async def get_low_stock_products(db: AsyncSession) -> List[InventoryLevel]:
        result = await db.execute(
            select(InventoryLevel).where(InventoryLevel.status == InventoryStatus.LOW_STOCK).order_by(InventoryLevel.id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_out_of_stock_products(db: AsyncSession) -> List[InventoryLevel]:
        result = await db.execute(
            select(InventoryLevel).where(InventoryLevel.status == InventoryStatus.OUT_OF_STOCK).order_by(InventoryLevel.id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def create_stock_alert(db: AsyncSession, product_id: int, alert_data: dict) -> StockAlert:
        if await db.get(Product, product_id) is None:
            raise NotFoundError("Product")
        alert = StockAlert(product_id=product_id, **alert_data)
        db.add(alert)
        await db.commit()
        await db.refresh(alert)
        return alert


class WishlistService:
    """Wishlist service"""

    @staticmethod
    async def create_wishlist(db: AsyncSession, user_id: int, wishlist_data: dict) -> Wishlist:
        wishlist = Wishlist(user_id=user_id, share_token=str(uuid.uuid4()), **wishlist_data)
        db.add(wishlist)
        await db.commit()
        await db.refresh(wishlist)
        return wishlist

    @staticmethod
    async def get_user_wishlists(db: AsyncSession, user_id: int) -> List[Wishlist]:
        result = await db.execute(select(Wishlist).where(Wishlist.user_id == user_id).order_by(Wishlist.id))
        return list(result.scalars().all())

    @staticmethod
    async def get_wishlist(db: AsyncSession, wishlist_id: int) -> Optional[Wishlist]:
        return await db.get(Wishlist, wishlist_id)

    @staticmethod
    async def get_wishlist_by_share_token(db: AsyncSession, share_token: str) -> Optional[Wishlist]:
        return (await db.execute(
            select(Wishlist).where(Wishlist.share_token == share_token, Wishlist.is_public == True)  # noqa: E712 - SQL comparison
        )).scalar_one_or_none()

    @staticmethod
    async def add_to_wishlist(db: AsyncSession, wishlist_id: int, product_id: int, priority: int = 0) -> WishlistItem:
        if await db.get(Product, product_id) is None:
            raise NotFoundError("Product")
        existing = (await db.execute(
            select(WishlistItem).where(and_(WishlistItem.wishlist_id == wishlist_id, WishlistItem.product_id == product_id))
        )).scalar_one_or_none()
        if existing is not None:
            raise ValidationError("Product is already in this wishlist")
        item = WishlistItem(wishlist_id=wishlist_id, product_id=product_id, priority=priority)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def get_wishlist_item(db: AsyncSession, wishlist_item_id: int) -> Optional[WishlistItem]:
        """The item with its wishlist loaded, so the caller can check who owns it."""
        return (await db.execute(
            select(WishlistItem).options(selectinload(WishlistItem.wishlist))
            .where(WishlistItem.id == wishlist_item_id)
        )).scalar_one_or_none()

    @staticmethod
    async def remove_from_wishlist(db: AsyncSession, wishlist_item_id: int) -> None:
        item = await db.get(WishlistItem, wishlist_item_id)
        if item is None:
            raise NotFoundError("Wishlist item")
        await db.delete(item)
        await db.commit()

    @staticmethod
    async def get_wishlist_items(db: AsyncSession, wishlist_id: int) -> List[WishlistItem]:
        result = await db.execute(
            select(WishlistItem)
            .where(WishlistItem.wishlist_id == wishlist_id)
            .order_by(WishlistItem.priority.desc(), WishlistItem.id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def check_item_in_wishlist(db: AsyncSession, user_id: int, product_id: int) -> bool:
        count = (await db.execute(
            select(func.count(WishlistItem.id)).join(Wishlist, WishlistItem.wishlist_id == Wishlist.id).where(and_(
                Wishlist.user_id == user_id,
                WishlistItem.product_id == product_id,
            ))
        )).scalar_one()
        return count > 0


class ReturnService:
    """Return and refund service.

    Status moves forward only: initiated -> approved -> shipped -> received -> refunded,
    with rejection allowed before the return has been received.
    """

    @staticmethod
    async def create_return_request(db: AsyncSession, order_id: int, return_data: dict) -> Return:
        if await order_owner_id(db, order_id) is None:
            raise NotFoundError("Order")
        order_item_id = return_data.get("order_item_id")
        if order_item_id is not None:
            item = await db.get(OrderItem, order_item_id)
            if item is None or item.order_id != order_id:
                raise ValidationError("Order item does not belong to this order")
        return_request = Return(
            order_id=order_id,
            rma_number=f"RMA-{uuid.uuid4().hex[:8].upper()}",
            **return_data,
        )
        db.add(return_request)
        await db.commit()
        await db.refresh(return_request)
        return return_request

    @staticmethod
    async def get_return_request(db: AsyncSession, return_id: int) -> Optional[Return]:
        return await db.get(Return, return_id)

    @staticmethod
    async def _return(db: AsyncSession, return_id: int) -> Return:
        return_request = await db.get(Return, return_id)
        if return_request is None:
            raise NotFoundError("Return request")
        return return_request

    @staticmethod
    def _move(return_request: Return, allowed_from: tuple, to: ReturnStatus) -> None:
        if return_request.status not in allowed_from:
            raise ValidationError(
                f"Return cannot move from {return_request.status.value} to {to.value}"
            )
        return_request.status = to

    @staticmethod
    async def get_order_returns(db: AsyncSession, order_id: int) -> List[Return]:
        result = await db.execute(select(Return).where(Return.order_id == order_id).order_by(Return.id))
        return list(result.scalars().all())

    @staticmethod
    async def approve_return(db: AsyncSession, return_id: int, refund_amount: Optional[Decimal] = None) -> None:
        return_request = await ReturnService._return(db, return_id)
        ReturnService._move(return_request, (ReturnStatus.INITIATED,), ReturnStatus.APPROVED)
        return_request.approved_at = _now()
        if refund_amount is not None:
            return_request.refund_amount = refund_amount
        await db.commit()

    @staticmethod
    async def create_return_shipment(db: AsyncSession, return_id: int, shipment_data: dict) -> ReturnShipment:
        if await db.get(Return, return_id) is None:
            raise NotFoundError("Return request")
        shipment = ReturnShipment(return_id=return_id, **shipment_data)
        db.add(shipment)
        await db.commit()
        await db.refresh(shipment)
        return shipment

    @staticmethod
    async def receive_return(db: AsyncSession, return_id: int, quantity_received: int) -> None:
        return_request = await ReturnService._return(db, return_id)
        if quantity_received > return_request.quantity_requested:
            raise ValidationError("Received quantity exceeds the quantity requested")
        ReturnService._move(return_request, (ReturnStatus.APPROVED, ReturnStatus.SHIPPED), ReturnStatus.RECEIVED)
        return_request.quantity_received = quantity_received
        return_request.received_at = _now()
        await db.commit()

    @staticmethod
    async def process_refund(db: AsyncSession, return_id: int) -> None:
        return_request = await ReturnService._return(db, return_id)
        ReturnService._move(return_request, (ReturnStatus.RECEIVED,), ReturnStatus.REFUNDED)
        return_request.refunded_at = _now()
        await db.commit()

    @staticmethod
    async def reject_return(db: AsyncSession, return_id: int, reason: Optional[str] = None) -> None:
        return_request = await ReturnService._return(db, return_id)
        ReturnService._move(
            return_request, (ReturnStatus.INITIATED, ReturnStatus.APPROVED), ReturnStatus.REJECTED,
        )
        if reason:
            # The schema has no rejection column; the reason is kept with the request so the customer and staff can see it.
            note = f"Rejection reason: {reason}"
            return_request.reason_details = f"{return_request.reason_details}\n\n{note}" if return_request.reason_details else note
        await db.commit()

    @staticmethod
    async def get_pending_returns(db: AsyncSession) -> List[Return]:
        result = await db.execute(
            select(Return).where(Return.status.in_([
                ReturnStatus.INITIATED,
                ReturnStatus.APPROVED,
                ReturnStatus.SHIPPED,
                ReturnStatus.RECEIVED,
            ])).order_by(Return.id)
        )
        return list(result.scalars().all())
