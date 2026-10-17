"""Database session management"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

# Create async engine
_pool_options = (
    {"poolclass": NullPool}
    if settings.DB_NULL_POOL
    else {"pool_size": settings.DB_POOL_SIZE, "max_overflow": settings.DB_MAX_OVERFLOW}
)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    **_pool_options,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, future=True
)


async def get_session() -> AsyncSession:
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_db() -> AsyncSession:
    """Dependency for getting database session (alias)"""
    async with AsyncSessionLocal() as session:
        yield session
