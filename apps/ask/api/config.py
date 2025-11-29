"""
Application configuration using Pydantic Settings
Loads environment variables and provides type-safe config
Extends shared BaseSettings with ASK-specific fields
"""
import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse, urlunparse
from dotenv import load_dotenv
from shared_backend.config.base import BaseSettings, get_env_with_fallback, get_env_int_with_fallback

# Load app-specific .env.production from repo root
BASE_DIR = Path(__file__).resolve().parents[2]  # Go up from api/config.py to ask/
APP_ENV_PATH = BASE_DIR.parent / "ask.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application (override base)
    APP_NAME: str = "ASK: Daily Research"
    
    # Database
    DATABASE_URL: str = os.getenv("ASK_DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///./ask.db"))
    DATABASE_URL_OVERRIDE: str = os.getenv("ASK_DATABASE_URL_OVERRIDE", "")
    DATABASE_PASSWORD_OVERRIDE: str = os.getenv("ASK_DATABASE_PASSWORD_OVERRIDE", "")
    
    @property
    def database_url(self) -> str:
        """
        Resolve the database connection string, allowing overrides that keep
        secrets like passwords out of the base URL.
        """
        base_url = self.DATABASE_URL_OVERRIDE or self.DATABASE_URL
        if not base_url:
            base_url = "sqlite:///./ask.db"
        
        if self.DATABASE_PASSWORD_OVERRIDE:
            parsed = urlparse(base_url)
            username = parsed.username or ""
            encoded_password = quote_plus(self.DATABASE_PASSWORD_OVERRIDE)
            
            host_part = parsed.hostname or ""
            if not host_part and parsed.netloc:
                host_part = parsed.netloc.split("@")[-1]
            
            if parsed.port:
                host_with_port = f"{host_part}:{parsed.port}"
            else:
                host_with_port = host_part
            
            if host_with_port:
                if username:
                    netloc = f"{username}:{encoded_password}@{host_with_port}"
                else:
                    netloc = f":{encoded_password}@{host_with_port}"
            else:
                original_host = parsed.netloc.split("@")[-1] if parsed.netloc else ""
                if username:
                    netloc = f"{username}:{encoded_password}@{original_host}"
                else:
                    netloc = parsed.netloc or ""
            
            base_url = urlunparse(parsed._replace(netloc=netloc))
        
        # Ensure SQLAlchemy uses psycopg v3 driver when available
        try:
            import psycopg
            if base_url.startswith("postgresql://"):
                base_url = base_url.replace("postgresql://", "postgresql+psycopg://", 1)
        except Exception:
            pass
        
        return base_url
    
    # Payments - Razorpay
    RAZORPAY_KEY_ID: str = os.getenv("ASK_RAZORPAY_KEY_ID", os.getenv("RAZORPAY_KEY_ID", ""))
    RAZORPAY_KEY_SECRET: str = os.getenv("ASK_RAZORPAY_KEY_SECRET", os.getenv("RAZORPAY_KEY_SECRET", ""))
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("ASK_RAZORPAY_WEBHOOK_SECRET", os.getenv("RAZORPAY_WEBHOOK_SECRET", ""))
    
    # Legacy aliases (for backward compatibility)
    LIVE_KEY_ID: str = os.getenv("LIVE_KEY_ID", "")
    LIVE_KEY_SECRET: str = os.getenv("LIVE_KEY_SECRET", "")
    
    @property
    def razorpay_key_id(self) -> str:
        """Get Razorpay key ID, checking both variable names"""
        return self.RAZORPAY_KEY_ID or self.LIVE_KEY_ID
    
    @property
    def razorpay_key_secret(self) -> str:
        """Get Razorpay key secret, checking both variable names"""
        return self.RAZORPAY_KEY_SECRET or self.LIVE_KEY_SECRET
    
    # Pricing in paise (₹1 = 100 paise)
    # Shared across all projects - check prefixed first, then unprefixed, then default
    RAZORPAY_WEEK_AMOUNT: int = get_env_int_with_fallback("ASK_RAZORPAY_WEEK_AMOUNT", "RAZORPAY_WEEK_AMOUNT", 129900)
    RAZORPAY_MONTH_AMOUNT: int = get_env_int_with_fallback("ASK_RAZORPAY_MONTH_AMOUNT", "RAZORPAY_MONTH_AMOUNT", 349900)
    RAZORPAY_YEAR_AMOUNT: int = get_env_int_with_fallback("ASK_RAZORPAY_YEAR_AMOUNT", "RAZORPAY_YEAR_AMOUNT", 2999900)
    
    # Razorpay Plan IDs for subscriptions (created via scripts/create_razorpay_plans.py)
    # Shared across all projects - check prefixed first, then unprefixed, then default
    RAZORPAY_PLAN_WEEK: str = get_env_with_fallback("ASK_RAZORPAY_PLAN_WEEK", "RAZORPAY_PLAN_WEEK", "")
    RAZORPAY_PLAN_MONTH: str = get_env_with_fallback("ASK_RAZORPAY_PLAN_MONTH", "RAZORPAY_PLAN_MONTH", "")
    RAZORPAY_PLAN_YEAR: str = get_env_with_fallback("ASK_RAZORPAY_PLAN_YEAR", "RAZORPAY_PLAN_YEAR", "")
    
    # Frontend URL
    FRONTEND_URL: str = os.getenv("ASK_FRONTEND_URL", os.getenv("FRONTEND_URL", "http://localhost:3000"))
    
    class Config:
        # Environment variables loaded from ask.env.production
        # via load_dotenv() call above (before this class is initialized)
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

