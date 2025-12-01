"""
Cost and Usage Monitoring API Routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from api.database import get_db
try:
    from api.auth import get_current_user
    AUTH_AVAILABLE = True
except ImportError:
    # Fallback if auth not fully configured
    AUTH_AVAILABLE = False
    from api.models_db import User
    def get_current_user():
        # Simple dependency that returns None if auth not configured
        # In production, this should require proper authentication
        def _get_user(db: Session = Depends(get_db)):
            # Try to get first admin user or return None
            user = db.query(User).first()
            return user
        return Depends(_get_user)
from api.services.groq_service import get_groq_usage_stats
from api.utils.groq_monitor import (
    get_daily_usage,
    get_monthly_usage,
    check_groq_usage_alerts,
    GroqUsageAlert
)
try:
    from ..services.cost_service import (
        get_total_costs,
        get_payment_fees,
        get_cost_summary
    )
except ImportError:
    # Fallback if cost_service not available
    def get_total_costs(db, days=30):
        return {"error": "Cost service not available"}
    def get_payment_fees(db, days=30):
        return {"error": "Cost service not available"}
    def get_cost_summary(db):
        return {"error": "Cost service not available"}

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/costs")
async def get_costs(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:
    """
    Get current month costs breakdown
    
    Returns:
        Dictionary with cost breakdown
    """
    try:
        costs = get_total_costs(db)
        return costs
    except Exception as e:
        log.error(f"Failed to get costs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve costs")


@router.get("/usage")
async def get_usage(
    days: int = 30,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:
    """
    Get Groq usage statistics
    
    Args:
        days: Number of days to look back (default: 30)
        
    Returns:
        Dictionary with usage statistics
    """
    try:
        stats = get_groq_usage_stats(db, days=days)
        
        # Add daily and monthly breakdowns
        daily = get_daily_usage(db)
        monthly = get_monthly_usage(db)
        
        return {
            **stats,
            "daily": daily,
            "monthly": monthly
        }
    except Exception as e:
        log.error(f"Failed to get usage stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve usage statistics")


@router.get("/alerts")
async def get_alerts(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:
    """
    Get active cost and usage alerts
    
    Returns:
        Dictionary with list of active alerts
    """
    try:
        alerts = check_groq_usage_alerts(db)
        
        # Convert alerts to dictionaries
        alerts_list = [alert.to_dict() for alert in alerts]
        
        return {
            "alerts": alerts_list,
            "count": len(alerts_list),
            "critical_count": sum(1 for a in alerts if a.level == "critical"),
            "warning_count": sum(1 for a in alerts if a.level == "warning")
        }
    except Exception as e:
        log.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts")


@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:
    """
    Get comprehensive cost and usage summary
    
    Returns:
        Dictionary with complete summary
    """
    try:
        summary = get_cost_summary(db)
        return summary
    except Exception as e:
        log.error(f"Failed to get summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve summary")

