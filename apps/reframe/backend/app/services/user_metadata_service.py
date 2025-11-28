"""
User Metadata Service for Reframe
Handles user subscription and metadata storage in Redis
"""
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .redis_service import get_redis_service
from .subscription_service import calculate_expiry


async def get_user_metadata(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user metadata from Redis"""
    redis = get_redis_service()
    key = f"user:metadata:{user_id}"
    data = await redis.get(key)
    
    if not data:
        return None
    
    # Parse if it's a string, otherwise return as-is
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None
    
    return data if isinstance(data, dict) else None


async def set_user_metadata(user_id: str, metadata: Dict[str, Any]) -> None:
    """Set complete user metadata in Redis"""
    redis = get_redis_service()
    key = f"user:metadata:{user_id}"
    await redis.set(key, json.dumps(metadata))


async def initialize_user_trial(user_id: str, email: Optional[str] = None) -> None:
    """Initialize user with trial subscription (7 days)"""
    now = datetime.utcnow()
    trial_expiry = now + timedelta(days=7)  # 7 days trial
    
    metadata = {
        "subscription_tier": "trial",
        "subscription_status": "active",
        "subscription_expires_at": trial_expiry.isoformat(),
        "subscription_auto_renew": False,
        "email": email,
    }
    
    await set_user_metadata(user_id, metadata)


async def get_usage(user_id: str) -> int:
    """Get usage count for free users"""
    redis = get_redis_service()
    usage_key = f"usage:{user_id}:total"
    usage_str = await redis.get(usage_key)
    return int(usage_str) if usage_str else 0


async def increment_usage(user_id: str) -> int:
    """Increment usage count for free users"""
    redis = get_redis_service()
    usage_key = f"usage:{user_id}:total"
    return await redis.incr(usage_key)

