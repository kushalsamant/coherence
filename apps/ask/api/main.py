#!/usr/bin/env python3
"""
FastAPI Backend Server for ASK Research Tool
Provides REST API endpoints for Q&A pairs, themes, and content generation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Import routes
from api.routes import qa_pairs, themes, generate, stats, payments

# Create FastAPI app
app = FastAPI(
    title="ASK Research Tool API",
    description="API for browsing and generating research Q&A pairs",
    version="1.0.0"
)

# CORS middleware configuration
# Read CORS origins from environment variable or use defaults
cors_origins_env = os.getenv('ASK_CORS_ORIGINS', os.getenv('CORS_ORIGINS', ''))
if cors_origins_env:
    # Split comma-separated origins
    cors_origins = [origin.strip() for origin in cors_origins_env.split(',')]
else:
    # Default origins for development
    cors_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://ask.kvshvl.in",
        "https://www.ask.kvshvl.in",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qa_pairs.router, prefix="/api", tags=["qa-pairs"])
app.include_router(themes.router, prefix="/api", tags=["themes"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])

# Monitoring routes (require authentication)
try:
    from api.routes import monitoring
    app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])
except ImportError:
    pass  # Monitoring routes optional

# Mount static files for images
images_dir = Path(__file__).parent.parent / "images"
if images_dir.exists():
    app.mount("/static/images", StaticFiles(directory=str(images_dir)), name="images")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "ASK Research Tool API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "ASK Research Tool API",
            "version": "1.0.0"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

