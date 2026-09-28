"""Marketing services for email, SMS, segmentation, automation, analytics"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.marketing import (
    EmailCampaign, EmailTemplate, AutomationWorkflow, SMSCampaign,
    Segment, SegmentMembership, LeadScore, EmailMetric, ABTest,
    LoyaltyProgram, LoyaltyMember, LoyaltyTransaction
)
from datetime import datetime, timezone
import uuid


class EmailCampaignService:
    """Email campaign service"""

    @staticmethod
    def create_campaign(db: Session, org_id: int, campaign_data: dict) -> EmailCampaign:
        campaign = EmailCampaign(organization_id=org_id, **campaign_data)
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign

    @staticmethod
    def get_campaign(db: Session, campaign_id: int) -> EmailCampaign:
        return db.query(EmailCampaign).filter(EmailCampaign.id == campaign_id).first()

    @staticmethod
    def send_campaign(db: Session, campaign_id: int):
        campaign = EmailCampaignService.get_campaign(db, campaign_id)
        campaign.status = "sent"
        campaign.sent_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def record_email_event(db: Session, campaign_id: int, event_type: str):
        campaign = EmailCampaignService.get_campaign(db, campaign_id)

        if event_type == "open":
            campaign.opened_count += 1
        elif event_type == "click":
            campaign.clicked_count += 1
        elif event_type == "bounce":
            campaign.bounced_count += 1

        campaign.open_rate = (campaign.opened_count / campaign.sent_count) if campaign.sent_count > 0 else 0
        campaign.click_rate = (campaign.clicked_count / campaign.sent_count) if campaign.sent_count > 0 else 0
        campaign.bounce_rate = (campaign.bounced_count / campaign.sent_count) if campaign.sent_count > 0 else 0

        db.commit()


class SegmentationService:
    """Customer segmentation service"""

    @staticmethod
    def create_segment(db: Session, org_id: int, segment_data: dict) -> Segment:
        segment = Segment(organization_id=org_id, **segment_data)
        db.add(segment)
        db.commit()
        db.refresh(segment)
        return segment

    @staticmethod
    def get_segment(db: Session, segment_id: int) -> Segment:
        return db.query(Segment).filter(Segment.id == segment_id).first()

    @staticmethod
    def add_member_to_segment(db: Session, segment_id: int, user_id: int):
        membership = SegmentMembership(segment_id=segment_id, contact_id=user_id)
        db.add(membership)

        segment = SegmentationService.get_segment(db, segment_id)
        segment.contact_count = db.query(SegmentMembership).filter(
            SegmentMembership.segment_id == segment_id
        ).count()

        db.commit()

    @staticmethod
    def get_segment_members(db: Session, segment_id: int):
        return db.query(SegmentMembership).filter(
            SegmentMembership.segment_id == segment_id
        ).all()


class LeadScoringService:
    """Lead scoring service"""

    @staticmethod
    def get_or_create_lead_score(db: Session, user_id: int) -> LeadScore:
        score = db.query(LeadScore).filter(LeadScore.user_id == user_id).first()
        if not score:
            score = LeadScore(user_id=user_id)
            db.add(score)
            db.commit()
            db.refresh(score)
        return score

    @staticmethod
    def update_lead_score(db: Session, user_id: int, engagement: int = 0, purchase: int = 0, behavior: int = 0):
        score = LeadScoringService.get_or_create_lead_score(db, user_id)

        score.engagement_score += engagement
        score.purchase_score += purchase
        score.behavior_score += behavior
        score.total_score = score.engagement_score + score.purchase_score + score.behavior_score

        if score.total_score >= 80:
            score.status = "hot"
        elif score.total_score >= 50:
            score.status = "warm"
        else:
            score.status = "cold"

        db.commit()


class AutomationService:
    """Email automation service"""

    @staticmethod
    def create_workflow(db: Session, org_id: int, workflow_data: dict) -> AutomationWorkflow:
        workflow = AutomationWorkflow(organization_id=org_id, **workflow_data)
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return workflow

    @staticmethod
    def get_workflow(db: Session, workflow_id: int) -> AutomationWorkflow:
        return db.query(AutomationWorkflow).filter(AutomationWorkflow.id == workflow_id).first()


class AnalyticsService:
    """Marketing analytics service"""

    @staticmethod
    def record_metric(db: Session, campaign_id: int, metric_data: dict) -> EmailMetric:
        metric = EmailMetric(
            campaign_id=campaign_id,
            metric_date=datetime.now(timezone.utc),
            **metric_data
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric


class ABTestingService:
    """A/B testing service"""

    @staticmethod
    def create_test(db: Session, org_id: int, test_data: dict) -> ABTest:
        test = ABTest(organization_id=org_id, **test_data)
        db.add(test)
        db.commit()
        db.refresh(test)
        return test


class LoyaltyService:
    """Loyalty program service"""

    @staticmethod
    def create_program(db: Session, org_id: int, program_data: dict) -> LoyaltyProgram:
        program = LoyaltyProgram(organization_id=org_id, **program_data)
        db.add(program)
        db.commit()
        db.refresh(program)
        return program

    @staticmethod
    def enroll_member(db: Session, program_id: int, user_id: int) -> LoyaltyMember:
        member = LoyaltyMember(
            program_id=program_id,
            user_id=user_id,
            member_id=str(uuid.uuid4())
        )
        db.add(member)

        program = db.query(LoyaltyProgram).filter(LoyaltyProgram.id == program_id).first()
        program.total_members += 1

        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def add_points(db: Session, member_id: int, points: int, reason: str):
        member = db.query(LoyaltyMember).filter(LoyaltyMember.id == member_id).first()
        member.total_points += points
        member.available_points += points

        transaction = LoyaltyTransaction(
            member_id=member_id,
            transaction_type="earn",
            points=points,
            reason=reason
        )
        db.add(transaction)

        program = member.program
        program.total_points_distributed += points

        db.commit()

    @staticmethod
    def redeem_points(db: Session, member_id: int, points: int, reason: str):
        member = db.query(LoyaltyMember).filter(LoyaltyMember.id == member_id).first()

        if member.available_points < points:
            raise ValueError("Insufficient points")

        member.available_points -= points
        member.redeemed_points += points

        transaction = LoyaltyTransaction(
            member_id=member_id,
            transaction_type="redeem",
            points=points,
            reason=reason
        )
        db.add(transaction)
        db.commit()
