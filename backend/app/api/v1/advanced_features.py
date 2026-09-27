"""APIs for Modules 26-30"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.advanced_features_service import *
from pydantic import BaseModel

router = APIRouter(prefix="/resources", tags=["advanced"])

# ==================== MODULE 26: PERMISSIONS ====================

class PermissionGrant(BaseModel):
    resource_type: str
    resource_id: int
    user_id: int
    permission_level: str

@router.post("/permissions", status_code=status.HTTP_201_CREATED)
async def grant_permission(req: PermissionGrant, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Grant resource permission"""
    service = PermissionService(session)
    return await service.grant_permission(req.resource_type, req.resource_id, req.user_id, req.permission_level)

@router.get("/permissions/{resource_type}/{resource_id}")
async def check_permission(resource_type: str, resource_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Check permission"""
    service = PermissionService(session)
    perm = await service.get_permission(resource_type, resource_id, current_user.id)
    return {"has_access": perm is not None, "level": perm.permission_level if perm else None}

class ShareLinkCreate(BaseModel):
    resource_type: str
    resource_id: int
    permission_level: str = "view"

@router.post("/share-links", status_code=status.HTTP_201_CREATED)
async def create_share_link(req: ShareLinkCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create share link"""
    import secrets
    service = PermissionService(session)
    token = secrets.token_urlsafe(32)
    return await service.create_share_link(req.resource_type, req.resource_id, current_user.id, token, req.permission_level)

@router.get("/share-links/{token}")
async def get_share_link(token: str, session: AsyncSession = Depends(get_db)):
    """Get share link"""
    service = PermissionService(session)
    link = await service.get_share_link(token)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return link

# ==================== MODULE 27: FILE STORAGE ====================

@router.post("/files/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Upload file"""
    service = StorageService(session)
    file_key = f"{current_user.id}/{file.filename}"
    content = await file.read()
    return await service.upload_file(current_user.id, current_user.organization_id, file.filename, file_key, len(content), file.content_type)

@router.get("/files/{file_id}")
async def get_file(file_id: int, session: AsyncSession = Depends(get_db)):
    """Get file"""
    service = StorageService(session)
    file = await service.get_file(file_id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return file

@router.get("/files")
async def list_files(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List files"""
    service = StorageService(session)
    return await service.list_files(current_user.id)

@router.delete("/files/{file_id}")
async def delete_file(file_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Delete file"""
    service = StorageService(session)
    success = await service.delete_file(file_id)
    return {"deleted": success}

# ==================== MODULE 28: VIDEO PROCESSING ====================

class ProcessStart(BaseModel):
    video_id: int
    quality_level: str

@router.post("/videos/process", status_code=status.HTTP_201_CREATED)
async def start_processing(req: ProcessStart, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Start video processing"""
    service = VideoProcessingService(session)
    return await service.start_processing(req.video_id, req.quality_level)

@router.get("/videos/{video_id}/processes")
async def get_processes(video_id: int, session: AsyncSession = Depends(get_db)):
    """Get video processes"""
    service = VideoProcessingService(session)
    return await service.get_processes(video_id)

@router.post("/videos/{video_id}/thumbnails", status_code=status.HTTP_201_CREATED)
async def add_thumbnail(video_id: int, file_key: str, url: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add thumbnail"""
    service = VideoProcessingService(session)
    return await service.add_thumbnail(video_id, file_key, url)

# ==================== MODULE 29: COLLABORATION ====================

class CommentCreate(BaseModel):
    resource_type: str
    resource_id: int
    content: str

@router.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(req: CommentCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create comment"""
    service = CollaborationService(session)
    return await service.add_comment(req.resource_type, req.resource_id, current_user.id, req.content)

@router.get("/comments/{resource_type}/{resource_id}")
async def get_comments(resource_type: str, resource_id: int, session: AsyncSession = Depends(get_db)):
    """Get comments"""
    service = CollaborationService(session)
    return await service.get_comments(resource_type, resource_id)

class ReactionCreate(BaseModel):
    comment_id: int
    reaction_type: str

@router.post("/reactions", status_code=status.HTTP_201_CREATED)
async def add_reaction(req: ReactionCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add reaction"""
    service = CollaborationService(session)
    return await service.add_reaction(req.comment_id, current_user.id, req.reaction_type)

@router.get("/comments/{comment_id}/reactions")
async def get_reactions(comment_id: int, session: AsyncSession = Depends(get_db)):
    """Get reactions"""
    service = CollaborationService(session)
    return await service.get_reactions(comment_id)

# ==================== MODULE 30: RECOMMENDATIONS ====================

@router.get("/recommendations")
async def get_recommendations(limit: int = 10, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get recommendations"""
    service = RecommendationService(session)
    return await service.get_recommendations(current_user.id, limit)

@router.get("/recommendations/profile")
async def get_profile(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get personalization profile"""
    service = RecommendationService(session)
    profile = await service.get_personalization_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return profile

@router.get("/preferences")
async def get_preferences(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get user preferences"""
    service = RecommendationService(session)
    prefs = await service.get_user_preferences(current_user.id)
    if not prefs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return prefs

class PreferenceUpdate(BaseModel):
    preferred_categories: Optional[List[str]] = None
    preferred_creators: Optional[List[int]] = None

@router.put("/preferences")
async def update_preferences(req: PreferenceUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Update preferences"""
    service = RecommendationService(session)
    kwargs = req.dict(exclude_unset=True)
    return await service.update_preferences(current_user.id, **kwargs)

@router.post("/recommendations/{rec_id}/click")
async def click_recommendation(rec_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Record recommendation click"""
    service = RecommendationService(session)
    success = await service.record_recommendation_click(rec_id)
    return {"recorded": success}
