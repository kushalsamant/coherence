"""
Authentication module for Reframe FastAPI
Handles user authentication via NextAuth JWT tokens
Note: Reframe uses Redis for user data, not PostgreSQL
"""
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared_backend.auth.jwt import decode_nextauth_jwt


security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Dependency that returns the current authenticated user ID from JWT token.
    Note: This only validates the token and extracts user ID.
    User metadata is fetched separately from Redis.
    """
    token = credentials.credentials
    payload = decode_nextauth_jwt(token)
    
    # NextAuth stores user ID in 'sub' or 'id' field
    user_id = payload.get("sub") or payload.get("id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing user ID",
        )
    
    return str(user_id)


def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Optional[str]:
    """Get user email from JWT token"""
    token = credentials.credentials
    payload = decode_nextauth_jwt(token)
    return payload.get("email")

