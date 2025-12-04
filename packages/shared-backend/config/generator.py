"""
Configuration generator utility
Helps generate Settings classes for new projects
"""
from typing import Dict, List, Optional
from string import Template


SETTINGS_TEMPLATE = Template('''"""
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
APP_ENV_PATH = BASE_DIR.parent / "${app_name}.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application (override base)
    APP_NAME: str = "${app_display_name}"
    
    # Database (prefixed only; falls back to local sqlite if not set)
    DATABASE_URL: str = os.getenv("${app_prefix}_DATABASE_URL", "sqlite:///./${app_name}.db")
    
    # Payments - Razorpay (prefixed only)
    RAZORPAY_KEY_ID: str = os.getenv("${app_prefix}_RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("${app_prefix}_RAZORPAY_KEY_SECRET", "")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("${app_prefix}_RAZORPAY_WEBHOOK_SECRET", "")
    
    # Pricing in paise (₹1 = 100 paise)
    # Shared across all projects - prefixed variables only, with hard defaults
    RAZORPAY_WEEK_AMOUNT: int = get_env_int_with_fallback("${app_prefix}_RAZORPAY_WEEK_AMOUNT", "RAZORPAY_WEEK_AMOUNT", 129900)
    RAZORPAY_MONTH_AMOUNT: int = get_env_int_with_fallback("${app_prefix}_RAZORPAY_MONTH_AMOUNT", "RAZORPAY_MONTH_AMOUNT", 349900)
    RAZORPAY_YEAR_AMOUNT: int = get_env_int_with_fallback("${app_prefix}_RAZORPAY_YEAR_AMOUNT", "RAZORPAY_YEAR_AMOUNT", 2999900)
    
    # Razorpay Plan IDs for subscriptions
    # Shared across all projects - prefixed variables only
    RAZORPAY_PLAN_WEEKLY: str = get_env_with_fallback("${app_prefix}_RAZORPAY_PLAN_WEEKLY", "RAZORPAY_PLAN_WEEKLY", "")
    RAZORPAY_PLAN_MONTHLY: str = get_env_with_fallback("${app_prefix}_RAZORPAY_PLAN_MONTHLY", "RAZORPAY_PLAN_MONTHLY", "")
    RAZORPAY_PLAN_YEARLY: str = get_env_with_fallback("${app_prefix}_RAZORPAY_PLAN_YEARLY", "RAZORPAY_PLAN_YEARLY", "")
    
    # Frontend URL (prefixed only; defaults to localhost for development)
    FRONTEND_URL: str = os.getenv("${app_prefix}_FRONTEND_URL", "http://localhost:3000")
    
    # CORS
    CORS_ORIGINS: str = os.getenv(
        "${app_prefix}_CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001,https://${app_name}.kvshvl.in",
    )
    
    $custom_fields
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        # Environment variables loaded from ${app_name}.env.production
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
''')


def generate_settings_class(
    app_name: str,
    app_display_name: str,
    app_prefix: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Generate a Settings class configuration file
    
    Args:
        app_name: Lowercase app name (e.g., "ask", "reframe")
        app_display_name: Display name for the app (e.g., "ASK: Daily Research")
        app_prefix: Uppercase prefix for env vars (e.g., "ASK"). If None, auto-generated from app_name
        custom_fields: List of custom field definitions, each with:
            - name: Field name
            - type: Field type (str, int, bool, etc.)
            - default: Default value
            - env_var: Environment variable name
            - docstring: Optional docstring
    
    Returns:
        Generated Settings class code as string
    """
    if app_prefix is None:
        app_prefix = app_name.upper()
    
    # Generate custom fields section
    custom_fields_code = ""
    if custom_fields:
        for field in custom_fields:
            name = field.get("name", "")
            field_type = field.get("type", "str")
            default = field.get("default", "")
            env_var = field.get("env_var", f"{app_prefix}_{name.upper()}")
            docstring = field.get("docstring", "")
            
            if docstring:
                custom_fields_code += f'    # {docstring}\n'
            
            if field_type == "int":
                custom_fields_code += f'    {name}: {field_type} = get_env_int_with_fallback("{env_var}", "{env_var}", {default})\n'
            elif field_type == "bool":
                default_bool = str(default).lower() == "true"
                custom_fields_code += f'    {name}: {field_type} = os.getenv("{env_var}", "{default}").lower() == "true"\n'
            else:
                default_str = f'"{default}"' if isinstance(default, str) else default
                custom_fields_code += f'    {name}: {field_type} = os.getenv("{env_var}", {default_str})\n'
            custom_fields_code += "\n"
    
    return SETTINGS_TEMPLATE.substitute(
        app_name=app_name,
        app_display_name=app_display_name,
        app_prefix=app_prefix,
        custom_fields=custom_fields_code.strip() if custom_fields_code else "",
    )


# CLI usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python generator.py <app_name> <app_display_name> [app_prefix]")
        print("Example: python generator.py ask 'ASK: Daily Research' ASK")
        sys.exit(1)
    
    app_name = sys.argv[1]
    app_display_name = sys.argv[2]
    app_prefix = sys.argv[3] if len(sys.argv) > 3 else None
    
    output = generate_settings_class(
        app_name=app_name,
        app_display_name=app_display_name,
        app_prefix=app_prefix,
    )
    
    print(output)

