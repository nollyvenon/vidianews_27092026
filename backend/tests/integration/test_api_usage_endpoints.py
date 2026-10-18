"""Route tests: real requests are counted per endpoint and reported by the usage endpoint"""

import pytest

from app.main import api_usage_recorder


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


async def test_a_request_is_counted_under_its_route_and_reported_by_the_usage_endpoint(async_client, org_member):
    await async_client.get("/api/v1/content/categories", headers=org_member)
    await async_client.get("/api/v1/content/categories", headers=org_member)
    written = await api_usage_recorder.flush()

    assert written >= 2
    usage = (await async_client.get("/api/v1/api-docs/usage", headers=org_member)).json()
    row = next(item for item in usage if item["endpoint"] == "/api/v1/content/categories" and item["method"] == "GET")
    assert row["call_count"] >= 2
    assert row["average_response_time_ms"] >= 0


async def test_a_client_error_is_a_call_but_not_a_server_error(async_client, org_member):
    before = await async_client.get("/api/v1/api-docs/usage", headers=org_member)
    prior = next((item for item in before.json() if item["endpoint"] == "/api/v1/content/{content_id}" and item["method"] == "GET"), None)
    missing = await async_client.get("/api/v1/content/987654", headers=org_member)
    assert missing.status_code == 404
    await api_usage_recorder.flush()

    usage = (await async_client.get("/api/v1/api-docs/usage", headers=org_member)).json()
    row = next(item for item in usage if item["endpoint"] == "/api/v1/content/{content_id}" and item["method"] == "GET")
    assert row["call_count"] == (prior["call_count"] if prior else 0) + 1
    assert row["error_count"] == (prior["error_count"] if prior else 0)


async def test_quota_reports_the_recorded_calls_bandwidth_and_stored_media(async_client, org_member, reset_test_database):
    from sqlalchemy.orm import Session

    from app.models.content import MediaFile

    with Session(reset_test_database) as session:
        session.add(MediaFile(
            content_id=1,
            file_name="clip.mp4",
            file_type="video",
            mime_type="video/mp4",
            file_size=1024 ** 3,
            file_url="https://media.example.test/clip.mp4",
        ))
        session.commit()

    await async_client.get("/api/v1/content/categories", headers=org_member)
    await async_client.get("/api/v1/content/categories", headers=org_member)
    await api_usage_recorder.flush()

    quota = (await async_client.get("/api/v1/quota/usage", headers=org_member)).json()
    assert quota["api_calls"] >= 2
    assert quota["storage_gb"] == 1.0
    assert quota["bandwidth_gb"] > 0
