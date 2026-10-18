"""Route tests: each read of a content item counts one page view for the day"""

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analytics_reporting import PageViewMetrics


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


async def test_each_read_of_a_content_item_counts_a_page_view_for_today(async_client, org_member, reset_test_database):
    first = await async_client.get("/api/v1/content/1", headers=org_member)
    second = await async_client.get("/api/v1/content/1", headers=org_member)
    assert first.status_code == 200 and second.status_code == 200

    today = datetime.now(timezone.utc).replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
    with Session(reset_test_database) as session:
        rows = session.execute(
            select(PageViewMetrics).where(PageViewMetrics.content_id == 1, PageViewMetrics.date == today)
        ).scalars().all()
    assert len(rows) == 1
    assert rows[0].page_views == 2


async def test_a_missing_content_item_counts_no_page_view(async_client, org_member, reset_test_database):
    missing = await async_client.get("/api/v1/content/987654", headers=org_member)

    assert missing.status_code == 404
    with Session(reset_test_database) as session:
        assert session.execute(select(PageViewMetrics).where(PageViewMetrics.content_id == 987654)).first() is None
