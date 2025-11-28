"""
Retry logic with exponential backoff
Handles transient failures gracefully
"""
from typing import Callable, Any, Optional, Type, Tuple
import asyncio
import random
from functools import wraps
from datetime import datetime

from loguru import logger


class RetryConfig:
    """Retry configuration"""
    
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retry_on: Tuple[Type[Exception], ...] = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retry_on = retry_on


async def retry_with_backoff(
    func: Callable,
    config: Optional[RetryConfig] = None,
    *args,
    **kwargs
) -> Any:
    """
    Retry function with exponential backoff
    
    Args:
        func: Function to retry
        config: Retry configuration
        *args: Function arguments
        **kwargs: Function keyword arguments
    
    Returns:
        Function result
    
    Raises:
        Exception: Last exception if all retries fail
    """
    config = config or RetryConfig()
    last_exception = None
    
    for attempt in range(1, config.max_attempts + 1):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        except config.retry_on as e:
            last_exception = e
            
            if attempt >= config.max_attempts:
                logger.error(f"Retry exhausted after {attempt} attempts: {e}")
                raise e
            
            # Calculate delay with exponential backoff
            delay = min(
                config.initial_delay * (config.exponential_base ** (attempt - 1)),
                config.max_delay
            )
            
            # Add jitter to prevent thundering herd
            if config.jitter:
                delay = delay * (0.5 + random.random() * 0.5)
            
            logger.warning(
                f"Retry attempt {attempt}/{config.max_attempts} after {delay:.2f}s: {e}"
            )
            
            await asyncio.sleep(delay)
    
    # Should never reach here, but just in case
    if last_exception:
        raise last_exception
    raise Exception("Retry failed without exception")


def retry(config: Optional[RetryConfig] = None):
    """Decorator for retry with backoff"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_with_backoff(func, config, *args, **kwargs)
        return wrapper
    return decorator


async def retry_with_timeout(
    func: Callable,
    timeout_seconds: float,
    config: Optional[RetryConfig] = None,
    *args,
    **kwargs
) -> Any:
    """
    Retry function with timeout
    
    Args:
        func: Function to retry
        timeout_seconds: Maximum time to wait
        config: Retry configuration
        *args: Function arguments
        **kwargs: Function keyword arguments
    
    Returns:
        Function result
    
    Raises:
        asyncio.TimeoutError: If timeout exceeded
        Exception: Last exception if all retries fail
    """
    start_time = datetime.utcnow()
    config = config or RetryConfig()
    last_exception = None
    
    for attempt in range(1, config.max_attempts + 1):
        # Check timeout
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        if elapsed >= timeout_seconds:
            raise asyncio.TimeoutError(f"Retry timeout after {elapsed:.2f}s")
        
        try:
            # Calculate remaining timeout
            remaining_timeout = timeout_seconds - elapsed
            
            if asyncio.iscoroutinefunction(func):
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=remaining_timeout
                )
            else:
                return func(*args, **kwargs)
        
        except (asyncio.TimeoutError, *config.retry_on) as e:
            last_exception = e
            
            if attempt >= config.max_attempts:
                logger.error(f"Retry exhausted after {attempt} attempts: {e}")
                raise e
            
            # Calculate delay
            delay = min(
                config.initial_delay * (config.exponential_base ** (attempt - 1)),
                config.max_delay,
                timeout_seconds - elapsed
            )
            
            if delay <= 0:
                raise asyncio.TimeoutError("No time remaining for retry")
            
            if config.jitter:
                delay = delay * (0.5 + random.random() * 0.5)
            
            logger.warning(f"Retry attempt {attempt}/{config.max_attempts} after {delay:.2f}s: {e}")
            await asyncio.sleep(delay)
    
    if last_exception:
        raise last_exception
    raise Exception("Retry failed without exception")

