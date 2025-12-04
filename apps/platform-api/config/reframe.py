"""
Application configuration for Reframe backend
Extends shared BaseSettings with Reframe-specific fields
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from shared_backend.config.base import BaseSettings, get_env_int_with_fallback

# Load app-specific production environment if available (fallback for local/CI)
# Check Render's secret file location first, then fall back to repo root
RENDER_SECRET_PATH = Path("/etc/secrets/.env.local")
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
APP_ENV_PATH = WORKSPACE_ROOT / "reframe.env.production"

# Load from Render secret file if available (production), otherwise from repo root (local dev)
if RENDER_SECRET_PATH.exists():
    load_dotenv(RENDER_SECRET_PATH, override=False)
elif APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Application settings"""
    
    # Application (override base)
    APP_NAME: str = "Reframe API"
    
    # Redis (Upstash) - prefixed envs only
    UPSTASH_REDIS_REST_URL: str = os.getenv("REFRAME_UPSTASH_REDIS_REST_URL", "")
    UPSTASH_REDIS_REST_TOKEN: str = os.getenv("REFRAME_UPSTASH_REDIS_REST_TOKEN", "")

    # Groq - prefixed envs only
    GROQ_API_KEY: str = os.getenv("REFRAME_GROQ_API_KEY", "")

    # Limits
    FREE_LIMIT: int = int(os.getenv("REFRAME_FREE_LIMIT", "5"))

    # CORS - prefixed envs only, with default for local + production
    CORS_ORIGINS: str = os.getenv(
        "REFRAME_CORS_ORIGINS",
        "http://localhost:3000,https://reframe.kvshvl.in"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list"""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Admin Access - prefixed envs only
    ADMIN_EMAILS: str = os.getenv("REFRAME_ADMIN_EMAILS", "")
    
    class Config:
        case_sensitive = True
        extra = "ignore"


# Singleton instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Export for convenience
settings = get_settings()

