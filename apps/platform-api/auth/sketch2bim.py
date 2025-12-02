"""
Authentication and authorization
JWT validation and user dependency injection
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import secrets

from database.sketch2bim import get_db
from models.sketch2bim import User
from config.sketch2bim import settings
from shared_backend.auth.jwt import decode_nextauth_jwt
from shared_backend.subscription.utils import calculate_expiry, ensure_subscription_status, is_active_trial, has_active_subscription

# Security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token
    """
    token = credentials.credentials
    
    try:
        payload = decode_nextauth_jwt(token)
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
        payload = decode_nextauth_jwt(token)
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
    Replaces credit-based access control with subscription-based access control.
    """
    def check_subscription(user: User = Depends(get_current_user)):
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
    # Add admin email list to settings if needed
    admin_emails = ["admin@sketch2bim.com"]  # Configure this
    
    if user.email not in admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user

