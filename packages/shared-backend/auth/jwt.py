"""
JWT token handling utilities
"""

from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from ..config.base import get_settings


def get_jwt_secret() -> str:
    """
    Resolve the JWT secret used by NextAuth.
    
    Returns:
        JWT secret string
        
    Raises:
        HTTPException: If secret is not configured
    """
    settings = get_settings()
    secret = settings.NEXTAUTH_SECRET
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="NEXTAUTH_SECRET is not configured",
        )
    return secret


def decode_nextauth_jwt(token: str, secret: Optional[str] = None, algorithm: Optional[str] = None) -> dict:
    """
    Decode and validate NextAuth JWT token.
    
    Args:
        token: JWT token string
        secret: Optional JWT secret (uses settings if not provided)
        algorithm: Optional JWT algorithm (uses settings if not provided)
        
    Returns:
        Decoded JWT payload
        
    Raises:
        HTTPException: If token is invalid
    """
    settings = get_settings()
    secret = secret or get_jwt_secret()
    algorithm = algorithm or settings.JWT_ALGORITHM
    
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm],
        )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )

