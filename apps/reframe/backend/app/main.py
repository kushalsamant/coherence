"""
FastAPI Backend Server for Reframe
Provides REST API endpoint for text reframing
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import get_settings
from .routes import reframe

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for AI-powered text reframing with multiple human tones",
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
app.include_router(reframe.router)


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

    Minimal shared pattern with ASK/Sketch2BIM:
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
    return _build_error_response(
        message="Internal server error",
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

