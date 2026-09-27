"""Tests for advanced features (Modules 26-30)"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.base import Base
from app.models.advanced_features import *
from app.services.advanced_features_service import *


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


# Module 26: Permissions
@pytest.mark.asyncio
async def test_grant_permission(test_db):
    service = PermissionService(test_db)
    perm = await service.grant_permission("content", 1, 1, "edit")
    assert perm.permission_level == "edit"

@pytest.mark.asyncio
async def test_create_share_link(test_db):
    service = PermissionService(test_db)
    link = await service.create_share_link("content", 1, 1, "abc123token", "view")
    assert link.token == "abc123token"

# Module 27: Storage
@pytest.mark.asyncio
async def test_upload_file(test_db):
    service = StorageService(test_db)
    file = await service.upload_file(1, 1, "video.mp4", "s3://key", 1000000, "video/mp4")
    assert file.filename == "video.mp4"
    assert file.file_size == 1000000

@pytest.mark.asyncio
async def test_get_file(test_db):
    service = StorageService(test_db)
    uploaded = await service.upload_file(1, 1, "file.txt", "key", 100, "text/plain")
    retrieved = await service.get_file(uploaded.id)
    assert retrieved.filename == "file.txt"

# Module 28: Video Processing
@pytest.mark.asyncio
async def test_start_processing(test_db):
    service = VideoProcessingService(test_db)
    process = await service.start_processing(1, "full_hd")
    assert process.quality_level == "full_hd"

@pytest.mark.asyncio
async def test_add_thumbnail(test_db):
    service = VideoProcessingService(test_db)
    thumb = await service.add_thumbnail(1, "thumb_key", "https://cdn.example.com/thumb.jpg")
    assert thumb.is_primary == False

# Module 29: Collaboration
@pytest.mark.asyncio
async def test_add_comment(test_db):
    service = CollaborationService(test_db)
    comment = await service.add_comment("video", 1, 1, "Great video!")
    assert comment.content == "Great video!"

@pytest.mark.asyncio
async def test_add_reaction(test_db):
    service = CollaborationService(test_db)
    comment = await service.add_comment("video", 1, 1, "Nice")
    reaction = await service.add_reaction(comment.id, 2, "like")
    assert reaction.reaction_type == "like"

# Module 30: Recommendations
@pytest.mark.asyncio
async def test_add_recommendation(test_db):
    service = RecommendationService(test_db)
    rec = await service.add_recommendation(1, 100, 0.95, "Similar content", "collaborative_filtering")
    assert rec.score == 0.95

@pytest.mark.asyncio
async def test_record_click(test_db):
    service = RecommendationService(test_db)
    rec = await service.add_recommendation(1, 100, 0.8, "Trending", "trending")
    success = await service.record_recommendation_click(rec.id)
    assert success
