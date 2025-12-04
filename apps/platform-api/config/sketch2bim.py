"""
Application configuration using Pydantic Settings
Loads environment variables and provides type-safe config
Extends shared BaseSettings with Sketch2BIM-specific fields
"""
from typing import List
import os
from urllib.parse import quote_plus, urlparse, urlunparse
from pathlib import Path
from dotenv import load_dotenv
from shared_backend.config.base import BaseSettings, get_env_with_fallback, get_env_int_with_fallback

# Load app-specific production environment if available (fallback for local/CI)
# Check Render's secret file location first, then fall back to repo root
RENDER_SECRET_PATH = Path("/etc/secrets/.env.local")
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
APP_ENV_PATH = WORKSPACE_ROOT / "sketch2bim.env.production"

# Load from Render secret file if available (production), otherwise from repo root (local dev)
if RENDER_SECRET_PATH.exists():
    load_dotenv(RENDER_SECRET_PATH, override=False)
elif APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application (override base)
    APP_NAME: str = "Sketch-to-BIM"
    API_VERSION: str = "v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    REQUEST_TIMEOUT_SECONDS: float = 300.0  # 5 minutes default timeout
    
    # CORS
    CORS_ORIGINS: str = os.getenv(
        "SKETCH2BIM_CORS_ORIGINS",
        "http://localhost:3000",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Return allowed CORS origins as a list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Database
    # Upstash Postgres provides DATABASE_URL via environment variable
    # Use only prefixed env vars; fall back to local Postgres for development.
    DATABASE_URL: str = os.getenv("SKETCH2BIM_DATABASE_URL", "postgresql://postgres:password@localhost:5432/sketch2bim")
    DATABASE_URL_OVERRIDE: str = os.getenv("SKETCH2BIM_DATABASE_URL_OVERRIDE", "")
    DATABASE_PASSWORD_OVERRIDE: str = os.getenv("SKETCH2BIM_DATABASE_PASSWORD_OVERRIDE", "")

    @property
    def database_url(self) -> str:
        """
        Resolve the database connection string, allowing overrides that keep
        secrets like passwords out of the base URL.
        """
        base_url = self.DATABASE_URL_OVERRIDE or self.DATABASE_URL
        if not base_url:
            base_url = "postgresql://postgres:password@localhost:5432/sketch2bim"

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
                # Fall back to original netloc structure if host parsing failed
                original_host = parsed.netloc.split("@")[-1] if parsed.netloc else ""
                if username:
                    netloc = f"{username}:{encoded_password}@{original_host}"
                else:
                    netloc = parsed.netloc or ""

            base_url = urlunparse(parsed._replace(netloc=netloc))

        # Ensure SQLAlchemy uses psycopg v3 driver when available
        # Convert postgresql://... to postgresql+psycopg://...
        try:
            import psycopg  # noqa: F401
            if base_url.startswith("postgresql://"):
                base_url = base_url.replace("postgresql://", "postgresql+psycopg://", 1)
        except Exception:
            # psycopg not installed; keep original URL (e.g., psycopg2-binary environments)
            pass

        return base_url
    
    # Redis
    # Upstash provides REDIS_URL automatically when Upstash Redis is configured
    # Use only prefixed env vars; fall back to local Redis if not set.
    REDIS_URL: str = os.getenv("SKETCH2BIM_REDIS_URL", "redis://localhost:6379/0")
    UPSTASH_REDIS_REST_URL: str = os.getenv("SKETCH2BIM_UPSTASH_REDIS_REST_URL", "")
    UPSTASH_REDIS_REST_TOKEN: str = os.getenv("SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN", "")
    
    # Authentication - prefixed envs only
    SECRET_KEY: str = os.getenv("SKETCH2BIM_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    NEXTAUTH_SECRET: str = os.getenv("SKETCH2BIM_NEXTAUTH_SECRET", "")
    
    # Payments - Razorpay
    RAZORPAY_KEY_ID: str = os.getenv("SKETCH2BIM_RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("SKETCH2BIM_RAZORPAY_KEY_SECRET", "")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET", "")
    
    @property
    def razorpay_key_id(self) -> str:
        """Get Razorpay key ID"""
        return self.RAZORPAY_KEY_ID
    
    @property
    def razorpay_key_secret(self) -> str:
        """Get Razorpay key secret"""
        return self.RAZORPAY_KEY_SECRET
    
    # Pricing in paise (₹1 = 100 paise)
    # Trial tier handled separately (free)
    # Week: ₹1,299/week = 129900 paise
    # Monthly: ₹3,499/month = 349900 paise
    # Yearly: ₹29,999/year = 2999900 paise
    RAZORPAY_WEEK_AMOUNT: int = int(os.getenv("SKETCH2BIM_RAZORPAY_WEEK_AMOUNT", "129900"))
    RAZORPAY_MONTH_AMOUNT: int = int(os.getenv("SKETCH2BIM_RAZORPAY_MONTH_AMOUNT", "349900"))
    RAZORPAY_YEAR_AMOUNT: int = int(os.getenv("SKETCH2BIM_RAZORPAY_YEAR_AMOUNT", "2999900"))
    
    # Razorpay Plan IDs for subscriptions (created via scripts/create_razorpay_plans.py)
    RAZORPAY_PLAN_WEEKLY: str = os.getenv("SKETCH2BIM_RAZORPAY_PLAN_WEEKLY", "")
    RAZORPAY_PLAN_MONTHLY: str = os.getenv("SKETCH2BIM_RAZORPAY_PLAN_MONTHLY", "")
    RAZORPAY_PLAN_YEARLY: str = os.getenv("SKETCH2BIM_RAZORPAY_PLAN_YEARLY", "")
    
    # BunnyCDN - prefixed envs only
    BUNNY_STORAGE_ZONE: str = os.getenv("SKETCH2BIM_BUNNY_STORAGE_ZONE", "")
    BUNNY_ACCESS_KEY: str = os.getenv("SKETCH2BIM_BUNNY_ACCESS_KEY", "")
    BUNNY_CDN_HOSTNAME: str = os.getenv("SKETCH2BIM_BUNNY_CDN_HOSTNAME", "")
    BUNNY_REGION: str = "storage.bunnycdn.com"
    BUNNY_SIGNED_URL_KEY: str = ""
    BUNNY_SIGNED_URL_EXPIRY: int = 604800  # 7 days
    
    # ML Processing Agent
    ML_AGENT_ENABLED: bool = True  # Enable intelligent processing agent
    ML_AGENT_MAX_RETRIES: int = 2  # Maximum retry attempts
    ML_AGENT_PREPROCESSING_THRESHOLD: float = 50.0  # Quality threshold for preprocessing
    ML_AGENT_DETECTION_THRESHOLD: float = 30.0  # Confidence threshold for detection
    ML_AGENT_POST_IFC_THRESHOLD: float = 50.0  # Confidence threshold for post-IFC
    
    # Symbol Detector (Optional - requires trained PyTorch model)
    # Note: Symbol detection is disabled by default. To enable:
    # 1. Train a Faster R-CNN model using the training scripts in /train
    # 2. Set SYMBOL_DETECTOR_ENABLED=True
    # 3. Set SYMBOL_DETECTOR_MODEL_PATH to the path of your trained .pth model file
    # 4. Ensure PyTorch and torchvision are installed
    # Without a model, only geometric detection (walls, rooms) is available
    SYMBOL_DETECTOR_ENABLED: bool = False
    SYMBOL_DETECTOR_MODEL_PATH: str = ""  # Path to trained Faster R-CNN weights (.pth file)
    SYMBOL_DETECTOR_CLASS_FILE: str = "train/annotations/classes.yaml"
    SYMBOL_DETECTOR_CONFIDENCE: float = 0.45
    SYMBOL_DETECTOR_DEVICE: str = "auto"  # auto|cpu|cuda
    SYMBOL_DETECTOR_MAX_RESULTS: int = 200
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: str = "png,jpg,jpeg,pdf,dwg"
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    # Trial Tier
    # Note: FREE_CREDITS_LIMIT is deprecated and no longer used
    # Users start with 0 credits and get unlimited conversions during active trial
    # After trial expires, credits remain at 0 - users must upgrade
    FREE_CREDITS_LIMIT: int = 0  # Set to 0 - no free credits after trial
    
    # Monitoring
    LOG_LEVEL: str = "INFO"
    
    # Resource limit monitoring
    DATABASE_LIMIT_MB: int = 500  # Upstash Postgres limit (adjust based on your plan)
    REDIS_LIMIT_COMMANDS_PER_DAY: int = 10000  # Upstash free tier limit
    RESOURCE_ALERT_WARNING_THRESHOLD: int = 80  # Alert at 80% usage
    RESOURCE_ALERT_CRITICAL_THRESHOLD: int = 95  # Critical at 95% usage
    ALERT_EMAIL_ENABLED: bool = True
    ALERT_EMAIL_RECIPIENTS: str = "admin@sketch2bim.com"
    
    # IDS Validation (optional)
    IDS_FILE_PATH: str = ""  # Path to IDS file for validation
    
    # Heroku-style configuration
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.APP_ENV.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.APP_ENV.lower() == "development"
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of missing required fields
        Returns empty list if all required fields are present
        """
        missing = []
        required_fields = [
            'SECRET_KEY',
            'DATABASE_URL',
            'BUNNY_STORAGE_ZONE',
            'BUNNY_ACCESS_KEY',
            'BUNNY_CDN_HOSTNAME',
        ]
        
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                missing.append(field)
        
        # Check Razorpay keys
        if not self.razorpay_key_id or not self.razorpay_key_secret:
            missing.append('SKETCH2BIM_RAZORPAY_KEY_ID/SKETCH2BIM_RAZORPAY_KEY_SECRET')
        
        return missing
    
    class Config:
        # Environment variables loaded from sketch2bim.env.production
        # via load_dotenv() call above (before this class is initialized)
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables (useful for Alembic migrations)


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

