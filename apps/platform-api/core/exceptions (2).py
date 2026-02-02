"""
Custom exception classes for consistent error handling
"""
from fastapi import status


class AppException(Exception):
    """Base exception for all application errors"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class UnauthorizedException(AppException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Unauthorized", details: dict = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)


class ForbiddenException(AppException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Forbidden", details: dict = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, details)


class ValidationException(AppException):
    """Validation error exception"""
    def __init__(self, message: str = "Validation error", details: dict = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


class DatabaseException(AppException):
    """Database operation error"""
    def __init__(self, message: str = "Database error", details: dict = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)


class ExternalServiceException(AppException):
    """External service error (Groq, Razorpay, etc.)"""
    def __init__(self, message: str = "External service error", details: dict = None):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE, details)


class RateLimitException(AppException):
    """Rate limit exceeded exception"""
    def __init__(self, message: str = "Rate limit exceeded", details: dict = None):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS, details)


class InsufficientCreditsException(AppException):
    """Insufficient credits exception"""
    def __init__(self, message: str = "Insufficient credits", details: dict = None):
        super().__init__(message, status.HTTP_402_PAYMENT_REQUIRED, details)
