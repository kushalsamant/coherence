#!/usr/bin/env python3
"""
Unified FastAPI Backend Server for KVSHVL Platform
Combines ASK, Reframe, and Sketch2BIM backends into a single service
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
    from routers.ask import router as ask_router
    logger.info("✅ ASK router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import ASK router: {e}")
    raise

try:
    from routers.reframe import router as reframe_router
    logger.info("✅ Reframe router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Reframe router: {e}")
    raise

try:
    from routers.sketch2bim import router as sketch2bim_router
    logger.info("✅ Sketch2BIM router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Sketch2BIM router: {e}")
    raise

try:
    from routers import subscriptions
    logger.info("✅ Subscriptions router imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import Subscriptions router: {e}")
    raise

# Get CORS origins from centralized config
CORS_ORIGINS = settings.cors_origins_list

# Create FastAPI app
logger.info("Creating FastAPI application...")
app = FastAPI(
    title=settings.APP_NAME,
    description="Unified API for KVSHVL platform applications: ASK, Reframe, and Sketch2BIM",
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

app.include_router(ask_router, prefix="/api/ask", tags=["ask"])
logger.info("✅ ASK router included at /api/ask")

app.include_router(reframe_router, prefix="/api/reframe", tags=["reframe"])
logger.info("✅ Reframe router included at /api/reframe")

app.include_router(sketch2bim_router, prefix="/api/sketch2bim", tags=["sketch2bim"])
logger.info("✅ Sketch2BIM router included at /api/sketch2bim")

# Unified subscription routes
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
logger.info("✅ Subscriptions router included at /api/subscriptions")

logger.info("=" * 80)
logger.info("All routers loaded successfully. Application ready.")
logger.info("Available routes:")
logger.info("  - GET  /")
logger.info("  - GET  /health")
logger.info("  - GET  /health/live")
logger.info("  - GET  /health/ready")
logger.info("  - *    /api/ask/*")
logger.info("  - *    /api/reframe/*")
logger.info("  - *    /api/sketch2bim/*")
logger.info("  - *    /api/subscriptions/*")
logger.info("=" * 80)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler"""
    logger.info("🚀 Application startup complete!")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Workers: {settings.WORKERS}")
    
    # Test database connections
    logger.info("Testing database connections...")
    try:
        from database.ask import engine as ask_engine
        with ask_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ ASK database connection successful")
    except Exception as e:
        logger.error(f"❌ ASK database connection failed: {e}")
        logger.warning("Continuing without ASK database - some features may not work")
    
    try:
        from database.sketch2bim import engine as sketch2bim_engine
        with sketch2bim_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Sketch2BIM database connection successful")
    except Exception as e:
        logger.error(f"❌ Sketch2BIM database connection failed: {e}")
        logger.warning("Continuing without Sketch2BIM database - some features may not work")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": settings.APP_NAME,
        "version": settings.VERSION,
        "apps": ["ask", "reframe", "sketch2bim"],
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "health": "/health",
            "health_live": "/health/live",
            "health_ready": "/health/ready",
            "docs": "/docs" if not settings.is_production else None,
            "ask": "/api/ask",
            "reframe": "/api/reframe",
            "sketch2bim": "/api/sketch2bim",
            "subscriptions": "/api/subscriptions"
        }
    }


# Error handlers are registered via core.error_handlers.register_error_handlers()

