"""AI Provider service for managing providers and making API calls"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import httpx
import json
from app.models.ai_providers import (
    AIProvider, AIProviderAPIKey, AIModel, AIModelCall, ProviderUsage,
    ProviderType, ModelFamily, APIKeyStatus
)
from app.models.user import User
import math


class AIProviderService:
    """Service for managing AI providers and making API calls"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Provider Management
    async def create_provider(self, name: str, slug: str, provider_type: ProviderType,
                             api_url: str, **kwargs) -> AIProvider:
        """Create new AI provider"""
        provider = AIProvider(
            name=name,
            slug=slug,
            provider_type=provider_type,
            api_url=api_url,
            **kwargs
        )
        self.session.add(provider)
        await self.session.commit()
        await self.session.refresh(provider)
        return provider

    async def get_provider(self, provider_id: int) -> Optional[AIProvider]:
        """Get provider by ID"""
        stmt = select(AIProvider).where(AIProvider.id == provider_id)
        stmt = stmt.options(selectinload(AIProvider.api_keys), selectinload(AIProvider.models))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_provider_by_slug(self, slug: str) -> Optional[AIProvider]:
        """Get provider by slug"""
        stmt = select(AIProvider).where(AIProvider.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_providers(self, is_active: bool = True) -> List[AIProvider]:
        """Get all active providers"""
        stmt = select(AIProvider).where(AIProvider.is_active == is_active).order_by(AIProvider.priority.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_providers_by_type(self, provider_type: ProviderType) -> List[AIProvider]:
        """Get providers by type"""
        stmt = select(AIProvider).where(
            and_(AIProvider.provider_type == provider_type, AIProvider.is_active == True)
        ).order_by(AIProvider.priority.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_provider(self, provider_id: int, **kwargs) -> Optional[AIProvider]:
        """Update provider"""
        stmt = update(AIProvider).where(AIProvider.id == provider_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_provider(provider_id)

    async def delete_provider(self, provider_id: int) -> bool:
        """Delete provider"""
        stmt = delete(AIProvider).where(AIProvider.id == provider_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # API Key Management
    async def add_api_key(self, provider_id: int, key_name: str, key_value: str,
                         is_primary: bool = False, **kwargs) -> AIProviderAPIKey:
        """Add API key for provider"""
        api_key = AIProviderAPIKey(
            provider_id=provider_id,
            key_name=key_name,
            key_value=key_value,
            is_primary=is_primary,
            **kwargs
        )
        self.session.add(api_key)
        await self.session.commit()
        await self.session.refresh(api_key)
        return api_key

    async def get_api_key(self, key_id: int) -> Optional[AIProviderAPIKey]:
        """Get API key"""
        stmt = select(AIProviderAPIKey).where(AIProviderAPIKey.id == key_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_api_key(self, provider_id: int) -> Optional[AIProviderAPIKey]:
        """Get primary active API key for provider"""
        stmt = select(AIProviderAPIKey).where(
            and_(
                AIProviderAPIKey.provider_id == provider_id,
                AIProviderAPIKey.status == APIKeyStatus.ACTIVE,
                AIProviderAPIKey.is_primary == True
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_provider_api_keys(self, provider_id: int) -> List[AIProviderAPIKey]:
        """Get all API keys for provider"""
        stmt = select(AIProviderAPIKey).where(AIProviderAPIKey.provider_id == provider_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def revoke_api_key(self, key_id: int) -> bool:
        """Revoke API key"""
        stmt = update(AIProviderAPIKey).where(AIProviderAPIKey.id == key_id).values(
            status=APIKeyStatus.REVOKED
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Model Management
    async def register_model(self, provider_id: int, name: str, model_id: str,
                            family: ModelFamily, **kwargs) -> AIModel:
        """Register new AI model"""
        model = AIModel(
            provider_id=provider_id,
            name=name,
            model_id=model_id,
            family=family,
            **kwargs
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_model(self, model_id: int) -> Optional[AIModel]:
        """Get model by ID"""
        stmt = select(AIModel).where(AIModel.id == model_id)
        stmt = stmt.options(selectinload(AIModel.provider))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_models_by_family(self, family: ModelFamily) -> List[AIModel]:
        """Get models by family"""
        stmt = select(AIModel).where(
            and_(AIModel.family == family, AIModel.is_available == True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_available_models(self, provider_id: Optional[int] = None) -> List[AIModel]:
        """Get available models"""
        conditions = [AIModel.is_available == True]
        if provider_id:
            conditions.append(AIModel.provider_id == provider_id)

        stmt = select(AIModel).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_model(self, model_id: int, **kwargs) -> Optional[AIModel]:
        """Update model"""
        stmt = update(AIModel).where(AIModel.id == model_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_model(model_id)

    async def deprecate_model(self, model_id: int) -> Optional[AIModel]:
        """Deprecate model"""
        return await self.update_model(
            model_id,
            is_deprecated=True,
            deprecation_date=datetime.now(timezone.utc)
        )

    # Model Calls and Usage
    async def record_model_call(self, model_id: int, user_id: Optional[int],
                               request_tokens: int, response_tokens: int,
                               duration_ms: int, status: str = "success",
                               **kwargs) -> AIModelCall:
        """Record API call to model"""
        total_tokens = request_tokens + response_tokens

        # Get model to calculate cost
        model = await self.get_model(model_id)
        input_cost = (request_tokens / 1000) * (model.input_cost or 0.0)
        output_cost = (response_tokens / 1000) * (model.output_cost or 0.0)
        total_cost = input_cost + output_cost

        call = AIModelCall(
            model_id=model_id,
            user_id=user_id,
            request_tokens=request_tokens,
            response_tokens=response_tokens,
            total_tokens=total_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            duration_ms=duration_ms,
            status=status,
            **kwargs
        )
        self.session.add(call)

        # Update model totals
        await self.update_model(
            model_id,
            total_calls=model.total_calls + 1,
            total_tokens=model.total_tokens + total_tokens
        )

        # Update provider totals
        provider = model.provider
        await self.update_provider(
            provider.id,
            total_requests=provider.total_requests + 1,
            total_tokens=provider.total_tokens + total_tokens,
            total_cost=provider.total_cost + total_cost
        )

        await self.session.commit()
        await self.session.refresh(call)
        return call

    async def get_model_calls(self, model_id: int, limit: int = 100) -> List[AIModelCall]:
        """Get calls for model"""
        stmt = select(AIModelCall).where(AIModelCall.model_id == model_id).order_by(
            desc(AIModelCall.created_at)
        ).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_calls(self, user_id: int, limit: int = 100) -> List[AIModelCall]:
        """Get calls by user"""
        stmt = select(AIModelCall).where(AIModelCall.user_id == user_id).order_by(
            desc(AIModelCall.created_at)
        ).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Usage Analytics
    async def get_provider_usage(self, provider_id: int, days: int = 30) -> List[ProviderUsage]:
        """Get usage stats for provider"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(ProviderUsage).where(
            and_(
                ProviderUsage.provider_id == provider_id,
                ProviderUsage.usage_date >= cutoff
            )
        ).order_by(desc(ProviderUsage.usage_date))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def record_daily_usage(self, provider_id: int, usage_date: datetime,
                                 **stats) -> ProviderUsage:
        """Record daily usage statistics"""
        usage = ProviderUsage(
            provider_id=provider_id,
            usage_date=usage_date,
            **stats
        )
        self.session.add(usage)
        await self.session.commit()
        await self.session.refresh(usage)
        return usage

    async def get_usage_stats(self, provider_id: int, days: int = 7) -> Dict[str, Any]:
        """Get aggregated usage stats"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = select(
            func.sum(ProviderUsage.total_requests).label("total_requests"),
            func.sum(ProviderUsage.total_tokens).label("total_tokens"),
            func.sum(ProviderUsage.total_cost).label("total_cost"),
            func.avg(ProviderUsage.avg_latency_ms).label("avg_latency")
        ).where(
            and_(
                ProviderUsage.provider_id == provider_id,
                ProviderUsage.usage_date >= cutoff
            )
        )

        result = await self.session.execute(stmt)
        row = result.one()

        return {
            "period_days": days,
            "total_requests": row.total_requests or 0,
            "total_tokens": row.total_tokens or 0,
            "total_cost": row.total_cost or 0.0,
            "avg_latency_ms": row.avg_latency or 0.0
        }

    async def get_cost_breakdown(self, provider_id: int, days: int = 30) -> Dict[str, float]:
        """Get cost breakdown by model"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = select(
            AIModel.name,
            func.sum(AIModelCall.total_cost).label("cost")
        ).join(AIModelCall).where(
            and_(
                AIModel.provider_id == provider_id,
                AIModelCall.created_at >= cutoff
            )
        ).group_by(AIModel.name)

        result = await self.session.execute(stmt)
        return {name: cost for name, cost in result}

    # Provider Capabilities
    async def get_best_provider_for_task(self, requires_streaming: bool = False,
                                         requires_vision: bool = False,
                                         requires_function_calling: bool = False) -> Optional[AIProvider]:
        """Find best provider for specific task"""
        conditions = [AIProvider.is_active == True]

        if requires_streaming:
            conditions.append(AIProvider.supports_streaming == True)
        if requires_vision:
            conditions.append(AIProvider.supports_vision == True)
        if requires_function_calling:
            conditions.append(AIProvider.supports_function_calling == True)

        stmt = select(AIProvider).where(and_(*conditions)).order_by(
            AIProvider.priority.desc(),
            AIProvider.total_cost.asc()
        ).limit(1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_model_comparison(self, model_ids: List[int]) -> Dict[int, Dict[str, Any]]:
        """Compare multiple models"""
        result_dict = {}
        for model_id in model_ids:
            model = await self.get_model(model_id)
            if model:
                result_dict[model_id] = {
                    "name": model.name,
                    "family": model.family.value,
                    "context_window": model.context_window,
                    "input_cost": model.input_cost,
                    "output_cost": model.output_cost,
                    "total_calls": model.total_calls,
                    "total_tokens": model.total_tokens
                }
        return result_dict

    # Rate Limiting
    async def check_rate_limit(self, provider_id: int, api_key_id: int) -> bool:
        """Check if rate limit exceeded"""
        key = await self.get_api_key(api_key_id)
        if not key:
            return False

        provider = await self.get_provider(provider_id)
        return key.current_requests_today < provider.requests_per_day

    async def increment_rate_limit(self, api_key_id: int) -> None:
        """Increment daily request counter"""
        stmt = update(AIProviderAPIKey).where(
            AIProviderAPIKey.id == api_key_id
        ).values(
            current_requests_today=AIProviderAPIKey.current_requests_today + 1,
            last_request_at=datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def reset_daily_limits(self) -> None:
        """Reset daily rate limits (call once per day)"""
        stmt = update(AIProviderAPIKey).values(current_requests_today=0)
        await self.session.execute(stmt)
        await self.session.commit()

    # Statistics
    async def get_provider_stats(self, provider_id: int) -> Dict[str, Any]:
        """Get overall provider statistics"""
        provider = await self.get_provider(provider_id)
        if not provider:
            return {}

        # Get models
        models_stmt = select(func.count(AIModel.id)).where(AIModel.provider_id == provider_id)
        model_count = await self.session.scalar(models_stmt)

        # Get recent calls
        calls_stmt = select(func.count(AIModelCall.id)).where(
            AIModelCall.model_id.in_(
                select(AIModel.id).where(AIModel.provider_id == provider_id)
            )
        )
        call_count = await self.session.scalar(calls_stmt)

        return {
            "provider_id": provider.id,
            "name": provider.name,
            "type": provider.provider_type.value,
            "is_active": provider.is_active,
            "models": model_count,
            "total_calls": call_count,
            "total_tokens": provider.total_tokens,
            "total_cost": provider.total_cost,
            "requests_per_minute": provider.requests_per_minute,
            "requests_per_day": provider.requests_per_day
        }

    async def count_total_providers(self, is_active: bool = True) -> int:
        """Count total providers"""
        stmt = select(func.count(AIProvider.id))
        if is_active is not None:
            stmt = stmt.where(AIProvider.is_active == is_active)
        return await self.session.scalar(stmt)
