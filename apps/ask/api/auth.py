"""
Authentication dependencies for FastAPI
Handles user authentication via NextAuth JWT tokens
"""
from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models_db import User
from shared_backend.auth.jwt import decode_nextauth_jwt
from shared_backend.subscription.utils import (
    calculate_expiry,
    ensure_subscription_status,
    has_active_subscription,
)

security = HTTPBearer()


def _get_or_create_user(email: str, payload: dict, db: Session) -> User:
    """
    Fetch existing user or create a trial user on first login.
    """
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    user = User(
        email=email,
        name=payload.get("name"),
        google_id=payload.get("sub"),
        credits=0,
        subscription_tier="trial",
        subscription_status="active",
        subscription_expires_at=calculate_expiry("trial"),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency that returns the current authenticated user.
    """
    token = credentials.credentials
    payload = decode_nextauth_jwt(token)
    email: Optional[str] = payload.get("email")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing email",
        )
    
    user = _get_or_create_user(email, payload, db)
    ensure_subscription_status(user, db)
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Return the current user if a valid Authorization header is provided.
    """
    if not authorization:
        return None
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = decode_nextauth_jwt(token)
    except HTTPException:
        return None
    
    email: Optional[str] = payload.get("email")
    if not email:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        ensure_subscription_status(user, db)
    return user


def require_active_subscription():
    """
    Dependency to ensure the user has an active subscription (trial or paid).
    """
    def checker(user: User = Depends(get_current_user)) -> User:
        if not has_active_subscription(user):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Active subscription required. Please upgrade to continue.",
            )
        return user
    
    return checker

