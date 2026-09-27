"""API v1 router"""

from fastapi import APIRouter

# Import endpoints
from app.api.v1 import auth, health, tenants, organizations, profiles, settings, notifications, activity

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

__all__ = ["api_router"]
