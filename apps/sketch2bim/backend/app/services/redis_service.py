"""
Redis Service for Sketch2BIM
Handles Upstash Redis REST API operations for rate limiting
"""
import os
import json
from typing import Optional, Dict, Any
import httpx


class RedisService:
    """Upstash Redis REST API client"""
    
    def __init__(self):
        self.url = os.getenv("SKETCH2BIM_UPSTASH_REDIS_REST_URL")
        self.token = os.getenv("SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN")
        if not self.url or not self.token:
            raise ValueError("SKETCH2BIM_UPSTASH_REDIS_REST_URL and SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN must be set")
        
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
    
    async def setex(self, key: str, seconds: int, value: str) -> bool:
        """Set a value with expiration"""
        result = await self._request("SETEX", [key, str(seconds), value])
        return result == "OK"
    
    async def incr(self, key: str) -> int:
        """Increment a key"""
        result = await self._request("INCR", [key])
        return result or 0
    
    async def delete(self, *keys: str) -> int:
        """Delete keys from Redis"""
        result = await self._request("DEL", list(keys))
        return result or 0


# Singleton instance
_redis_service: Optional[RedisService] = None


def get_redis_service() -> RedisService:
    """Get Redis service singleton"""
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService()
    return _redis_service

