"""Tests for advanced features (Modules 26-30)"""

import pytest
from app.models.content import Video
from app.models.advanced_features import PermissionLevel, ReactionType
from app.services.advanced_features_service import (
    PermissionService,
    StorageService,
    VideoProcessingService,
    CollaborationService,
    RecommendationService,
)
from app.utils.exceptions import NotFoundError


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


@pytest.fixture
async def test_db(session):
    """The per-test async session shared with the seeded reference data."""
    yield session


@pytest.fixture
async def video(test_db):
    """A video attached to seeded content 1; the processing and comment tests use it."""
    row = Video(content_id=1, source_url="https://cdn.example.com/video.mp4")
    test_db.add(row)
    await test_db.commit()
    await test_db.refresh(row)
    return row


# Module 26: Permissions
@pytest.mark.asyncio
async def test_grant_permission(test_db):
    service = PermissionService(test_db)
    perm = await service.grant_permission("content", 1, 1, "edit")
    assert perm.permission == "edit"


@pytest.mark.asyncio
async def test_grant_permission_replaces_existing_level(test_db):
    service = PermissionService(test_db)
    await service.grant_permission("content", 1, 2, PermissionLevel.READ)
    updated = await service.grant_permission("content", 1, 2, PermissionLevel.ADMIN)
    assert updated.permission == PermissionLevel.ADMIN.value
    assert await service.get_permission("content", 1, 2) == PermissionLevel.ADMIN


@pytest.mark.asyncio
async def test_get_permission_defaults_to_none(test_db):
    service = PermissionService(test_db)
    assert await service.get_permission("content", 1, 2) == PermissionLevel.NONE


@pytest.mark.asyncio
async def test_grant_permission_rejects_unknown_level(test_db):
    service = PermissionService(test_db)
    with pytest.raises(ValueError):
        await service.grant_permission("content", 1, 1, "superuser")


@pytest.mark.asyncio
async def test_create_share_link(test_db):
    service = PermissionService(test_db)
    link = await service.create_share_link("content", 1, 1, "abc123token", "read")
    assert link.token == "abc123token"


@pytest.mark.asyncio
async def test_share_link_lookup_and_duplicate_token(test_db):
    service = PermissionService(test_db)
    await service.create_share_link("content", 1, 1, "dup-token", "read")
    found = await service.get_share_link("dup-token")
    assert found is not None
    assert found.resource_id == 1
    with pytest.raises(ValueError):
        await service.create_share_link("content", 1, 1, "dup-token", "read")


# Module 27: Storage
@pytest.mark.asyncio
async def test_upload_file(test_db):
    service = StorageService(test_db)
    file = await service.upload_file(1, 1, "video.mp4", "s3://key", 1000000, "video/mp4")
    assert file.filename == "video.mp4"
    assert file.size_bytes == 1000000


@pytest.mark.asyncio
async def test_get_file(test_db):
    service = StorageService(test_db)
    uploaded = await service.upload_file(1, 1, "file.txt", "key", 100, "text/plain")
    retrieved = await service.get_file(uploaded.id)
    assert retrieved.filename == "file.txt"


@pytest.mark.asyncio
async def test_delete_file_hides_it_from_lookup(test_db):
    service = StorageService(test_db)
    uploaded = await service.upload_file(1, 1, "gone.txt", "key", 10, "text/plain")
    assert await service.delete_file(uploaded.id) is True
    assert await service.get_file(uploaded.id) is None
    assert await service.delete_file(uploaded.id) is False


@pytest.mark.asyncio
async def test_upload_file_rejects_negative_size(test_db):
    service = StorageService(test_db)
    with pytest.raises(ValueError):
        await service.upload_file(1, 1, "bad.txt", "key", -1, "text/plain")


# Module 28: Video Processing
@pytest.mark.asyncio
async def test_start_processing(test_db, video):
    service = VideoProcessingService(test_db)
    process = await service.start_processing(video.id, "1080p")
    assert process.quality == "1080p"
    assert process.status == "pending"


@pytest.mark.asyncio
async def test_update_processing_status_stamps_times(test_db, video):
    service = VideoProcessingService(test_db)
    job = await service.start_processing(video.id, "720p")
    running = await service.update_processing_status(job.id, "processing")
    assert running.started_at is not None
    done = await service.update_processing_status(job.id, "completed", output_url="https://cdn.example.com/720p.mp4")
    assert done.completed_at is not None
    assert done.output_url == "https://cdn.example.com/720p.mp4"


@pytest.mark.asyncio
async def test_start_processing_requires_existing_video(test_db):
    service = VideoProcessingService(test_db)
    with pytest.raises(NotFoundError):
        await service.start_processing(999999, "720p")


@pytest.mark.asyncio
async def test_add_thumbnail(test_db, video):
    service = VideoProcessingService(test_db)
    thumb = await service.add_thumbnail(video.id, "https://cdn.example.com/thumb.jpg")
    assert thumb.is_default == False


@pytest.mark.asyncio
async def test_add_default_thumbnail_clears_previous_default(test_db, video):
    service = VideoProcessingService(test_db)
    first = await service.add_thumbnail(video.id, "https://cdn.example.com/a.jpg", make_default=True)
    second = await service.add_thumbnail(video.id, "https://cdn.example.com/b.jpg", make_default=True)
    await test_db.refresh(first)
    assert first.is_default is False
    assert second.is_default is True


# Module 29: Collaboration
@pytest.mark.asyncio
async def test_add_comment(test_db, video):
    service = CollaborationService(test_db)
    comment = await service.add_comment("video", video.id, 1, "Great video!")
    assert comment.body == "Great video!"
    assert comment.content_id == 1


@pytest.mark.asyncio
async def test_add_comment_rejects_empty_body(test_db, video):
    service = CollaborationService(test_db)
    with pytest.raises(ValueError):
        await service.add_comment("video", video.id, 1, "   ")


@pytest.mark.asyncio
async def test_add_reaction(test_db, video):
    service = CollaborationService(test_db)
    comment = await service.add_comment("video", video.id, 1, "Nice")
    reaction = await service.add_reaction(comment.id, 2, "like")
    assert reaction.reaction_type == "like"


@pytest.mark.asyncio
async def test_add_reaction_replaces_previous_reaction(test_db, video):
    service = CollaborationService(test_db)
    comment = await service.add_comment("video", video.id, 1, "Nice")
    await service.add_reaction(comment.id, 2, ReactionType.LIKE)
    updated = await service.add_reaction(comment.id, 2, ReactionType.LOVE)
    assert updated.reaction_type == ReactionType.LOVE


# Module 30: Recommendations
@pytest.mark.asyncio
async def test_add_recommendation(test_db):
    service = RecommendationService(test_db)
    rec = await service.add_recommendation(1, 100, 0.95, "Similar content", "collaborative")
    assert rec.score == 0.95
    assert rec.reason == "Similar content"


@pytest.mark.asyncio
async def test_record_click(test_db):
    service = RecommendationService(test_db)
    rec = await service.add_recommendation(1, 100, 0.8, "Trending", "trending")
    success = await service.record_recommendation_click(rec.id)
    assert success
    await test_db.refresh(rec)
    assert rec.clicked is True
