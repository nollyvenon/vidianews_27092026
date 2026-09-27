"""API v1 router"""

from fastapi import APIRouter

# Import endpoints
from app.api.v1 import auth, health, tenants

api_router = APIRouter()

# Include routes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tenants.router, tags=["tenants"])

__all__ = ["api_router"]
