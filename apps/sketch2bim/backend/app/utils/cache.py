"""
Simple caching utilities for processing operations
Uses Redis for distributed caching
"""
from typing import Optional, Any
import json
import hashlib
from loguru import logger

from ..config import settings


def get_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate cache key from prefix and arguments
    
    Args:
        prefix: Cache key prefix (e.g., "plan_detection")
        *args: Positional arguments to hash
        **kwargs: Keyword arguments to hash
    
    Returns:
        Cache key string
    """
    # Create hash from arguments
    key_data = {
        'args': args,
        'kwargs': kwargs
    }
    key_str = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    
    return f"sketch2bim:{prefix}:{key_hash}"


def get_from_cache(key: str) -> Optional[Any]:
    """
    Get value from cache
    
    Args:
        key: Cache key
    
    Returns:
        Cached value or None
    """
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.REDIS_URL)
        
        # Track Redis command usage
        from ..monitoring.redis_monitor import increment_redis_command_count
        increment_redis_command_count()
        
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.warning(f"Cache get failed: {e}")
    
    return None


def set_to_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Set value in cache with TTL
    
    Args:
        key: Cache key
        value: Value to cache (must be JSON serializable)
        ttl: Time to live in seconds (default: 1 hour)
    
    Returns:
        True if successful
    """
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.REDIS_URL)
        
        # Track Redis command usage
        from ..monitoring.redis_monitor import increment_redis_command_count
        increment_redis_command_count()
        
        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )
        return True
    except Exception as e:
        logger.warning(f"Cache set failed: {e}")
        return False


def delete_from_cache(key: str) -> bool:
    """
    Delete key from cache
    
    Args:
        key: Cache key
    
    Returns:
        True if successful
    """
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.REDIS_URL)
        
        # Track Redis command usage
        from ..monitoring.redis_monitor import increment_redis_command_count
        increment_redis_command_count()
        
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Cache delete failed: {e}")
        return False


def cache_plan_detection(sketch_hash: str, plan_data: dict, ttl: int = 7200) -> bool:
    """
    Cache plan detection results
    
    Args:
        sketch_hash: Hash of sketch image
        plan_data: Detected plan data
        ttl: Cache TTL in seconds (default: 2 hours)
    
    Returns:
        True if successful
    """
    key = get_cache_key("plan_detection", sketch_hash=sketch_hash)
    return set_to_cache(key, plan_data, ttl)


def get_cached_plan_detection(sketch_hash: str) -> Optional[dict]:
    """
    Get cached plan detection results
    
    Args:
        sketch_hash: Hash of sketch image
    
    Returns:
        Cached plan data or None
    """
    key = get_cache_key("plan_detection", sketch_hash=sketch_hash)
    return get_from_cache(key)


def cache_ifc_generation(plan_data_hash: str, ifc_url: str, ttl: int = 86400) -> bool:
    """
    Cache IFC generation results
    
    Args:
        plan_data_hash: Hash of plan data
        ifc_url: Generated IFC URL
        ttl: Cache TTL in seconds (default: 24 hours)
    
    Returns:
        True if successful
    """
    key = get_cache_key("ifc_generation", plan_data_hash=plan_data_hash)
    return set_to_cache(key, {"ifc_url": ifc_url}, ttl)


def get_cached_ifc_generation(plan_data_hash: str) -> Optional[str]:
    """
    Get cached IFC generation result
    
    Args:
        plan_data_hash: Hash of plan data
    
    Returns:
        Cached IFC URL or None
    """
    key = get_cache_key("ifc_generation", plan_data_hash=plan_data_hash)
    cached = get_from_cache(key)
    if cached:
        return cached.get("ifc_url")
    return None
