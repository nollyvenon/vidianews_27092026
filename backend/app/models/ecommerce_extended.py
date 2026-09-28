"""Extended ecommerce models for shipping, inventory, wishlists, and returns"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text,
    Enum as SQLEnum, Float, Index, Table, UniqueConstraint, Numeric, DECIMAL
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


# ============================================================================
# ENUMS
# ============================================================================

class ShippingCarrier(str, enum.Enum):
    """Shipping carriers"""
    FEDEX = "fedex"
    UPS = "ups"
    USPS = "usps"
    DHL = "dhl"
    LOCAL = "local"


class InventoryStatus(str, enum.Enum):
    """Inventory status"""
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class ReturnStatus(str, enum.Enum):
    """Return status"""
    INITIATED = "initiated"
    APPROVED = "approved"
    SHIPPED = "shipped"
    RECEIVED = "received"
    PROCESSING = "processing"
    REFUNDED = "refunded"
    REJECTED = "rejected"


class ReturnReason(str, enum.Enum):
    """Return reasons"""
    DAMAGED = "damaged"
    DEFECTIVE = "defective"
    NOT_AS_DESCRIBED = "not_as_described"
    WRONG_ITEM = "wrong_item"
    NO_LONGER_NEEDED = "no_longer_needed"
    SIZE_ISSUE = "size_issue"
    COLOR_ISSUE = "color_issue"
    OTHER = "other"


# ============================================================================
# MODULE 106: SHIPPING & FULFILLMENT
# ============================================================================

class ShippingAddress(Base):
    """Shipping addresses"""
    __tablename__ = "shipping_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Address details
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    phone = Column(String(20))

    # Metadata
    is_default = Column(Boolean, default=False)
    nickname = Column(String(100))

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_shipping_address_user", "user_id"),
        Index("idx_shipping_address_default", "is_default"),
    )


class Shipment(Base):
    """Shipment records"""
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)

    # Shipping details
    carrier = Column(SQLEnum(ShippingCarrier), nullable=False)
    tracking_number = Column(String(100), unique=True, index=True)
    shipping_label_url = Column(String(500))

    # Weight and dimensions
    weight_lbs = Column(Float)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)

    # Rates
    base_rate = Column(DECIMAL(10, 2))
    insurance_cost = Column(DECIMAL(10, 2), default=0)
    handling_fee = Column(DECIMAL(10, 2), default=0)
    total_cost = Column(DECIMAL(10, 2))

    # Status tracking
    status = Column(String(50), index=True)
    estimated_delivery_date = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))

    # Relationships
    tracking_events = relationship("TrackingEvent", back_populates="shipment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_shipment_order", "order_id"),
        Index("idx_shipment_tracking", "tracking_number"),
        Index("idx_shipment_carrier", "carrier"),
    )


class TrackingEvent(Base):
    """Shipment tracking events"""
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, index=True)

    # Event details
    status = Column(String(100), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    timestamp = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    shipment = relationship("Shipment", back_populates="tracking_events")

    __table_args__ = (
        Index("idx_tracking_event_shipment", "shipment_id"),
    )


# ============================================================================
# MODULE 107: INVENTORY MANAGEMENT
# ============================================================================

class InventoryLevel(Base):
    """Product inventory levels"""
    __tablename__ = "inventory_levels"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Stock quantities
    quantity_on_hand = Column(Integer, default=0, index=True)
    quantity_reserved = Column(Integer, default=0)
    quantity_available = Column(Integer, default=0)

    # Reorder info
    reorder_level = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=50)

    # Status
    status = Column(SQLEnum(InventoryStatus), default=InventoryStatus.IN_STOCK, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_counted_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_inventory_product", "product_id"),
        Index("idx_inventory_status", "status"),
    )


class InventoryTransaction(Base):
    """Inventory transaction log"""
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    # Transaction details
    transaction_type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String(255))

    # Reference
    reference_type = Column(String(50))
    reference_id = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_inventory_transaction_product", "product_id"),
        Index("idx_inventory_transaction_created", "created_at"),
    )


class StockAlert(Base):
    """Low stock alerts"""
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # Alert details
    alert_type = Column(String(50), nullable=False)
    threshold = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    # Notification
    email_notify = Column(Boolean, default=True)
    notify_users = relationship("User", secondary="stock_alert_subscribers")

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_stock_alert_product", "product_id"),
    )


# ============================================================================
# MODULE 109: WISHLISTS
# ============================================================================

class Wishlist(Base):
    """User wishlists"""
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=False)

    # Metadata
    share_token = Column(String(255), unique=True, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_wishlist_user", "user_id"),
        Index("idx_wishlist_share_token", "share_token"),
    )


class WishlistItem(Base):
    """Items in wishlist"""
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # Priority
    priority = Column(Integer, default=0)
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    added_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    wishlist = relationship("Wishlist", back_populates="items")

    __table_args__ = (
        Index("idx_wishlist_item_wishlist", "wishlist_id"),
        Index("idx_wishlist_item_product", "product_id"),
        UniqueConstraint("wishlist_id", "product_id", name="uq_wishlist_product"),
    )


# ============================================================================
# MODULE 110: RETURNS & REFUNDS
# ============================================================================

class Return(Base):
    """Return requests"""
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), index=True)

    # Return details
    reason = Column(SQLEnum(ReturnReason), nullable=False)
    reason_details = Column(Text)
    status = Column(SQLEnum(ReturnStatus), default=ReturnStatus.INITIATED, index=True)

    # Return authorization
    rma_number = Column(String(50), unique=True, index=True)
    return_label_url = Column(String(500))

    # Quantities
    quantity_requested = Column(Integer, nullable=False)
    quantity_received = Column(Integer)

    # Condition
    item_condition = Column(String(50))

    # Refund details
    refund_amount = Column(DECIMAL(12, 2))
    refund_method = Column(String(50))

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    approved_at = Column(DateTime(timezone=True))
    shipped_at = Column(DateTime(timezone=True))
    received_at = Column(DateTime(timezone=True))
    refunded_at = Column(DateTime(timezone=True))

    # Relationships
    tracking_numbers = Column(JSON)

    __table_args__ = (
        Index("idx_return_order", "order_id"),
        Index("idx_return_status", "status"),
        Index("idx_return_rma", "rma_number"),
    )


class ReturnShipment(Base):
    """Return shipments"""
    __tablename__ = "return_shipments"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(Integer, ForeignKey("returns.id", ondelete="CASCADE"), nullable=False, index=True)

    # Shipping details
    carrier = Column(SQLEnum(ShippingCarrier), nullable=False)
    tracking_number = Column(String(100), unique=True, index=True)

    # Status
    status = Column(String(50), index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    shipped_at = Column(DateTime(timezone=True))
    received_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_return_shipment_return", "return_id"),
    )
