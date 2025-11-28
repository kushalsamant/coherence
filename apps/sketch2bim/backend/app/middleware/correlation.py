"""
Request correlation ID middleware
Adds correlation IDs to all requests for distributed tracing
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import uuid
from typing import Optional
from contextvars import ContextVar

from ..utils.logging import set_correlation_id

# Context variable for request ID
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation IDs to requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Get or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID") or request.headers.get("X-Request-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # Set in context
        set_correlation_id(correlation_id)
        request_id_var.set(correlation_id)
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Request-ID"] = correlation_id
        
        return response


def get_request_id() -> Optional[str]:
    """Get current request ID from context"""
    return request_id_var.get()

