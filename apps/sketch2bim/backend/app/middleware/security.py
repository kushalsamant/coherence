"""
Security middleware for rate limiting, CORS, CSRF protection
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from typing import Dict, Tuple
from collections import defaultdict
from datetime import datetime, timedelta

from ..config import settings
from ..utils import check_rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next):
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        
        # Cleanup old entries periodically
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(current_time)
            self.last_cleanup = current_time
        
        # Check rate limit
        if not self._check_rate_limit(client_id):
            return Response(
                content="Rate limit exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": "100",
                    "X-RateLimit-Remaining": "0"
                }
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self._get_remaining_requests(client_id)
        response.headers["X-RateLimit-Limit"] = "100"
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    def _check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit"""
        now = time.time()
        window_start = now - 3600  # 1 hour window
        
        # Filter requests in the last hour
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        # Check limit (100 requests per hour)
        if len(self.requests[client_id]) >= 100:
            return False
        
        # Record this request
        self.requests[client_id].append(now)
        return True
    
    def _get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        window_start = now - 3600
        recent_requests = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        return max(0, 100 - len(recent_requests))
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove old rate limit entries"""
        cutoff = current_time - 7200  # 2 hours
        for client_id in list(self.requests.keys()):
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > cutoff
            ]
            if not self.requests[client_id]:
                del self.requests[client_id]


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # HSTS (only for HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy (adjust as needed)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.razorpay.com;"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class RequestSizeMiddleware(BaseHTTPMiddleware):
    """Limit request body size"""
    
    def __init__(self, app: ASGIApp, max_size: int = None):
        super().__init__(app)
        self.max_size = max_size or settings.max_upload_size_bytes
    
    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > self.max_size:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Request body too large. Max size: {self.max_size / 1024 / 1024:.1f}MB"
                    )
            except ValueError:
                pass  # Invalid content-length, let it through
        
        response = await call_next(request)
        return response

