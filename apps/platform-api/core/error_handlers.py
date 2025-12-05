"""
Global error handlers for FastAPI application
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.exceptions import AppException
from core.config import settings
import logging
import traceback

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle custom application exceptions
    Returns consistent error response format
    """
    logger.error(f"AppException: {exc.message}", extra={
        "status_code": exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "details": exc.details
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details if settings.DEBUG else None,
            "path": request.url.path
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors
    Returns detailed validation error information
    """
    errors = exc.errors()
    logger.warning(f"Validation error: {errors}", extra={
        "path": request.url.path,
        "method": request.method
    })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": errors if settings.DEBUG else "Invalid request data",
            "path": request.url.path
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle standard HTTP exceptions
    """
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}", extra={
        "path": request.url.path,
        "method": request.method,
        "status_code": exc.status_code
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "path": request.url.path
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions
    Logs full traceback and returns generic error to client
    """
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc()
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "path": request.url.path
        }
    )


def register_error_handlers(app):
    """
    Register all error handlers with the FastAPI application
    Call this function during app initialization
    """
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("✅ Error handlers registered")
