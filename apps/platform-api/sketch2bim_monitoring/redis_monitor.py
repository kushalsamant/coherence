"""
Redis usage monitoring
Tracks Redis command count per day and alerts when approaching limits
"""
from typing import Dict, Any, Optional
from datetime import datetime, date
import redis
from ..config import settings
from loguru import logger

# Default limits (can be overridden via environment)
REDIS_LIMIT_COMMANDS_PER_DAY = int(getattr(settings, 'REDIS_LIMIT_COMMANDS_PER_DAY', 10000))  # Upstash free tier

# Redis key for tracking daily command count
REDIS_COMMANDS_COUNTER_KEY = "sketch2bim:monitoring:redis_commands_today"
REDIS_COMMANDS_DATE_KEY = "sketch2bim:monitoring:redis_commands_date"


def get_redis_client() -> Optional[redis.Redis]:
    """Get Redis client"""
    try:
        return redis.Redis.from_url(settings.REDIS_URL)
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        return None


def increment_redis_command_count():
    """
    Increment Redis command counter
    Call this on each Redis operation
    """
    try:
        client = get_redis_client()
        if not client:
            return
        
        # Check if date has changed (reset counter if new day)
        today = date.today().isoformat()
        stored_date = client.get(REDIS_COMMANDS_DATE_KEY)
        
        if stored_date is None or stored_date.decode() != today:
            # New day - reset counter
            client.set(REDIS_COMMANDS_DATE_KEY, today)
            client.set(REDIS_COMMANDS_COUNTER_KEY, 0)
        
        # Increment counter
        client.incr(REDIS_COMMANDS_COUNTER_KEY)
    except Exception as e:
        logger.warning(f"Error incrementing Redis command count: {e}")


def get_redis_usage() -> Dict[str, Any]:
    """
    Get Redis command usage for today
    
    Returns:
        dict with commands_today, limit_per_day, percentage_used, status
    """
    try:
        client = get_redis_client()
        if not client:
            return {
                "commands_today": 0,
                "limit_per_day": REDIS_LIMIT_COMMANDS_PER_DAY,
                "percentage_used": 0,
                "status": "error",
                "error": "Redis not available"
            }
        
        # Check if date has changed (reset counter if new day)
        today = date.today().isoformat()
        stored_date = client.get(REDIS_COMMANDS_DATE_KEY)
        
        if stored_date is None or stored_date.decode() != today:
            # New day - reset counter
            client.set(REDIS_COMMANDS_DATE_KEY, today)
            client.set(REDIS_COMMANDS_COUNTER_KEY, 0)
            commands_today = 0
        else:
            commands_today = int(client.get(REDIS_COMMANDS_COUNTER_KEY) or 0)
        
        percentage_used = (commands_today / REDIS_LIMIT_COMMANDS_PER_DAY) * 100 if REDIS_LIMIT_COMMANDS_PER_DAY > 0 else 0
        
        # Determine status
        if percentage_used >= 95:
            status = "critical"
        elif percentage_used >= 80:
            status = "warning"
        else:
            status = "ok"
        
        return {
            "commands_today": commands_today,
            "limit_per_day": REDIS_LIMIT_COMMANDS_PER_DAY,
            "percentage_used": round(percentage_used, 2),
            "status": status,
            "remaining_commands": REDIS_LIMIT_COMMANDS_PER_DAY - commands_today,
            "date": today
        }
    except Exception as e:
        logger.error(f"Error getting Redis usage: {e}")
        return {
            "commands_today": 0,
            "limit_per_day": REDIS_LIMIT_COMMANDS_PER_DAY,
            "percentage_used": 0,
            "status": "error",
            "error": str(e)
        }


def get_redis_info() -> Dict[str, Any]:
    """
    Get additional Redis information
    
    Returns:
        dict with Redis info
    """
    try:
        client = get_redis_client()
        if not client:
            return {
                "connected": False,
                "error": "Redis not available"
            }
        
        info = client.info()
        return {
            "connected": True,
            "redis_version": info.get("redis_version", "unknown"),
            "used_memory_human": info.get("used_memory_human", "unknown"),
            "used_memory": info.get("used_memory", 0),
            "connected_clients": info.get("connected_clients", 0),
            "total_commands_processed": info.get("total_commands_processed", 0)
        }
    except Exception as e:
        logger.error(f"Error getting Redis info: {e}")
        return {
            "connected": False,
            "error": str(e)
        }

