"""
Authentication dependencies
Use these in route handlers to require authentication
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[str]:
    """
    Extract user ID from JWT token or session
    This is a placeholder - implement your auth logic here
    
    Returns:
        User ID if authenticated, raises HTTPException if not
    """
    # TODO: Implement actual authentication logic
    # For now, this is a placeholder
    
    # Example: Extract from token
    # token = credentials.credentials
    # payload = decode_jwt(token)
    # return payload.get("user_id")
    
    raise HTTPException(status_code=401, detail="Authentication required")


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    Extract user ID from token if present, otherwise return None
    Use this for optional authentication (e.g., public endpoints with user-specific features)
    """
    if not credentials:
        return None
    
    # TODO: Implement actual authentication logic
    return None

