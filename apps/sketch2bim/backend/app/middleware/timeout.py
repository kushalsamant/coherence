"""
Request timeout middleware
Enforces maximum request processing time
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import asyncio
from typing import Optional

from ..config import settings


class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce request timeouts"""
    
    def __init__(self, app: ASGIApp, timeout_seconds: Optional[float] = None):
        super().__init__(app)
        self.timeout_seconds = timeout_seconds or getattr(settings, 'REQUEST_TIMEOUT_SECONDS', 300.0)
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Wrap the request in a timeout
            response = await asyncio.wait_for(
                call_next(request),
                timeout=self.timeout_seconds
            )
            return response
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Request timeout after {self.timeout_seconds} seconds"
            )

