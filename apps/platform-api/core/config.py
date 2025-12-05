"""
Centralized Configuration Management
Uses Pydantic Settings for type-safe environment variable handling

Note: Environment variables in Render use PLATFORM_ prefix for platform-wide settings
and app-specific prefixes (ASK_, REFRAME_, SKETCH2BIM_) for app-specific settings.
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
    - App-specific: ASK_DATABASE_URL, REFRAME_GROQ_API_KEY, etc.
    """
    
    # Application Configuration (from PLATFORM_ prefix)
    APP_NAME: str = Field(default="KVSHVL Platform API", alias="PLATFORM_APP_NAME")
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", alias="PLATFORM_ENVIRONMENT")
    DEBUG: bool = Field(default=False, alias="PLATFORM_DEBUG")
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # CORS Configuration (from PLATFORM_ prefix)
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,https://kvshvl.in,https://www.kvshvl.in",
        alias="PLATFORM_CORS_ORIGINS"
    )
    
    # Database URLs (app-specific, no prefix)
    ASK_DATABASE_URL: str = Field(default="", description="PostgreSQL connection string for ASK database")
    SKETCH2BIM_DATABASE_URL: str = Field(default="", description="PostgreSQL connection string for Sketch2BIM database")
    
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
    
    # AI Service API Keys (app-specific, no prefix)
    ASK_GROQ_API_KEY: str = Field(default="", description="Groq API key for ASK")
    REFRAME_GROQ_API_KEY: str = Field(default="", description="Groq API key for Reframe")
    SKETCH2BIM_GROQ_API_KEY: str = Field(default="", description="Groq API key for Sketch2BIM")
    SKETCH2BIM_REPLICATE_API_KEY: str = Field(default="", description="Replicate API key for Sketch2BIM")
    
    # Groq API Configuration (app-specific)
    ASK_GROQ_MODEL: str = "llama-3.1-70b-versatile"
    ASK_GROQ_API_BASE: str = "https://api.groq.com/openai/v1"
    
    # Reframe Configuration (app-specific)
    REFRAME_FREE_LIMIT: int = 5
    
    # Sketch2BIM Storage Configuration (app-specific)
    SKETCH2BIM_BUNNY_STORAGE_ZONE: str = Field(default="", description="BunnyCDN storage zone")
    SKETCH2BIM_BUNNY_ACCESS_KEY: str = Field(default="", description="BunnyCDN access key")
    SKETCH2BIM_BUNNY_CDN_HOSTNAME: str = Field(default="", description="BunnyCDN hostname")
    SKETCH2BIM_REPLICATE_MODEL_ID: str = "kushalsamant/sketch2bim-processor"
    
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
    model_config = SettingsConfigDict(
        env_file=".env",
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
