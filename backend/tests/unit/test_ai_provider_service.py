"""Tests for AI provider service"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.ai_providers import (
    AIProvider, AIProviderAPIKey, AIModel, ProviderType, ModelFamily, APIKeyStatus
)
from app.services.ai_provider_service import AIProviderService
from app.db.base import Base


@pytest.fixture
async def db_session():
    """Create test database"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def service(db_session):
    """Create service"""
    return AIProviderService(db_session)


class TestProviderManagement:
    """Test provider CRUD operations"""

    async def test_create_provider(self, service):
        """Test creating provider"""
        provider = await service.create_provider(
            name="OpenAI",
            slug="openai",
            provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        assert provider.id is not None
        assert provider.name == "OpenAI"

    async def test_get_provider(self, service):
        """Test getting provider"""
        created = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        fetched = await service.get_provider(created.id)
        assert fetched.name == "OpenAI"

    async def test_get_providers(self, service):
        """Test listing providers"""
        await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        await service.create_provider(
            name="Claude", slug="claude", provider_type=ProviderType.ANTHROPIC,
            api_url="https://api.anthropic.com"
        )
        providers = await service.get_providers()
        assert len(providers) >= 2

    async def test_update_provider(self, service):
        """Test updating provider"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        updated = await service.update_provider(provider.id, is_active=False)
        assert updated.is_active is False

    async def test_delete_provider(self, service):
        """Test deleting provider"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        deleted = await service.delete_provider(provider.id)
        assert deleted is True


class TestAPIKeyManagement:
    """Test API key operations"""

    async def test_add_api_key(self, service):
        """Test adding API key"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        key = await service.add_api_key(
            provider.id, "test_key", "sk-test123", is_primary=True
        )
        assert key.id is not None
        assert key.key_name == "test_key"

    async def test_get_active_api_key(self, service):
        """Test getting active API key"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        await service.add_api_key(
            provider.id, "primary", "sk-primary", is_primary=True
        )
        key = await service.get_active_api_key(provider.id)
        assert key is not None
        assert key.is_primary is True

    async def test_revoke_api_key(self, service):
        """Test revoking API key"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        key = await service.add_api_key(
            provider.id, "test", "sk-test", is_primary=True
        )
        revoked = await service.revoke_api_key(key.id)
        assert revoked is True


class TestModelManagement:
    """Test model registration and management"""

    async def test_register_model(self, service):
        """Test registering model"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        model = await service.register_model(
            provider.id, "GPT-4", "gpt-4", ModelFamily.GPT,
            context_window=8192, input_cost=0.03, output_cost=0.06
        )
        assert model.id is not None
        assert model.name == "GPT-4"

    async def test_get_available_models(self, service):
        """Test getting available models"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        await service.register_model(
            provider.id, "GPT-4", "gpt-4", ModelFamily.GPT
        )
        models = await service.get_available_models(provider.id)
        assert len(models) >= 1

    async def test_get_models_by_family(self, service):
        """Test getting models by family"""
        provider = await service.create_provider(
            name="Anthropic", slug="anthropic", provider_type=ProviderType.ANTHROPIC,
            api_url="https://api.anthropic.com"
        )
        await service.register_model(
            provider.id, "Claude 3", "claude-3", ModelFamily.CLAUDE
        )
        models = await service.get_models_by_family(ModelFamily.CLAUDE)
        assert len(models) >= 1

    async def test_deprecate_model(self, service):
        """Test deprecating model"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        model = await service.register_model(
            provider.id, "GPT-3.5", "gpt-3.5-turbo", ModelFamily.GPT
        )
        deprecated = await service.deprecate_model(model.id)
        assert deprecated.is_deprecated is True


class TestUsageTracking:
    """Test usage and analytics"""

    async def test_record_model_call(self, service):
        """Test recording model call"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        model = await service.register_model(
            provider.id, "GPT-4", "gpt-4", ModelFamily.GPT,
            input_cost=0.03, output_cost=0.06
        )
        call = await service.record_model_call(
            model.id, user_id=1, request_tokens=100,
            response_tokens=50, duration_ms=500
        )
        assert call.id is not None
        assert call.total_tokens == 150

    async def test_get_user_calls(self, service):
        """Test getting user's calls"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        model = await service.register_model(
            provider.id, "GPT-4", "gpt-4", ModelFamily.GPT
        )
        await service.record_model_call(
            model.id, user_id=1, request_tokens=100,
            response_tokens=50, duration_ms=500
        )
        calls = await service.get_user_calls(1)
        assert len(calls) >= 1


class TestProviderComparison:
    """Test provider comparison and selection"""

    async def test_get_best_provider_for_task(self, service):
        """Test selecting best provider"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1",
            supports_vision=True, supports_streaming=True
        )
        best = await service.get_best_provider_for_task(
            requires_vision=True, requires_streaming=True
        )
        assert best is not None

    async def test_get_model_comparison(self, service):
        """Test comparing models"""
        provider = await service.create_provider(
            name="OpenAI", slug="openai", provider_type=ProviderType.OPENAI,
            api_url="https://api.openai.com/v1"
        )
        m1 = await service.register_model(
            provider.id, "GPT-4", "gpt-4", ModelFamily.GPT
        )
        m2 = await service.register_model(
            provider.id, "GPT-3.5", "gpt-3.5", ModelFamily.GPT
        )
        comparison = await service.get_model_comparison([m1.id, m2.id])
        assert len(comparison) == 2
