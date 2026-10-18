"""Ecommerce API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.services.ecommerce_service import (
    ProductService, CartService, CheckoutService, PaymentService, OrderService
)
from app.models.user import User
from app.models.ecommerce import PaymentDetail
from app.core.config import settings
import stripe
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: Decimal
    category: str
    status: str = "draft"


class ProductResponse(ProductBase):
    id: int
    stock_quantity: int
    average_rating: float
    review_count: int


class ProductReviewRequest(BaseModel):
    rating: int
    title: Optional[str] = None
    review_text: Optional[str] = None


class CartItemRequest(BaseModel):
    product_id: int
    quantity: int
    selected_attributes: Optional[dict] = None


class CartResponse(BaseModel):
    id: int
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    discount: Decimal
    total: Decimal
    item_count: int


class CheckoutRequest(BaseModel):
    billing_address: dict
    shipping_address: dict
    email: str
    phone: Optional[str] = None
    shipping_method: str


class PaymentRequest(BaseModel):
    payment_method: str
    amount: Decimal
    card_token: Optional[str] = None


class OrderItemResponse(BaseModel):
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    order_number: str
    email: str
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    discount: Decimal
    total: Decimal
    order_status: str
    shipping_status: str
    shipping_method: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# ============================================================================
# PRODUCTS
# ============================================================================

@router.get("/products", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products"""
    return ProductService.get_products(db, skip=skip, limit=limit, category=category)


@router.get("/products/search", response_model=List[ProductResponse])
def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search products"""
    return ProductService.search_products(db, q, skip=skip, limit=limit)


@router.get("/products/featured", response_model=List[ProductResponse])
def get_featured_products(db: Session = Depends(get_db)):
    """Get featured products"""
    return ProductService.get_featured_products(db)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new product (admin only)"""
    return ProductService.create_product(db, product.dict())


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update product (admin only)"""
    return ProductService.update_product(db, product_id, product.dict())

@router.post("/products/{product_id}/reviews")
def add_product_review(
    product_id: int,
    review: ProductReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add product review"""
    return ProductService.add_product_review(db, product_id, current_user.id, review.dict())


@router.get("/products/{product_id}/reviews")
def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get product reviews"""
    return ProductService.get_product_reviews(db, product_id, skip=skip, limit=limit)


# ============================================================================
# CART
# ============================================================================

@router.get("/cart", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's cart"""
    cart = CartService.get_or_create_cart(db, current_user.id)
    return cart


@router.post("/cart/items")
def add_to_cart(
    item: CartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    cart = CartService.get_or_create_cart(db, current_user.id)
    return CartService.add_to_cart(
        db, cart.id, item.product_id, item.quantity, item.selected_attributes
    )


@router.put("/cart/items/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    CartService.update_cart_item(db, item_id, quantity)
    return {"status": "success"}


@router.delete("/cart/items/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    CartService.remove_from_cart(db, item_id)
    return {"status": "success"}


@router.delete("/cart")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear cart"""
    cart = CartService.get_or_create_cart(db, current_user.id)
    CartService.clear_cart(db, cart.id)
    return {"status": "success"}


# ============================================================================
# CHECKOUT
# ============================================================================

@router.post("/checkout")
def create_checkout(
    checkout: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create checkout session"""
    cart = CartService.get_or_create_cart(db, current_user.id)
    try:
        return CheckoutService.create_checkout_session(db, current_user.id, cart.id, checkout.dict())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/checkout/{checkout_id}")
def get_checkout(
    checkout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get checkout session"""
    checkout = CheckoutService.get_checkout_session(db, checkout_id)
    if not checkout or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    return checkout


@router.post("/checkout/{checkout_id}/coupon")
def apply_coupon(
    checkout_id: int,
    coupon_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Apply coupon code"""
    checkout = CheckoutService.get_checkout_session(db, checkout_id)
    if not checkout or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    CheckoutService.apply_coupon(db, checkout_id, coupon_code)
    return {"status": "success"}


# ============================================================================
# PAYMENTS
# ============================================================================

@router.post("/checkout/{checkout_id}/payment")
def process_payment(
    checkout_id: int,
    payment: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Charge the checkout total by card and create the order once the charge succeeds.

    The amount is always the checkout total; the client's amount is ignored. Only card
    payments through Stripe are supported.
    """
    checkout = CheckoutService.get_checkout_session(db, checkout_id)
    if not checkout or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    if payment.payment_method != "stripe":
        raise HTTPException(status_code=422, detail="Only card payments are supported")
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Card payments are not configured on this server")
    if not payment.card_token:
        raise HTTPException(status_code=422, detail="A card payment method is required")
    if db.query(PaymentDetail).filter(PaymentDetail.checkout_id == checkout_id).first():
        raise HTTPException(status_code=409, detail="This checkout has already been paid")

    payment_detail = PaymentService.create_payment(
        db,
        checkout_id,
        {"payment_method": payment.payment_method, "amount": checkout.total, "currency": "USD"},
    )
    try:
        PaymentService.process_stripe_payment(db, payment_detail.id, payment.card_token)
    except stripe.error.CardError as exc:
        raise HTTPException(status_code=402, detail=exc.user_message or "Your card was declined")
    except stripe.error.StripeError as exc:
        raise HTTPException(status_code=502, detail="The payment provider could not complete the charge")

    db.refresh(payment_detail)
    order = OrderService.create_order(db, current_user.id, checkout, payment_detail)
    return {
        "payment_id": payment_detail.id,
        "status": payment_detail.status.value,
        "amount": str(payment_detail.amount),
        "currency": payment_detail.currency,
        "order_id": order.id,
        "order_number": order.order_number,
    }


# ============================================================================
# ORDERS
# ============================================================================

@router.get("/orders", response_model=List[OrderResponse])
def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's orders"""
    return OrderService.get_user_orders(db, current_user.id, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get order details"""
    order = OrderService.get_order(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel order"""
    order = OrderService.get_order(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    OrderService.cancel_order(db, order_id)
    return {"status": "success"}
