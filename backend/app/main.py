from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import get_settings
from backend.app.database import async_session_factory, init_db
from backend.app.routers import (
    auth_router,
    availability_router,
    blog_router,
    inquiries_router,
    testimonials_router,
    venues_router,
)
from backend.app.schemas.contracts import ProblemDetail
from backend.app.seed import seed_data

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application Lifespan Context Manager.
    Handles startup database initialization, auto-migration, and seed data.
    """
    # Initialize database tables
    await init_db()

    # Automatically seed authentic WordPress data if database is fresh
    async with async_session_factory() as session:
        await seed_data(session)

    yield

    # Clean shutdown tasks (if any)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Luxury Editorial Backend for The Royal Banquet Palace & Grand Ballrooms in Dwarka, Delhi.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)

# ─── CORS CONFIGURATION ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── RFC 9457 PROBLEM DETAILS ERROR HANDLERS ────────────────────────────────
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Formats standard HTTPExceptions into RFC 9457 Problem Details."""
    content = ProblemDetail(
        type=f"https://theroyalbanquetpalace.com/errors/{exc.status_code}",
        title="Request Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=str(request.url.path),
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats Pydantic validation errors into RFC 9457 Problem Details."""
    errors = exc.errors()
    detail_msg = "; ".join([f"{'.'.join(str(l) for l in err['loc'])}: {err['msg']}" for err in errors])
    content = ProblemDetail(
        type="https://theroyalbanquetpalace.com/errors/validation-error",
        title="Validation Error",
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail_msg,
        instance=str(request.url.path),
    ).model_dump()
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches unhandled exceptions and masks internal details."""
    content = ProblemDetail(
        type="https://theroyalbanquetpalace.com/errors/internal-server-error",
        title="Internal Server Error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred while processing the reservation. Our team has been notified.",
        instance=str(request.url.path),
    ).model_dump()
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)


# ─── ROUTER MOUNTING ────────────────────────────────────────────────────────
api_v1_prefix = "/api/v1"
app.include_router(inquiries_router, prefix=api_v1_prefix)
app.include_router(venues_router, prefix=api_v1_prefix)
app.include_router(availability_router, prefix=api_v1_prefix)
app.include_router(testimonials_router, prefix=api_v1_prefix)
app.include_router(blog_router, prefix=api_v1_prefix)
app.include_router(auth_router, prefix=api_v1_prefix)


# ─── STATIC MEDIA MOUNTS ────────────────────────────────────────────────────
# Ensure static assets and scraped copies can be served seamlessly
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
assets_path = os.path.join(base_dir, "assets")
scraped_path = os.path.join(base_dir, "scraped_redesign_copy")

if os.path.isdir(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

if os.path.isdir(scraped_path):
    app.mount("/scraped_redesign_copy", StaticFiles(directory=scraped_path), name="scraped_copy")


# ─── SYSTEM STATUS & HEALTH CHECK ───────────────────────────────────────────
@app.get("/", tags=["System Information"])
async def root():
    """Welcome endpoint providing service metadata and API entry points."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "documentation": "/docs",
        "endpoints": {
            "inquiries": f"{api_v1_prefix}/inquiries",
            "venues": f"{api_v1_prefix}/venues",
            "availability": f"{api_v1_prefix}/availability/check",
            "testimonials": f"{api_v1_prefix}/testimonials",
            "blog": f"{api_v1_prefix}/blog",
            "auth": f"{api_v1_prefix}/auth/login",
        },
        "status": "operational"
    }


@app.get("/health", tags=["System Information"])
async def health_check():
    """Liveness probe verifying server health."""
    return {"status": "healthy", "service": "The Royal Banquet Palace API"}
