"""
Structured logging configuration for production
Implements JSON logging for better log aggregation and searching
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from core.config import settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    Outputs logs as JSON for better parsing in log aggregation systems
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "platform-api",
            "environment": settings.ENVIRONMENT,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from LogRecord
        # Extra fields are added directly as attributes, not in an 'extra' dict
        standard_attrs = {
            'name', 'msg', 'args', 'created', 'filename', 'funcName', 'levelname',
            'levelno', 'lineno', 'module', 'msecs', 'message', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'exc_info',
            'exc_text', 'stack_info', 'getMessage', 'taskName'
        }
        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith('_'):
                log_data[key] = value
        
        # Add file location in debug mode
        if settings.DEBUG:
            log_data.update({
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName
            })
        
        return json.dumps(log_data)


class ReadableFormatter(logging.Formatter):
    """
    Human-readable formatter for development
    Uses colored output and clear formatting
    """
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors and readable structure"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        level = f"{color}{record.levelname:8s}{reset}"
        logger_name = f"{record.name:30s}"
        message = record.getMessage()
        
        formatted = f"{timestamp} | {level} | {logger_name} | {message}"
        
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


def setup_logging():
    """
    Configure application logging based on environment
    - Production: JSON logging
    - Development: Readable colored logging
    """
    # Determine log level
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    # Select formatter based on environment
    if settings.is_production:
        formatter = JSONFormatter()
    else:
        formatter = ReadableFormatter()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={log_level}, format={'JSON' if settings.is_production else 'Readable'}")
    
    return logger
