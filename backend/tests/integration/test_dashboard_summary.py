"""Route tests for the dashboard home totals: each user sees their own content, chats and this month's payments."""

from datetime import datetime, timedelta, timezone

from app.core.security import create_access_token
from app.models.ai_advanced import Chat
from app.models.content import Content, ContentStatus, ContentType
from app.models.monetization import Invoice, Payment, PaymentStatus, Subscription
from app.models.user import User


async def _headers_for(session, user_id: int) -> dict:
    user = await session.get(User, user_id)
    return {"Authorization": f"Bearer {create_access_token({'sub': user.email, 'user_id': user.id})}"}


def _content(slug: str, creator: int, content_type: ContentType) -> Content:
    return Content(
        title=slug.title(), slug=slug, content_type=content_type, status=ContentStatus.PUBLISHED,
        creator_user_id=creator,
    )


async def _payment(session, user_id: int, amount: str, status: PaymentStatus, when: datetime) -> None:
    subscription = Subscription(user_id=user_id, organization_id=1, amount=0.0)
    session.add(subscription)
    await session.flush()
    invoice = Invoice(subscription_id=subscription.id, amount=float(amount), status=status)
    session.add(invoice)
    await session.flush()
    session.add(Payment(
        user_id=user_id, invoice_id=invoice.id, amount=float(amount), status=status, created_at=when,
    ))
    await session.commit()


class TestDashboardSummary:
    async def test_anonymous_requests_are_rejected(self, async_client, reference_data):
        assert (await async_client.get("/api/v1/dashboard/summary")).status_code == 401

    async def test_a_new_user_sees_zeros(self, async_client, reference_data, session):
        response = await async_client.get("/api/v1/dashboard/summary", headers=await _headers_for(session, 2))
        assert response.status_code == 200
        assert response.json() == {"videos": 0, "articles": 0, "chats": 0, "monthly_spend": 0.0}

    async def test_totals_count_only_the_callers_own_records(self, async_client, reference_data, session):
        session.add_all([
            _content("first-video", 2, ContentType.VIDEO),
            _content("second-video", 2, ContentType.VIDEO),
            _content("an-article", 2, ContentType.ARTICLE),
            _content("someone-elses-video", 1, ContentType.VIDEO),
            Chat(user_id=2, title="Plan"),
            Chat(user_id=2, title="Ideas"),
            Chat(user_id=1, title="Not mine"),
        ])
        await session.commit()

        mine = await async_client.get("/api/v1/dashboard/summary", headers=await _headers_for(session, 2))
        assert mine.json()["videos"] == 2
        assert mine.json()["articles"] == 1
        assert mine.json()["chats"] == 2

    async def test_spend_counts_completed_payments_from_this_month(self, async_client, reference_data, session):
        now = datetime.now(timezone.utc)
        await _payment(session, 2, "10.00", PaymentStatus.COMPLETED, now)
        await _payment(session, 2, "5.50", PaymentStatus.COMPLETED, now)
        await _payment(session, 2, "99.00", PaymentStatus.PENDING, now)
        await _payment(session, 2, "42.00", PaymentStatus.COMPLETED, now - timedelta(days=62))

        response = await async_client.get("/api/v1/dashboard/summary", headers=await _headers_for(session, 2))

        assert response.json()["monthly_spend"] == 15.5
