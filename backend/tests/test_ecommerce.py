"""Tests for ecommerce services"""

import pytest
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.ecommerce import (
    Product, ProductReview, Cart, CartItem, CheckoutSession, PaymentDetail,
    Refund, Order, OrderItem, ProductStatus, CartItemStatus, CheckoutStatus,
    PaymentStatus, OrderStatus, ShippingStatus, PaymentMethod
)
from app.models.auth import User
from app.services.ecommerce_service import (
    ProductService, CartService, CheckoutService, PaymentService, OrderService
)


class TestProductService:
    """Product service tests"""

    def test_create_product(self, db: Session):
        """Test creating a product"""
        product_data = {
            "sku": "TEST-001",
            "name": "Test Product",
            "price": Decimal("99.99"),
            "category": "electronics",
            "status": "published"
        }
        product = ProductService.create_product(db, product_data)

        assert product.id is not None
        assert product.sku == "TEST-001"
        assert product.name == "Test Product"
        assert product.price == Decimal("99.99")

    def test_get_product(self, db: Session, sample_product: Product):
        """Test getting a product"""
        product = ProductService.get_product(db, sample_product.id)

        assert product is not None
        assert product.id == sample_product.id
        assert product.sku == sample_product.sku

    def test_get_products(self, db: Session, sample_product: Product):
        """Test getting products list"""
        products = ProductService.get_products(db)

        assert len(products) > 0
        assert any(p.id == sample_product.id for p in products)

    def test_search_products(self, db: Session, sample_product: Product):
        """Test searching products"""
        results = ProductService.search_products(db, sample_product.name)

        assert len(results) > 0
        assert any(p.id == sample_product.id for p in results)

    def test_get_featured_products(self, db: Session):
        """Test getting featured products"""
        featured_products = ProductService.get_featured_products(db)

        assert isinstance(featured_products, list)

    def test_add_product_review(self, db: Session, sample_product: Product, sample_user: User):
        """Test adding product review"""
        review_data = {
            "rating": 5,
            "title": "Great product",
            "review_text": "This is a great product"
        }
        review = ProductService.add_product_review(
            db, sample_product.id, sample_user.id, review_data
        )

        assert review.id is not None
        assert review.rating == 5
        assert review.product_id == sample_product.id


class TestCartService:
    """Shopping cart service tests"""

    def test_get_or_create_cart(self, db: Session, sample_user: User):
        """Test getting or creating cart"""
        cart = CartService.get_or_create_cart(db, sample_user.id)

        assert cart.id is not None
        assert cart.user_id == sample_user.id

    def test_add_to_cart(self, db: Session, sample_user: User, sample_product: Product):
        """Test adding item to cart"""
        cart = CartService.get_or_create_cart(db, sample_user.id)
        cart_item = CartService.add_to_cart(db, cart.id, sample_product.id, 2)

        assert cart_item.quantity == 2
        assert cart_item.product_id == sample_product.id
        assert cart_item.line_total == 2 * sample_product.price

    def test_remove_from_cart(self, db: Session, sample_user: User, sample_product: Product):
        """Test removing item from cart"""
        cart = CartService.get_or_create_cart(db, sample_user.id)
        cart_item = CartService.add_to_cart(db, cart.id, sample_product.id, 1)

        CartService.remove_from_cart(db, cart_item.id)

        db.refresh(cart)
        assert cart.item_count == 0

    def test_clear_cart(self, db: Session, sample_user: User, sample_product: Product):
        """Test clearing cart"""
        cart = CartService.get_or_create_cart(db, sample_user.id)
        CartService.add_to_cart(db, cart.id, sample_product.id, 2)

        CartService.clear_cart(db, cart.id)

        db.refresh(cart)
        assert cart.item_count == 0
        assert cart.total == Decimal("0.00")


class TestCheckoutService:
    """Checkout service tests"""

    def test_create_checkout_session(self, db: Session, sample_user: User):
        """Test creating checkout session"""
        cart = CartService.get_or_create_cart(db, sample_user.id)

        checkout_data = {
            "billing_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            },
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            },
            "email": "test@example.com",
            "phone": "555-1234"
        }

        checkout = CheckoutService.create_checkout_session(
            db, sample_user.id, cart.id, checkout_data
        )

        assert checkout.id is not None
        assert checkout.checkout_token is not None
        assert checkout.user_id == sample_user.id

    def test_get_checkout_session(self, db: Session, sample_checkout: CheckoutSession):
        """Test getting checkout session"""
        checkout = CheckoutService.get_checkout_session(db, sample_checkout.id)

        assert checkout is not None
        assert checkout.id == sample_checkout.id

    def test_apply_coupon(self, db: Session, sample_checkout: CheckoutSession):
        """Test applying coupon"""
        CheckoutService.apply_coupon(db, sample_checkout.id, "DISCOUNT10")

        db.refresh(sample_checkout)
        assert sample_checkout.coupon_code == "DISCOUNT10"
        assert sample_checkout.discount > Decimal("0.00")


class TestPaymentService:
    """Payment service tests"""

    def test_create_payment(self, db: Session, sample_checkout: CheckoutSession):
        """Test creating payment"""
        payment_data = {
            "payment_method": "stripe",
            "amount": sample_checkout.total,
            "currency": "USD"
        }

        payment = PaymentService.create_payment(db, sample_checkout.id, payment_data)

        assert payment.id is not None
        assert payment.checkout_id == sample_checkout.id
        assert payment.amount == sample_checkout.total


class TestOrderService:
    """Order service tests"""

    def test_create_order(
        self, db: Session, sample_user: User, sample_checkout: CheckoutSession,
        sample_payment: PaymentDetail
    ):
        """Test creating order"""
        order = OrderService.create_order(db, sample_user.id, sample_checkout, sample_payment)

        assert order.id is not None
        assert order.order_number is not None
        assert order.user_id == sample_user.id
        assert order.total == sample_checkout.total

    def test_get_order(self, db: Session, sample_order: Order):
        """Test getting order"""
        order = OrderService.get_order(db, sample_order.id)

        assert order is not None
        assert order.id == sample_order.id

    def test_get_user_orders(self, db: Session, sample_user: User, sample_order: Order):
        """Test getting user orders"""
        orders = OrderService.get_user_orders(db, sample_user.id)

        assert len(orders) > 0
        assert any(o.id == sample_order.id for o in orders)

    def test_update_order_status(self, db: Session, sample_order: Order):
        """Test updating order status"""
        OrderService.update_order_status(db, sample_order.id, OrderStatus.SHIPPED)

        db.refresh(sample_order)
        assert sample_order.order_status == OrderStatus.SHIPPED

    def test_cancel_order(self, db: Session, sample_order: Order):
        """Test cancelling order"""
        OrderService.cancel_order(db, sample_order.id)

        db.refresh(sample_order)
        assert sample_order.order_status == OrderStatus.CANCELLED


# Fixtures

@pytest.fixture
def sample_product(db: Session) -> Product:
    """Create sample product"""
    product = Product(
        sku="TEST-PRODUCT-001",
        name="Sample Product",
        price=Decimal("99.99"),
        category="electronics",
        status=ProductStatus.PUBLISHED,
        stock_quantity=100
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture
def sample_user(db: Session) -> User:
    """Create sample user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_checkout(db: Session, sample_user: User) -> CheckoutSession:
    """Create sample checkout session"""
    cart = CartService.get_or_create_cart(db, sample_user.id)
    checkout = CheckoutSession(
        checkout_token="test-token-123",
        user_id=sample_user.id,
        cart_id=cart.id,
        billing_address={"street": "123 Main", "city": "NY"},
        shipping_address={"street": "123 Main", "city": "NY"},
        email="test@example.com",
        subtotal=Decimal("99.99"),
        total=Decimal("107.99")
    )
    db.add(checkout)
    db.commit()
    db.refresh(checkout)
    return checkout


@pytest.fixture
def sample_payment(db: Session, sample_checkout: CheckoutSession) -> PaymentDetail:
    """Create sample payment"""
    payment = PaymentDetail(
        checkout_id=sample_checkout.id,
        payment_method=PaymentMethod.STRIPE,
        amount=sample_checkout.total
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@pytest.fixture
def sample_order(db: Session, sample_user: User, sample_checkout: CheckoutSession, sample_payment: PaymentDetail) -> Order:
    """Create sample order"""
    order = Order(
        order_number="ORD-001",
        user_id=sample_user.id,
        billing_address={"street": "123 Main", "city": "NY"},
        shipping_address={"street": "123 Main", "city": "NY"},
        email="test@example.com",
        subtotal=Decimal("99.99"),
        tax=Decimal("8.00"),
        total=Decimal("107.99"),
        payment_method=PaymentMethod.STRIPE,
        payment_id="txn_123"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
