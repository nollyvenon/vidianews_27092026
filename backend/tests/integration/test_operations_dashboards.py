"""Route tests for the operations dashboards: video processing, the live feed, and test suite results"""

from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.models.advanced_features import ProcessingStatus, VideoProcess, VideoQualityLevel
from app.models.advanced_platform import WebSocketConnection, WebSocketConnectionStatus
from app.models.api_monitoring import TestSuite
from app.models.content import Content, ContentType, Video


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


def _utc_now() -> datetime:
    return datetime.utcnow()


def _add_video(session: Session, *, content_id: int, creator_id: int, title: str, encoding_status: str) -> Video:
    if session.get(Content, content_id) is None:
        session.add(Content(
            id=content_id,
            title=title,
            slug=f"video-{content_id}",
            content_type=ContentType.VIDEO,
            creator_user_id=creator_id,
        ))
        session.flush()
    video = Video(content_id=content_id, source_url=f"https://media.example.test/{content_id}.mp4", encoding_status=encoding_status)
    session.add(video)
    session.flush()
    return video


class TestVideoProcessing:
    async def test_a_creators_videos_show_status_and_transcoding_progress(self, async_client, org_member, reset_test_database):
        qualities = list(VideoQualityLevel)
        with Session(reset_test_database) as session:
            video = _add_video(session, content_id=1, creator_id=1, title="Seed Content", encoding_status="in_progress")
            session.add_all([
                VideoProcess(video_id=video.id, quality=qualities[0], status=ProcessingStatus.COMPLETED),
                VideoProcess(video_id=video.id, quality=qualities[1], status=ProcessingStatus.PENDING),
            ])
            session.commit()

        response = await async_client.get("/api/v1/content/videos/processing", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert len(rows) == 1
        assert rows[0]["title"] == "Seed Content"
        assert rows[0]["status"] == "in_progress"
        assert rows[0]["progress"] == 50
        assert [item["status"] for item in rows[0]["qualities"]] == ["completed", "pending"]

    async def test_a_video_with_no_transcodes_yet_reports_its_encoding_status(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            _add_video(session, content_id=1, creator_id=1, title="Seed Content", encoding_status="completed")
            session.commit()

        rows = (await async_client.get("/api/v1/content/videos/processing", headers=org_member)).json()

        assert rows[0]["progress"] == 100
        assert rows[0]["qualities"] == []

    async def test_other_creators_videos_are_not_listed(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            _add_video(session, content_id=2, creator_id=2, title="Someone Else", encoding_status="pending")
            session.commit()

        rows = (await async_client.get("/api/v1/content/videos/processing", headers=org_member)).json()

        assert rows == []

    async def test_video_processing_requires_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/content/videos/processing")

        assert response.status_code in (401, 403)


class TestLiveFeed:
    async def test_a_broadcast_appears_in_the_feed_newest_first(self, async_client, platform_admin):
        first = await async_client.post(
            "/api/v1/websocket/broadcast",
            json={"event_type": "message", "event_source": "live-feed", "user_ids": [], "payload": {"message": "First"}},
            headers=platform_admin,
        )
        second = await async_client.post(
            "/api/v1/websocket/broadcast",
            json={"event_type": "message", "event_source": "live-feed", "user_ids": [], "payload": {"message": "Second"}},
            headers=platform_admin,
        )
        assert first.status_code == 200 and second.status_code == 200

        feed = await async_client.get("/api/v1/websocket/events?limit=10", headers=platform_admin)

        assert feed.status_code == 200
        assert [event["payload"]["message"] for event in feed.json()] == ["Second", "First"]
        assert feed.json()[0]["event_source"] == "live-feed"

    async def test_the_feed_limit_is_enforced(self, async_client, platform_admin):
        for index in range(3):
            await async_client.post(
                "/api/v1/websocket/broadcast",
                json={"event_type": "message", "event_source": "live-feed", "user_ids": [], "payload": {"message": str(index)}},
                headers=platform_admin,
            )

        feed = await async_client.get("/api/v1/websocket/events?limit=2", headers=platform_admin)

        assert len(feed.json()) == 2

    async def test_presence_counts_connected_sockets_and_the_idle_ones(self, async_client, org_member, reset_test_database):
        now = _utc_now()
        with Session(reset_test_database) as session:
            session.add_all([
                WebSocketConnection(user_id=1, connection_id="fresh", status=WebSocketConnectionStatus.CONNECTED,
                                    last_heartbeat=now),
                WebSocketConnection(user_id=2, connection_id="stale", status=WebSocketConnectionStatus.CONNECTED,
                                    last_heartbeat=now - timedelta(minutes=30)),
                WebSocketConnection(user_id=2, connection_id="gone", status=WebSocketConnectionStatus.DISCONNECTED,
                                    last_heartbeat=now),
            ])
            session.commit()

        response = await async_client.get("/api/v1/websocket/presence", headers=org_member)

        assert response.status_code == 200
        assert response.json() == {"online": 2, "idle": 1}

    async def test_the_live_feed_requires_a_signed_in_user(self, async_client):
        assert (await async_client.get("/api/v1/websocket/events")).status_code in (401, 403)
        assert (await async_client.get("/api/v1/websocket/presence")).status_code in (401, 403)


class TestTestSuites:
    async def test_suites_report_their_recorded_results_ordered_by_name(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            session.add_all([
                TestSuite(name="E2E Tests", test_count=42, passed=41, failed=1, skipped=0, coverage_percentage=92.14),
                TestSuite(name="Unit Tests", test_count=250, passed=245, failed=5, skipped=0, coverage_percentage=94.5),
            ])
            session.commit()

        response = await async_client.get("/api/v1/testing/suites", headers=org_member)

        assert response.status_code == 200
        rows = response.json()
        assert [row["name"] for row in rows] == ["E2E Tests", "Unit Tests"]
        assert rows[0]["coverage_percentage"] == 92.1
        assert rows[1]["passed"] == 245
        assert rows[1]["failed"] == 5
        assert rows[1]["last_run_at"] is None

    async def test_the_suite_list_requires_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/testing/suites")

        assert response.status_code in (401, 403)
