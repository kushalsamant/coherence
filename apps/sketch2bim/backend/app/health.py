"""
Comprehensive health check endpoints
Provides liveness, readiness, and startup probes
"""
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database import get_db
from ..config import settings
from loguru import logger

router = APIRouter(tags=["health"])


class HealthStatus:
    """Health check status"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


async def check_database(db: Session) -> Dict[str, Any]:
    """Check database connectivity"""
    try:
        # Simple query to test connection
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        return {
            "status": HealthStatus.HEALTHY,
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": HealthStatus.UNHEALTHY,
            "message": f"Database connection failed: {str(e)}"
        }


async def check_redis() -> Dict[str, Any]:
    """Check Redis connectivity"""
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        redis_client.ping()
        redis_client.close()
        return {
            "status": HealthStatus.HEALTHY,
            "message": "Redis connection successful"
        }
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        return {
            "status": HealthStatus.DEGRADED,
            "message": f"Redis connection failed: {str(e)}"
        }


async def check_external_services() -> Dict[str, Any]:
    """Check external service availability"""
    services = {}
    
    # Check BunnyCDN (if configured)
    if settings.BUNNY_ACCESS_KEY:
        try:
            import requests
            response = requests.get(
                f"https://{settings.BUNNY_REGION}/{settings.BUNNY_STORAGE_ZONE}/",
                headers={"AccessKey": settings.BUNNY_ACCESS_KEY},
                timeout=3
            )
            if response.status_code in [200, 401]:  # 401 means auth works, just no access
                services["bunnycdn"] = {"status": HealthStatus.HEALTHY}
            else:
                services["bunnycdn"] = {"status": HealthStatus.DEGRADED}
        except Exception as e:
            services["bunnycdn"] = {
                "status": HealthStatus.DEGRADED,
                "message": str(e)
            }
    
    return services


@router.get("/health")
async def health_check():
    """
    Basic health check (liveness probe)
    Returns 200 if the service is running
    """
    return {
        "status": HealthStatus.HEALTHY,
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.API_VERSION
    }


@router.get("/health/ready")
async def readiness_check(response: Response, db: Session = Depends(get_db)):
    """
    Readiness probe
    Checks if the service is ready to accept traffic
    Verifies database and critical dependencies
    """
    checks = {
        "database": await check_database(db),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Determine overall status
    db_status = checks["database"]["status"]
    overall_status = HealthStatus.HEALTHY if db_status == HealthStatus.HEALTHY else HealthStatus.UNHEALTHY
    
    status_code = 200 if overall_status == HealthStatus.HEALTHY else 503
    response.status_code = status_code
    
    return {
        "status": overall_status,
        "checks": checks
    }


@router.get("/health/live")
async def liveness_check():
    """
    Liveness probe
    Simple check to see if the process is alive
    """
    return {
        "status": HealthStatus.HEALTHY,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/startup")
async def startup_check(response: Response, db: Session = Depends(get_db)):
    """
    Startup probe
    Checks if the service has finished initializing
    """
    checks = {
        "database": await check_database(db),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    db_status = checks["database"]["status"]
    overall_status = HealthStatus.HEALTHY if db_status == HealthStatus.HEALTHY else HealthStatus.UNHEALTHY
    
    status_code = 200 if overall_status == HealthStatus.HEALTHY else 503
    response.status_code = status_code
    
    return {
        "status": overall_status,
        "checks": checks
    }


@router.get("/health/detailed")
async def detailed_health_check(response: Response, db: Session = Depends(get_db)):
    """
    Detailed health check with all dependencies
    Includes database, Redis, and external services
    Enhanced with Heroku-style health check patterns
    """
    checks = {
        "database": await check_database(db),
        "redis": await check_redis(),
        "external_services": await check_external_services(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Add application-level metrics
    try:
        import psutil
        process = psutil.Process()
        checks["application_metrics"] = {
            "status": HealthStatus.HEALTHY,
            "cpu_percent": process.cpu_percent(interval=0.1),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "memory_percent": process.memory_percent(),
        }
    except ImportError:
        checks["application_metrics"] = {
            "status": HealthStatus.HEALTHY,
            "message": "psutil not available for detailed metrics"
        }
    except Exception as e:
        checks["application_metrics"] = {
            "status": HealthStatus.DEGRADED,
            "message": f"Error collecting metrics: {str(e)}"
        }
    
    # Determine overall status
    db_status = checks["database"]["status"]
    redis_status = checks["redis"]["status"]
    
    # Critical: database must be healthy
    if db_status != HealthStatus.HEALTHY:
        overall_status = HealthStatus.UNHEALTHY
    # Degraded: Redis or external services down
    elif redis_status == HealthStatus.UNHEALTHY:
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY
    
    status_code = 200 if overall_status == HealthStatus.HEALTHY else (503 if overall_status == HealthStatus.UNHEALTHY else 200)
    response.status_code = status_code
    
    return {
        "status": overall_status,
        "checks": checks,
        "service": settings.APP_NAME,
        "version": settings.API_VERSION,
        "environment": settings.APP_ENV
    }

