"""Marketing API endpoints

Every record here belongs to an organization. Routes act only on records of the signed-in
user's organization; a record from another organization is answered with 404, the same as
a missing one, so ids cannot be probed across organizations.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.marketing import EmailCampaign, LoyaltyMember, LoyaltyProgram, Segment
from app.models.organizations import OrganizationMember
from app.models.user import User
from app.services.marketing_service import (
    AutomationService,
    EmailCampaignService,
    LeadScoringService,
    LoyaltyService,
    SegmentationService,
)


def _organization_id(current_user: User) -> int:
    """Organization of the signed-in user; marketing records are always created inside it."""
    if current_user.organization_id is None:
        raise HTTPException(status_code=422, detail="Your account has no organization yet. Create one under Organizations first.")
    return current_user.organization_id


async def _owned(session: AsyncSession, model, record_id: int, organization_id: int, label: str):
    """Record of the caller's organization, or 404."""
    record = (await session.execute(
        select(model).where(model.id == record_id, model.organization_id == organization_id)
    )).scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return record


async def _owned_member(session: AsyncSession, member_id: int, organization_id: int) -> LoyaltyMember:
    """Loyalty membership whose program belongs to the caller's organization, or 404."""
    member = (await session.execute(
        select(LoyaltyMember)
        .join(LoyaltyProgram, LoyaltyMember.program_id == LoyaltyProgram.id)
        .where(LoyaltyMember.id == member_id, LoyaltyProgram.organization_id == organization_id)
    )).scalar_one_or_none()
    if member is None:
        raise HTTPException(status_code=404, detail="Loyalty member not found")
    return member


async def _lead_in_scope(session: AsyncSession, current_user: User, user_id: int) -> None:
    """A lead is open to its own person and to active members of the caller's organization."""
    if user_id == current_user.id:
        return
    organization_id = _organization_id(current_user)
    member = (await session.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == user_id,
            OrganizationMember.status == "active",
        )
    )).scalar_one_or_none()
    if member is None:
        raise HTTPException(status_code=403, detail="Lead scores can only be read or changed for members of your organization")


router = APIRouter()


# SCHEMAS
class EmailCampaignRequest(BaseModel):
    name: str
    subject: str
    html_content: str
    email_type: str
    from_email: str


class SegmentRequest(BaseModel):
    name: str
    description: Optional[str] = None
    segmentation_type: str


class WorkflowRequest(BaseModel):
    name: str
    trigger_event: str
    workflow_config: dict


class LoyaltyProgramRequest(BaseModel):
    name: str
    description: Optional[str] = None
    points_per_dollar: float = 1.0


# EMAIL CAMPAIGNS
@router.post("/campaigns")
async def create_campaign(
    campaign: EmailCampaignRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create email campaign"""
    return await EmailCampaignService(session).create_campaign(_organization_id(current_user), campaign.model_dump())


@router.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get campaign"""
    return await _owned(session, EmailCampaign, campaign_id, _organization_id(current_user), "Campaign")


@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Send campaign"""
    await _owned(session, EmailCampaign, campaign_id, _organization_id(current_user), "Campaign")
    await EmailCampaignService(session).send_campaign(campaign_id)
    return {"status": "sent"}


# SEGMENTATION
@router.post("/segments")
async def create_segment(
    segment: SegmentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create customer segment"""
    return await SegmentationService(session).create_segment(_organization_id(current_user), segment.model_dump())


@router.get("/segments/{segment_id}")
async def get_segment(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get segment"""
    return await _owned(session, Segment, segment_id, _organization_id(current_user), "Segment")


@router.get("/segments/{segment_id}/members")
async def get_segment_members(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get segment members"""
    await _owned(session, Segment, segment_id, _organization_id(current_user), "Segment")
    return await SegmentationService(session).get_segment_members(segment_id)


# LEAD SCORING
@router.get("/leads/{user_id}/score")
async def get_lead_score(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get lead score"""
    await _lead_in_scope(session, current_user, user_id)
    return await LeadScoringService(session).get_or_create_lead_score(user_id)


@router.put("/leads/{user_id}/score")
async def update_lead_score(
    user_id: int,
    engagement: int = 0,
    purchase: int = 0,
    behavior: int = 0,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update lead score"""
    await _lead_in_scope(session, current_user, user_id)
    await LeadScoringService(session).update_lead_score(user_id, engagement, purchase, behavior)
    return {"status": "updated"}


# AUTOMATION
@router.post("/workflows")
async def create_workflow(
    workflow: WorkflowRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create automation workflow"""
    return await AutomationService(session).create_workflow(_organization_id(current_user), workflow.model_dump())


# LOYALTY PROGRAM
@router.post("/loyalty-programs")
async def create_loyalty_program(
    program: LoyaltyProgramRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create loyalty program"""
    organization_id = _organization_id(current_user)
    existing = (await session.execute(
        select(LoyaltyProgram.id).where(LoyaltyProgram.organization_id == organization_id).limit(1)
    )).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="This organization already has a loyalty program")
    return await LoyaltyService(session).create_program(organization_id, program.model_dump())


@router.post("/loyalty-programs/{program_id}/enroll/{user_id}")
async def enroll_in_loyalty(
    program_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Enroll in loyalty program"""
    await _owned(session, LoyaltyProgram, program_id, _organization_id(current_user), "Loyalty program")
    return await LoyaltyService(session).enroll_member(program_id, user_id)


@router.post("/loyalty-members/{member_id}/add-points")
async def add_loyalty_points(
    member_id: int,
    points: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Add loyalty points"""
    await _owned_member(session, member_id, _organization_id(current_user))
    await LoyaltyService(session).add_points(member_id, points, reason)
    return {"status": "points_added"}


@router.post("/loyalty-members/{member_id}/redeem-points")
async def redeem_loyalty_points(
    member_id: int,
    points: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Redeem loyalty points"""
    await _owned_member(session, member_id, _organization_id(current_user))
    try:
        await LoyaltyService(session).redeem_points(member_id, points, reason)
        return {"status": "points_redeemed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
