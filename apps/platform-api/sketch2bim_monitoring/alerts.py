"""
Resource limit alerting system
Checks all resource limits and sends alerts when thresholds are exceeded
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from .redis_monitor import get_redis_usage
from .storage_monitor import get_storage_usage
from ..config import settings
from sqlalchemy.orm import Session

# Alert thresholds (can be overridden via environment)
ALERT_WARNING_THRESHOLD = int(getattr(settings, 'RESOURCE_ALERT_WARNING_THRESHOLD', 80))  # 80%
ALERT_CRITICAL_THRESHOLD = int(getattr(settings, 'RESOURCE_ALERT_CRITICAL_THRESHOLD', 95))  # 95%

# Alert email configuration
ALERT_EMAIL_ENABLED = getattr(settings, 'ALERT_EMAIL_ENABLED', True)
ALERT_EMAIL_RECIPIENTS = getattr(settings, 'ALERT_EMAIL_RECIPIENTS', 'admin@sketch2bim.com')


class ResourceAlert:
    """Resource alert data structure"""
    
    def __init__(
        self,
        resource: str,
        level: str,
        message: str,
        current: float,
        limit: float,
        percentage: float,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource = resource
        self.level = level  # 'warning' or 'critical'
        self.message = message
        self.current = current
        self.limit = limit
        self.percentage = percentage
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "resource": self.resource,
            "level": self.level,
            "message": self.message,
            "current": self.current,
            "limit": self.limit,
            "percentage": self.percentage,
            "details": self.details,
            "timestamp": self.timestamp
        }


def check_resource_limits(db_session: Session) -> List[ResourceAlert]:
    """
    Check all resource limits and return alerts
    
    Args:
        db_session: Database session
        
    Returns:
        List of ResourceAlert objects
    """
    from .database_monitor import get_database_size
    
    alerts = []
    
    # Check database size
    try:
        db_info = get_database_size(db_session)
        if db_info.get("status") in ["warning", "critical"]:
            alerts.append(ResourceAlert(
                resource="database",
                level=db_info["status"],
                message=f"Database size is {db_info['percentage_used']:.1f}% of limit ({db_info['size_mb']:.1f}MB / {db_info['limit_mb']}MB)",
                current=db_info["size_mb"],
                limit=db_info["limit_mb"],
                percentage=db_info["percentage_used"],
                details=db_info
            ))
    except Exception as e:
        logger.error(f"Error checking database limits: {e}")
    
    # Check Redis usage
    try:
        redis_info = get_redis_usage()
        if redis_info.get("status") in ["warning", "critical"]:
            alerts.append(ResourceAlert(
                resource="redis",
                level=redis_info["status"],
                message=f"Redis usage is {redis_info['percentage_used']:.1f}% of limit ({redis_info['commands_today']} / {redis_info['limit_per_day']} commands today)",
                current=redis_info["commands_today"],
                limit=redis_info["limit_per_day"],
                percentage=redis_info["percentage_used"],
                details=redis_info
            ))
    except Exception as e:
        logger.error(f"Error checking Redis limits: {e}")
    
    # Check storage usage (optional - no hard limit, but can alert on cost)
    try:
        storage_info = get_storage_usage()
        # Alert if storage cost exceeds $10/month (arbitrary threshold)
        if storage_info.get("cost_estimate_usd", 0) > 10:
            alerts.append(ResourceAlert(
                resource="storage",
                level="warning",
                message=f"Storage cost estimate is ${storage_info['cost_estimate_usd']:.2f}/month ({storage_info['size_gb']:.1f}GB)",
                current=storage_info["cost_estimate_usd"],
                limit=10.0,  # $10 threshold
                percentage=(storage_info["cost_estimate_usd"] / 10.0) * 100,
                details=storage_info
            ))
    except Exception as e:
        logger.error(f"Error checking storage limits: {e}")
    
    return alerts


def send_alert(alert: ResourceAlert) -> bool:
    """
    Send alert via configured channel
    
    Args:
        alert: ResourceAlert object
        
    Returns:
        True if sent successfully
    """
    # Log alert
    logger.warning(f"Resource alert [{alert.level.upper()}]: {alert.message}")
    
    # Send email if enabled
    if ALERT_EMAIL_ENABLED and ALERT_EMAIL_RECIPIENTS:
        try:
            recipients = [r.strip() for r in ALERT_EMAIL_RECIPIENTS.split(",")]
            
            subject = f"[{alert.level.upper()}] Resource Limit Alert: {alert.resource}"
            
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: {'#dc2626' if alert.level == 'critical' else '#f59e0b'};">
                    Resource Limit Alert
                </h2>
                
                <div style="background-color: {'#fee2e2' if alert.level == 'critical' else '#fef3c7'}; 
                            padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <p><strong>Resource:</strong> {alert.resource.title()}</p>
                    <p><strong>Level:</strong> {alert.level.upper()}</p>
                    <p><strong>Message:</strong> {alert.message}</p>
                    <p><strong>Usage:</strong> {alert.percentage:.1f}% ({alert.current} / {alert.limit})</p>
                </div>
                
                <h3>Details:</h3>
                <pre style="background-color: #f3f4f6; padding: 10px; border-radius: 4px; overflow-x: auto;">
{_format_details(alert.details)}
                </pre>
                
                <h3>Recommended Actions:</h3>
                <ul>
                    {_get_recommendations(alert)}
                </ul>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                <p style="color: #999; font-size: 12px;">
                    Sketch-to-BIM Monitoring System<br>
                    Timestamp: {alert.timestamp}
                </p>
            </body>
            </html>
            """
            
            # Email alerts disabled - users check dashboard for status
            # Log alert instead
            logger.warning(f"Resource alert: {subject}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")
            return False
    
    return True


def _format_details(details: Dict[str, Any]) -> str:
    """Format alert details for display"""
    import json
    return json.dumps(details, indent=2)


def _get_recommendations(alert: ResourceAlert) -> str:
    """Get recommendations based on alert type"""
    recommendations = {
        "database": [
            "Consider upgrading Supabase plan or migrating to self-hosted PostgreSQL",
            "Review and clean up old job data if no longer needed",
            "Archive completed jobs to reduce database size"
        ],
        "redis": [
            "Consider upgrading Upstash plan or migrating to self-hosted Redis",
            "Review rate limiting configuration",
            "Optimize cache usage to reduce Redis commands"
        ],
        "storage": [
            "Review BunnyCDN storage usage",
            "Consider implementing automatic cleanup of old files",
            "Review storage retention policies"
        ]
    }
    
    resource_recs = recommendations.get(alert.resource, ["Monitor resource usage closely"])
    
    return "\n".join([f"<li>{rec}</li>" for rec in resource_recs])


def check_and_send_alerts(db_session) -> List[ResourceAlert]:
    """
    Check resource limits and send alerts
    
    Args:
        db_session: Database session
        
    Returns:
        List of alerts that were sent
    """
    alerts = check_resource_limits(db_session)
    
    for alert in alerts:
        send_alert(alert)
    
    return alerts

