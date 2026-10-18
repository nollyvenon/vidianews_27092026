"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App
    APP_NAME: str = "AetherCMS AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/aether_cms"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    # Disable connection pooling (set by the test harness). Connections then
    # are never shared across event loops, e.g. TestClient's loop vs pytest's.
    DB_NULL_POOL: bool = False

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    # Meilisearch
    MEILISEARCH_URL: str = "http://meilisearch:7700"
    MEILISEARCH_API_KEY: Optional[str] = None

    # Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333

    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # Email. When SMTP_HOST is unset, outgoing mail is not sent and verification links are
    # written to the server log instead (development only; see email_sender).
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@aethercms.com"
    SMTP_STARTTLS: bool = True

    # Accounts must confirm their email before the first sign-in. Keep this on in production.
    EMAIL_VERIFICATION_REQUIRED: bool = True
    # Public URL of the web app; used to build links that are sent by email.
    FRONTEND_URL: str = "http://localhost:3000"

    # AI chat replies (Anthropic Messages API)
    AI_CHAT_MODEL: str = "claude-haiku-5-5"
    AI_CHAT_MAX_TOKENS: int = 1024
    AI_CHAT_SYSTEM_PROMPT: str = "You are a helpful assistant inside the AetherCMS AI publishing platform."

    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"

    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
