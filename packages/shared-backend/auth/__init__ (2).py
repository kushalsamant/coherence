"""
Shared Authentication Package
Unified authentication utilities for KVSHVL platform
"""

from .jwt import decode_nextauth_jwt, get_jwt_secret
from .dependencies import (
    get_current_user,
    get_current_user_optional,
    require_active_subscription,
    is_admin,
)

__all__ = [
    "decode_nextauth_jwt",
    "get_jwt_secret",
    "get_current_user",
    "get_current_user_optional",
    "require_active_subscription",
    "is_admin",
]

