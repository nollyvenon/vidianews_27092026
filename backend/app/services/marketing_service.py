"""Marketing services for email, segmentation, lead scoring, automation, analytics and loyalty (async)."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.marketing import (
    ABTest,
    AutomationWorkflow,
    EmailCampaign,
    EmailMetric,
    LeadScore,
    LoyaltyMember,
    LoyaltyProgram,
    LoyaltyTransaction,
    Segment,
    SegmentMembership,
)
from app.utils.exceptions import NotFoundError


class EmailCampaignService:
    """Email campaign service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_campaign(self, org_id: int, campaign_data: dict) -> EmailCampaign:
        campaign = EmailCampaign(organization_id=org_id, **campaign_data)
        self.session.add(campaign)
        await self.session.commit()
        await self.session.refresh(campaign)
        return campaign

    async def get_campaign(self, campaign_id: int) -> Optional[EmailCampaign]:
        return await self.session.get(EmailCampaign, campaign_id)

    async def send_campaign(self, campaign_id: int) -> None:
        campaign = await self.get_campaign(campaign_id)
        if campaign is None:
            raise NotFoundError("Campaign")
        campaign.status = "sent"
        campaign.sent_at = datetime.now(timezone.utc)
        await self.session.commit()

    async def record_email_event(self, campaign_id: int, event_type: str) -> None:
        campaign = await self.get_campaign(campaign_id)
        if campaign is None:
            raise NotFoundError("Campaign")

        if event_type == "open":
            campaign.opened_count += 1
        elif event_type == "click":
            campaign.clicked_count += 1
        elif event_type == "bounce":
            campaign.bounced_count += 1

        sent = campaign.sent_count
        campaign.open_rate = (campaign.opened_count / sent) if sent > 0 else 0
        campaign.click_rate = (campaign.clicked_count / sent) if sent > 0 else 0
        campaign.bounce_rate = (campaign.bounced_count / sent) if sent > 0 else 0
        await self.session.commit()


class SegmentationService:
    """Customer segmentation service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_segment(self, org_id: int, segment_data: dict) -> Segment:
        segment = Segment(organization_id=org_id, **segment_data)
        self.session.add(segment)
        await self.session.commit()
        await self.session.refresh(segment)
        return segment

    async def get_segment(self, segment_id: int) -> Optional[Segment]:
        return await self.session.get(Segment, segment_id)

    async def add_member_to_segment(self, segment_id: int, user_id: int) -> None:
        segment = await self.get_segment(segment_id)
        if segment is None:
            raise NotFoundError("Segment")
        self.session.add(SegmentMembership(segment_id=segment_id, contact_id=user_id))
        await self.session.flush()
        count = (await self.session.execute(
            select(func.count(SegmentMembership.id)).where(SegmentMembership.segment_id == segment_id)
        )).scalar_one()
        segment.contact_count = count
        await self.session.commit()

    async def get_segment_members(self, segment_id: int) -> list:
        result = await self.session.execute(
            select(SegmentMembership).where(SegmentMembership.segment_id == segment_id).order_by(SegmentMembership.id)
        )
        return list(result.scalars().all())


class LeadScoringService:
    """Lead scoring service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_lead_score(self, user_id: int) -> LeadScore:
        score = (await self.session.execute(
            select(LeadScore).where(LeadScore.user_id == user_id)
        )).scalar_one_or_none()
        if score is None:
            score = LeadScore(user_id=user_id)
            self.session.add(score)
            await self.session.commit()
            await self.session.refresh(score)
        return score

    async def update_lead_score(self, user_id: int, engagement: int = 0, purchase: int = 0, behavior: int = 0) -> None:
        score = await self.get_or_create_lead_score(user_id)
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
        await self.session.commit()


class AutomationService:
    """Email automation service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_workflow(self, org_id: int, workflow_data: dict) -> AutomationWorkflow:
        workflow = AutomationWorkflow(organization_id=org_id, **workflow_data)
        self.session.add(workflow)
        await self.session.commit()
        await self.session.refresh(workflow)
        return workflow

    async def get_workflow(self, workflow_id: int) -> Optional[AutomationWorkflow]:
        return await self.session.get(AutomationWorkflow, workflow_id)


class AnalyticsService:
    """Marketing analytics service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_metric(self, campaign_id: int, metric_data: dict) -> EmailMetric:
        metric = EmailMetric(campaign_id=campaign_id, metric_date=datetime.now(timezone.utc), **metric_data)
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric


class ABTestingService:
    """A/B testing service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_test(self, org_id: int, test_data: dict) -> ABTest:
        test = ABTest(organization_id=org_id, **test_data)
        self.session.add(test)
        await self.session.commit()
        await self.session.refresh(test)
        return test


class LoyaltyService:
    """Loyalty program service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_program(self, org_id: int, program_data: dict) -> LoyaltyProgram:
        program = LoyaltyProgram(organization_id=org_id, **program_data)
        self.session.add(program)
        await self.session.commit()
        await self.session.refresh(program)
        return program

    async def enroll_member(self, program_id: int, user_id: int) -> LoyaltyMember:
        program = await self.session.get(LoyaltyProgram, program_id)
        if program is None:
            raise NotFoundError("Loyalty program")
        member = LoyaltyMember(program_id=program_id, user_id=user_id, member_id=str(uuid.uuid4()))
        self.session.add(member)
        program.total_members += 1
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def _member(self, member_id: int) -> LoyaltyMember:
        member = await self.session.get(LoyaltyMember, member_id)
        if member is None:
            raise NotFoundError("Loyalty member")
        return member

    async def add_points(self, member_id: int, points: int, reason: str) -> None:
        member = await self._member(member_id)
        member.total_points += points
        member.available_points += points
        self.session.add(LoyaltyTransaction(
            member_id=member_id, transaction_type="earn", points=points, reason=reason,
        ))
        program = await self.session.get(LoyaltyProgram, member.program_id)
        program.total_points_distributed += points
        await self.session.commit()

    async def redeem_points(self, member_id: int, points: int, reason: str) -> None:
        member = await self._member(member_id)
        if member.available_points < points:
            raise ValueError("Insufficient points")
        member.available_points -= points
        member.redeemed_points += points
        self.session.add(LoyaltyTransaction(
            member_id=member_id, transaction_type="redeem", points=points, reason=reason,
        ))
        await self.session.commit()

