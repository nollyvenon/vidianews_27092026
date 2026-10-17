"""API v1 router"""

from fastapi import APIRouter

# Import endpoints
from app.api.v1 import auth, health, tenants, organizations, profiles, settings, notifications, activity, content, ai_providers, ai_core, ai_advanced, integrations, advanced_features, monetization, security_performance, api_monitoring, logging_analytics, social_messaging, streaming_premium, community_compliance, content_quality, publishing_distribution, user_management, enterprise_features, analytics_reporting, platform_completion, advanced_platform, ecommerce, ecommerce_extended, marketing, memberships, courses, analytics_admin

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
# These modules expose several named routers (each with its own tags) instead of one `router`.
for _sub_router in (
    user_management.email_router, user_management.segment_router, user_management.subscriber_router,
    user_management.notification_router, user_management.webhook_router,
    user_management.api_key_router, user_management.personalization_router,
):
    api_router.include_router(_sub_router)
for _sub_router in (
    enterprise_features.security_router, enterprise_features.moderation_router,
    enterprise_features.rate_limit_router, enterprise_features.notification_router,
    enterprise_features.reporting_router,
):
    api_router.include_router(_sub_router)
for _sub_router in (
    analytics_reporting.analytics_router, analytics_reporting.behavior_router,
    analytics_reporting.heatmap_router, analytics_reporting.search_router,
    analytics_reporting.cache_router, analytics_reporting.performance_router,
    analytics_reporting.admin_router, analytics_reporting.featureflag_router,
):
    api_router.include_router(_sub_router)
api_router.include_router(platform_completion.router, tags=["platform-completion"])
for _sub_router in (
    advanced_platform.websocket_router, advanced_platform.jobs_router,
    advanced_platform.pipeline_router, advanced_platform.cache_router,
    advanced_platform.api_docs_router,
):
    api_router.include_router(_sub_router)
api_router.include_router(ecommerce.router, tags=["ecommerce"])
api_router.include_router(ecommerce_extended.router, tags=["ecommerce-extended"])
api_router.include_router(marketing.router, tags=["marketing"])
api_router.include_router(memberships.router, tags=["memberships"])
api_router.include_router(courses.router, tags=["courses"])
api_router.include_router(analytics_admin.router, tags=["analytics-admin"])

__all__ = ["api_router"]
