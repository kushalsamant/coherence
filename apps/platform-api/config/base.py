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

# Load unified .env.local from repo root for local development
# For production, environment variables are set in Render dashboard or secret files
# Check Render's secret file location first, then fall back to repo root
RENDER_SECRET_PATH = Path("/etc/secrets/.env.local")
REPO_ROOT = Path(__file__).resolve().parents[3]  # Go up to repo root
APP_ENV_PATH = REPO_ROOT / ".env.local"

# Load from Render secret file if available (production), otherwise from repo root (local dev)
if RENDER_SECRET_PATH.exists():
    load_dotenv(RENDER_SECRET_PATH, override=False)
elif APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application (override base)
    APP_NAME: str = "ASK: Daily Research"

    # Database (prefixed only; falls back to local sqlite if not set)
    DATABASE_URL: str = os.getenv("ASK_DATABASE_URL", "sqlite:///./ask.db")
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
    
    # Payments - Razorpay (prefixed only; unprefixed RAZORPAY_* no longer used)
    RAZORPAY_KEY_ID: str = os.getenv("ASK_RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("ASK_RAZORPAY_KEY_SECRET", "")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("ASK_RAZORPAY_WEBHOOK_SECRET", "")
    
    @property
    def razorpay_key_id(self) -> str:
        """Get Razorpay key ID"""
        return self.RAZORPAY_KEY_ID
    
    @property
    def razorpay_key_secret(self) -> str:
        """Get Razorpay key secret"""
        return self.RAZORPAY_KEY_SECRET
    
    # Pricing in paise (₹1 = 100 paise)
    RAZORPAY_WEEKLY_AMOUNT: int = int(os.getenv("ASK_RAZORPAY_WEEKLY_AMOUNT", "129900"))
    RAZORPAY_MONTHLY_AMOUNT: int = int(os.getenv("ASK_RAZORPAY_MONTHLY_AMOUNT", "349900"))
    RAZORPAY_YEARLY_AMOUNT: int = int(os.getenv("ASK_RAZORPAY_YEARLY_AMOUNT", "2999900"))
    
    # Razorpay Plan IDs for subscriptions (created via scripts/create_razorpay_plans.py)
    RAZORPAY_PLAN_WEEKLY: str = os.getenv("ASK_RAZORPAY_PLAN_WEEKLY", "")
    RAZORPAY_PLAN_MONTHLY: str = os.getenv("ASK_RAZORPAY_PLAN_MONTHLY", "")
    RAZORPAY_PLAN_YEARLY: str = os.getenv("ASK_RAZORPAY_PLAN_YEARLY", "")

    # Frontend URL (prefixed only; defaults to localhost for development)
    FRONTEND_URL: str = os.getenv("ASK_FRONTEND_URL", "http://localhost:3000")

    # CORS
    CORS_ORIGINS: str = os.getenv(
        "ASK_CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001,https://ask.kvshvl.in,https://www.ask.kvshvl.in",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

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

