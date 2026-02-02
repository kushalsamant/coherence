"""
Database setup and session management for Platform
SQLAlchemy with async support
Uses shared platform database for user and subscription management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from core.config import settings

# Create database engine - uses shared platform database
engine = create_engine(
    settings.PLATFORM_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables using SQLAlchemy's create_all().
    
    Note: This is a fallback method. The preferred approach is to use Alembic
    migrations (via run_migrations() in app.utils.migrations), which provides
    version control, rollback capability, and handles data migrations safely.
    
    This function is kept as a fallback when
    auto-migrations are disabled or fail.
    """
    Base.metadata.create_all(bind=engine)
