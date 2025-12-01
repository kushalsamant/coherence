"""
Database size monitoring
Tracks PostgreSQL database size and alerts when approaching limits
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
from ..config import settings
from loguru import logger

# Default limits (can be overridden via environment)
DATABASE_LIMIT_MB = int(getattr(settings, 'DATABASE_LIMIT_MB', 500))  # Supabase free tier


def get_database_size(db: Session) -> Dict[str, Any]:
    """
    Get current database size in MB
    
    Args:
        db: Database session
        
    Returns:
        dict with size_mb, size_bytes, limit_mb, percentage_used, status
    """
    try:
        # Query database size
        # Extract database name from connection string
        result = db.execute(text("SELECT pg_database_size(current_database())"))
        size_bytes = result.scalar()
        
        if size_bytes is None:
            logger.warning("Could not determine database size")
            return {
                "size_mb": 0,
                "size_bytes": 0,
                "limit_mb": DATABASE_LIMIT_MB,
                "percentage_used": 0,
                "status": "unknown",
                "error": "Could not determine database size"
            }
        
        size_mb = size_bytes / (1024 * 1024)
        percentage_used = (size_mb / DATABASE_LIMIT_MB) * 100 if DATABASE_LIMIT_MB > 0 else 0
        
        # Determine status
        if percentage_used >= 95:
            status = "critical"
        elif percentage_used >= 80:
            status = "warning"
        else:
            status = "ok"
        
        return {
            "size_mb": round(size_mb, 2),
            "size_bytes": size_bytes,
            "limit_mb": DATABASE_LIMIT_MB,
            "percentage_used": round(percentage_used, 2),
            "status": status,
            "remaining_mb": round(DATABASE_LIMIT_MB - size_mb, 2)
        }
    except Exception as e:
        logger.error(f"Error getting database size: {e}")
        return {
            "size_mb": 0,
            "size_bytes": 0,
            "limit_mb": DATABASE_LIMIT_MB,
            "percentage_used": 0,
            "status": "error",
            "error": str(e)
        }


def get_table_sizes(db: Session) -> Dict[str, Any]:
    """
    Get size breakdown by table
    
    Args:
        db: Database session
        
    Returns:
        dict with table sizes
    """
    try:
        query = text("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
                pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """)
        
        result = db.execute(query)
        tables = []
        for row in result:
            tables.append({
                "schema": row[0],
                "table": row[1],
                "size": row[2],
                "size_bytes": row[3]
            })
        
        return {
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        logger.error(f"Error getting table sizes: {e}")
        return {
            "tables": [],
            "count": 0,
            "error": str(e)
        }

