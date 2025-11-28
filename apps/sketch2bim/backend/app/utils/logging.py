"""
Enhanced logging configuration with structured logging and correlation IDs
"""
import sys
import uuid
from contextvars import ContextVar
from typing import Optional, Dict, Any

from loguru import logger

# Context variable for correlation ID
correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


def configure_logging(log_level: str = "INFO", json_format: bool = False):
    """
    Configure structured logging
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        json_format: Use JSON format for log aggregation
    """
    logger.remove()
    
    if json_format:
        # JSON format for log aggregation (Loki, CloudWatch, etc.)
        logger.add(
            sys.stderr,
            format="{time} | {level} | {name}:{function}:{line} | {message} | {extra}",
            level=log_level,
            serialize=True,  # Output as JSON
            backtrace=True,
            diagnose=True
        )
    else:
        # Human-readable format
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
            level=log_level,
            backtrace=True,
            diagnose=True
        )
    
    # Add file logging
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | {extra}",
        backtrace=True,
        diagnose=True
    )


def set_correlation_id(cid: Optional[str] = None) -> str:
    """
    Set correlation ID for request tracing
    
    Args:
        cid: Correlation ID (generates new if None)
        
    Returns:
        Correlation ID
    """
    if cid is None:
        cid = str(uuid.uuid4())
    correlation_id.set(cid)
    return cid


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID"""
    return correlation_id.get()


def log_with_context(
    level: str,
    message: str,
    **kwargs
):
    """
    Log with correlation ID and additional context
    
    Args:
        level: Log level (info, warning, error, etc.)
        message: Log message
        **kwargs: Additional context fields
    """
    cid = get_correlation_id()
    extra = {"correlation_id": cid, **kwargs}
    
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message, **extra)


def log_job_with_context(job_id: str, event: str, details: Optional[Dict[str, Any]] = None):
    """
    Log job event with correlation ID
    
    Args:
        job_id: Job identifier
        event: Event name
        details: Additional details
    """
    cid = get_correlation_id()
    log_data = {
        "correlation_id": cid,
        "job_id": job_id,
        "event": event,
        "details": details or {}
    }
    logger.info(f"Job event: {event}", **log_data)

