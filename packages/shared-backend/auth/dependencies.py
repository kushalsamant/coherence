"""
FastAPI authentication dependencies
"""

from datetime import datetime
from typing import Optional, Callable, TypeVar
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .jwt import decode_jwt_token, decode_supabase_jwt, decode_nextauth_jwt
try:
    from ..config.base import get_settings
except ImportError:
    # Fallback if config not available
    import os
    def get_settings():
        class Settings:
            ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(",") if os.getenv("ADMIN_EMAILS") else []
        return Settings()

# Type variable for User model
T = TypeVar('T')

# Security scheme
security = HTTPBearer()


def get_current_user_factory(
    get_db: Callable,
    UserModel: type,
    calculate_expiry: Callable,
    ensure_subscription_status: Callable,
) -> Callable:
    """
    Factory function to create get_current_user dependency.
    
    Args:
        get_db: Database session dependency
        UserModel: SQLAlchemy User model class
        calculate_expiry: Function to calculate subscription expiry
        ensure_subscription_status: Function to ensure subscription status
        
    Returns:
        get_current_user dependency function
    """
    def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ) -> UserModel:
        """
        Dependency that returns the current authenticated user.
        """
        token = credentials.credentials
        # Try Supabase JWT first, then fall back to NextAuth (legacy)
        try:
            payload = decode_supabase_jwt(token)
            email: Optional[str] = payload.get("email") or payload.get("user_metadata", {}).get("email")
        except HTTPException:
            payload = decode_nextauth_jwt(token)
            email: Optional[str] = payload.get("email")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing email",
            )
        
        # Get or create user
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            # Create user on first login
            user = UserModel(
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
        else:
            # Update last login
            if hasattr(user, 'last_login'):
                user.last_login = datetime.utcnow()
                db.commit()
                db.refresh(user)
        
        # Ensure subscription status
        ensure_subscription_status(user, db)
        
        # Check if user is active
        if hasattr(user, 'is_active') and not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        return user
    
    return get_current_user


def get_current_user_optional_factory(
    get_db: Callable,
    UserModel: type,
    ensure_subscription_status: Callable,
) -> Callable:
    """
    Factory function to create get_current_user_optional dependency.
    
    Args:
        get_db: Database session dependency
        UserModel: SQLAlchemy User model class
        ensure_subscription_status: Function to ensure subscription status
        
    Returns:
        get_current_user_optional dependency function
    """
    def get_current_user_optional(
        authorization: Optional[str] = Header(None),
        db: Session = Depends(get_db),
    ) -> Optional[UserModel]:
        """
        Return the current user if a valid Authorization header is provided.
        """
        if not authorization:
            return None
        
        token = authorization.replace("Bearer ", "")
        try:
            # Try Supabase JWT first, then fall back to NextAuth (legacy)
            try:
                payload = decode_supabase_jwt(token)
                email: Optional[str] = payload.get("email") or payload.get("user_metadata", {}).get("email")
            except HTTPException:
                payload = decode_nextauth_jwt(token)
                email: Optional[str] = payload.get("email")
        except HTTPException:
            return None
        if not email:
            return None
        
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if user:
            ensure_subscription_status(user, db)
        return user
    
    return get_current_user_optional


def require_active_subscription_factory(
    get_current_user: Callable,
    has_active_subscription: Callable,
) -> Callable:
    """
    Factory function to create require_active_subscription dependency.
    
    Args:
        get_current_user: get_current_user dependency
        has_active_subscription: Function to check if user has active subscription
        
    Returns:
        require_active_subscription dependency function
    """
    def require_active_subscription(user = Depends(get_current_user)):
        """
        Dependency to ensure the user has an active subscription (trial or paid).
        """
        if not has_active_subscription(user):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Active subscription required. Please upgrade to continue.",
            )
        return user
    
    return require_active_subscription


def is_admin_factory(
    get_current_user: Callable,
    admin_emails: Optional[list[str]] = None,
) -> Callable:
    """
    Factory function to create is_admin dependency.
    
    Args:
        get_current_user: get_current_user dependency
        admin_emails: List of admin email addresses (uses settings if not provided)
        
    Returns:
        is_admin dependency function
    """
    def is_admin(user = Depends(get_current_user)):
        """
        Check if user has admin privileges.
        """
        settings = get_settings()
        emails = admin_emails or settings.ADMIN_EMAILS or []
        
        if user.email not in emails:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )
        
        return user
    
    return is_admin


# Convenience functions that need to be configured per app
def get_current_user(*args, **kwargs):
    """
    Placeholder - use get_current_user_factory() to create the actual dependency.
    This is a convenience function that should be replaced with the factory result.
    """
    raise NotImplementedError(
        "Use get_current_user_factory() to create the dependency for your app"
    )


def get_current_user_optional(*args, **kwargs):
    """
    Placeholder - use get_current_user_optional_factory() to create the actual dependency.
    """
    raise NotImplementedError(
        "Use get_current_user_optional_factory() to create the dependency for your app"
    )


def require_active_subscription(*args, **kwargs):
    """
    Placeholder - use require_active_subscription_factory() to create the actual dependency.
    """
    raise NotImplementedError(
        "Use require_active_subscription_factory() to create the dependency for your app"
    )


def is_admin(*args, **kwargs):
    """
    Placeholder - use is_admin_factory() to create the actual dependency.
    """
    raise NotImplementedError(
        "Use is_admin_factory() to create the dependency for your app"
    )

