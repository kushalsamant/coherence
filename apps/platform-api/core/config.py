"""
Centralized Configuration Management
Uses Pydantic Settings for type-safe environment variable handling

Note: Environment variables use PLATFORM_ prefix for platform-wide settings.
App-specific settings are now in each app's repository.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    Environment variable mapping:
    - Platform-wide: PLATFORM_APP_NAME, PLATFORM_ENVIRONMENT, etc.
    - Platform-wide: PLATFORM_DATABASE_URL, PLATFORM_NEXTAUTH_SECRET, etc.
    - Note: Sketch2BIM-specific configs are in the sketch2bim repository
    """
    
    # Application Configuration (from PLATFORM_ prefix)
    APP_NAME: str = Field(default="KVSHVL API", alias="PLATFORM_APP_NAME")
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", alias="PLATFORM_ENVIRONMENT")
    DEBUG: bool = Field(default=False, alias="PLATFORM_DEBUG")
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # CORS Configuration (from PLATFORM_ prefix)
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,https://kvshvl.in,https://www.kvshvl.in,https://sketch2bim.kvshvl.in",
        alias="PLATFORM_CORS_ORIGINS"
    )
    
    # Database URLs (platform-wide, shared database)
    PLATFORM_DATABASE_URL: str = Field(default="", description="PostgreSQL connection string for platform database (shared by home site and sketch2bim)")
    
    # Database Pool Settings
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis Configuration (from PLATFORM_ prefix)
    UPSTASH_REDIS_REST_URL: str = Field(default="", alias="PLATFORM_UPSTASH_REDIS_REST_URL")
    UPSTASH_REDIS_REST_TOKEN: str = Field(default="", alias="PLATFORM_UPSTASH_REDIS_REST_TOKEN")
    
    # Authentication (from PLATFORM_ prefix)
    AUTH_SECRET: str = Field(default="", alias="PLATFORM_AUTH_SECRET")
    NEXTAUTH_SECRET: str = Field(default="", alias="PLATFORM_NEXTAUTH_SECRET")
    
    # Admin Configuration (from PLATFORM_ prefix)
    ADMIN_EMAILS: str = Field(
        default="writetokushaldsamant@gmail.com",
        alias="PLATFORM_ADMIN_EMAILS"
    )
    
    # Razorpay Configuration (from PLATFORM_ prefix)
    RAZORPAY_KEY_ID: str = Field(default="", alias="PLATFORM_RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: str = Field(default="", alias="PLATFORM_RAZORPAY_KEY_SECRET")
    RAZORPAY_WEBHOOK_SECRET: str = Field(default="", alias="PLATFORM_RAZORPAY_WEBHOOK_SECRET")
    RAZORPAY_PLAN_WEEKLY: str = Field(default="", alias="PLATFORM_RAZORPAY_PLAN_WEEKLY")
    RAZORPAY_PLAN_MONTHLY: str = Field(default="", alias="PLATFORM_RAZORPAY_PLAN_MONTHLY")
    RAZORPAY_PLAN_YEARLY: str = Field(default="", alias="PLATFORM_RAZORPAY_PLAN_YEARLY")
    
    # Note: App-specific configuration (e.g., SKETCH2BIM_*) is now in each app's repository
    # Platform only handles shared infrastructure (auth, payments, database)
    
    # Computed Properties
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def admin_emails_list(self) -> List[str]:
        """Get admin emails as a list"""
        return [email.strip().lower() for email in self.ADMIN_EMAILS.split(",") if email.strip()]
    
    # Pydantic V2 configuration
    # Load backend env file based on environment
    # Default to .env.local.backend for development, .env.production.backend for production
    _env_file = ".env.local.backend"
    if os.getenv("PLATFORM_ENVIRONMENT", "").lower() == "production" or os.getenv("NODE_ENV", "").lower() == "production":
        _env_file = ".env.production.backend"
    
    model_config = SettingsConfigDict(
        env_file=_env_file,
        env_file_encoding="utf-8",
        case_sensitive=True,
        # Allow both direct names and aliases (for PLATFORM_ prefix)
        populate_by_name=True,
        # Extra fields allowed (for flexibility)
        extra="allow"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Using lru_cache ensures settings are only loaded once
    """
    return Settings()


# Global settings instance
settings = get_settings()
