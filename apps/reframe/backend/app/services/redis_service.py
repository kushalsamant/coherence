"""
Redis Service for Reframe
Handles Upstash Redis REST API operations for user metadata and usage tracking
"""
import os
import json
from typing import Optional, Dict, Any
import httpx


class RedisService:
    """Upstash Redis REST API client"""
    
    def __init__(self):
        self.url = os.getenv("REFRAME_UPSTASH_REDIS_REST_URL")
        self.token = os.getenv("REFRAME_UPSTASH_REDIS_REST_TOKEN")
        if not self.url or not self.token:
            raise ValueError("UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN must be set")
        
        self.base_url = f"{self.url}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def _request(self, command: str, args: list) -> Any:
        """Make a request to Upstash Redis REST API"""
        async with httpx.AsyncClient() as client:
            # Upstash REST API format
            payload = [command] + args
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()
            # Upstash returns result directly, not wrapped in "result" key
            return result
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value from Redis"""
        result = await self._request("GET", [key])
        return result if result else None
    
    async def set(self, key: str, value: str) -> bool:
        """Set a value in Redis"""
        result = await self._request("SET", [key, value])
        return result == "OK"
    
    async def delete(self, *keys: str) -> int:
        """Delete keys from Redis"""
        result = await self._request("DEL", list(keys))
        return result or 0
    
    async def incr(self, key: str) -> int:
        """Increment a key"""
        result = await self._request("INCR", [key])
        return result or 0
    
    async def incrby(self, key: str, increment: int) -> int:
        """Increment a key by a value"""
        result = await self._request("INCRBY", [key, str(increment)])
        return result or 0
    
    async def incrbyfloat(self, key: str, increment: float) -> float:
        """Increment a key by a float value"""
        result = await self._request("INCRBYFLOAT", [key, str(increment)])
        return float(result) if result else 0.0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on a key"""
        result = await self._request("EXPIRE", [key, str(seconds)])
        return result == 1
    
    async def hset(self, key: str, field: str, value: str) -> int:
        """Set a field in a hash"""
        result = await self._request("HSET", [key, field, value])
        return result or 0
    
    async def hget(self, key: str, field: str) -> Optional[str]:
        """Get a field from a hash"""
        result = await self._request("HGET", [key, field])
        return result if result else None
    
    async def hgetall(self, key: str) -> Dict[str, str]:
        """Get all fields from a hash"""
        result = await self._request("HGETALL", [key])
        if not result:
            return {}
        # HGETALL returns a list of [field1, value1, field2, value2, ...]
        if isinstance(result, list):
            return dict(zip(result[::2], result[1::2]))
        return result if isinstance(result, dict) else {}


# Singleton instance
_redis_service: Optional[RedisService] = None


def get_redis_service() -> RedisService:
    """Get Redis service singleton"""
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService()
    return _redis_service

