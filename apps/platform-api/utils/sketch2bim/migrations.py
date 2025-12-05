"""
Database migration utilities for Sketch2BIM
Automatically runs Alembic migrations on application startup
"""
from pathlib import Path
from alembic import command
from alembic.config import Config
from loguru import logger
from typing import Optional

from config.sketch2bim import settings


def get_alembic_config() -> Config:
    """
    Get Alembic configuration object
    """
    # Get the repository root (3 levels up from utils/sketch2bim/)
    repo_root = Path(__file__).resolve().parents[4]
    alembic_ini_path = repo_root / "database" / "migrations" / "sketch2bim" / "alembic.ini"
    
    # Create Alembic config
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(alembic_ini_path.parent))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    return alembic_cfg


def run_migrations() -> bool:
    """
    Run Alembic migrations automatically on startup.
    
    This function programmatically runs 'alembic upgrade head' to ensure
    the database schema is up-to-date before the application starts.
    
    Returns:
        bool: True if migrations succeeded, False otherwise
        
    Note:
        Migration failures are logged but don't crash the application.
        This allows the app to start even if migrations fail, but you should
        investigate and fix migration issues promptly.
    """
    # Check if auto-migrations are enabled
    auto_run = getattr(settings, 'AUTO_RUN_MIGRATIONS', True)
    if not auto_run:
        logger.info("Auto-run migrations disabled (AUTO_RUN_MIGRATIONS=false). Skipping migrations.")
        return True
    
    try:
        logger.info("Running database migrations...")
        alembic_cfg = get_alembic_config()
        
        # Run migrations to head
        command.upgrade(alembic_cfg, "head")
        
        logger.success("Database migrations completed successfully")
        return True
        
    except Exception as e:
        logger.error(
            f"Failed to run database migrations: {e}",
            exc_info=True
        )
        logger.warning(
            "Application will continue to start, but database schema may be out of date. "
            "Please investigate and fix migration issues."
        )
        return False


def get_current_revision() -> Optional[str]:
    """
    Get the current database revision.
    
    Returns:
        str: Current revision string, or None if unable to determine
    """
    try:
        alembic_cfg = get_alembic_config()
        current_rev = command.current(alembic_cfg, verbose=False)
        return current_rev if current_rev else None
    except Exception as e:
        logger.debug(f"Could not determine current revision: {e}")
        return None


def get_head_revision() -> Optional[str]:
    """
    Get the head (latest) migration revision.
    
    Returns:
        str: Head revision string, or None if unable to determine
    """
    try:
        alembic_cfg = get_alembic_config()
        from alembic.script import ScriptDirectory
        script = ScriptDirectory.from_config(alembic_cfg)
        head_rev = script.get_current_head()
        return head_rev if head_rev else None
    except Exception as e:
        logger.debug(f"Could not determine head revision: {e}")
        return None

