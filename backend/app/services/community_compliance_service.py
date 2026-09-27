"""Services for Community, Gamification & Compliance: Modules 61-65"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc, func
from typing import Optional, List
from datetime import datetime, timezone
from app.models.community_compliance import *


class CommunityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_thread(self, creator_id: int, category: str, title: str, description: str = None) -> ForumThread:
        thread = ForumThread(creator_id=creator_id, category=category, title=title, description=description)
        self.session.add(thread)
        await self.session.commit()
        await self.session.refresh(thread)
        return thread

    async def get_threads(self, category: str = None, limit: int = 20) -> List[ForumThread]:
        stmt = select(ForumThread)
        if category:
            stmt = stmt.where(ForumThread.category == category)
        stmt = stmt.order_by(desc(ForumThread.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_reply(self, thread_id: int, author_id: int, content: str) -> ForumReply:
        reply = ForumReply(thread_id=thread_id, author_id=author_id, content=content)
        self.session.add(reply)
        await self.session.commit()
        await self.session.refresh(reply)
        return reply


class GamificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_badge(self, name: str, description: str, badge_type: str) -> Badge:
        badge = Badge(name=name, description=description, badge_type=badge_type)
        self.session.add(badge)
        await self.session.commit()
        await self.session.refresh(badge)
        return badge

    async def award_badge(self, user_id: int, badge_id: int) -> UserBadge:
        user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
        self.session.add(user_badge)
        await self.session.commit()
        await self.session.refresh(user_badge)
        return user_badge

    async def get_user_badges(self, user_id: int) -> List[UserBadge]:
        stmt = select(UserBadge).where(UserBadge.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_leaderboard(self, user_id: int, points: int, views: int) -> Leaderboard:
        stmt = select(Leaderboard).where(Leaderboard.user_id == user_id)
        result = await self.session.execute(stmt)
        entry = result.scalar_one_or_none()
        if entry:
            entry.points = points
            entry.views = views
        else:
            entry = Leaderboard(user_id=user_id, points=points, views=views)
            self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry


class ReportingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_report(self, creator_id: int, report_type: str, data: dict) -> Report:
        report = Report(creator_id=creator_id, report_type=report_type, data=data, period_start=datetime.now(timezone.utc))
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get_creator_reports(self, creator_id: int) -> List[Report]:
        stmt = select(Report).where(Report.creator_id == creator_id).order_by(desc(Report.generated_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def request_data_export(self, user_id: int, export_type: str) -> DataExport:
        export = DataExport(user_id=user_id, export_type=export_type)
        self.session.add(export)
        await self.session.commit()
        await self.session.refresh(export)
        return export


class ComplianceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_policy(self, name: str, description: str, requirements: dict) -> CompliancePolicy:
        policy = CompliancePolicy(name=name, description=description, requirements=requirements)
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def check_user_compliance(self, user_id: int) -> Optional[UserCompliance]:
        stmt = select(UserCompliance).where(UserCompliance.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def log_audit(self, user_id: int, action: str, resource: str = None, changes: dict = None) -> AuditLog:
        log = AuditLog(user_id=user_id, action=action, resource=resource, changes=changes)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log


class LocalizationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_language(self, code: str, name: str) -> Language:
        stmt = select(Language).where(Language.code == code)
        result = await self.session.execute(stmt)
        lang = result.scalar_one_or_none()
        if not lang:
            lang = Language(code=code, name=name)
            self.session.add(lang)
            await self.session.commit()
            await self.session.refresh(lang)
        return lang

    async def get_translation(self, language_code: str, key: str) -> Optional[Translation]:
        stmt = select(Translation).join(Language).where(and_(Language.code == language_code, Translation.key == key))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def set_user_language(self, user_id: int, language_id: int) -> UserLocalization:
        stmt = select(UserLocalization).where(UserLocalization.user_id == user_id)
        result = await self.session.execute(stmt)
        loc = result.scalar_one_or_none()
        if loc:
            loc.language_id = language_id
        else:
            loc = UserLocalization(user_id=user_id, language_id=language_id)
            self.session.add(loc)
        await self.session.commit()
        await self.session.refresh(loc)
        return loc
