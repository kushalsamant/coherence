"""
Health check endpoints for Kubernetes-style probes
"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.platform import get_db as get_platform_db
import os

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check endpoint
    Returns service information and status
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "Platform API",
            "version": "1.0.0",
            "app": "platform"
        },
    )


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """
    Kubernetes liveness probe
    Indicates if the service is running and should receive traffic
    Returns 200 if service is alive, 503 if not
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "alive",
            "service": "Platform API"
        }
    )


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_probe(
    platform_db: Session = Depends(get_platform_db)
):
    """
    Kubernetes readiness probe
    Indicates if the service is ready to handle requests
    Checks:
    - Database connectivity (Platform)
    - Critical environment variables
    
    Returns 200 if ready, 503 if not ready
    """
    checks = {}
    all_healthy = True
    
    # Check Platform database
    try:
        platform_db.execute(text("SELECT 1"))
        checks["platform_database"] = "ok"
    except Exception as e:
        checks["platform_database"] = f"error: {str(e)}"
        all_healthy = False
    
    # Check critical environment variables
    required_env_vars = [
        "PLATFORM_DATABASE_URL",
    ]
    
    for env_var in required_env_vars:
        if not os.getenv(env_var):
            checks[f"env_{env_var.lower()}"] = "missing"
            all_healthy = False
        else:
            checks[f"env_{env_var.lower()}"] = "ok"
    
    if not all_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "service": "Platform API",
                "checks": checks
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "service": "Platform API",
            "checks": checks
        }
    )
