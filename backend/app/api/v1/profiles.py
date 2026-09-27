"""User profile API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.profile_service import ProfileService
from app.utils.exceptions import NotFoundError, ConflictError, ValidationError
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


# Schemas
class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    timezone: Optional[str] = None
    is_public: Optional[bool] = None


class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1)
    category: Optional[str] = None
    proficiency: str = "intermediate"
    years_experience: int = 0


class SkillResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    proficiency: str
    years_experience: int
    endorsed_count: int

    class Config:
        from_attributes = True


class ExperienceCreate(BaseModel):
    company: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    start_date: datetime
    end_date: Optional[datetime] = None
    current: bool = False
    description: Optional[str] = None


class ExperienceResponse(BaseModel):
    id: int
    company: str
    title: str
    start_date: datetime
    end_date: Optional[datetime]
    current: bool
    description: Optional[str]

    class Config:
        from_attributes = True


class EducationCreate(BaseModel):
    school: str = Field(..., min_length=1)
    start_date: datetime
    end_date: Optional[datetime] = None
    degree: Optional[str] = None
    field: Optional[str] = None


class EducationResponse(BaseModel):
    id: int
    school: str
    degree: Optional[str]
    field: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    location: Optional[str]
    timezone: str
    is_public: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Profile endpoints
@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get current user's profile"""
    try:
        service = ProfileService(session)
        return await service.get_or_create_profile(current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update current user's profile"""
    try:
        service = ProfileService(session)
        return await service.update_profile(
            current_user.id,
            **profile_update.dict(exclude_unset=True)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user profile"""
    try:
        service = ProfileService(session)
        return await service.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{user_id}/summary", response_model=dict)
async def get_profile_summary(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get profile summary"""
    try:
        service = ProfileService(session)
        return await service.get_profile_summary(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Skills endpoints
@router.post("/me/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def add_skill(
    skill: SkillCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add skill to profile"""
    try:
        service = ProfileService(session)
        return await service.add_skill(
            current_user.id,
            skill.name,
            skill.category,
            skill.proficiency,
            skill.years_experience,
        )
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}/skills", response_model=list[SkillResponse])
async def get_skills(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user skills"""
    try:
        service = ProfileService(session)
        return await service.get_skills(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete skill"""
    try:
        service = ProfileService(session)
        await service.delete_skill(skill_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Experience endpoints
@router.post("/me/experiences", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_experience(
    experience: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add work experience"""
    try:
        service = ProfileService(session)
        return await service.add_experience(
            current_user.id,
            experience.company,
            experience.title,
            experience.start_date,
            experience.end_date,
            experience.current,
            description=experience.description,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}/experiences", response_model=list[ExperienceResponse])
async def get_experiences(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user experiences"""
    try:
        service = ProfileService(session)
        return await service.get_experiences(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete experience"""
    try:
        service = ProfileService(session)
        await service.delete_experience(experience_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Education endpoints
@router.post("/me/educations", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    education: EducationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add education"""
    try:
        service = ProfileService(session)
        return await service.add_education(
            current_user.id,
            education.school,
            education.start_date,
            education.end_date,
            degree=education.degree,
            field=education.field,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}/educations", response_model=list[EducationResponse])
async def get_educations(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user educations"""
    try:
        service = ProfileService(session)
        return await service.get_educations(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/educations/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete education"""
    try:
        service = ProfileService(session)
        await service.delete_education(education_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
