"""User profile service"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.profiles import UserProfile, UserSkill, UserExperience, UserEducation, UserBadge
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, ValidationError
from app.utils.logger import logger


class ProfileService:
    """Service for managing user profiles"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Profile operations
    async def get_or_create_profile(self, user_id: int) -> UserProfile:
        """Get or create user profile"""
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
        profile = (await self.session.execute(stmt)).scalar_one_or_none()

        if not profile:
            profile = UserProfile(user_id=user_id)
            self.session.add(profile)
            await self.session.commit()
            logger.info(f"Profile created for user {user_id}")

        return profile

    async def get_profile(self, user_id: int) -> UserProfile:
        """Get user profile"""
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
        profile = (await self.session.execute(stmt)).scalar_one_or_none()
        if not profile:
            raise NotFoundError(f"Profile for user {user_id} not found")
        return profile

    async def update_profile(self, user_id: int, **kwargs) -> UserProfile:
        """Update user profile"""
        profile = await self.get_or_create_profile(user_id)

        allowed_fields = {
            "bio", "avatar_url", "cover_url", "title", "department", "location",
            "phone", "website", "twitter", "linkedin", "github", "timezone",
            "language", "notification_preferences", "privacy_settings", "is_public",
            "show_email", "show_phone", "custom_fields"
        }

        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(profile, key):
                setattr(profile, key, value)

        profile.last_profile_update = datetime.now(timezone.utc)
        profile.updated_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Profile updated: user {user_id}")
        return profile

    async def get_public_profile(self, user_id: int) -> dict:
        """Get public profile view"""
        profile = await self.get_profile(user_id)

        if not profile.is_public:
            raise ValidationError("This profile is not public")

        return {
            "user_id": user_id,
            "title": profile.title,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "location": profile.location,
            "skills": await self.get_skills(user_id),
            "experiences": await self.get_experiences(user_id),
            "badges": await self.get_badges(user_id),
        }

    # Skill operations
    async def add_skill(
        self,
        user_id: int,
        name: str,
        category: str = None,
        proficiency: str = "intermediate",
        years_experience: int = 0,
    ) -> UserSkill:
        """Add skill to user profile"""
        profile = await self.get_or_create_profile(user_id)

        # Check if skill already exists
        stmt = select(UserSkill).where(
            and_(UserSkill.profile_id == profile.id, UserSkill.name == name)
        )
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError(f"Skill '{name}' already exists")

        skill = UserSkill(
            profile_id=profile.id,
            name=name,
            category=category,
            proficiency=proficiency,
            years_experience=years_experience,
        )
        self.session.add(skill)
        await self.session.commit()

        logger.info(f"Skill added to user {user_id}: {name}")
        return skill

    async def get_skills(self, user_id: int) -> list[UserSkill]:
        """Get user skills"""
        profile = await self.get_profile(user_id)
        stmt = select(UserSkill).where(UserSkill.profile_id == profile.id).order_by(UserSkill.endorsed_count.desc())
        skills = (await self.session.execute(stmt)).scalars().all()
        return skills

    async def update_skill(self, skill_id: int, **kwargs) -> UserSkill:
        """Update skill"""
        stmt = select(UserSkill).where(UserSkill.id == skill_id)
        skill = (await self.session.execute(stmt)).scalar_one_or_none()
        if not skill:
            raise NotFoundError("Skill not found")

        for key, value in kwargs.items():
            if key in {"proficiency", "years_experience"} and hasattr(skill, key):
                setattr(skill, key, value)

        skill.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return skill

    async def delete_skill(self, skill_id: int) -> None:
        """Delete skill"""
        stmt = select(UserSkill).where(UserSkill.id == skill_id)
        skill = (await self.session.execute(stmt)).scalar_one_or_none()
        if not skill:
            raise NotFoundError("Skill not found")

        await self.session.delete(skill)
        await self.session.commit()
        logger.info(f"Skill deleted: {skill_id}")

    async def endorse_skill(self, skill_id: int) -> UserSkill:
        """Endorse skill"""
        stmt = select(UserSkill).where(UserSkill.id == skill_id)
        skill = (await self.session.execute(stmt)).scalar_one_or_none()
        if not skill:
            raise NotFoundError("Skill not found")

        skill.endorsed_count += 1
        await self.session.commit()
        return skill

    # Experience operations
    async def add_experience(
        self,
        user_id: int,
        company: str,
        title: str,
        start_date: datetime,
        end_date: datetime = None,
        current: bool = False,
        **kwargs
    ) -> UserExperience:
        """Add work experience"""
        profile = await self.get_or_create_profile(user_id)

        experience = UserExperience(
            profile_id=profile.id,
            company=company,
            title=title,
            start_date=start_date,
            end_date=end_date,
            current=current,
            **{k: v for k, v in kwargs.items() if k in {"description", "employment_type", "location", "skills"}}
        )
        self.session.add(experience)
        await self.session.commit()

        logger.info(f"Experience added to user {user_id}: {company}")
        return experience

    async def get_experiences(self, user_id: int) -> list[UserExperience]:
        """Get user experiences"""
        profile = await self.get_profile(user_id)
        stmt = select(UserExperience).where(UserExperience.profile_id == profile.id).order_by(UserExperience.start_date.desc())
        experiences = (await self.session.execute(stmt)).scalars().all()
        return experiences

    async def update_experience(self, experience_id: int, **kwargs) -> UserExperience:
        """Update experience"""
        stmt = select(UserExperience).where(UserExperience.id == experience_id)
        exp = (await self.session.execute(stmt)).scalar_one_or_none()
        if not exp:
            raise NotFoundError("Experience not found")

        allowed = {"description", "employment_type", "location", "end_date", "current", "skills"}
        for key, value in kwargs.items():
            if key in allowed and hasattr(exp, key):
                setattr(exp, key, value)

        exp.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return exp

    async def delete_experience(self, experience_id: int) -> None:
        """Delete experience"""
        stmt = select(UserExperience).where(UserExperience.id == experience_id)
        exp = (await self.session.execute(stmt)).scalar_one_or_none()
        if not exp:
            raise NotFoundError("Experience not found")

        await self.session.delete(exp)
        await self.session.commit()

    # Education operations
    async def add_education(
        self,
        user_id: int,
        school: str,
        start_date: datetime,
        end_date: datetime = None,
        **kwargs
    ) -> UserEducation:
        """Add education"""
        profile = await self.get_or_create_profile(user_id)

        education = UserEducation(
            profile_id=profile.id,
            school=school,
            start_date=start_date,
            end_date=end_date,
            **{k: v for k, v in kwargs.items() if k in {"degree", "field", "description", "grade"}}
        )
        self.session.add(education)
        await self.session.commit()

        logger.info(f"Education added to user {user_id}: {school}")
        return education

    async def get_educations(self, user_id: int) -> list[UserEducation]:
        """Get user educations"""
        profile = await self.get_profile(user_id)
        stmt = select(UserEducation).where(UserEducation.profile_id == profile.id).order_by(UserEducation.start_date.desc())
        educations = (await self.session.execute(stmt)).scalars().all()
        return educations

    async def delete_education(self, education_id: int) -> None:
        """Delete education"""
        stmt = select(UserEducation).where(UserEducation.id == education_id)
        edu = (await self.session.execute(stmt)).scalar_one_or_none()
        if not edu:
            raise NotFoundError("Education not found")

        await self.session.delete(edu)
        await self.session.commit()

    # Badge operations
    async def award_badge(
        self,
        user_id: int,
        badge_name: str,
        badge_type: str = "achievement",
        **kwargs
    ) -> UserBadge:
        """Award badge to user"""
        profile = await self.get_or_create_profile(user_id)

        badge = UserBadge(
            profile_id=profile.id,
            badge_name=badge_name,
            badge_type=badge_type,
            **{k: v for k, v in kwargs.items() if k in {"description", "icon_url", "expires_at", "metadata"}}
        )
        self.session.add(badge)
        await self.session.commit()

        logger.info(f"Badge awarded to user {user_id}: {badge_name}")
        return badge

    async def get_badges(self, user_id: int) -> list[UserBadge]:
        """Get user badges"""
        profile = await self.get_profile(user_id)
        stmt = select(UserBadge).where(UserBadge.profile_id == profile.id).order_by(UserBadge.earned_at.desc())
        badges = (await self.session.execute(stmt)).scalars().all()
        return badges

    async def get_profile_summary(self, user_id: int) -> dict:
        """Get complete profile summary"""
        profile = await self.get_profile(user_id)
        skills = await self.get_skills(user_id)
        experiences = await self.get_experiences(user_id)
        educations = await self.get_educations(user_id)
        badges = await self.get_badges(user_id)

        return {
            "profile": profile,
            "skills_count": len(skills),
            "experiences_count": len(experiences),
            "educations_count": len(educations),
            "badges_count": len(badges),
            "profile_completeness": self._calculate_completeness(profile),
        }

    def _calculate_completeness(self, profile: UserProfile) -> int:
        """Calculate profile completeness percentage"""
        fields = {
            "bio": bool(profile.bio),
            "avatar_url": bool(profile.avatar_url),
            "title": bool(profile.title),
            "location": bool(profile.location),
            "website": bool(profile.website),
        }
        return int((sum(fields.values()) / len(fields)) * 100)
