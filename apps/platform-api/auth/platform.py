"""
Platform Authentication and Authorization
JWT validation and user dependency injection for platform (home site)
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import os

from database.platform import get_db
from models.platform_user import User
from shared_backend.auth.jwt import decode_jwt_token, decode_supabase_jwt, decode_nextauth_jwt
from shared_backend.subscription.utils import calculate_expiry, ensure_subscription_status, is_active_trial, has_active_subscription

# JWT secret from platform (shared with sketch2bim)
PLATFORM_NEXTAUTH_SECRET = os.getenv("PLATFORM_NEXTAUTH_SECRET", "")
if not PLATFORM_NEXTAUTH_SECRET:
    raise ValueError("PLATFORM_NEXTAUTH_SECRET environment variable is required")

# Security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token
    Creates user on first login if they don't exist
    """
    token = credentials.credentials
    
    try:
        # Try Supabase JWT first, then fall back to NextAuth (legacy)
        try:
            payload = decode_supabase_jwt(token)
            # Supabase JWT has email in user metadata or directly
            email: str = payload.get("email") or payload.get("user_metadata", {}).get("email")
        except HTTPException:
            # Fall back to NextAuth JWT (legacy)
        payload = decode_nextauth_jwt(token, PLATFORM_NEXTAUTH_SECRET)
        email: str = payload.get("email")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get or create user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Create user on first login
            user = User(
                email=email,
                name=payload.get("name"),
                google_id=payload.get("sub"),
                credits=0,  # Start with 0 credits - unlimited conversions during trial
                subscription_tier="trial",
                subscription_status="active",
                subscription_expires_at=calculate_expiry("trial")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        ensure_subscription_status(user, db)
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise
    """
    if not authorization:
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        # Try Supabase JWT first, then fall back to NextAuth (legacy)
        try:
            payload = decode_supabase_jwt(token)
            email: str = payload.get("email") or payload.get("user_metadata", {}).get("email")
        except HTTPException:
        payload = decode_nextauth_jwt(token, PLATFORM_NEXTAUTH_SECRET)
        email: str = payload.get("email")
        
        if email:
            user = db.query(User).filter(User.email == email).first()
            if user:
                ensure_subscription_status(user, db)
            return user
    except:
        pass
    
    return None


def require_active_subscription():
    """
    Dependency to check if user has an active subscription (trial or paid tier).
    Uses direct database query for fast performance.
    """
    def check_subscription(user: User = Depends(get_current_user)):
        # Direct database query - fast (< 10ms)
        if not has_active_subscription(user):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Active subscription required. Please upgrade to continue."
            )
        return user
    return check_subscription


def is_admin(user: User = Depends(get_current_user)) -> User:
    """
    Check if user has admin privileges
    """
    # Admin emails from environment or settings
    admin_emails_str = os.getenv("PLATFORM_ADMIN_EMAILS", "")
    admin_emails = [email.strip().lower() for email in admin_emails_str.split(",") if email.strip()]
    
    if user.email.lower() not in admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user
