#!/usr/bin/env python3
"""
FastAPI Backend Server for ASK Research Tool
Provides REST API endpoints for Q&A pairs, themes, and content generation
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Import routes
from api.routes import qa_pairs, themes, generate, stats, payments
from api.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="ASK Research Tool API",
    description="API for browsing and generating research Q&A pairs",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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

# Platform feasibility analysis routes (require authentication)
try:
    from api.routes import feasibility
    app.include_router(feasibility.router, prefix="/api/feasibility", tags=["feasibility"])
except ImportError:
    pass  # Feasibility routes optional

# Mount static files for images
images_dir = Path(__file__).parent.parent / "images"
if images_dir.exists():
    app.mount("/static/images", StaticFiles(directory=str(images_dir)), name="images")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": settings.APP_NAME, "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": "1.0.0",
            "environment": settings.APP_ENV,
        },
    )


def _build_error_response(
    message: str,
    status_code: int,
    error_code: str,
) -> JSONResponse:
    """
    Build a structured error response.

    This mirrors the minimal pattern used in Sketch2BIM:
    { "success": false, "error": { "code", "message" } }
    """
    payload = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }
    return JSONResponse(status_code=status_code, content=payload)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Standardize HTTPException responses to a common error envelope.
    """
    message = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    return _build_error_response(
        message=message,
        status_code=exc.status_code,
        error_code="HTTP_ERROR",
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Fallback handler for uncaught exceptions.
    """
    # Avoid leaking internals to clients; details stay in logs.
    return _build_error_response(
        message="Internal server error",
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

