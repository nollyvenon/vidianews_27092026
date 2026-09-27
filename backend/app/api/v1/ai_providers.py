"""AI Provider management API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.ai_providers import ProviderType, ModelFamily, APIKeyStatus
from app.services.ai_provider_service import AIProviderService
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai-providers", tags=["ai-providers"])

# Schemas
class ProviderCreate(BaseModel):
    name: str
    slug: str
    provider_type: ProviderType
    api_url: str
    api_version: Optional[str] = None
    requests_per_minute: int = 60
    supports_streaming: bool = False
    supports_function_calling: bool = False
    supports_vision: bool = False

class ProviderResponse(BaseModel):
    id: int
    name: str
    slug: str
    provider_type: str
    description: Optional[str]
    is_active: bool
    total_requests: int
    total_tokens: int
    total_cost: float
    created_at: datetime

    class Config:
        from_attributes = True

class APIKeyCreate(BaseModel):
    key_name: str
    key_value: str
    is_primary: bool = False

class APIKeyResponse(BaseModel):
    id: int
    key_name: str
    status: str
    is_primary: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ModelCreate(BaseModel):
    name: str
    model_id: str
    family: ModelFamily
    context_window: Optional[int] = None
    input_cost: float = 0.0
    output_cost: float = 0.0
    supports_vision: bool = False
    supports_streaming: bool = False

class ModelResponse(BaseModel):
    id: int
    name: str
    model_id: str
    family: str
    provider_id: int
    context_window: Optional[int]
    input_cost: float
    output_cost: float
    is_available: bool
    total_calls: int
    created_at: datetime

    class Config:
        from_attributes = True

# Provider Endpoints
@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(req: ProviderCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create new AI provider"""
    service = AIProviderService(session)
    return await service.create_provider(**req.model_dump())

@router.get("/", response_model=List[ProviderResponse])
async def list_providers(is_active: bool = Query(True), session: AsyncSession = Depends(get_db)):
    """List AI providers"""
    service = AIProviderService(session)
    return await service.get_providers(is_active=is_active)

@router.get("/by-type/{provider_type}", response_model=List[ProviderResponse])
async def get_providers_by_type(provider_type: ProviderType, session: AsyncSession = Depends(get_db)):
    """Get providers by type"""
    service = AIProviderService(session)
    return await service.get_providers_by_type(provider_type)

@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(provider_id: int, session: AsyncSession = Depends(get_db)):
    """Get provider by ID"""
    service = AIProviderService(session)
    provider = await service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return provider

@router.put("/{provider_id}", response_model=ProviderResponse)
async def update_provider(provider_id: int, updates: dict, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Update provider"""
    service = AIProviderService(session)
    provider = await service.update_provider(provider_id, **updates)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return provider

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider(provider_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Delete provider"""
    service = AIProviderService(session)
    if not await service.delete_provider(provider_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# API Key Endpoints
@router.post("/{provider_id}/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def add_api_key(provider_id: int, req: APIKeyCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add API key"""
    service = AIProviderService(session)
    provider = await service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.add_api_key(provider_id, req.key_name, req.key_value, req.is_primary)

@router.get("/{provider_id}/api-keys", response_model=List[APIKeyResponse])
async def get_provider_keys(provider_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get API keys for provider"""
    service = AIProviderService(session)
    return await service.get_provider_api_keys(provider_id)

@router.delete("/{provider_id}/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(provider_id: int, key_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Revoke API key"""
    service = AIProviderService(session)
    if not await service.revoke_api_key(key_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Model Endpoints
@router.post("/{provider_id}/models", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def register_model(provider_id: int, req: ModelCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Register new model"""
    service = AIProviderService(session)
    return await service.register_model(provider_id, req.name, req.model_id, req.family, **req.model_dump(exclude={"name", "model_id", "family"}))

@router.get("/{provider_id}/models", response_model=List[ModelResponse])
async def get_provider_models(provider_id: int, session: AsyncSession = Depends(get_db)):
    """Get models for provider"""
    service = AIProviderService(session)
    return await service.get_available_models(provider_id)

@router.get("/models/by-family/{family}", response_model=List[ModelResponse])
async def get_models_by_family(family: ModelFamily, session: AsyncSession = Depends(get_db)):
    """Get models by family"""
    service = AIProviderService(session)
    return await service.get_models_by_family(family)

@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, session: AsyncSession = Depends(get_db)):
    """Get model details"""
    service = AIProviderService(session)
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return model

@router.post("/models/{model_id}/deprecate", status_code=status.HTTP_200_OK)
async def deprecate_model(model_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Deprecate model"""
    service = AIProviderService(session)
    model = await service.deprecate_model(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return model

# Usage and Analytics
@router.get("/{provider_id}/stats", response_model=dict)
async def get_provider_stats(provider_id: int, session: AsyncSession = Depends(get_db)):
    """Get provider statistics"""
    service = AIProviderService(session)
    stats = await service.get_provider_stats(provider_id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return stats

@router.get("/{provider_id}/usage", response_model=dict)
async def get_usage_stats(provider_id: int, days: int = Query(7, ge=1, le=365), session: AsyncSession = Depends(get_db)):
    """Get usage statistics"""
    service = AIProviderService(session)
    return await service.get_usage_stats(provider_id, days)

@router.get("/{provider_id}/costs", response_model=dict)
async def get_cost_breakdown(provider_id: int, days: int = Query(30, ge=1, le=365), session: AsyncSession = Depends(get_db)):
    """Get cost breakdown"""
    service = AIProviderService(session)
    return await service.get_cost_breakdown(provider_id, days)

# Comparison and Selection
@router.post("/compare", response_model=dict)
async def compare_models(model_ids: List[int], session: AsyncSession = Depends(get_db)):
    """Compare multiple models"""
    service = AIProviderService(session)
    return await service.get_model_comparison(model_ids)

@router.post("/best-for-task", response_model=Optional[ProviderResponse])
async def get_best_provider(
    requires_streaming: bool = False,
    requires_vision: bool = False,
    requires_function_calling: bool = False,
    session: AsyncSession = Depends(get_db)
):
    """Find best provider for task"""
    service = AIProviderService(session)
    return await service.get_best_provider_for_task(
        requires_streaming, requires_vision, requires_function_calling
    )
