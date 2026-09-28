"""Services module"""

from .auth_service import AuthService
from .content_quality_service import (
    ContentCalendarService,
    ProofreadingService,
    PlagiarismDetectionService,
    ReadabilityService,
    BrandVoiceService
)
from .ecommerce_service import (
    ProductService,
    CartService,
    CheckoutService,
    PaymentService,
    OrderService
)
from .ecommerce_extended_service import (
    ShippingService,
    InventoryService,
    WishlistService,
    ReturnService
)
from .marketing_service import (
    EmailCampaignService,
    SegmentationService,
    LeadScoringService,
    AutomationService,
    AnalyticsService,
    ABTestingService,
    LoyaltyService
)
from .memberships_service import (
    MembershipTypeService,
    MembershipSubscriptionService,
    MembershipInvoiceService,
    MembershipPaymentMethodService
)
from .courses_service import (
    CourseService,
    LessonService,
    CourseSectionService,
    EnrollmentService,
    StudentLessonProgressService,
    CourseReviewService,
    AssignmentService,
    AssignmentSubmissionService,
    CertificateService
)

__all__ = [
    "AuthService",
    "ContentCalendarService",
    "ProofreadingService",
    "PlagiarismDetectionService",
    "ReadabilityService",
    "BrandVoiceService",
    "ProductService",
    "CartService",
    "CheckoutService",
    "PaymentService",
    "OrderService",
    "ShippingService",
    "InventoryService",
    "WishlistService",
    "ReturnService",
    "EmailCampaignService",
    "SegmentationService",
    "LeadScoringService",
    "AutomationService",
    "AnalyticsService",
    "ABTestingService",
    "LoyaltyService",
    "MembershipTypeService",
    "MembershipSubscriptionService",
    "MembershipInvoiceService",
    "MembershipPaymentMethodService",
    "CourseService",
    "LessonService",
    "CourseSectionService",
    "EnrollmentService",
    "StudentLessonProgressService",
    "CourseReviewService",
    "AssignmentService",
    "AssignmentSubmissionService",
    "CertificateService"
]
