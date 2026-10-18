"""Route tests for the platform cache: hits and misses are recorded, expired entries are not served, and the
metrics come from what was actually recorded"""

from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.models.advanced_platform import CacheEntry


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


async def test_a_stored_value_is_a_hit_and_an_unknown_key_is_a_miss(async_client, org_member):
    stored = await async_client.post(
        "/api/v1/cache/set", json={"cache_key": "home", "cache_value": {"title": "Front page"}}, headers=org_member,
    )
    assert stored.status_code == 200

    hit = await async_client.get("/api/v1/cache/get/home", headers=org_member)
    miss = await async_client.get("/api/v1/cache/get/unknown-key", headers=org_member)

    assert hit.json() == {"title": "Front page"}
    assert miss.json() is None


async def test_the_metrics_report_the_recorded_hits_and_misses(async_client, org_member):
    await async_client.post(
        "/api/v1/cache/set", json={"cache_key": "a", "cache_value": {"n": 1}}, headers=org_member,
    )
    await async_client.get("/api/v1/cache/get/a", headers=org_member)
    await async_client.get("/api/v1/cache/get/a", headers=org_member)
    await async_client.get("/api/v1/cache/get/missing", headers=org_member)

    metrics = (await async_client.get("/api/v1/cache-metrics", headers=org_member)).json()

    assert metrics["total_requests"] == 3
    assert metrics["total_hits"] == 2
    assert metrics["total_misses"] == 1
    assert metrics["average_response_time_ms"] >= 0
    assert metrics["memory_usage_mb"] > 0


async def test_repeated_metric_reads_do_not_invent_accesses(async_client, org_member):
    await async_client.get("/api/v1/cache/get/nothing", headers=org_member)

    first = (await async_client.get("/api/v1/cache-metrics", headers=org_member)).json()
    second = (await async_client.get("/api/v1/cache-metrics", headers=org_member)).json()

    assert first["total_requests"] == second["total_requests"] == 1
    assert first["total_misses"] == second["total_misses"] == 1


async def test_an_expired_entry_is_removed_and_counted_as_a_miss(async_client, org_member, reset_test_database):
    await async_client.post(
        "/api/v1/cache/set", json={"cache_key": "stale", "cache_value": {"x": 1}, "ttl_seconds": 60}, headers=org_member,
    )
    with Session(reset_test_database) as session:
        entry = session.query(CacheEntry).filter(CacheEntry.cache_key == "stale").one()
        entry.expires_at = datetime.utcnow() - timedelta(seconds=5)
        session.commit()

    response = await async_client.get("/api/v1/cache/get/stale", headers=org_member)

    assert response.json() is None
    with Session(reset_test_database) as session:
        assert session.query(CacheEntry).filter(CacheEntry.cache_key == "stale").first() is None


async def test_the_cache_metrics_require_a_signed_in_user(async_client):
    assert (await async_client.get("/api/v1/cache-metrics")).status_code in (401, 403)
