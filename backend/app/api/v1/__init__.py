"""API v1 router"""

from fastapi import APIRouter

# Import endpoints
from app.api.v1 import auth, health, tenants, organizations, profiles, settings, notifications, activity, content, ai_providers, ai_core, ai_advanced, integrations, advanced_features, monetization, security_performance, api_monitoring, logging_analytics, social_messaging, streaming_premium, community_compliance, content_quality, publishing_distribution, user_management, enterprise_features, analytics_reporting, platform_completion, advanced_platform, ecommerce

api_router = APIRouter()

# Include routes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tenants.router, tags=["tenants"])
api_router.include_router(organizations.router, tags=["organizations"])
api_router.include_router(profiles.router, tags=["profiles"])
api_router.include_router(settings.router, tags=["settings"])
api_router.include_router(notifications.router, tags=["notifications"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(content.router, tags=["content"])
api_router.include_router(ai_providers.router, tags=["ai-providers"])
api_router.include_router(ai_core.router, tags=["ai-core"])
api_router.include_router(ai_advanced.router, tags=["ai-advanced"])
api_router.include_router(integrations.router, tags=["system"])
api_router.include_router(advanced_features.router, tags=["advanced"])
api_router.include_router(monetization.router, tags=["monetization"])
api_router.include_router(security_performance.router, tags=["security"])
api_router.include_router(api_monitoring.router, tags=["api-monitoring"])
api_router.include_router(logging_analytics.router, tags=["logging-analytics"])
api_router.include_router(social_messaging.router, tags=["social-messaging"])
api_router.include_router(streaming_premium.router, tags=["streaming-premium"])
api_router.include_router(community_compliance.router, tags=["community-compliance"])
api_router.include_router(content_quality.router, tags=["content-quality"])
api_router.include_router(publishing_distribution.router, tags=["publishing-distribution"])
api_router.include_router(user_management.router, tags=["user-management"])
api_router.include_router(enterprise_features.router, tags=["enterprise-features"])
api_router.include_router(analytics_reporting.router, tags=["analytics-reporting"])
api_router.include_router(platform_completion.router, tags=["platform-completion"])
api_router.include_router(advanced_platform.router, tags=["advanced-platform"])
api_router.include_router(ecommerce.router, tags=["ecommerce"])

__all__ = ["api_router"]
