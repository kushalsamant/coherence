#!/usr/bin/env python3
"""
KVSHVL Platform API Server
FastAPI backend for platform - Subscription management and user authentication
Note: Sketch2BIM API is now in a separate repository
"""

import sys
import os
from pathlib import Path

# Add the application root to Python path for module imports FIRST
app_root = Path(__file__).parent.resolve()
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

# Configure logging using centralized config
from core.logging_config import setup_logging
logger = setup_logging()

# Import configuration
from core.config import settings

# Log startup information
logger.info("=" * 80)
logger.info(f"{settings.APP_NAME} - Starting Up")
logger.info("=" * 80)
logger.info(f"Version: {settings.VERSION}")
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"Debug mode: {settings.DEBUG}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"App root: {app_root}")
logger.info("=" * 80)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.error_handlers import register_error_handlers
from sqlalchemy import text

# Import app-specific routers
logger.info("Importing routers...")
try:
    from routers import health
    logger.info("✅ Health router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Health router: {e}")
    raise

try:
    from routers import subscriptions
    logger.info("✅ Subscriptions router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Subscriptions router: {e}")
    raise

try:
    from routers import users
    logger.info("✅ Users router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Users router: {e}")
    raise

# Note: Sketch2BIM router is now in the sketch2bim repository

# Get CORS origins from centralized config
CORS_ORIGINS = settings.cors_origins_list

# Create FastAPI app
logger.info("Creating FastAPI application...")
app = FastAPI(
    title=settings.APP_NAME,
    description="KVSHVL Platform API - Subscription management and user authentication",
    version=settings.VERSION,
    docs_url="/docs" if not settings.is_production else None,  # Disable docs in production for security
    redoc_url="/redoc" if not settings.is_production else None
)
logger.info("✅ FastAPI app created successfully")

# Register error handlers
register_error_handlers(app)

# CORS middleware configuration
logger.info(f"Configuring CORS with {len(CORS_ORIGINS)} origins")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)
logger.info("✅ CORS middleware configured")

# Include app-specific routers with path prefixes
logger.info("Including routers...")

# Health check routes (no prefix - at root level)
app.include_router(health.router)
logger.info("✅ Health router included at root level")

# Note: Sketch2BIM router is now in the sketch2bim repository (separate deployment)

# Platform subscription routes
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
logger.info("✅ Subscriptions router included at /api/subscriptions")

# Platform user routes (for external apps)
app.include_router(users.router, prefix="/api/users", tags=["users"])
logger.info("✅ Users router included at /api/users")

logger.info("=" * 80)
logger.info("All routers loaded successfully. Application ready.")
logger.info("Available routes:")
logger.info("  - GET  /")
logger.info("  - GET  /health")
logger.info("  - GET  /health/live")
logger.info("  - GET  /health/ready")
logger.info("  - *    /api/subscriptions/*")
logger.info("  - *    /api/users/*")
logger.info("=" * 80)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler"""
    logger.info("🚀 Application startup complete!")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Workers: {settings.WORKERS}")
    
    # Test database connection
    logger.info("Testing database connection...")
    try:
        from database.platform import engine as platform_engine
        with platform_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Platform database connection successful")
    except Exception as e:
        logger.error(f"❌ Platform database connection failed: {e}")
        logger.warning("Continuing without database - some features may not work")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": settings.APP_NAME,
        "version": settings.VERSION,
        "app": "platform",
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "description": "KVSHVL Platform API - Subscription management and user authentication",
        "endpoints": {
            "health": "/health",
            "health_live": "/health/live",
            "health_ready": "/health/ready",
            "docs": "/docs" if not settings.is_production else None,
            "subscriptions": "/api/subscriptions",
            "users": "/api/users"
        }
    }


# Error handlers are registered via core.error_handlers.register_error_handlers()

