"""API v1 router"""

from fastapi import APIRouter

# Import endpoints
from app.api.v1 import auth, health, tenants, organizations, profiles, settings, notifications, activity, content, ai_providers, ai_core, ai_advanced, integrations, advanced_features, monetization

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

__all__ = ["api_router"]
