"""
Cost monitoring alerts
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

log = logging.getLogger(__name__)

# Alert thresholds (can be overridden via environment)
MONTHLY_COST_THRESHOLD = float(os.getenv('GROQ_MONTHLY_COST_THRESHOLD', '50.0'))  # $50/month
DAILY_USAGE_SPIKE_THRESHOLD = 2.0  # 2x daily average (requests)


class GroqUsageAlert:
    """Groq usage alert data structure"""
    
    def __init__(
        self,
        level: str,
        message: str,
        current_value: float,
        threshold: float,
        details: Optional[Dict] = None
    ):
        self.level = level  # 'warning' or 'critical'
        self.message = message
        self.current_value = current_value
        self.threshold = threshold
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert alert to dictionary"""
        return {
            "level": self.level,
            "message": self.message,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "details": self.details,
            "timestamp": self.timestamp
        }


def check_groq_usage_alerts(
    db: Session,
    GroqUsageModel,
    monthly_cost_threshold: Optional[float] = None
) -> List[GroqUsageAlert]:
    """
    Check Groq usage and return alerts if thresholds are exceeded.
    
    Args:
        db: Database session
        GroqUsageModel: SQLAlchemy GroqUsage model class
        monthly_cost_threshold: Optional monthly cost threshold (uses default if not provided)
        
    Returns:
        List of GroqUsageAlert objects
    """
    alerts = []
    monthly_threshold = monthly_cost_threshold or MONTHLY_COST_THRESHOLD
    
    try:
        # Get monthly usage
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end_of_month = datetime(today.year + 1, 1, 1)
        else:
            end_of_month = datetime(today.year, today.month + 1, 1)
        
        monthly_usage = db.query(GroqUsageModel).filter(
            GroqUsageModel.created_at >= start_of_month,
            GroqUsageModel.created_at < end_of_month
        ).all()
        
        monthly_cost = sum(float(u.cost_usd) for u in monthly_usage)
        
        if monthly_cost > monthly_threshold:
            alerts.append(GroqUsageAlert(
                level="critical" if monthly_cost > monthly_threshold * 1.5 else "warning",
                message=f"Monthly Groq cost (${monthly_cost:.2f}) exceeds threshold (${monthly_threshold:.2f})",
                current_value=monthly_cost,
                threshold=monthly_threshold,
                details={"year": today.year, "month": today.month, "request_count": len(monthly_usage)}
            ))
        
    except Exception as e:
        log.error(f"Error checking Groq usage alerts: {e}")
    
    return alerts

