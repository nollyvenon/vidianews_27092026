"""Ecommerce services for products, cart, checkout, payments, and orders"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.ecommerce import (
    Product, ProductReview, Cart, CartItem, CheckoutSession, PaymentDetail,
    Refund, Order, OrderItem, ProductStatus, CartItemStatus, CheckoutStatus,
    PaymentStatus, OrderStatus, ShippingStatus, PaymentMethod
)
from app.models.auth import User
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import uuid
import stripe


class ProductService:
    """Product management service"""

    @staticmethod
    def create_product(db: Session, product_data: dict) -> Product:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100, category=None, status=ProductStatus.PUBLISHED):
        query = db.query(Product).filter(Product.status == status)
        if category:
            query = query.filter(Product.category == category)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_product(db: Session, product_id: int, update_data: dict) -> Product:
        product = ProductService.get_product(db, product_id)
        for key, value in update_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = ProductService.get_product(db, product_id)
        db.delete(product)
        db.commit()

    @staticmethod
    def search_products(db: Session, query: str, skip: int = 0, limit: int = 50):
        return db.query(Product).filter(
            Product.status == ProductStatus.PUBLISHED,
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.sku.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_featured_products(db: Session, limit: int = 20):
        return db.query(Product).filter(
            Product.is_featured == True,
            Product.status == ProductStatus.PUBLISHED
        ).limit(limit).all()

    @staticmethod
    def add_product_review(db: Session, product_id: int, user_id: int, review_data: dict) -> ProductReview:
        review = ProductReview(product_id=product_id, user_id=user_id, **review_data)
        db.add(review)

        product = ProductService.get_product(db, product_id)
        reviews = db.query(ProductReview).filter(ProductReview.product_id == product_id).all()
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        product.average_rating = avg_rating
        product.review_count = len(reviews)

        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_product_reviews(db: Session, product_id: int, skip: int = 0, limit: int = 50):
        return db.query(ProductReview).filter(
            ProductReview.product_id == product_id
        ).offset(skip).limit(limit).all()


class CartService:
    """Shopping cart service"""

    @staticmethod
    def get_or_create_cart(db: Session, user_id: int) -> Cart:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def add_to_cart(db: Session, cart_id: int, product_id: int, quantity: int, selected_attributes: dict = None) -> CartItem:
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        product = ProductService.get_product(db, product_id)

        existing_item = db.query(CartItem).filter(
            and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        ).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.line_total = Decimal(existing_item.quantity) * existing_item.unit_price
        else:
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
                line_total=Decimal(quantity) * product.price,
                selected_attributes=selected_attributes
            )
            db.add(cart_item)

        CartService.update_cart_totals(db, cart_id)
        db.commit()
        return existing_item or cart_item

    @staticmethod
    def update_cart_item(db: Session, cart_item_id: int, quantity: int):
        item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        item.quantity = quantity
        item.line_total = Decimal(quantity) * item.unit_price
        CartService.update_cart_totals(db, item.cart_id)
        db.commit()

    @staticmethod
    def remove_from_cart(db: Session, cart_item_id: int):
        item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        cart_id = item.cart_id
        db.delete(item)
        CartService.update_cart_totals(db, cart_id)
        db.commit()

    @staticmethod
    def update_cart_totals(db: Session, cart_id: int):
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

        subtotal = sum(item.line_total for item in items)
        cart.subtotal = subtotal
        cart.item_count = sum(item.quantity for item in items)
        cart.tax = subtotal * Decimal("0.08")
        cart.total = cart.subtotal + cart.tax + cart.shipping - cart.discount

    @staticmethod
    def clear_cart(db: Session, cart_id: int):
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        cart.subtotal = Decimal("0.00")
        cart.item_count = 0
        cart.total = Decimal("0.00")
        db.commit()

    @staticmethod
    def get_cart(db: Session, cart_id: int) -> Cart:
        return db.query(Cart).filter(Cart.id == cart_id).first()


class CheckoutService:
    """Checkout service"""

    @staticmethod
    def create_checkout_session(db: Session, user_id: int, cart_id: int, checkout_data: dict) -> CheckoutSession:
        cart = CartService.get_cart(db, cart_id)
        checkout = CheckoutSession(
            checkout_token=str(uuid.uuid4()),
            user_id=user_id,
            cart_id=cart_id,
            **checkout_data
        )
        checkout.subtotal = cart.subtotal
        checkout.tax = cart.tax
        checkout.total = cart.total

        db.add(checkout)
        db.commit()
        db.refresh(checkout)
        return checkout

    @staticmethod
    def get_checkout_session(db: Session, checkout_id: int) -> CheckoutSession:
        return db.query(CheckoutSession).filter(CheckoutSession.id == checkout_id).first()

    @staticmethod
    def update_checkout_session(db: Session, checkout_id: int, update_data: dict) -> CheckoutSession:
        checkout = CheckoutService.get_checkout_session(db, checkout_id)
        for key, value in update_data.items():
            setattr(checkout, key, value)
        db.commit()
        db.refresh(checkout)
        return checkout

    @staticmethod
    def apply_coupon(db: Session, checkout_id: int, coupon_code: str):
        checkout = CheckoutService.get_checkout_session(db, checkout_id)
        checkout.coupon_code = coupon_code
        discount = Decimal("0.10") * checkout.subtotal
        checkout.discount = discount
        checkout.total = checkout.subtotal + checkout.tax + checkout.shipping - discount
        db.commit()


class PaymentService:
    """Payment processing service"""

    @staticmethod
    def create_payment(db: Session, checkout_id: int, payment_data: dict) -> PaymentDetail:
        payment = PaymentDetail(
            checkout_id=checkout_id,
            **payment_data
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def process_stripe_payment(db: Session, payment_id: int, token: str):
        payment = db.query(PaymentDetail).filter(PaymentDetail.id == payment_id).first()

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency=payment.currency.lower(),
                payment_method=token,
                confirm=True
            )

            payment.stripe_payment_intent_id = intent.id
            payment.transaction_id = intent.id
            payment.status = PaymentStatus.COMPLETED
            payment.processed_at = datetime.now(timezone.utc)

            db.commit()
            return payment
        except stripe.error.CardError as e:
            payment.status = PaymentStatus.FAILED
            payment.error_message = str(e)
            db.commit()
            raise

    @staticmethod
    def process_refund(db: Session, payment_id: int, amount: Decimal, reason: str):
        payment = db.query(PaymentDetail).filter(PaymentDetail.id == payment_id).first()

        try:
            refund = stripe.Refund.create(
                payment_intent=payment.stripe_payment_intent_id,
                amount=int(amount * 100)
            )

            refund_record = Refund(
                payment_id=payment_id,
                amount=amount,
                reason=reason,
                refund_transaction_id=refund.id,
                status=PaymentStatus.COMPLETED
            )

            db.add(refund_record)
            payment.status = PaymentStatus.REFUNDED
            db.commit()
            return refund_record
        except stripe.error.StripeError as e:
            raise


class OrderService:
    """Order management service"""

    @staticmethod
    def create_order(db: Session, user_id: int, checkout_session: CheckoutSession, payment: PaymentDetail) -> Order:
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        order = Order(
            order_number=order_number,
            user_id=user_id,
            billing_address=checkout_session.billing_address,
            shipping_address=checkout_session.shipping_address,
            email=checkout_session.email,
            phone=checkout_session.phone,
            subtotal=checkout_session.subtotal,
            tax=checkout_session.tax,
            shipping=checkout_session.shipping,
            discount=checkout_session.discount,
            total=checkout_session.total,
            payment_method=payment.payment_method,
            payment_id=payment.transaction_id,
            shipping_method=checkout_session.shipping_method
        )

        cart = CartService.get_cart(db, checkout_session.cart_id)
        for cart_item in cart.items:
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                line_total=cart_item.line_total,
                selected_attributes=cart_item.selected_attributes
            )
            db.add(order_item)

        db.add(order)
        CartService.clear_cart(db, checkout_session.cart_id)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 50):
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: OrderStatus):
        order = OrderService.get_order(db, order_id)
        order.order_status = status
        db.commit()

    @staticmethod
    def update_shipping_status(db: Session, order_id: int, status: ShippingStatus, tracking_number: str = None):
        order = OrderService.get_order(db, order_id)
        order.shipping_status = status
        if tracking_number:
            order.tracking_number = tracking_number
        if status == ShippingStatus.SHIPPED:
            order.shipped_at = datetime.now(timezone.utc)
        elif status == ShippingStatus.DELIVERED:
            order.delivered_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def cancel_order(db: Session, order_id: int):
        order = OrderService.get_order(db, order_id)
        order.order_status = OrderStatus.CANCELLED
        db.commit()
