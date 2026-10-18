"""Route tests for the AI usage trend: one point per day, oldest first, empty days as zero"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.ai_advanced import MonitoringMetric, UsageMetric


def _record(session: Session, user_id: int, value: float, days_ago: int) -> None:
    session.add(
        UsageMetric(
            user_id=user_id,
            metric_type=MonitoringMetric.TOKENS,
            value=value,
            created_at=datetime.now(timezone.utc) - timedelta(days=days_ago),
        )
    )


class TestDailyUsage:
    async def test_each_day_shows_its_recorded_total_with_empty_days_as_zero(self, async_client, org_member, reference_data, reset_test_database):
        with Session(reset_test_database) as session:
            _record(session, 1, 120, days_ago=0)
            _record(session, 1, 30, days_ago=0)
            _record(session, 1, 50, days_ago=2)
            session.commit()

        response = await async_client.get("/api/v1/ai/metrics/usage/daily?days=3", headers=org_member)

        assert response.status_code == 200
        points = response.json()
        assert len(points) == 3
        # Oldest first: two days ago (50), yesterday (no usage, so zero), today (120 + 30).
        assert [point["total"] for point in points] == [50.0, 0.0, 150.0]
        assert points[0]["date"] < points[-1]["date"]
        assert points[-1]["date"] == datetime.now(timezone.utc).date().isoformat()

    async def test_only_the_callers_usage_is_counted(self, async_client, org_member, reference_data, reset_test_database):
        with Session(reset_test_database) as session:
            _record(session, 2, 999, days_ago=0)
            session.commit()

        response = await async_client.get("/api/v1/ai/metrics/usage/daily?days=1", headers=org_member)

        assert response.json()[0]["total"] == 0.0

    async def test_the_window_is_limited_to_ninety_days(self, async_client, org_member):
        response = await async_client.get("/api/v1/ai/metrics/usage/daily?days=91", headers=org_member)

        assert response.status_code == 422
