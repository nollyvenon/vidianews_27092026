"""Route tests for the advanced platform dashboard: pipelines, API usage, the cache summary, pending jobs and system health"""

from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.models.advanced_platform import APIUsageMetrics, BackgroundJob, CacheEntry, DataPipeline, JobStatus


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


class TestPipelines:
    async def test_pipelines_are_listed_most_recently_run_first_with_their_failures(self, async_client, org_member, reset_test_database):
        now = datetime.utcnow()
        with Session(reset_test_database) as session:
            session.add_all([
                DataPipeline(name="Never Run", source_type="events", destination_type="analytics", status="draft",
                             is_active=False, failure_count=3),
                DataPipeline(name="User Sync", source_type="database", destination_type="warehouse", status="active",
                             is_active=True, failure_count=0, last_run=now - timedelta(hours=2), last_success=now - timedelta(hours=2)),
                DataPipeline(name="Event Pipeline", source_type="events", destination_type="lake", status="active",
                             is_active=True, failure_count=1, last_run=now - timedelta(hours=1)),
            ])
            session.commit()

        response = await async_client.get("/api/v1/pipelines/", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert [row["name"] for row in rows] == ["Event Pipeline", "User Sync", "Never Run"]
        assert rows[0]["failure_count"] == 1
        assert rows[2]["last_run"] is None
        assert rows[1]["is_active"] is True

    async def test_pipelines_require_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/pipelines/")

        assert response.status_code in (401, 403)


class TestApiUsage:
    async def test_measured_endpoints_are_listed_busiest_first(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            session.add_all([
                APIUsageMetrics(endpoint="/content", method="GET", call_count=54321, error_count=12, average_response_time_ms=18.0),
                APIUsageMetrics(endpoint="/users", method="GET", call_count=12345, error_count=23, average_response_time_ms=41.456),
            ])
            session.commit()

        response = await async_client.get("/api/v1/api-docs/usage", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert [(row["endpoint"], row["call_count"]) for row in rows] == [("/content", 54321), ("/users", 12345)]
        assert rows[1]["average_response_time_ms"] == 41.46
        assert rows[1]["error_count"] == 23

    async def test_usage_list_is_not_mistaken_for_a_document_id(self, async_client, org_member):
        response = await async_client.get("/api/v1/api-docs/usage", headers=org_member)

        assert response.status_code == 200
        assert response.json() == []


class TestCacheSummary:
    async def test_the_summary_counts_entries_hits_and_memory(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            session.add_all([
                CacheEntry(cache_key="home", cache_value={"a": 1}, hit_count=10, size_bytes=1024 * 1024),
                CacheEntry(cache_key="feed", cache_value={"b": 2}, hit_count=5, size_bytes=512 * 1024),
            ])
            session.commit()

        response = await async_client.get("/api/v1/cache-summary", headers=org_member)

        assert response.status_code == 200
        assert response.json() == {"entries": 2, "total_hits": 15, "memory_usage_mb": 1.5}

    async def test_the_summary_of_an_empty_cache_is_zero(self, async_client, org_member):
        response = await async_client.get("/api/v1/cache-summary", headers=org_member)

        assert response.json() == {"entries": 0, "total_hits": 0, "memory_usage_mb": 0.0}


class TestPendingJobs:
    async def test_pending_jobs_are_listed_with_their_priority(self, async_client, platform_admin, reset_test_database):
        with Session(reset_test_database) as session:
            session.add_all([
                BackgroundJob(job_type="email_notification", status=JobStatus.PENDING, priority=2, payload={}),
                BackgroundJob(job_type="data_export", status=JobStatus.RUNNING, priority=1, payload={}),
            ])
            session.commit()

        response = await async_client.get("/api/v1/jobs/pending", headers=platform_admin)

        assert response.status_code == 200
        types = [row["job_type"] for row in response.json()]
        assert "email_notification" in types


class TestSystemHealth:
    async def test_health_reports_the_database_and_the_job_queue(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            session.add(BackgroundJob(job_type="failing", status=JobStatus.FAILED, priority=0, payload={}))
            session.commit()

        response = await async_client.get("/api/v1/system/health/checks", headers=org_member)

        assert response.status_code == 200
        body = response.json()
        checks = {check["name"]: check for check in body["checks"]}
        assert checks["Database"]["status"] == "healthy"
        assert checks["Background jobs"]["status"] == "degraded"
        assert checks["Background jobs"]["failed"] == 1
        assert body["metrics"]["cpu_percent"] >= 0
        assert body["metrics"]["database_latency_ms"] >= 0
