"""Marketing API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.marketing_service import (
    EmailCampaignService, SegmentationService, LeadScoringService,
    AutomationService, AnalyticsService, ABTestingService, LoyaltyService
)
from app.models.auth import User
from pydantic import BaseModel
from typing import List, Optional

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
    return EmailCampaignService.create_campaign(db, 1, campaign.dict())


@router.get("/campaigns/{campaign_id}")
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get campaign"""
    campaign = EmailCampaignService.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/campaigns/{campaign_id}/send")
def send_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send campaign"""
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
    return SegmentationService.create_segment(db, 1, segment.dict())


@router.get("/segments/{segment_id}")
def get_segment(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get segment"""
    segment = SegmentationService.get_segment(db, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment


@router.get("/segments/{segment_id}/members")
def get_segment_members(
    segment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get segment members"""
    return SegmentationService.get_segment_members(db, segment_id)


# LEAD SCORING
@router.get("/leads/{user_id}/score")
def get_lead_score(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get lead score"""
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
    return AutomationService.create_workflow(db, 1, workflow.dict())


# LOYALTY PROGRAM
@router.post("/loyalty-programs")
def create_loyalty_program(
    program: LoyaltyProgramRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create loyalty program"""
    return LoyaltyService.create_program(db, 1, program.dict())


@router.post("/loyalty-programs/{program_id}/enroll/{user_id}")
def enroll_in_loyalty(
    program_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in loyalty program"""
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
    try:
        LoyaltyService.redeem_points(db, member_id, points, reason)
        return {"status": "points_redeemed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
