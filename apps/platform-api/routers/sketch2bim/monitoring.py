"""
Monitoring routes for resource usage and alerts
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.sketch2bim import get_db
from auth.sketch2bim import is_admin
from sketch2bim_models import User
from services.sketch2bim.database_monitor import get_database_size, get_table_sizes
from services.sketch2bim.redis_monitor import get_redis_usage, get_redis_info
from services.sketch2bim.storage_monitor import get_storage_usage
from services.sketch2bim.alerts import check_resource_limits, ResourceAlert

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/status")
def get_monitoring_status(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get all resource status
    
    Returns:
        Combined status of all resources
    """
    from datetime import datetime
    from ..monitoring.metrics import update_resource_metrics
    
    # Update Prometheus metrics
    update_resource_metrics(db)
    
    return {
        "database": get_database_size(db),
        "redis": get_redis_usage(),
        "storage": get_storage_usage(),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/database-size")
def get_database_size_endpoint(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get database size information
    
    Returns:
        Database size and usage statistics
    """
    return get_database_size(db)


@router.get("/database-size/tables")
def get_database_table_sizes(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get database table size breakdown
    
    Returns:
        Table sizes sorted by size
    """
    return get_table_sizes(db)


@router.get("/redis-usage")
def get_redis_usage_endpoint(
    admin: User = Depends(is_admin)
) -> Dict[str, Any]:
    """
    Get Redis usage information
    
    Returns:
        Redis command usage statistics
    """
    return get_redis_usage()


@router.get("/redis-info")
def get_redis_info_endpoint(
    admin: User = Depends(is_admin)
) -> Dict[str, Any]:
    """
    Get Redis server information
    
    Returns:
        Redis server details
    """
    return get_redis_info()


@router.get("/storage-usage")
def get_storage_usage_endpoint(
    admin: User = Depends(is_admin)
) -> Dict[str, Any]:
    """
    Get storage usage information
    
    Returns:
        Storage usage and cost estimates
    """
    return get_storage_usage()


@router.get("/alerts")
def get_alerts(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current resource limit alerts
    
    Returns:
        List of active alerts
    """
    alerts = check_resource_limits(db)
    return {
        "alerts": [alert.to_dict() for alert in alerts],
        "count": len(alerts),
        "critical_count": len([a for a in alerts if a.level == "critical"]),
        "warning_count": len([a for a in alerts if a.level == "warning"])
    }


@router.get("/recommendations")
def get_recommendations(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get migration recommendations based on current usage
    
    Returns:
        Recommendations for when to migrate services
    """
    db_info = get_database_size(db)
    redis_info = get_redis_usage()
    storage_info = get_storage_usage()
    
    recommendations = []
    
    # Database recommendations
    if db_info.get("percentage_used", 0) > 80:
        recommendations.append({
            "service": "database",
            "priority": "high" if db_info.get("percentage_used", 0) > 95 else "medium",
            "message": f"Database is {db_info.get('percentage_used', 0):.1f}% full. Consider upgrading Upstash Postgres plan or migrating to self-hosted PostgreSQL.",
            "current_usage": f"{db_info.get('size_mb', 0):.1f}MB / {db_info.get('limit_mb', 0)}MB",
            "options": [
                "Upgrade Upstash Postgres plan",
                "Migrate to self-hosted PostgreSQL (Hetzner, DigitalOcean, Oracle Cloud)",
                "Archive old job data"
            ]
        })
    
    # Redis recommendations
    if redis_info.get("percentage_used", 0) > 80:
        recommendations.append({
            "service": "redis",
            "priority": "high" if redis_info.get("percentage_used", 0) > 95 else "medium",
            "message": f"Redis usage is {redis_info.get('percentage_used', 0):.1f}% of daily limit. Consider migrating to self-hosted Redis or upgrading Upstash plan.",
            "current_usage": f"{redis_info.get('commands_today', 0)} / {redis_info.get('limit_per_day', 0)} commands today",
            "options": [
                "Upgrade Upstash plan",
                "Migrate to self-hosted Redis",
                "Optimize cache usage"
            ]
        })
    
    # Storage recommendations
    if storage_info.get("cost_estimate_usd", 0) > 10:
        recommendations.append({
            "service": "storage",
            "priority": "low",
            "message": f"Storage cost estimate is ${storage_info.get('cost_estimate_usd', 0):.2f}/month. Consider implementing cleanup policies.",
            "current_usage": f"{storage_info.get('size_gb', 0):.1f}GB",
            "options": [
                "Implement automatic file cleanup (7-day retention)",
                "Migrate to self-hosted storage (MinIO, S3-compatible)",
                "Review storage retention policies"
            ]
        })
    
    return {
        "recommendations": recommendations,
        "count": len(recommendations),
        "high_priority_count": len([r for r in recommendations if r["priority"] == "high"])
    }

