"""Ecommerce models for products, cart, checkout, payments, and orders"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text,
    Enum as SQLEnum, Float, Index, Table, UniqueConstraint, Numeric, DECIMAL
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum
import uuid


# ============================================================================
# ENUMS
# ============================================================================

class ProductStatus(str, enum.Enum):
    """Product status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DISCONTINUED = "discontinued"


class ProductCategory(str, enum.Enum):
    """Product categories"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    FOOD = "food"
    HOME = "home"
    SPORTS = "sports"
    OTHER = "other"


class CartItemStatus(str, enum.Enum):
    """Cart item status"""
    ACTIVE = "active"
    SAVED_FOR_LATER = "saved_for_later"
    REMOVED = "removed"


class CheckoutStatus(str, enum.Enum):
    """Checkout process status"""
    INITIATED = "initiated"
    ABANDONED = "abandoned"
    COMPLETED = "completed"
    PROCESSING = "processing"


class PaymentStatus(str, enum.Enum):
    """Payment status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    """Payment methods"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    BANK_TRANSFER = "bank_transfer"
    WALLET = "wallet"


class OrderStatus(str, enum.Enum):
    """Order status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class ShippingStatus(str, enum.Enum):
    """Shipping status"""
    NOT_SHIPPED = "not_shipped"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    LOST = "lost"
    RETURNED = "returned"


# ============================================================================
# MODULE 101: PRODUCTS & CATALOG
# ============================================================================

class Product(Base):
    """Product model for ecommerce"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    long_description = Column(Text)

    # Pricing
    price = Column(DECIMAL(12, 2), nullable=False, index=True)
    cost = Column(DECIMAL(12, 2))  # Cost to vendor
    discount_price = Column(DECIMAL(12, 2))
    discount_percentage = Column(Float)

    # Inventory
    stock_quantity = Column(Integer, default=0, index=True)
    low_stock_threshold = Column(Integer, default=10)

    # Metadata
    category = Column(SQLEnum(ProductCategory), nullable=False, index=True)
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.DRAFT, index=True)

    # Images
    main_image_url = Column(String(500))
    images = Column(JSON)  # List of image URLs

    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))

    # Marketing
    is_featured = Column(Boolean, default=False, index=True)
    is_bestseller = Column(Boolean, default=False)

    # Attributes
    attributes = Column(JSON)  # Custom attributes (size, color, etc.)
    variants = Column(JSON)  # Product variants

    # Ratings & Reviews
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_product_status", "status"),
        Index("idx_product_category", "category"),
        Index("idx_product_featured", "is_featured"),
        Index("idx_product_price", "price"),
    )


class ProductReview(Base):
    """Product reviews and ratings"""
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(255))
    review_text = Column(Text)

    # Metadata
    is_verified = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (
        Index("idx_review_product", "product_id"),
        Index("idx_review_user", "user_id"),
        Index("idx_review_rating", "rating"),
    )


# ============================================================================
# MODULE 102: SHOPPING CART
# ============================================================================

class Cart(Base):
    """Shopping cart"""
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    session_id = Column(String(255), index=True)  # For anonymous users

    # Cart state
    subtotal = Column(DECIMAL(12, 2), default=0.00)
    tax = Column(DECIMAL(12, 2), default=0.00)
    shipping = Column(DECIMAL(12, 2), default=0.00)
    discount = Column(DECIMAL(12, 2), default=0.00)
    total = Column(DECIMAL(12, 2), default=0.00)

    # Metadata
    item_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_cart_user", "user_id"),
        Index("idx_cart_session", "session_id"),
    )


class CartItem(Base):
    """Items in shopping cart"""
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # Item details
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    line_total = Column(DECIMAL(12, 2), nullable=False)

    # Status
    status = Column(SQLEnum(CartItemStatus), default=CartItemStatus.ACTIVE, index=True)

    # Selected variants/attributes
    selected_attributes = Column(JSON)  # Selected size, color, etc.

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

    __table_args__ = (
        Index("idx_cart_item_cart", "cart_id"),
        Index("idx_cart_item_product", "product_id"),
        Index("idx_cart_item_status", "status"),
    )


# ============================================================================
# MODULE 103: CHECKOUT
# ============================================================================

class CheckoutSession(Base):
    """Checkout session"""
    __tablename__ = "checkout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    checkout_token = Column(String(255), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), index=True)

    # Checkout data
    billing_address = Column(JSON, nullable=False)
    shipping_address = Column(JSON, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))

    # Shipping method
    shipping_method = Column(String(100))
    shipping_cost = Column(DECIMAL(12, 2), default=0.00)

    # Order totals
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    tax = Column(DECIMAL(12, 2), default=0.00)
    discount = Column(DECIMAL(12, 2), default=0.00)
    total = Column(DECIMAL(12, 2), nullable=False)

    # Discount/Coupon
    coupon_code = Column(String(50), index=True)

    # Status
    status = Column(SQLEnum(CheckoutStatus), default=CheckoutStatus.INITIATED, index=True)

    # Metadata
    notes = Column(Text)
    metadata = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))

    # Relationships
    payment_details = relationship("PaymentDetail", uselist=False, back_populates="checkout", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_checkout_user", "user_id"),
        Index("idx_checkout_status", "status"),
        Index("idx_checkout_token", "checkout_token"),
    )


# ============================================================================
# MODULE 104: PAYMENT PROCESSING
# ============================================================================

class PaymentDetail(Base):
    """Payment details"""
    __tablename__ = "payment_details"

    id = Column(Integer, primary_key=True, index=True)
    checkout_id = Column(Integer, ForeignKey("checkout_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Payment info
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)

    # Transaction details
    transaction_id = Column(String(255), unique=True, index=True)
    stripe_payment_intent_id = Column(String(255), unique=True, index=True)

    # Amount
    amount = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(3), default="USD")

    # Card details (encrypted in production)
    card_last_four = Column(String(4))
    card_brand = Column(String(50))

    # Processing details
    error_message = Column(Text)
    processor_response = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime(timezone=True))

    # Relationships
    checkout = relationship("CheckoutSession", back_populates="payment_details")
    refunds = relationship("Refund", back_populates="payment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_payment_checkout", "checkout_id"),
        Index("idx_payment_status", "status"),
        Index("idx_payment_transaction", "transaction_id"),
    )


class Refund(Base):
    """Refund records"""
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payment_details.id", ondelete="CASCADE"), nullable=False, index=True)

    # Refund details
    amount = Column(DECIMAL(12, 2), nullable=False)
    reason = Column(String(255), nullable=False)
    description = Column(Text)

    # Processing
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    refund_transaction_id = Column(String(255), unique=True, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime(timezone=True))

    # Relationships
    payment = relationship("PaymentDetail", back_populates="refunds")

    __table_args__ = (
        Index("idx_refund_payment", "payment_id"),
        Index("idx_refund_status", "status"),
    )


# ============================================================================
# MODULE 105: ORDER MANAGEMENT
# ============================================================================

class Order(Base):
    """Order model"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Addresses
    billing_address = Column(JSON, nullable=False)
    shipping_address = Column(JSON, nullable=False)

    # Contact
    email = Column(String(255), nullable=False)
    phone = Column(String(20))

    # Order totals
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    tax = Column(DECIMAL(12, 2), default=0.00)
    shipping = Column(DECIMAL(12, 2), default=0.00)
    discount = Column(DECIMAL(12, 2), default=0.00)
    total = Column(DECIMAL(12, 2), nullable=False)

    # Status tracking
    order_status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    shipping_status = Column(SQLEnum(ShippingStatus), default=ShippingStatus.NOT_SHIPPED, index=True)

    # Payment
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    payment_id = Column(String(255), index=True)

    # Shipping
    shipping_method = Column(String(100))
    tracking_number = Column(String(100), index=True)

    # Notes
    customer_notes = Column(Text)
    internal_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_order_user", "user_id"),
        Index("idx_order_status", "order_status"),
        Index("idx_order_shipping_status", "shipping_status"),
        Index("idx_order_number", "order_number"),
        Index("idx_order_created", "created_at"),
    )


class OrderItem(Base):
    """Items in an order"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    # Item details
    product_name = Column(String(255), nullable=False)
    product_sku = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    line_total = Column(DECIMAL(12, 2), nullable=False)

    # Selected attributes
    selected_attributes = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (
        Index("idx_order_item_order", "order_id"),
        Index("idx_order_item_product", "product_id"),
    )
