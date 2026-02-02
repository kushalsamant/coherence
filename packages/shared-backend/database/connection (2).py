"""
Database connection utilities with schema support
"""

import os
from typing import Optional
from urllib.parse import quote_plus, urlparse, urlunparse
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_database_url(
    base_url: Optional[str] = None,
    password_override: Optional[str] = None,
    schema: Optional[str] = None
) -> str:
    """
    Resolve database connection string with optional schema and password override.
    
    Args:
        base_url: Base database URL
        password_override: Optional password override
        schema: Optional PostgreSQL schema name
        
    Returns:
        Database connection string
    """
    # Get base URL from environment if not provided
    if not base_url:
        base_url = os.getenv("DATABASE_URL", "postgresql://localhost/kvshvl_platform")
    
    # Handle password override
    if password_override:
        parsed = urlparse(base_url)
        username = parsed.username or ""
        encoded_password = quote_plus(password_override)
        
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


def create_engine_with_schema(
    database_url: str,
    schema: Optional[str] = None,
    pool_pre_ping: bool = True,
    pool_size: int = 10,
    max_overflow: int = 20,
    echo: bool = False
) -> Engine:
    """
    Create SQLAlchemy engine with schema support.
    
    Args:
        database_url: Database connection string
        schema: Optional PostgreSQL schema name
        pool_pre_ping: Enable connection pool pre-ping
        pool_size: Connection pool size
        max_overflow: Maximum overflow connections
        echo: Enable SQL echo
        
    Returns:
        SQLAlchemy engine
    """
    engine = create_engine(
        database_url,
        pool_pre_ping=pool_pre_ping,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=echo
    )
    
    # Set default schema if provided
    if schema:
        def set_schema(connection, connection_record):
            connection.execute(text(f"SET search_path TO {schema}, public"))
        
        from sqlalchemy import event
        event.listen(engine, "connect", set_schema)
    
    return engine

