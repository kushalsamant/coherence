"""
Base configuration settings
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings as PydanticBaseSettings
from dotenv import load_dotenv


def get_env_with_fallback(prefixed_key: str, unprefixed_key: str, default: str) -> str:
    """
    Get environment variable with fallback chain that properly handles empty strings.
    
    Checks prefixed key first, then unprefixed key, then uses default.
    Empty strings are treated as missing values and trigger fallback.
    
    Args:
        prefixed_key: The prefixed environment variable name (e.g., "SKETCH2BIM_RAZORPAY_WEEKLY_AMOUNT")
        unprefixed_key: The unprefixed environment variable name (e.g., "RAZORPAY_WEEKLY_AMOUNT")
        default: Default value to use if both are missing or empty
    
    Returns:
        The environment variable value or default
    """
    # Check prefixed first
    prefixed_value = os.getenv(prefixed_key)
    if prefixed_value and prefixed_value.strip():
        return prefixed_value
    
    # Check unprefixed
    unprefixed_value = os.getenv(unprefixed_key)
    if unprefixed_value and unprefixed_value.strip():
        return unprefixed_value
    
    # Use default
    return default


def get_env_int_with_fallback(prefixed_key: str, unprefixed_key: str, default: int) -> int:
    """
    Get environment variable as integer with fallback chain that properly handles empty strings.
    
    Checks prefixed key first, then unprefixed key, then uses default.
    Empty strings are treated as missing values and trigger fallback.
    
    Args:
        prefixed_key: The prefixed environment variable name (e.g., "SKETCH2BIM_RAZORPAY_WEEKLY_AMOUNT")
        unprefixed_key: The unprefixed environment variable name (e.g., "RAZORPAY_WEEKLY_AMOUNT")
        default: Default integer value to use if both are missing or empty
    
    Returns:
        The environment variable value as integer or default
    """
    value = get_env_with_fallback(prefixed_key, unprefixed_key, str(default))
    try:
        return int(value)
    except ValueError:
        return default


class BaseSettings(PydanticBaseSettings):
    """Base application settings"""
    
    # Application
    APP_NAME: str = "KVSHVL Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Authentication
    AUTH_URL: str = os.getenv("AUTH_URL", "http://localhost:3000")
    NEXTAUTH_SECRET: str = os.getenv("NEXTAUTH_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    # Admin emails (can be overridden)
    ADMIN_EMAILS: list[str] = []
    
    class Config:
        case_sensitive = True
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance
_settings: Optional[BaseSettings] = None


def get_settings() -> BaseSettings:
    """Get settings singleton"""
    global _settings
    if _settings is None:
        # Note: App-specific .env.production files are loaded by each app's config
        # This base class relies on system environment variables or .env files
        
        _settings = BaseSettings()
    return _settings

