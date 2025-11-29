"""
Main FastAPI application
Sketch-to-BIM Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import os

from .config import settings
from .database import init_db
from .utils.migrations import run_migrations
from .routes import auth, generate, payments, admin, extraction, iterations, variations, referrals, logs, monitoring
from .monitoring.metrics import get_metrics, get_metrics_content_type

# Configure enhanced logging
from .utils.logging import configure_logging
configure_logging(
    log_level=settings.LOG_LEVEL,
    json_format=os.getenv("SKETCH2BIM_JSON_LOGGING", os.getenv("JSON_LOGGING", "false")).lower() == "true"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info("Starting Sketch-to-BIM Backend")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Run database migrations
    try:
        migration_success = run_migrations()
        if migration_success:
            logger.success("Database migrations completed")
        else:
            logger.warning("Database migrations completed with warnings")
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        logger.warning("Application will continue to start, but database schema may be out of date")
    
    # Initialize database
    try:
        init_db()
        logger.success("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Sketch-to-BIM Backend")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Convert architectural sketches to editable BIM models using computer vision",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID middleware (add first to track all requests)
from .middleware.correlation import CorrelationMiddleware
app.add_middleware(CorrelationMiddleware)

# Timeout middleware
from .middleware.timeout import TimeoutMiddleware
app.add_middleware(TimeoutMiddleware, timeout_seconds=getattr(settings, 'REQUEST_TIMEOUT_SECONDS', 300.0))

# Security middleware
from .middleware.security import (
    SecurityHeadersMiddleware,
    RequestSizeMiddleware
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeMiddleware, max_size=settings.max_upload_size_bytes)


# Health check
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": settings.APP_NAME,
        "version": settings.API_VERSION
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.API_VERSION,
            "environment": settings.APP_ENV
        }
    )


@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    from fastapi.responses import Response
    return Response(
        content=get_metrics(),
        media_type=get_metrics_content_type()
    )


# Include routers
from .health import router as health_router
app.include_router(health_router)  # Health checks at root level

app.include_router(auth.router, prefix="/api/v1")
app.include_router(generate.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(extraction.router, prefix="/api/v1")
app.include_router(iterations.router, prefix="/api/v1")
app.include_router(variations.router, prefix="/api/v1")
app.include_router(referrals.router, prefix="/api/v1")
app.include_router(logs.router, prefix="/api/v1")
app.include_router(monitoring.router, prefix="/api/v1")


# Exception handlers
from .exceptions import BackendError
from .utils.logging import get_correlation_id

@app.exception_handler(BackendError)
async def backend_error_handler(request, exc: BackendError):
    """Handle custom backend errors"""
    correlation_id = get_correlation_id()
    
    logger.error(
        f"Backend error: {exc.error_code} - {exc.message}",
        correlation_id=correlation_id,
        error_code=exc.error_code,
        details=exc.details,
        context=exc.context
    )
    
    response_data = exc.to_dict()
    if correlation_id:
        response_data["correlation_id"] = correlation_id
    
    if settings.DEBUG and exc.context:
        response_data["context"] = exc.context
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    correlation_id = get_correlation_id()
    
    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        correlation_id=correlation_id,
        status_code=exc.status_code
    )
    
    response_data = {
        "error": exc.detail,
        "status_code": exc.status_code
    }
    
    if correlation_id:
        response_data["correlation_id"] = correlation_id
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data,
        headers=exc.headers
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    correlation_id = get_correlation_id()
    
    logger.error(
        f"Unhandled exception: {exc}",
        correlation_id=correlation_id,
        exc_info=True
    )
    
    response_data = {
        "error": "Internal server error",
        "error_code": "INTERNAL_SERVER_ERROR",
        "status_code": 500
    }
    
    if correlation_id:
        response_data["correlation_id"] = correlation_id
    
    if settings.DEBUG:
        import traceback
        response_data["detail"] = str(exc)
        response_data["traceback"] = traceback.format_exc()
    
    return JSONResponse(
        status_code=500,
        content=response_data
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS
    )

