"""
Circuit breaker implementation for external service calls
Prevents cascading failures and provides fallback mechanisms
"""
from enum import Enum
from typing import Callable, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
from functools import wraps

from loguru import logger


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5  # Open circuit after N failures
    success_threshold: int = 2  # Close circuit after N successes (half-open)
    timeout_seconds: int = 60  # Time before trying half-open
    expected_exception: type = Exception


class CircuitBreaker:
    """Circuit breaker for external service calls"""
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Exception: If circuit is open or function fails
        """
        async with self._lock:
            # Check if circuit should transition to half-open
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    logger.info(f"Circuit breaker {self.name} transitioning to HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception(f"Circuit breaker {self.name} is OPEN. Service unavailable.")
        
        # Attempt the call
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Success
            await self._record_success()
            return result
        
        except self.config.expected_exception as e:
            await self._record_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.timeout_seconds
    
    async def _record_success(self):
        """Record successful call"""
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    logger.info(f"Circuit breaker {self.name} closing (service recovered)")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                # Reset failure count on success
                self.failure_count = 0
    
    async def _record_failure(self):
        """Record failed call"""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            
            if self.state == CircuitState.HALF_OPEN:
                # Failed during half-open, go back to open
                logger.warning(f"Circuit breaker {self.name} reopening (service still failing)")
                self.state = CircuitState.OPEN
                self.success_count = 0
            elif self.failure_count >= self.config.failure_threshold:
                # Too many failures, open circuit
                logger.error(f"Circuit breaker {self.name} opening after {self.failure_count} failures")
                self.state = CircuitState.OPEN
    
    def get_state(self) -> CircuitState:
        """Get current circuit state"""
        return self.state
    
    def reset(self):
        """Manually reset circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logger.info(f"Circuit breaker {self.name} manually reset")


# Global circuit breakers
_circuit_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
    """Get or create circuit breaker instance"""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, config)
    return _circuit_breakers[name]


def circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None):
    """Decorator for circuit breaker"""
    def decorator(func: Callable):
        cb = get_circuit_breaker(name, config)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await cb.call(func, *args, **kwargs)
        
        return wrapper
    return decorator

