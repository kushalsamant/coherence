"""
JWT token handling utilities
Supports both NextAuth (legacy) and Supabase Auth JWT tokens
"""

from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
import os
import requests
from ..config.base import get_settings


def get_jwt_secret() -> str:
    """
    Resolve the JWT secret used by NextAuth (legacy).
    
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


def get_supabase_jwt_secret() -> Optional[str]:
    """
    Get Supabase JWT secret from environment.
    Supabase uses a JWT secret that can be obtained from the project settings.
    """
    return os.getenv("SUPABASE_JWT_SECRET") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def decode_supabase_jwt(token: str) -> dict:
    """
    Decode and validate Supabase JWT token.
    
    Args:
        token: Supabase JWT token string
        
    Returns:
        Decoded JWT payload
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        # Supabase JWT uses HS256 algorithm
        # The secret is the JWT secret from Supabase project settings
        secret = get_supabase_jwt_secret()
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase JWT secret not configured",
            )
        
        # Decode without verification first to get the header
        unverified = jwt.get_unverified_header(token)
        
        # Decode with verification
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
        )
        
        # Verify it's a Supabase token
        if payload.get("iss") != "supabase":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not a Supabase token",
            )
        
        return payload
        
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Supabase authentication token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_jwt_token(token: str, secret: Optional[str] = None, algorithm: Optional[str] = None) -> dict:
    """
    Decode JWT token - tries Supabase first, then NextAuth (legacy).
    
    Args:
        token: JWT token string
        secret: Optional JWT secret (for NextAuth)
        algorithm: Optional JWT algorithm (for NextAuth)
        
    Returns:
        Decoded JWT payload
        
    Raises:
        HTTPException: If token is invalid
    """
    # Try Supabase first
    try:
        return decode_supabase_jwt(token)
    except HTTPException:
        # If Supabase fails, try NextAuth (legacy)
        return decode_nextauth_jwt(token, secret, algorithm)


def decode_nextauth_jwt(token: str, secret: Optional[str] = None, algorithm: Optional[str] = None) -> dict:
    """
    Decode and validate NextAuth JWT token (legacy).
    
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

