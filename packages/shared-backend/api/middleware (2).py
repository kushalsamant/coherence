"""
Common FastAPI middleware
"""
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def setup_cors_middleware(app, cors_origins: List[str], allow_credentials: bool = True):
    """
    Setup CORS middleware with standard configuration
    
    Args:
        app: FastAPI application instance
        cors_origins: List of allowed origins
        allow_credentials: Whether to allow credentials
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def build_error_response(
    message: str,
    status_code: int,
    error_code: str,
    correlation_id: Optional[str] = None,
    details: Optional[dict] = None,
) -> JSONResponse:
    """
    Build a structured error response.
    
    Standard format: { "success": false, "error": { "code", "message" } }
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Application error code
        correlation_id: Optional correlation ID for tracing
        details: Optional additional error details
    """
    payload = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }
    
    if correlation_id:
        payload["correlation_id"] = correlation_id
    
    if details:
        payload["error"]["details"] = details
    
    return JSONResponse(status_code=status_code, content=payload)


def setup_standard_error_handlers(app, include_correlation: bool = False, debug: bool = False):
    """
    Setup standard error handlers for FastAPI app
    
    Args:
        app: FastAPI application instance
        include_correlation: Whether to include correlation IDs in responses
        debug: Whether to include debug information in errors
    """
    from fastapi import HTTPException
    
    def get_correlation_id(request: Request) -> Optional[str]:
        """Extract correlation ID from request headers if available"""
        if include_correlation:
            return request.headers.get("X-Correlation-ID")
        return None
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Standardize HTTPException responses"""
        correlation_id = get_correlation_id(request) if include_correlation else None
        message = exc.detail if isinstance(exc.detail, str) else "HTTP error"
        return build_error_response(
            message=message,
            status_code=exc.status_code,
            error_code="HTTP_ERROR",
            correlation_id=correlation_id,
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Fallback handler for uncaught exceptions"""
        correlation_id = get_correlation_id(request) if include_correlation else None
        
        logger.exception(f"Unhandled exception: {exc}", exc_info=True)
        
        error_details = None
        if debug:
            import traceback
            error_details = {
                "exception": str(exc),
                "traceback": traceback.format_exc().splitlines(),
            }
        
        return build_error_response(
            message="Internal server error",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            correlation_id=correlation_id,
            details=error_details,
        )

