"""Marketing API endpoints

Every record here belongs to an organization. Routes act only on records of the signed-in
user's organization; a record from another organization is answered with 404, the same as
a missing one, so ids cannot be probed across organizations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.services.marketing_service import (
    EmailCampaignService, SegmentationService, LeadScoringService,
    AutomationService, AnalyticsService, ABTestingService, LoyaltyService
)
from app.models.marketing import EmailCampaign, LoyaltyMember, LoyaltyProgram, Segment
from app.models.organizations import OrganizationMember
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional


def _organization_id(current_user: User) -> int:
    """Organization of the signed-in user; marketing records are always created inside it."""
    if current_user.organization_id is None:
        raise HTTPException(status_code=422, detail="Your account has no organization yet. Create one under Organizations first.")
    return current_user.organization_id


def _owned(db: Session, model, record_id: int, organization_id: int, label: str):
    """Record of the caller's organization, or 404."""
    record = db.query(model).filter(model.id == record_id, model.organization_id == organization_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return record


def _owned_member(db: Session, member_id: int, organization_id: int) -> LoyaltyMember:
    """Loyalty membership whose program belongs to the caller's organization, or 404."""
    member = (
        db.query(LoyaltyMember)
        .join(LoyaltyProgram, LoyaltyMember.program_id == LoyaltyProgram.id)
        .filter(LoyaltyMember.id == member_id, LoyaltyProgram.organization_id == organization_id)
        .first()
    )
    if member is None:
        raise HTTPException(status_code=404, detail="Loyalty member not found")
    return member


def _lead_in_scope(db: Session, current_user: User, user_id: int) -> None:
    """A lead is open to its own person and to active members of the caller's organization."""
    if user_id == current_user.id:
        return
    organization_id = _organization_id(current_user)
    member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == user_id,
        OrganizationMember.status == "active",
    ).first()
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
def create_campaign(
    campaign: EmailCampaignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create email campaign"""
    return EmailCampaignService.create_campaign(db, _organization_id(current_user), campaign.dict())


@router.get("/campaigns/{campaign_id}")
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get campaign"""
    return _owned(db, EmailCampaign, campaign_id, _organization_id(current_user), "Campaign")


@router.post("/campaigns/{campaign_id}/send")
def send_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send campaign"""
    _owned(db, EmailCampaign, campaign_id, _organization_id(current_user), "Campaign")
    EmailCampaignService.send_campaign(db, campaign_id)
    return {"status": "sent"}


# SEGMENTATION
@router.post("/segments")
def create_segment(
    segment: SegmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create customer segment"""
    return SegmentationService.create_segment(db, _organization_id(current_user), segment.dict())


@router.get("/segments/{segment_id}")
def get_segment(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get segment"""
    return _owned(db, Segment, segment_id, _organization_id(current_user), "Segment")


@router.get("/segments/{segment_id}/members")
def get_segment_members(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get segment members"""
    _owned(db, Segment, segment_id, _organization_id(current_user), "Segment")
    return SegmentationService.get_segment_members(db, segment_id)


# LEAD SCORING
@router.get("/leads/{user_id}/score")
def get_lead_score(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get lead score"""
    _lead_in_scope(db, current_user, user_id)
    return LeadScoringService.get_or_create_lead_score(db, user_id)


@router.put("/leads/{user_id}/score")
def update_lead_score(
    user_id: int,
    engagement: int = 0,
    purchase: int = 0,
    behavior: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update lead score"""
    _lead_in_scope(db, current_user, user_id)
    LeadScoringService.update_lead_score(db, user_id, engagement, purchase, behavior)
    return {"status": "updated"}


# AUTOMATION
@router.post("/workflows")
def create_workflow(
    workflow: WorkflowRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create automation workflow"""
    return AutomationService.create_workflow(db, _organization_id(current_user), workflow.dict())


# LOYALTY PROGRAM
@router.post("/loyalty-programs")
def create_loyalty_program(
    program: LoyaltyProgramRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create loyalty program"""
    organization_id = _organization_id(current_user)
    if db.query(LoyaltyProgram).filter(LoyaltyProgram.organization_id == organization_id).first() is not None:
        raise HTTPException(status_code=409, detail="This organization already has a loyalty program")
    return LoyaltyService.create_program(db, organization_id, program.dict())


@router.post("/loyalty-programs/{program_id}/enroll/{user_id}")
def enroll_in_loyalty(
    program_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in loyalty program"""
    _owned(db, LoyaltyProgram, program_id, _organization_id(current_user), "Loyalty program")
    return LoyaltyService.enroll_member(db, program_id, user_id)


@router.post("/loyalty-members/{member_id}/add-points")
def add_loyalty_points(
    member_id: int,
    points: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add loyalty points"""
    _owned_member(db, member_id, _organization_id(current_user))
    LoyaltyService.add_points(db, member_id, points, reason)
    return {"status": "points_added"}


@router.post("/loyalty-members/{member_id}/redeem-points")
def redeem_loyalty_points(
    member_id: int,
    points: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Redeem loyalty points"""
    _owned_member(db, member_id, _organization_id(current_user))
    try:
        LoyaltyService.redeem_points(db, member_id, points, reason)
        return {"status": "points_redeemed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
