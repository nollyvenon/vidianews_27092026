"""Membership models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum
from app.db.base import Base


class MembershipTier(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class MembershipType(Base):
    __tablename__ = "membership_types"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    name = Column(String(255), nullable=False)
    tier = Column(SQLEnum(MembershipTier), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0.0)
    billing_cycle = Column(SQLEnum(BillingCycle), default=BillingCycle.MONTHLY)
    max_courses = Column(Integer, default=-1)
    max_students = Column(Integer, default=-1)
    features = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    subscriptions = relationship("MembershipSubscription", back_populates="membership_type")


class MembershipSubscription(Base):
    __tablename__ = "membership_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    membership_type_id = Column(Integer, ForeignKey("membership_types.id"), nullable=False, index=True)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    renewal_date = Column(DateTime)
    stripe_subscription_id = Column(String(255), unique=True, index=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User")
    membership_type = relationship("MembershipType", back_populates="subscriptions")
    invoices = relationship("MembershipInvoice", back_populates="subscription")
    payment_methods = relationship("MembershipPaymentMethod", back_populates="subscription")


class MembershipInvoice(Base):
    __tablename__ = "membership_invoices"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("membership_subscriptions.id"), nullable=False, index=True)
    invoice_number = Column(String(255), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime)
    stripe_invoice_id = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    subscription = relationship("MembershipSubscription", back_populates="invoices")


class MembershipPaymentMethod(Base):
    __tablename__ = "membership_payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("membership_subscriptions.id"), nullable=False, index=True)
    card_brand = Column(String(50))
    card_last_four = Column(String(4))
    stripe_payment_method_id = Column(String(255), unique=True, index=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    subscription = relationship("MembershipSubscription", back_populates="payment_methods")
