"""Membership and subscription services"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.memberships import (
    MembershipType, MembershipSubscription, MembershipInvoice, MembershipPaymentMethod
)
from datetime import datetime, timezone, timedelta
import uuid


class MembershipTypeService:
    @staticmethod
    def create_membership_type(db: Session, org_id: int, type_data: dict) -> MembershipType:
        membership = MembershipType(organization_id=org_id, **type_data)
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership

    @staticmethod
    def get_membership_type(db: Session, membership_id: int) -> MembershipType:
        return db.query(MembershipType).filter(MembershipType.id == membership_id).first()

    @staticmethod
    def list_membership_types(db: Session, org_id: int):
        return db.query(MembershipType).filter(
            and_(MembershipType.organization_id == org_id, MembershipType.is_active == True)
        ).all()

    @staticmethod
    def update_membership_type(db: Session, membership_id: int, update_data: dict) -> MembershipType:
        membership = MembershipTypeService.get_membership_type(db, membership_id)
        for key, value in update_data.items():
            setattr(membership, key, value)
        membership.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(membership)
        return membership


class MembershipSubscriptionService:
    @staticmethod
    def subscribe_user(db: Session, user_id: int, membership_type_id: int,
                      stripe_subscription_id: str = None) -> MembershipSubscription:
        membership_type = db.query(MembershipType).filter(MembershipType.id == membership_type_id).first()
        start_date = datetime.now(timezone.utc)

        if membership_type.billing_cycle.value == "monthly":
            renewal_date = start_date + timedelta(days=30)
        elif membership_type.billing_cycle.value == "quarterly":
            renewal_date = start_date + timedelta(days=90)
        else:
            renewal_date = start_date + timedelta(days=365)

        subscription = MembershipSubscription(
            user_id=user_id,
            membership_type_id=membership_type_id,
            start_date=start_date,
            renewal_date=renewal_date,
            stripe_subscription_id=stripe_subscription_id
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def get_active_subscription(db: Session, user_id: int) -> MembershipSubscription:
        return db.query(MembershipSubscription).filter(
            and_(
                MembershipSubscription.user_id == user_id,
                MembershipSubscription.status == "active"
            )
        ).first()

    @staticmethod
    def cancel_subscription(db: Session, subscription_id: int):
        subscription = db.query(MembershipSubscription).filter(
            MembershipSubscription.id == subscription_id
        ).first()
        subscription.status = "cancelled"
        subscription.end_date = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def renew_subscription(db: Session, subscription_id: int):
        subscription = db.query(MembershipSubscription).filter(
            MembershipSubscription.id == subscription_id
        ).first()
        subscription.status = "active"
        subscription.start_date = subscription.renewal_date

        membership_type = subscription.membership_type
        if membership_type.billing_cycle.value == "monthly":
            subscription.renewal_date = subscription.renewal_date + timedelta(days=30)
        elif membership_type.billing_cycle.value == "quarterly":
            subscription.renewal_date = subscription.renewal_date + timedelta(days=90)
        else:
            subscription.renewal_date = subscription.renewal_date + timedelta(days=365)

        db.commit()

    @staticmethod
    def pause_subscription(db: Session, subscription_id: int):
        subscription = db.query(MembershipSubscription).filter(
            MembershipSubscription.id == subscription_id
        ).first()
        subscription.status = "paused"
        db.commit()


class MembershipInvoiceService:
    @staticmethod
    def create_invoice(db: Session, subscription_id: int, amount: float,
                      stripe_invoice_id: str = None) -> MembershipInvoice:
        subscription = db.query(MembershipSubscription).filter(
            MembershipSubscription.id == subscription_id
        ).first()

        invoice_number = f"INV-{int(datetime.now(timezone.utc).timestamp())}"
        tax_amount = amount * 0.1

        invoice = MembershipInvoice(
            subscription_id=subscription_id,
            invoice_number=invoice_number,
            amount=amount,
            tax_amount=tax_amount,
            total_amount=amount + tax_amount,
            due_date=datetime.now(timezone.utc) + timedelta(days=30),
            stripe_invoice_id=stripe_invoice_id
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def mark_invoice_paid(db: Session, invoice_id: int):
        invoice = db.query(MembershipInvoice).filter(MembershipInvoice.id == invoice_id).first()
        invoice.status = "paid"
        invoice.paid_date = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def get_subscription_invoices(db: Session, subscription_id: int):
        return db.query(MembershipInvoice).filter(
            MembershipInvoice.subscription_id == subscription_id
        ).order_by(MembershipInvoice.created_at.desc()).all()


class MembershipPaymentMethodService:
    @staticmethod
    def add_payment_method(db: Session, subscription_id: int, card_brand: str,
                          card_last_four: str, stripe_payment_method_id: str) -> MembershipPaymentMethod:
        payment_method = MembershipPaymentMethod(
            subscription_id=subscription_id,
            card_brand=card_brand,
            card_last_four=card_last_four,
            stripe_payment_method_id=stripe_payment_method_id,
            is_default=True
        )
        db.add(payment_method)

        db.query(MembershipPaymentMethod).filter(
            and_(
                MembershipPaymentMethod.subscription_id == subscription_id,
                MembershipPaymentMethod.id != payment_method.id
            )
        ).update({"is_default": False})

        db.commit()
        db.refresh(payment_method)
        return payment_method

    @staticmethod
    def get_payment_methods(db: Session, subscription_id: int):
        return db.query(MembershipPaymentMethod).filter(
            MembershipPaymentMethod.subscription_id == subscription_id
        ).all()

    @staticmethod
    def set_default_payment_method(db: Session, payment_method_id: int):
        payment_method = db.query(MembershipPaymentMethod).filter(
            MembershipPaymentMethod.id == payment_method_id
        ).first()

        db.query(MembershipPaymentMethod).filter(
            MembershipPaymentMethod.subscription_id == payment_method.subscription_id
        ).update({"is_default": False})

        payment_method.is_default = True
        db.commit()
