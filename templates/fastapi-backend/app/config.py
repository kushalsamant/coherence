"""
Application configuration using Pydantic Settings
Loads environment variables and provides type-safe config
Extends shared BaseSettings with app-specific fields
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from shared_backend.config.base import BaseSettings, get_env_with_fallback, get_env_int_with_fallback

# Load app-specific .env.production from repo root
BASE_DIR = Path(__file__).resolve().parents[2]  # Go up from app/config.py to backend/
APP_ENV_PATH = BASE_DIR.parent / "{{APP_NAME}}.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application (override base)
    APP_NAME: str = "{{APP_DISPLAY_NAME}}"
    
    # Database (prefixed only; falls back to local sqlite if not set)
    DATABASE_URL: str = os.getenv("{{APP_PREFIX}}_DATABASE_URL", "sqlite:///./{{APP_NAME}}.db")
    
    # Payments - Razorpay (prefixed only)
    RAZORPAY_KEY_ID: str = os.getenv("{{APP_PREFIX}}_RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("{{APP_PREFIX}}_RAZORPAY_KEY_SECRET", "")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("{{APP_PREFIX}}_RAZORPAY_WEBHOOK_SECRET", "")
    
    # Pricing in paise (₹1 = 100 paise)
    # Shared across all projects - prefixed variables only, with hard defaults
    RAZORPAY_WEEK_AMOUNT: int = get_env_int_with_fallback("{{APP_PREFIX}}_RAZORPAY_WEEK_AMOUNT", "RAZORPAY_WEEK_AMOUNT", 129900)
    RAZORPAY_MONTH_AMOUNT: int = get_env_int_with_fallback("{{APP_PREFIX}}_RAZORPAY_MONTH_AMOUNT", "RAZORPAY_MONTH_AMOUNT", 349900)
    RAZORPAY_YEAR_AMOUNT: int = get_env_int_with_fallback("{{APP_PREFIX}}_RAZORPAY_YEAR_AMOUNT", "RAZORPAY_YEAR_AMOUNT", 2999900)
    
    # Razorpay Plan IDs for subscriptions
    # Shared across all projects - prefixed variables only
    RAZORPAY_PLAN_WEEKLY: str = get_env_with_fallback("{{APP_PREFIX}}_RAZORPAY_PLAN_WEEKLY", "RAZORPAY_PLAN_WEEKLY", "")
    RAZORPAY_PLAN_MONTHLY: str = get_env_with_fallback("{{APP_PREFIX}}_RAZORPAY_PLAN_MONTHLY", "RAZORPAY_PLAN_MONTHLY", "")
    RAZORPAY_PLAN_YEARLY: str = get_env_with_fallback("{{APP_PREFIX}}_RAZORPAY_PLAN_YEARLY", "RAZORPAY_PLAN_YEARLY", "")
    
    # Frontend URL (prefixed only; defaults to localhost for development)
    FRONTEND_URL: str = os.getenv("{{APP_PREFIX}}_FRONTEND_URL", "http://localhost:3000")
    
    # CORS
    CORS_ORIGINS: str = os.getenv(
        "{{APP_PREFIX}}_CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001,https://{{APP_NAME}}.kvshvl.in",
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        # Environment variables loaded from {{APP_NAME}}.env.production
        # via load_dotenv() call above
        case_sensitive = True
        extra = "ignore"


# Singleton instance
_settings = None

def get_settings() -> Settings:
    """Get settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Export for convenience
settings = get_settings()

