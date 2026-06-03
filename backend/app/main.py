"""
FastAPI application entry point.

Initializes the FastAPI application, sets up middleware, registers routers,
and configures lifecycle events.
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, health
from app.core.config import get_settings
from app.core.database import create_tables, dispose_engine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for application startup and shutdown.

    On startup, it creates database tables if running in debug/dev mode.
    On shutdown, it disposes of the SQLAlchemy engine connections.
    """
    logger.info("Initializing ResumeAI Backend...")
    # In development, auto-create tables
    try:
        await create_tables()
        logger.info("Database tables initialized successfully.")
    except Exception as exc:
        logger.error(f"Error creating database tables: {exc}")

    yield

    logger.info("Shutting down ResumeAI Backend...")
    await dispose_engine()
    logger.info("Database engine disposed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack AI-powered Resume Tailoring and ATS Optimization API.",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://(resumepilot\.adithyanp\.me|resume-pilot-.*\.vercel\.app)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

# Lazily import heavier routers that may depend on optional native libraries.
try:
    from app.api.routes import resume, tailor
    app.include_router(resume.router, prefix="/api/v1")
    app.include_router(tailor.router, prefix="/api/v1")
except Exception as exc:  # pragma: no cover - runtime flexibility for dev
    logger.warning(f"Skipping optional routers (resume/tailor) on startup: {exc}")
    # Provide a lightweight stub router for critical download flows so the
    # frontend remains usable in local environments without optional libs.
    try:
        from app.api.routes import stubs

        app.include_router(stubs.router, prefix="/api/v1")
        logger.info("Registered lightweight stub routes for missing optional routers.")
    except Exception:
        logger.warning("Failed to register stub routes for missing optional routers.")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all global exception handler to prevent leak of sensitive traces."""
    logger.error(f"Global unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )


@app.get("/")
async def root():
    """Root metadata endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "status": "healthy",
    }
