"""FastAPI application entry point"""

import asyncio
import contextlib
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.api_usage_middleware import ApiUsageMiddleware
from app.db.session import AsyncSessionLocal, engine
from app.db.base import Base
from app.services.api_usage_recorder import FLUSH_INTERVAL_SECONDS, ApiUsageRecorder

# Import routers
from app.api.v1 import api_router

logger = logging.getLogger(__name__)

api_usage_recorder = ApiUsageRecorder(AsyncSessionLocal)


async def _flush_api_usage_periodically() -> None:
    """Write aggregated endpoint usage even when traffic is too light to trigger a batch."""
    while True:
        await asyncio.sleep(FLUSH_INTERVAL_SECONDS)
        await api_usage_recorder.flush()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    if settings.auto_create_schema:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    else:
        logger.info("Startup schema creation is disabled; run `alembic upgrade head` to update the database.")
    flusher = asyncio.create_task(_flush_api_usage_periodically())
    yield
    # Shutdown
    flusher.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await flusher
    await api_usage_recorder.flush()
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


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """A write that breaks a database constraint (for example a reference to a record that does not exist)
    is the client's conflict, not a server failure. The database's own wording is kept out of the response."""
    logger.warning("Database constraint refused a write on %s %s: %s", request.method, request.url.path, exc.orig)
    return JSONResponse(
        status_code=409,
        content={"detail": "The request conflicts with existing data or refers to a record that does not exist"},
    )


# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

# Count calls, errors and response times per endpoint (written in batches; see api_usage_recorder)
app.add_middleware(
    ApiUsageMiddleware,
    recorder=api_usage_recorder,
    routes=lambda: app.router.routes,
    prefix=settings.API_PREFIX,
)


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
