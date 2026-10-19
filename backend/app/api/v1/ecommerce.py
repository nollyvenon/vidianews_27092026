"""Ecommerce API endpoints.

Access rules:
- The catalog is public for published products. Drafts are visible to administrators only;
  creating and changing products requires the ecommerce administrator role.
- Carts, checkouts, orders and cart items belong to the signed-in user. Anything of another
  user's is answered with 404.
- A card charge is made only for a checkout that has no completed payment yet, so a declined
  card can be retried.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

import stripe
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import is_admin, require_admin
from app.core.config import settings
from app.core.security import get_current_user, get_optional_current_user
from app.db.session import get_db
from app.models.ecommerce import CartItem, DiscountType, ProductStatus
from app.models.user import User
from app.services.coupon_service import CouponService
from app.services.ecommerce_service import (
    CartService,
    CheckoutService,
    OrderService,
    PaymentService,
    ProductService,
)

router = APIRouter()

require_ecommerce_admin = require_admin("ecommerce")


class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    status: str = "draft"


class ProductResponse(ProductBase):
    id: int
    stock_quantity: int
    average_rating: float
    review_count: int


class ProductReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    review_text: Optional[str] = None


class CartItemRequest(BaseModel):
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1, le=1000)
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


async def _is_ecommerce_admin(session: AsyncSession, user: Optional[User]) -> bool:
    return user is not None and await is_admin(session, user.id, "ecommerce")


async def _own_cart_item(session: AsyncSession, user: User, item_id: int) -> CartItem:
    item = await CartService(session).get_cart_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart = await CartService(session).get_cart(item.cart_id)
    if cart is None or cart.user_id != user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


# ============================================================================
# PRODUCTS
# ============================================================================

@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
):
    """Published products"""
    return await ProductService(session).get_products(skip=skip, limit=limit, category=category)


@router.get("/products/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    """Published products matching the text"""
    return await ProductService(session).search_products(q, skip=skip, limit=limit)


@router.get("/products/featured", response_model=List[ProductResponse])
async def get_featured_products(session: AsyncSession = Depends(get_db)):
    return await ProductService(session).get_featured_products()


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    session: AsyncSession = Depends(get_db),
):
    """A published product; drafts are visible to ecommerce administrators only"""
    product = await ProductService(session).get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.status != ProductStatus.PUBLISHED and not await _is_ecommerce_admin(session, current_user):
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductBase,
    _admin: User = Depends(require_ecommerce_admin),
    session: AsyncSession = Depends(get_db),
):
    """Create a product (ecommerce administrators)"""
    return await ProductService(session).create_product(product.model_dump())


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductBase,
    _admin: User = Depends(require_ecommerce_admin),
    session: AsyncSession = Depends(get_db),
):
    """Update a product (ecommerce administrators)"""
    return await ProductService(session).update_product(product_id, product.model_dump())


@router.post("/products/{product_id}/reviews", status_code=201)
async def add_product_review(
    product_id: int,
    review: ProductReviewRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    product = await ProductService(session).get_product(product_id)
    if product is None or product.status != ProductStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Product not found")
    return await ProductService(session).add_product_review(product_id, current_user.id, review.model_dump())


@router.get("/products/{product_id}/reviews")
async def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    product = await ProductService(session).get_product(product_id)
    if product is None or product.status != ProductStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Product not found")
    return await ProductService(session).get_product_reviews(product_id, skip=skip, limit=limit)


# ============================================================================
# CART
# ============================================================================

@router.get("/cart", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await CartService(session).get_or_create_cart(current_user.id)


@router.post("/cart/items", status_code=201)
async def add_to_cart(
    item: CartItemRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    cart = await CartService(session).get_or_create_cart(current_user.id)
    return await CartService(session).add_to_cart(cart.id, item.product_id, item.quantity, item.selected_attributes)


@router.put("/cart/items/{item_id}")
async def update_cart_item(
    item_id: int,
    quantity: int = Query(..., ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _own_cart_item(session, current_user, item_id)
    await CartService(session).update_cart_item(item_id, quantity)
    return {"status": "success"}


@router.delete("/cart/items/{item_id}")
async def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await _own_cart_item(session, current_user, item_id)
    await CartService(session).remove_from_cart(item_id)
    return {"status": "success"}


@router.delete("/cart")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    cart = await CartService(session).get_or_create_cart(current_user.id)
    await CartService(session).clear_cart(cart.id)
    return {"status": "success"}


# ============================================================================
# CHECKOUT
# ============================================================================

@router.post("/checkout", status_code=201)
async def create_checkout(
    checkout: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    cart = await CartService(session).get_or_create_cart(current_user.id)
    try:
        return await CheckoutService(session).create_checkout_session(current_user.id, cart.id, checkout.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/checkout/{checkout_id}")
async def get_checkout(
    checkout_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    checkout = await CheckoutService(session).get_checkout_session(checkout_id)
    if checkout is None or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    return checkout


@router.post("/checkout/{checkout_id}/coupon")
async def apply_coupon(
    checkout_id: int,
    coupon_code: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    checkout = await CheckoutService(session).get_checkout_session(checkout_id)
    if checkout is None or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    checkout = await CheckoutService(session).apply_coupon(checkout_id, coupon_code)
    return {
        "status": "success",
        "coupon_code": checkout.coupon_code,
        "discount": checkout.discount,
        "total": checkout.total,
    }


class CouponRequest(BaseModel):
    code: str = Field(min_length=3, max_length=50)
    discount_type: DiscountType
    discount_value: Decimal = Field(gt=0)
    min_subtotal: Decimal = Field(default=Decimal("0.00"), ge=0)
    max_redemptions: Optional[int] = Field(default=None, ge=1)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class CouponStatusRequest(BaseModel):
    is_active: bool


class CouponResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    min_subtotal: Decimal
    max_redemptions: Optional[int]
    redemption_count: int
    valid_from: Optional[datetime]
    valid_until: Optional[datetime]
    is_active: bool
    created_at: Optional[datetime]


@router.get("/coupons", response_model=List[CouponResponse])
async def list_coupons(
    _admin: User = Depends(require_ecommerce_admin),
    session: AsyncSession = Depends(get_db),
):
    """Every coupon with its redemption count (administrators only)"""
    return await CouponService.list_coupons(session)


@router.post("/coupons", response_model=CouponResponse, status_code=201)
async def create_coupon(
    request: CouponRequest,
    _admin: User = Depends(require_ecommerce_admin),
    session: AsyncSession = Depends(get_db),
):
    """Create a discount code (administrators only)"""
    return await CouponService.create_coupon(session, request.model_dump())


@router.patch("/coupons/{coupon_id}", response_model=CouponResponse)
async def set_coupon_status(
    coupon_id: int,
    request: CouponStatusRequest,
    _admin: User = Depends(require_ecommerce_admin),
    session: AsyncSession = Depends(get_db),
):
    """Enable or disable a discount code (administrators only)"""
    return await CouponService.set_active(session, coupon_id, request.is_active)


# ============================================================================
# PAYMENTS
# ============================================================================

@router.post("/checkout/{checkout_id}/payment")
async def process_payment(
    checkout_id: int,
    payment: PaymentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Charge the checkout total by card and create the order once the charge succeeds.

    The amount is always the checkout total; the client's amount is ignored. Only card
    payments through Stripe are supported.
    """
    checkout = await CheckoutService(session).get_checkout_session(checkout_id)
    if checkout is None or checkout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Checkout not found")
    if payment.payment_method != "stripe":
        raise HTTPException(status_code=422, detail="Only card payments are supported")
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Card payments are not configured on this server")
    if not payment.card_token:
        raise HTTPException(status_code=422, detail="A card payment method is required")

    payments = PaymentService(session)
    if await payments.completed_payment_for(checkout_id) is not None:
        raise HTTPException(status_code=409, detail="This checkout has already been paid")

    payment_detail = await payments.create_payment(
        checkout_id,
        {"payment_method": payment.payment_method, "amount": checkout.total, "currency": "USD"},
    )
    try:
        await payments.process_stripe_payment(payment_detail.id, payment.card_token)
    except stripe.error.CardError as exc:
        raise HTTPException(status_code=402, detail=exc.user_message or "Your card was declined") from exc
    except stripe.error.StripeError as err:
        raise HTTPException(status_code=502, detail="The payment provider could not complete the charge") from err

    await session.refresh(payment_detail)
    order = await OrderService(session).create_order(current_user.id, checkout, payment_detail)
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
async def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await OrderService(session).get_user_orders(current_user.id, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    order = await OrderService(session).get_order(order_id)
    if order is None or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    order = await OrderService(session).get_order(order_id)
    if order is None or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    await OrderService(session).cancel_order(order_id)
    return {"status": "success"}
