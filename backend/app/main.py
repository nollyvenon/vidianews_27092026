"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.utils.logger import logger

# Import routers
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    # Create tables one at a time, in repeated passes, so a legacy table with a
    # broken foreign key cannot block the rest (news, users, ...).
    from app.models.news import NewsBase
    pending = list(Base.metadata.tables.values()) + list(NewsBase.metadata.tables.values())
    for _ in range(5):
        failed = []
        for table in pending:
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(table.create, checkfirst=True)
            except Exception as exc:  # noqa: BLE001
                failed.append((table, exc))
        if not failed or len(failed) == len(pending):
            pending = failed and [t for t, _ in failed]
            for t, exc in failed:
                logger.warning("could not create table %s: %s", t.name, str(exc).splitlines()[0][:160])
            break
        pending = [t for t, _ in failed]
    from app.services.news import scheduler as news_scheduler
    news_scheduler.start()
    yield
    # Shutdown
    await news_scheduler.stop()
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise AI Publishing Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
