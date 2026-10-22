"""FastAPI application entry point"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
    from app.models import site as _site_models  # noqa: F401 - registers the admin/analytics tables
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
    from app.services.news.migrate import ensure_columns
    await ensure_columns(engine)
    from app.services.site import adminauth, maintenance, sitesettings
    try:
        await adminauth.bootstrap_admin()
    except Exception as exc:  # noqa: BLE001 - a bad bootstrap value must not stop the API
        logger.warning("admin bootstrap skipped: %s", getattr(exc, "detail", exc))
    await sitesettings.seed_default_pages()
    if settings.APP_ENV.lower() == "production" and settings.SECRET_KEY.startswith("your-secret-key"):
        logger.warning("SECRET_KEY is still the default; set a long random value in production")
    from app.services.news import scheduler as news_scheduler
    news_scheduler.start()
    maintenance.start()
    yield
    # Shutdown
    await maintenance.stop()
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


class SecurityHeaders:
    """Pure ASGI middleware (BaseHTTPMiddleware can cancel background tasks when a client disconnects)."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        admin = scope["path"].startswith(f"{settings.API_PREFIX}/admin")

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                present = {k.lower() for k, _ in headers}
                extra = [(b"x-content-type-options", b"nosniff"), (b"referrer-policy", b"strict-origin-when-cross-origin")]
                if admin:
                    extra += [(b"cache-control", b"no-store"), (b"x-robots-tag", b"noindex, nofollow")]
                headers.extend((k, v) for k, v in extra if k not in present or admin)
            await send(message)

        await self.app(scope, receive, send_with_headers)


app.add_middleware(SecurityHeaders)


# Uploaded advert images (admin uploads are validated and renamed; only images are ever written here)
_uploads = Path(settings.UPLOAD_DIR)
(_uploads / "ads").mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(_uploads)), name="media")

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
