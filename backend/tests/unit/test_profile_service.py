"""Unit tests for ProfileService"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.profile_service import ProfileService
from app.models.profiles import UserProfile, UserSkill, UserExperience, UserEducation
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError
from app.core.security import hash_password


@pytest.fixture
async def test_user(session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        email="test@example.com",
        password_hash=hash_password("password"),
        first_name="Test",
        last_name="User",
        status="active",
    )
    session.add(user)
    await session.flush()
    return user


class TestProfileManagement:
    async def test_create_profile(self, session: AsyncSession, test_user: User):
        """Test creating profile"""
        service = ProfileService(session)
        profile = await service.get_or_create_profile(test_user.id)

        assert profile.id is not None
        assert profile.user_id == test_user.id

    async def test_get_profile(self, session: AsyncSession, test_user: User):
        """Test getting profile"""
        service = ProfileService(session)
        created = await service.get_or_create_profile(test_user.id)

        retrieved = await service.get_profile(test_user.id)
        assert retrieved.id == created.id

    async def test_update_profile(self, session: AsyncSession, test_user: User):
        """Test updating profile"""
        service = ProfileService(session)
        await service.get_or_create_profile(test_user.id)

        updated = await service.update_profile(
            test_user.id,
            bio="Test bio",
            title="Senior Developer",
            location="San Francisco"
        )

        assert updated.bio == "Test bio"
        assert updated.title == "Senior Developer"
        assert updated.location == "San Francisco"

    async def test_profile_completeness(self, session: AsyncSession, test_user: User):
        """Test profile completeness calculation"""
        service = ProfileService(session)
        profile = await service.get_or_create_profile(test_user.id)

        completeness = service._calculate_completeness(profile)
        assert completeness == 0  # No fields filled

        await service.update_profile(test_user.id, bio="Test", title="Dev")
        updated = await service.get_profile(test_user.id)
        completeness = service._calculate_completeness(updated)
        assert completeness > 0


class TestSkillManagement:
    async def test_add_skill(self, session: AsyncSession, test_user: User):
        """Test adding skill"""
        service = ProfileService(session)

        skill = await service.add_skill(
            test_user.id,
            "Python",
            category="backend",
            proficiency="expert"
        )

        assert skill.name == "Python"
        assert skill.category == "backend"
        assert skill.proficiency == "expert"

    async def test_add_duplicate_skill(self, session: AsyncSession, test_user: User):
        """Test cannot add duplicate skill"""
        service = ProfileService(session)

        await service.add_skill(test_user.id, "Python")

        with pytest.raises(ConflictError):
            await service.add_skill(test_user.id, "Python")

    async def test_get_skills(self, session: AsyncSession, test_user: User):
        """Test getting skills"""
        service = ProfileService(session)

        await service.add_skill(test_user.id, "Python", proficiency="expert")
        await service.add_skill(test_user.id, "JavaScript", proficiency="intermediate")

        skills = await service.get_skills(test_user.id)

        assert len(skills) == 2
        names = [s.name for s in skills]
        assert "Python" in names
        assert "JavaScript" in names

    async def test_endorse_skill(self, session: AsyncSession, test_user: User):
        """Test endorsing skill"""
        service = ProfileService(session)

        skill = await service.add_skill(test_user.id, "Python")
        assert skill.endorsed_count == 0

        endorsed = await service.endorse_skill(skill.id)
        assert endorsed.endorsed_count == 1


class TestExperienceManagement:
    async def test_add_experience(self, session: AsyncSession, test_user: User):
        """Test adding experience"""
        service = ProfileService(session)

        start = datetime.now(timezone.utc) - timedelta(days=365)
        exp = await service.add_experience(
            test_user.id,
            company="Acme",
            title="Senior Dev",
            start_date=start,
            current=True
        )

        assert exp.company == "Acme"
        assert exp.title == "Senior Dev"
        assert exp.current is True

    async def test_get_experiences(self, session: AsyncSession, test_user: User):
        """Test getting experiences"""
        service = ProfileService(session)

        start1 = datetime.now(timezone.utc) - timedelta(days=730)
        start2 = datetime.now(timezone.utc) - timedelta(days=365)

        await service.add_experience(test_user.id, "Company1", "Role1", start1)
        await service.add_experience(test_user.id, "Company2", "Role2", start2, current=True)

        exps = await service.get_experiences(test_user.id)

        assert len(exps) == 2
        # Should be sorted by start_date descending
        assert exps[0].company == "Company2"


class TestEducationManagement:
    async def test_add_education(self, session: AsyncSession, test_user: User):
        """Test adding education"""
        service = ProfileService(session)

        start = datetime.now(timezone.utc) - timedelta(days=1095)
        edu = await service.add_education(
            test_user.id,
            school="MIT",
            degree="BS",
            field="Computer Science",
            start_date=start
        )

        assert edu.school == "MIT"
        assert edu.degree == "BS"
        assert edu.field == "Computer Science"

    async def test_get_educations(self, session: AsyncSession, test_user: User):
        """Test getting educations"""
        service = ProfileService(session)

        start = datetime.now(timezone.utc) - timedelta(days=1095)
        await service.add_education(test_user.id, "MIT", start_date=start)
        await service.add_education(test_user.id, "Stanford", start_date=start)

        edus = await service.get_educations(test_user.id)
        assert len(edus) == 2


class TestProfileSummary:
    async def test_get_profile_summary(self, session: AsyncSession, test_user: User):
        """Test getting profile summary"""
        service = ProfileService(session)

        # Add various items
        await service.add_skill(test_user.id, "Python")
        await service.add_skill(test_user.id, "JavaScript")

        start = datetime.now(timezone.utc) - timedelta(days=365)
        await service.add_experience(test_user.id, "Company", "Role", start)

        edu_start = datetime.now(timezone.utc) - timedelta(days=1095)
        await service.add_education(test_user.id, "MIT", start_date=edu_start)

        summary = await service.get_profile_summary(test_user.id)

        assert summary["skills_count"] == 2
        assert summary["experiences_count"] == 1
        assert summary["educations_count"] == 1
        assert summary["profile_completeness"] >= 0
