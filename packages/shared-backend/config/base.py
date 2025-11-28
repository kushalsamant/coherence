"""
Base configuration settings
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings as PydanticBaseSettings
from dotenv import load_dotenv


class BaseSettings(PydanticBaseSettings):
    """Base application settings"""
    
    # Application
    APP_NAME: str = "KVSHVL Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Authentication
    AUTH_URL: str = os.getenv("AUTH_URL", "http://localhost:3000")
    AUTH_SECRET: str = os.getenv("AUTH_SECRET", "")
    NEXTAUTH_SECRET: str = os.getenv("NEXTAUTH_SECRET") or os.getenv("AUTH_SECRET", "")
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

