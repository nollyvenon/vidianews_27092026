"""Tests for ecommerce services (async)."""

from decimal import Decimal

import pytest

from app.models.ecommerce import (
    CheckoutSession,
    Order,
    OrderStatus,
    PaymentDetail,
    PaymentMethod,
    Product,
    ProductStatus,
)
from app.models.user import User
from app.services.ecommerce_service import (
    CartService,
    CheckoutService,
    OrderService,
    PaymentService,
    ProductService,
)

SHIPPING = {
    "shipping_method": "standard",
    "billing_address": {"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"},
    "shipping_address": {"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"},
    "email": "test@example.com",
    "phone": "555-1234",
}


@pytest.fixture
async def sample_product(session) -> Product:
    product = Product(
        sku="TEST-PRODUCT-001",
        name="Sample Product",
        price=Decimal("99.99"),
        category="electronics",
        status=ProductStatus.PUBLISHED,
        stock_quantity=100,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest.fixture
async def sample_user(session) -> User:
    user = User(email="test@example.com", password_hash="password_hash")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def sample_checkout(session, sample_user) -> CheckoutSession:
    cart = await CartService(session).get_or_create_cart(sample_user.id)
    checkout = CheckoutSession(
        checkout_token="test-token-123",
        user_id=sample_user.id,
        cart_id=cart.id,
        billing_address={"street": "123 Main", "city": "NY"},
        shipping_address={"street": "123 Main", "city": "NY"},
        email="test@example.com",
        subtotal=Decimal("99.99"),
        total=Decimal("107.99"),
    )
    session.add(checkout)
    await session.commit()
    await session.refresh(checkout)
    return checkout


@pytest.fixture
async def sample_payment(session, sample_checkout) -> PaymentDetail:
    payment = PaymentDetail(
        checkout_id=sample_checkout.id,
        payment_method=PaymentMethod.STRIPE,
        amount=sample_checkout.total,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


@pytest.fixture
async def sample_order(session, sample_user) -> Order:
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
        payment_id="txn_123",
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


class TestProductService:
    async def test_create_product(self, session):
        product = await ProductService(session).create_product({
            "sku": "TEST-001",
            "name": "Test Product",
            "price": Decimal("99.99"),
            "category": "electronics",
            "status": "published",
        })
        assert product.id is not None
        assert product.price == Decimal("99.99")

    async def test_get_products_and_get_product(self, session, sample_product):
        service = ProductService(session)
        assert (await service.get_product(sample_product.id)).sku == sample_product.sku
        assert any(p.id == sample_product.id for p in await service.get_products())

    async def test_drafts_are_not_listed_as_published(self, session, sample_product):
        sample_product.status = ProductStatus.DRAFT
        await session.commit()
        assert await ProductService(session).get_products() == []

    async def test_search_products(self, session, sample_product):
        results = await ProductService(session).search_products(sample_product.name)
        assert any(p.id == sample_product.id for p in results)

    async def test_get_featured_products(self, session):
        assert isinstance(await ProductService(session).get_featured_products(), list)

    async def test_add_product_review_updates_the_product(self, session, sample_product, sample_user):
        service = ProductService(session)
        review = await service.add_product_review(sample_product.id, sample_user.id, {
            "rating": 5, "title": "Great product", "review_text": "This is a great product",
        })
        assert review.rating == 5
        await session.refresh(sample_product)
        assert sample_product.review_count == 1
        assert sample_product.average_rating == 5

    async def test_review_of_a_missing_product_is_not_found(self, session, sample_user):
        from app.utils.exceptions import NotFoundError

        with pytest.raises(NotFoundError):
            await ProductService(session).add_product_review(999999, sample_user.id, {"rating": 3})


class TestCartService:
    async def test_get_or_create_cart(self, session, sample_user):
        cart = await CartService(session).get_or_create_cart(sample_user.id)
        assert cart.user_id == sample_user.id
        assert (await CartService(session).get_or_create_cart(sample_user.id)).id == cart.id

    async def test_add_to_cart_prices_the_line(self, session, sample_user, sample_product):
        service = CartService(session)
        cart = await service.get_or_create_cart(sample_user.id)
        item = await service.add_to_cart(cart.id, sample_product.id, 2)
        assert item.quantity == 2
        assert item.line_total == 2 * sample_product.price
        await session.refresh(cart)
        assert cart.item_count == 2

    async def test_adding_the_same_product_adds_to_the_quantity(self, session, sample_user, sample_product):
        service = CartService(session)
        cart = await service.get_or_create_cart(sample_user.id)
        await service.add_to_cart(cart.id, sample_product.id, 1)
        item = await service.add_to_cart(cart.id, sample_product.id, 2)
        assert item.quantity == 3

    async def test_remove_from_cart(self, session, sample_user, sample_product):
        service = CartService(session)
        cart = await service.get_or_create_cart(sample_user.id)
        item = await service.add_to_cart(cart.id, sample_product.id, 1)
        await service.remove_from_cart(item.id)
        await session.refresh(cart)
        assert cart.item_count == 0

    async def test_clear_cart(self, session, sample_user, sample_product):
        service = CartService(session)
        cart = await service.get_or_create_cart(sample_user.id)
        await service.add_to_cart(cart.id, sample_product.id, 2)
        await service.clear_cart(cart.id)
        await session.refresh(cart)
        assert cart.item_count == 0
        assert cart.total == Decimal("0.00")

    async def test_unknown_cart_item_is_not_found(self, session):
        from app.utils.exceptions import NotFoundError

        with pytest.raises(NotFoundError):
            await CartService(session).remove_from_cart(999999)


class TestCheckoutService:
    async def test_create_checkout_session_from_the_cart(self, session, sample_user, sample_product):
        cart = await CartService(session).get_or_create_cart(sample_user.id)
        await CartService(session).add_to_cart(cart.id, sample_product.id, 1)
        checkout = await CheckoutService(session).create_checkout_session(sample_user.id, cart.id, dict(SHIPPING))
        assert checkout.checkout_token is not None
        assert checkout.user_id == sample_user.id
        assert checkout.total > checkout.subtotal

    async def test_empty_cart_cannot_check_out(self, session, sample_user):
        cart = await CartService(session).get_or_create_cart(sample_user.id)
        with pytest.raises(ValueError, match="empty"):
            await CheckoutService(session).create_checkout_session(sample_user.id, cart.id, dict(SHIPPING))

    async def test_get_checkout_session(self, session, sample_checkout):
        assert (await CheckoutService(session).get_checkout_session(sample_checkout.id)).id == sample_checkout.id

    async def test_apply_coupon(self, session, sample_checkout):
        await CheckoutService(session).apply_coupon(sample_checkout.id, "DISCOUNT10")
        await session.refresh(sample_checkout)
        assert sample_checkout.coupon_code == "DISCOUNT10"
        assert sample_checkout.discount > Decimal("0.00")


class TestPaymentService:
    async def test_create_payment(self, session, sample_checkout):
        payment = await PaymentService(session).create_payment(sample_checkout.id, {
            "payment_method": "stripe", "amount": sample_checkout.total, "currency": "USD",
        })
        assert payment.checkout_id == sample_checkout.id
        assert payment.amount == sample_checkout.total

    async def test_only_a_completed_payment_counts_as_paid(self, session, sample_checkout):
        service = PaymentService(session)
        failed = await service.create_payment(sample_checkout.id, {"payment_method": "stripe", "amount": Decimal("1")})
        failed.status = "failed"
        await session.commit()
        assert await service.completed_payment_for(sample_checkout.id) is None


class TestOrderService:
    async def test_create_order_copies_the_checkout_and_clears_the_cart(
        self, session, sample_user, sample_checkout, sample_payment,
    ):
        order = await OrderService(session).create_order(sample_user.id, sample_checkout, sample_payment)
        assert order.order_number.startswith("ORD-")
        assert order.total == sample_checkout.total

    async def test_get_order_includes_its_items(self, session, sample_order):
        order = await OrderService(session).get_order(sample_order.id)
        assert order.id == sample_order.id
        assert order.items == []

    async def test_get_user_orders(self, session, sample_user, sample_order):
        orders = await OrderService(session).get_user_orders(sample_user.id)
        assert any(o.id == sample_order.id for o in orders)

    async def test_update_order_status(self, session, sample_order):
        service = OrderService(session)
        await service.update_order_status(sample_order.id, OrderStatus.SHIPPED)
        await session.refresh(sample_order)
        assert sample_order.order_status == OrderStatus.SHIPPED

    async def test_cancel_order(self, session, sample_order):
        await OrderService(session).cancel_order(sample_order.id)
        await session.refresh(sample_order)
        assert sample_order.order_status == OrderStatus.CANCELLED

    async def test_missing_order_is_not_found(self, session):
        from app.utils.exceptions import NotFoundError

        with pytest.raises(NotFoundError):
            await OrderService(session).cancel_order(999999)
