"""Ecommerce services for products, cart, checkout, payments, and orders (async).

Card charges and refunds call Stripe in a worker thread so the event loop keeps serving requests.
Timestamps are naive UTC to match the ecommerce columns.
"""

import asyncio
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

import stripe
from sqlalchemy import and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.ecommerce import (
    Cart,
    CartItem,
    CheckoutSession,
    Order,
    OrderItem,
    OrderStatus,
    PaymentDetail,
    PaymentStatus,
    Product,
    ProductReview,
    ProductStatus,
    Refund,
    ShippingStatus,
)
from app.services.coupon_service import CouponService
from app.utils.exceptions import NotFoundError

# Shipping charges by method, in the order currency. The checkout total adds the chosen rate.
SHIPPING_RATES = {
    "standard": Decimal("5.00"),
    "express": Decimal("15.00"),
    "overnight": Decimal("25.00"),
}

TAX_RATE = Decimal("0.08")


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ProductService:
    """Product management service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def get_products(self, skip: int = 0, limit: int = 100, category: Optional[str] = None,
                           status: ProductStatus = ProductStatus.PUBLISHED) -> List[Product]:
        stmt = select(Product).where(Product.status == status)
        if category:
            stmt = stmt.where(Product.category == category)
        result = await self.session.execute(stmt.order_by(Product.id).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_product(self, product_id: int, update_data: dict) -> Product:
        product = await self.get_product(product_id)
        if product is None:
            raise NotFoundError("Product")
        for key, value in update_data.items():
            setattr(product, key, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        if product is None:
            raise NotFoundError("Product")
        await self.session.delete(product)
        await self.session.commit()

    async def search_products(self, query: str, skip: int = 0, limit: int = 50) -> List[Product]:
        result = await self.session.execute(
            select(Product).where(
                Product.status == ProductStatus.PUBLISHED,
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%"),
                ),
            ).order_by(Product.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_featured_products(self, limit: int = 20) -> List[Product]:
        result = await self.session.execute(
            select(Product).where(
                Product.is_featured == True,  # noqa: E712 - SQL comparison
                Product.status == ProductStatus.PUBLISHED,
            ).order_by(Product.id).limit(limit)
        )
        return list(result.scalars().all())

    async def add_product_review(self, product_id: int, user_id: int, review_data: dict) -> ProductReview:
        product = await self.get_product(product_id)
        if product is None:
            raise NotFoundError("Product")
        review = ProductReview(product_id=product_id, user_id=user_id, **review_data)
        self.session.add(review)
        await self.session.flush()
        ratings = (await self.session.execute(
            select(ProductReview.rating).where(ProductReview.product_id == product_id)
        )).scalars().all()
        product.average_rating = sum(ratings) / len(ratings) if ratings else 0
        product.review_count = len(ratings)
        await self.session.commit()
        await self.session.refresh(review)
        return review

    async def get_product_reviews(self, product_id: int, skip: int = 0, limit: int = 50) -> List[ProductReview]:
        result = await self.session.execute(
            select(ProductReview).where(ProductReview.product_id == product_id)
            .order_by(ProductReview.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())


class CartService:
    """Shopping cart service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_cart(self, user_id: int) -> Cart:
        cart = (await self.session.execute(select(Cart).where(Cart.user_id == user_id))).scalar_one_or_none()
        if cart is None:
            cart = Cart(user_id=user_id)
            self.session.add(cart)
            await self.session.commit()
            await self.session.refresh(cart)
        return cart

    async def add_to_cart(self, cart_id: int, product_id: int, quantity: int,
                          selected_attributes: Optional[dict] = None) -> CartItem:
        cart = await self.get_cart(cart_id)
        if cart is None:
            raise NotFoundError("Cart")
        product = await self.session.get(Product, product_id)
        if product is None:
            raise NotFoundError("Product")

        item = (await self.session.execute(
            select(CartItem).where(and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id))
        )).scalar_one_or_none()
        if item is not None:
            item.quantity += quantity
            item.line_total = Decimal(item.quantity) * item.unit_price
        else:
            item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
                line_total=Decimal(quantity) * product.price,
                selected_attributes=selected_attributes,
            )
            self.session.add(item)
        await self.update_cart_totals(cart_id)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_cart_item(self, cart_item_id: int) -> Optional[CartItem]:
        return await self.session.get(CartItem, cart_item_id)

    async def _item(self, cart_item_id: int) -> CartItem:
        item = await self.session.get(CartItem, cart_item_id)
        if item is None:
            raise NotFoundError("Cart item")
        return item

    async def update_cart_item(self, cart_item_id: int, quantity: int) -> None:
        item = await self._item(cart_item_id)
        item.quantity = quantity
        item.line_total = Decimal(quantity) * item.unit_price
        await self.update_cart_totals(item.cart_id)
        await self.session.commit()

    async def remove_from_cart(self, cart_item_id: int) -> None:
        item = await self._item(cart_item_id)
        cart_id = item.cart_id
        await self.session.delete(item)
        await self.update_cart_totals(cart_id)
        await self.session.commit()

    async def update_cart_totals(self, cart_id: int) -> None:
        # Pending item changes must reach the database before the totals are summed from it.
        await self.session.flush()
        cart = await self.get_cart(cart_id)
        items = (await self.session.execute(select(CartItem).where(CartItem.cart_id == cart_id))).scalars().all()
        subtotal = sum((item.line_total for item in items), Decimal("0.00"))
        cart.subtotal = subtotal
        cart.item_count = sum(item.quantity for item in items)
        cart.tax = subtotal * TAX_RATE
        cart.total = cart.subtotal + cart.tax + cart.shipping - cart.discount

    async def clear_cart(self, cart_id: int) -> None:
        await self.session.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
        cart = await self.get_cart(cart_id)
        cart.subtotal = Decimal("0.00")
        cart.item_count = 0
        cart.total = Decimal("0.00")
        await self.session.commit()

    async def get_cart(self, cart_id: int) -> Optional[Cart]:
        return await self.session.get(Cart, cart_id)

    async def get_cart_items(self, cart_id: int) -> List[CartItem]:
        result = await self.session.execute(
            select(CartItem).where(CartItem.cart_id == cart_id)
            .options(selectinload(CartItem.product)).order_by(CartItem.id)
        )
        return list(result.scalars().all())


class CheckoutService:
    """Checkout service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_checkout_session(self, user_id: int, cart_id: int, checkout_data: dict) -> CheckoutSession:
        cart = await CartService(self.session).get_cart(cart_id)
        if cart is None or cart.item_count == 0:
            raise ValueError("Your cart is empty")
        shipping_method = checkout_data.get("shipping_method")
        if shipping_method not in SHIPPING_RATES:
            raise ValueError(f"Unknown shipping method: {shipping_method}")

        shipping_cost = SHIPPING_RATES[shipping_method]
        checkout = CheckoutSession(
            checkout_token=str(uuid.uuid4()),
            user_id=user_id,
            cart_id=cart_id,
            **checkout_data,
        )
        checkout.subtotal = cart.subtotal
        checkout.tax = cart.tax
        checkout.shipping_cost = shipping_cost
        checkout.discount = Decimal("0.00")
        checkout.total = cart.subtotal + cart.tax + shipping_cost - checkout.discount
        self.session.add(checkout)
        await self.session.commit()
        await self.session.refresh(checkout)
        return checkout

    async def get_checkout_session(self, checkout_id: int) -> Optional[CheckoutSession]:
        return await self.session.get(CheckoutSession, checkout_id)

    async def update_checkout_session(self, checkout_id: int, update_data: dict) -> CheckoutSession:
        checkout = await self.get_checkout_session(checkout_id)
        if checkout is None:
            raise NotFoundError("Checkout")
        for key, value in update_data.items():
            setattr(checkout, key, value)
        await self.session.commit()
        await self.session.refresh(checkout)
        return checkout

    async def apply_coupon(self, checkout_id: int, coupon_code: str) -> CheckoutSession:
        checkout = await self.get_checkout_session(checkout_id)
        if checkout is None:
            raise NotFoundError("Checkout")
        return await CouponService.apply_to_checkout(self.session, checkout, coupon_code)


class PaymentService:
    """Payment processing service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, checkout_id: int, payment_data: dict) -> PaymentDetail:
        payment = PaymentDetail(checkout_id=checkout_id, **payment_data)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def completed_payment_for(self, checkout_id: int) -> Optional[PaymentDetail]:
        return (await self.session.execute(
            select(PaymentDetail).where(
                PaymentDetail.checkout_id == checkout_id,
                PaymentDetail.status == PaymentStatus.COMPLETED,
            )
        )).scalar_one_or_none()

    async def process_stripe_payment(self, payment_id: int, token: str) -> PaymentDetail:
        payment = await self.session.get(PaymentDetail, payment_id)
        if payment is None:
            raise NotFoundError("Payment")
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            intent = await asyncio.to_thread(
                stripe.PaymentIntent.create,
                amount=int(payment.amount * 100),
                currency=payment.currency.lower(),
                payment_method=token,
                confirm=True,
            )
        except stripe.error.CardError as error:
            payment.status = PaymentStatus.FAILED
            payment.error_message = str(error)
            await self.session.commit()
            raise

        payment.stripe_payment_intent_id = intent.id
        payment.transaction_id = intent.id
        payment.status = PaymentStatus.COMPLETED
        payment.processed_at = _utc_now_naive()
        await self.session.commit()
        return payment

    async def process_refund(self, payment_id: int, amount: Decimal, reason: str) -> Refund:
        payment = await self.session.get(PaymentDetail, payment_id)
        if payment is None:
            raise NotFoundError("Payment")
        stripe.api_key = settings.STRIPE_SECRET_KEY
        refund = await asyncio.to_thread(
            stripe.Refund.create,
            payment_intent=payment.stripe_payment_intent_id,
            amount=int(amount * 100),
        )
        record = Refund(
            payment_id=payment_id,
            amount=amount,
            reason=reason,
            refund_transaction_id=refund.id,
            status=PaymentStatus.COMPLETED,
        )
        self.session.add(record)
        payment.status = PaymentStatus.REFUNDED
        await self.session.commit()
        await self.session.refresh(record)
        return record


class OrderService:
    """Order management service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_id: int, checkout_session: CheckoutSession, payment: PaymentDetail) -> Order:
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=user_id,
            billing_address=checkout_session.billing_address,
            shipping_address=checkout_session.shipping_address,
            email=checkout_session.email,
            phone=checkout_session.phone,
            subtotal=checkout_session.subtotal,
            tax=checkout_session.tax,
            shipping=checkout_session.shipping_cost,
            discount=checkout_session.discount,
            total=checkout_session.total,
            payment_method=payment.payment_method,
            payment_id=payment.transaction_id,
            shipping_method=checkout_session.shipping_method,
        )
        self.session.add(order)
        await self.session.flush()

        cart_items = await CartService(self.session).get_cart_items(checkout_session.cart_id)
        for cart_item in cart_items:
            self.session.add(OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                line_total=cart_item.line_total,
                selected_attributes=cart_item.selected_attributes,
            ))
        await CartService(self.session).clear_cart(checkout_session.cart_id)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order(self, order_id: int) -> Optional[Order]:
        result = await self.session.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    async def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
        result = await self.session.execute(
            select(Order).where(Order.user_id == user_id).options(selectinload(Order.items))
            .order_by(Order.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_order_status(self, order_id: int, status: OrderStatus) -> None:
        order = await self.get_order(order_id)
        if order is None:
            raise NotFoundError("Order")
        order.order_status = status
        await self.session.commit()

    async def update_shipping_status(self, order_id: int, status: ShippingStatus,
                                     tracking_number: Optional[str] = None) -> None:
        order = await self.get_order(order_id)
        if order is None:
            raise NotFoundError("Order")
        order.shipping_status = status
        if tracking_number:
            order.tracking_number = tracking_number
        if status == ShippingStatus.SHIPPED:
            order.shipped_at = _utc_now_naive()
        elif status == ShippingStatus.DELIVERED:
            order.delivered_at = _utc_now_naive()
        await self.session.commit()

    async def cancel_order(self, order_id: int) -> None:
        order = await self.get_order(order_id)
        if order is None:
            raise NotFoundError("Order")
        order.order_status = OrderStatus.CANCELLED
        await self.session.commit()
