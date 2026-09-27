"""Services for Modules 26-30"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from app.models.advanced_features import *


class PermissionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def grant_permission(self, resource_type: str, resource_id: int, user_id: int, level: str) -> ResourcePermission:
        perm = ResourcePermission(resource_type=resource_type, resource_id=resource_id, user_id=user_id, permission_level=level)
        self.session.add(perm)
        await self.session.commit()
        await self.session.refresh(perm)
        return perm

    async def get_permission(self, resource_type: str, resource_id: int, user_id: int) -> Optional[ResourcePermission]:
        stmt = select(ResourcePermission).where(
            and_(ResourcePermission.resource_type == resource_type,
                 ResourcePermission.resource_id == resource_id,
                 ResourcePermission.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_share_link(self, resource_type: str, resource_id: int, user_id: int, token: str, level: str) -> ShareLink:
        link = ShareLink(resource_type=resource_type, resource_id=resource_id, created_by_user_id=user_id, token=token, permission_level=level)
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)
        return link

    async def get_share_link(self, token: str) -> Optional[ShareLink]:
        stmt = select(ShareLink).where(ShareLink.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_share_link(self, link_id: int) -> bool:
        stmt = update(ShareLink).where(ShareLink.id == link_id).values(is_active=False)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0


class StorageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upload_file(self, user_id: int, org_id: int, filename: str, file_key: str, size: int, mime: str) -> StorageFile:
        file = StorageFile(user_id=user_id, organization_id=org_id, filename=filename, file_key=file_key, file_size=size, mime_type=mime, url=f"s3://{file_key}")
        self.session.add(file)
        await self.session.commit()
        await self.session.refresh(file)
        return file

    async def get_file(self, file_id: int) -> Optional[StorageFile]:
        stmt = select(StorageFile).where(StorageFile.id == file_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_files(self, user_id: int) -> List[StorageFile]:
        stmt = select(StorageFile).where(StorageFile.user_id == user_id).order_by(desc(StorageFile.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_file(self, file_id: int) -> bool:
        stmt = delete(StorageFile).where(StorageFile.id == file_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def add_cdn_url(self, file_id: int, cdn_url: str, provider: str) -> CDNUrl:
        cdn = CDNUrl(storage_file_id=file_id, cdn_url=cdn_url, cdn_provider=provider)
        self.session.add(cdn)
        await self.session.commit()
        await self.session.refresh(cdn)
        return cdn


class VideoProcessingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def start_processing(self, video_id: int, quality: str) -> VideoProcess:
        process = VideoProcess(video_id=video_id, quality_level=quality)
        self.session.add(process)
        await self.session.commit()
        await self.session.refresh(process)
        return process

    async def update_progress(self, process_id: int, progress: float, status: str) -> bool:
        stmt = update(VideoProcess).where(VideoProcess.id == process_id).values(progress=progress, status=status)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_processes(self, video_id: int) -> List[VideoProcess]:
        stmt = select(VideoProcess).where(VideoProcess.video_id == video_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_thumbnail(self, video_id: int, file_key: str, url: str, is_primary: bool = False) -> Thumbnail:
        thumb = Thumbnail(video_id=video_id, file_key=file_key, url=url, is_primary=is_primary)
        self.session.add(thumb)
        await self.session.commit()
        await self.session.refresh(thumb)
        return thumb


class CollaborationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_comment(self, resource_type: str, resource_id: int, user_id: int, content: str) -> Comment:
        comment = Comment(resource_type=resource_type, resource_id=resource_id, user_id=user_id, content=content)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comments(self, resource_type: str, resource_id: int) -> List[Comment]:
        stmt = select(Comment).where(
            and_(Comment.resource_type == resource_type, Comment.resource_id == resource_id)
        ).order_by(desc(Comment.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_reaction(self, comment_id: int, user_id: int, reaction_type: str) -> Reaction:
        reaction = Reaction(comment_id=comment_id, user_id=user_id, reaction_type=reaction_type)
        self.session.add(reaction)
        await self.session.commit()
        await self.session.refresh(reaction)
        return reaction

    async def get_reactions(self, comment_id: int) -> List[Reaction]:
        stmt = select(Reaction).where(Reaction.comment_id == comment_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class RecommendationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_preferences(self, user_id: int) -> Optional[UserPreference]:
        stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_preferences(self, user_id: int, **kwargs) -> UserPreference:
        stmt = update(UserPreference).where(UserPreference.user_id == user_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_user_preferences(user_id)

    async def add_recommendation(self, user_id: int, content_id: int, score: float, reason: str, algorithm: str) -> Recommendation:
        rec = Recommendation(user_id=user_id, content_id=content_id, score=score, reason=reason, algorithm=algorithm)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def get_recommendations(self, user_id: int, limit: int = 10) -> List[Recommendation]:
        stmt = select(Recommendation).where(
            Recommendation.user_id == user_id
        ).order_by(desc(Recommendation.score)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_recommendation_click(self, rec_id: int) -> bool:
        stmt = update(Recommendation).where(Recommendation.id == rec_id).values(is_clicked=True)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_personalization_profile(self, user_id: int) -> Optional[PersonalizationProfile]:
        stmt = select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
