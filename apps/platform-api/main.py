#!/usr/bin/env python3
"""
Unified FastAPI Backend Server for KVSHVL Platform
Combines ASK, Reframe, and Sketch2BIM backends into a single service
"""

import sys
from pathlib import Path

# Add the application root to Python path for module imports
# This allows imports like "from models.xxx import yyy" to work
app_root = Path(__file__).parent.resolve()
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

# Import app-specific routers
from routers.ask import router as ask_router
from routers.reframe import router as reframe_router
from routers.sketch2bim import router as sketch2bim_router
from routers import subscriptions

# Get CORS origins from environment
CORS_ORIGINS = os.getenv(
    "PLATFORM_CORS_ORIGINS",
    "http://localhost:3000,https://kvshvl.in,https://www.kvshvl.in,https://ask.kvshvl.in,https://reframe.kvshvl.in,https://sketch2bim.kvshvl.in"
).split(",")

# Create FastAPI app
app = FastAPI(
    title="KVSHVL Platform API",
    description="Unified API for KVSHVL platform applications: ASK, Reframe, and Sketch2BIM",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include app-specific routers with path prefixes
app.include_router(ask_router, prefix="/api/ask", tags=["ask"])
app.include_router(reframe_router, prefix="/api/reframe", tags=["reframe"])
app.include_router(sketch2bim_router, prefix="/api/sketch2bim", tags=["sketch2bim"])

# Unified subscription routes
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "KVSHVL Platform API",
        "version": "1.0.0",
        "apps": ["ask", "reframe", "sketch2bim"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "KVSHVL Platform API",
            "version": "1.0.0",
            "apps": ["ask", "reframe", "sketch2bim"]
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if os.getenv("PLATFORM_DEBUG", "false").lower() == "true" else "An error occurred"
        }
    )

