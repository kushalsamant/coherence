"""
Custom exception hierarchy for the backend
Provides structured error handling with error codes and context
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status


class BackendError(Exception):
    """Base exception for all backend errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.context = context or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API response"""
        result = {
            "error": self.message,
            "error_code": self.error_code,
            "status_code": self.status_code
        }
        if self.details:
            result["details"] = self.details
        return result


class ValidationError(BackendError):
    """Input validation error"""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details or {}
        )
        self.field = field
        if field:
            self.details["field"] = field


class NotFoundError(BackendError):
    """Resource not found error"""
    
    def __init__(self, resource_type: str, resource_id: Optional[str] = None):
        message = f"{resource_type} not found"
        if resource_id:
            message += f": {resource_id}"
        
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource_type": resource_type, "resource_id": resource_id}
        )


class AuthenticationError(BackendError):
    """Authentication failure"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(BackendError):
    """Authorization failure (insufficient permissions)"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN
        )


class RateLimitError(BackendError):
    """Rate limit exceeded"""
    
    def __init__(self, retry_after: Optional[int] = None):
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": retry_after} if retry_after else {}
        )


class ExternalServiceError(BackendError):
    """External service failure (Replicate, BunnyCDN, etc.)"""
    
    def __init__(
        self,
        service: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{service} error: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"service": service, **(details or {})}
        )


class ProcessingError(BackendError):
    """Job processing error"""
    
    def __init__(self, message: str, job_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="PROCESSING_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"job_id": job_id, **(details or {})} if job_id else (details or {})
        )


class ConfigurationError(BackendError):
    """Configuration error"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"config_key": config_key} if config_key else {}
        )


class DatabaseError(BackendError):
    """Database operation error"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(
            message=f"Database error: {message}",
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"operation": operation} if operation else {}
        )

