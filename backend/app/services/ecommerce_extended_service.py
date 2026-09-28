"""Extended ecommerce services for shipping, inventory, wishlists, and returns"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.ecommerce_extended import (
    ShippingAddress, Shipment, TrackingEvent, InventoryLevel, InventoryTransaction,
    StockAlert, Wishlist, WishlistItem, Return, ReturnShipment,
    ShippingCarrier, InventoryStatus, ReturnStatus, ReturnReason
)
from app.models.ecommerce import Order, OrderItem
from datetime import datetime, timezone, timedelta
import uuid


class ShippingService:
    """Shipping and fulfillment service"""

    @staticmethod
    def create_shipping_address(db: Session, user_id: int, address_data: dict) -> ShippingAddress:
        address = ShippingAddress(user_id=user_id, **address_data)
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def get_user_shipping_addresses(db: Session, user_id: int):
        return db.query(ShippingAddress).filter(ShippingAddress.user_id == user_id).all()

    @staticmethod
    def create_shipment(db: Session, order_id: int, shipment_data: dict) -> Shipment:
        shipment = Shipment(order_id=order_id, **shipment_data)
        db.add(shipment)
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def add_tracking_event(db: Session, shipment_id: int, event_data: dict) -> TrackingEvent:
        event = TrackingEvent(shipment_id=shipment_id, **event_data)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_shipment_tracking(db: Session, shipment_id: int):
        return db.query(TrackingEvent).filter(
            TrackingEvent.shipment_id == shipment_id
        ).order_by(TrackingEvent.timestamp.desc()).all()

    @staticmethod
    def update_shipment_status(db: Session, shipment_id: int, status: str):
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        shipment.status = status
        if status == "delivered":
            shipment.delivered_at = datetime.now(timezone.utc)
        db.commit()


class InventoryService:
    """Inventory management service"""

    @staticmethod
    def get_or_create_inventory_level(db: Session, product_id: int) -> InventoryLevel:
        inventory = db.query(InventoryLevel).filter(
            InventoryLevel.product_id == product_id
        ).first()

        if not inventory:
            inventory = InventoryLevel(product_id=product_id)
            db.add(inventory)
            db.commit()
            db.refresh(inventory)

        return inventory

    @staticmethod
    def update_stock(db: Session, product_id: int, quantity: int, reason: str, reference_type: str = None, reference_id: int = None):
        inventory = InventoryService.get_or_create_inventory_level(db, product_id)
        inventory.quantity_on_hand += quantity

        if inventory.quantity_on_hand <= inventory.reorder_level:
            inventory.status = InventoryStatus.LOW_STOCK
        elif inventory.quantity_on_hand <= 0:
            inventory.status = InventoryStatus.OUT_OF_STOCK
        else:
            inventory.status = InventoryStatus.IN_STOCK

        inventory.quantity_available = max(0, inventory.quantity_on_hand - inventory.quantity_reserved)

        transaction = InventoryTransaction(
            product_id=product_id,
            transaction_type="adjustment",
            quantity=quantity,
            reason=reason,
            reference_type=reference_type,
            reference_id=reference_id
        )
        db.add(transaction)
        db.commit()

    @staticmethod
    def reserve_stock(db: Session, product_id: int, quantity: int):
        inventory = InventoryService.get_or_create_inventory_level(db, product_id)
        inventory.quantity_reserved += quantity
        inventory.quantity_available = max(0, inventory.quantity_on_hand - inventory.quantity_reserved)
        db.commit()

    @staticmethod
    def release_stock(db: Session, product_id: int, quantity: int):
        inventory = InventoryService.get_or_create_inventory_level(db, product_id)
        inventory.quantity_reserved -= quantity
        inventory.quantity_available = max(0, inventory.quantity_on_hand - inventory.quantity_reserved)
        db.commit()

    @staticmethod
    def get_low_stock_products(db: Session):
        return db.query(InventoryLevel).filter(
            InventoryLevel.status == InventoryStatus.LOW_STOCK
        ).all()

    @staticmethod
    def get_out_of_stock_products(db: Session):
        return db.query(InventoryLevel).filter(
            InventoryLevel.status == InventoryStatus.OUT_OF_STOCK
        ).all()

    @staticmethod
    def create_stock_alert(db: Session, product_id: int, alert_data: dict) -> StockAlert:
        alert = StockAlert(product_id=product_id, **alert_data)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert


class WishlistService:
    """Wishlist service"""

    @staticmethod
    def create_wishlist(db: Session, user_id: int, wishlist_data: dict) -> Wishlist:
        wishlist = Wishlist(
            user_id=user_id,
            share_token=str(uuid.uuid4()),
            **wishlist_data
        )
        db.add(wishlist)
        db.commit()
        db.refresh(wishlist)
        return wishlist

    @staticmethod
    def get_user_wishlists(db: Session, user_id: int):
        return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()

    @staticmethod
    def get_wishlist(db: Session, wishlist_id: int) -> Wishlist:
        return db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()

    @staticmethod
    def get_wishlist_by_share_token(db: Session, share_token: str) -> Wishlist:
        return db.query(Wishlist).filter(
            Wishlist.share_token == share_token,
            Wishlist.is_public == True
        ).first()

    @staticmethod
    def add_to_wishlist(db: Session, wishlist_id: int, product_id: int, priority: int = 0) -> WishlistItem:
        item = WishlistItem(wishlist_id=wishlist_id, product_id=product_id, priority=priority)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def remove_from_wishlist(db: Session, wishlist_item_id: int):
        item = db.query(WishlistItem).filter(WishlistItem.id == wishlist_item_id).first()
        db.delete(item)
        db.commit()

    @staticmethod
    def get_wishlist_items(db: Session, wishlist_id: int):
        return db.query(WishlistItem).filter(
            WishlistItem.wishlist_id == wishlist_id
        ).order_by(WishlistItem.priority.desc()).all()

    @staticmethod
    def check_item_in_wishlist(db: Session, user_id: int, product_id: int) -> bool:
        count = db.query(WishlistItem).join(Wishlist).filter(
            and_(
                Wishlist.user_id == user_id,
                WishlistItem.product_id == product_id
            )
        ).count()
        return count > 0


class ReturnService:
    """Return and refund service"""

    @staticmethod
    def create_return_request(db: Session, order_id: int, return_data: dict) -> Return:
        rma_number = f"RMA-{uuid.uuid4().hex[:8].upper()}"

        return_request = Return(
            order_id=order_id,
            rma_number=rma_number,
            **return_data
        )
        db.add(return_request)
        db.commit()
        db.refresh(return_request)
        return return_request

    @staticmethod
    def get_return_request(db: Session, return_id: int) -> Return:
        return db.query(Return).filter(Return.id == return_id).first()

    @staticmethod
    def get_order_returns(db: Session, order_id: int):
        return db.query(Return).filter(Return.order_id == order_id).all()

    @staticmethod
    def approve_return(db: Session, return_id: int, refund_amount: float = None):
        return_request = ReturnService.get_return_request(db, return_id)
        return_request.status = ReturnStatus.APPROVED
        return_request.approved_at = datetime.now(timezone.utc)

        if refund_amount:
            return_request.refund_amount = refund_amount

        db.commit()

    @staticmethod
    def create_return_shipment(db: Session, return_id: int, shipment_data: dict) -> ReturnShipment:
        shipment = ReturnShipment(return_id=return_id, **shipment_data)
        db.add(shipment)
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def receive_return(db: Session, return_id: int, quantity_received: int):
        return_request = ReturnService.get_return_request(db, return_id)
        return_request.quantity_received = quantity_received
        return_request.status = ReturnStatus.RECEIVED
        return_request.received_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def process_refund(db: Session, return_id: int):
        return_request = ReturnService.get_return_request(db, return_id)
        return_request.status = ReturnStatus.REFUNDED
        return_request.refunded_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def reject_return(db: Session, return_id: int, reason: str = None):
        return_request = ReturnService.get_return_request(db, return_id)
        return_request.status = ReturnStatus.REJECTED
        db.commit()

    @staticmethod
    def get_pending_returns(db: Session):
        return db.query(Return).filter(
            Return.status.in_([
                ReturnStatus.INITIATED,
                ReturnStatus.APPROVED,
                ReturnStatus.SHIPPED,
                ReturnStatus.RECEIVED
            ])
        ).all()
