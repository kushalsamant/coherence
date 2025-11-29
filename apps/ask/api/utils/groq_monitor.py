"""
Groq Usage Monitoring and Alerting
Tracks usage and sends alerts when thresholds are exceeded
"""

import logging
import os
import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

log = logging.getLogger(__name__)

# Alert thresholds (can be overridden via environment)
MONTHLY_COST_THRESHOLD = float(__import__('os').getenv('GROQ_MONTHLY_COST_THRESHOLD', '50.0'))  # $50/month
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


def get_daily_usage(db: Session, date: Optional[datetime] = None) -> Dict:
    """
    Get Groq usage for a specific day
    
    Args:
        db: Database session
        date: Date to check (defaults to today)
        
    Returns:
        Dictionary with usage statistics
    """
    try:
        from ..models_db import GroqUsage
        
        if date is None:
            date = datetime.utcnow()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        usage_records = db.query(GroqUsage).filter(
            GroqUsage.created_at >= start_of_day,
            GroqUsage.created_at < end_of_day
        ).all()
        
        total_input_tokens = sum(u.input_tokens for u in usage_records)
        total_output_tokens = sum(u.output_tokens for u in usage_records)
        total_cost = sum(float(u.cost_usd) for u in usage_records)
        
        return {
            "date": start_of_day.isoformat(),
            "request_count": len(usage_records),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_cost_usd": round(total_cost, 6)
        }
    except Exception as e:
        log.error(f"Failed to get daily usage: {e}")
        return {
            "date": (date or datetime.utcnow()).isoformat(),
            "request_count": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0
        }


def get_monthly_usage(db: Session, year: Optional[int] = None, month: Optional[int] = None) -> Dict:
    """
    Get Groq usage for a specific month
    
    Args:
        db: Database session
        year: Year to check (defaults to current year)
        month: Month to check (defaults to current month)
        
    Returns:
        Dictionary with usage statistics
    """
    try:
        from ..models_db import GroqUsage
        
        now = datetime.utcnow()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        
        start_of_month = datetime(year, month, 1)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1)
        else:
            end_of_month = datetime(year, month + 1, 1)
        
        usage_records = db.query(GroqUsage).filter(
            GroqUsage.created_at >= start_of_month,
            GroqUsage.created_at < end_of_month
        ).all()
        
        total_input_tokens = sum(u.input_tokens for u in usage_records)
        total_output_tokens = sum(u.output_tokens for u in usage_records)
        total_cost = sum(float(u.cost_usd) for u in usage_records)
        
        return {
            "year": year,
            "month": month,
            "request_count": len(usage_records),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_cost_usd": round(total_cost, 6)
        }
    except Exception as e:
        log.error(f"Failed to get monthly usage: {e}")
        return {
            "year": year or datetime.utcnow().year,
            "month": month or datetime.utcnow().month,
            "request_count": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0
        }


def check_groq_usage_alerts(db: Session) -> List[GroqUsageAlert]:
    """
    Check Groq usage and return alerts if thresholds are exceeded
    
    Args:
        db: Database session
        
    Returns:
        List of GroqUsageAlert objects
    """
    alerts = []
    
    try:
        # Check monthly cost
        monthly_usage = get_monthly_usage(db)
        monthly_cost = monthly_usage["total_cost_usd"]
        
        if monthly_cost > MONTHLY_COST_THRESHOLD:
            alerts.append(GroqUsageAlert(
                level="critical" if monthly_cost > MONTHLY_COST_THRESHOLD * 1.5 else "warning",
                message=f"Monthly Groq cost (${monthly_cost:.2f}) exceeds threshold (${MONTHLY_COST_THRESHOLD:.2f})",
                current_value=monthly_cost,
                threshold=MONTHLY_COST_THRESHOLD,
                details=monthly_usage
            ))
        
        # Check for usage spikes (compare today vs average of last 7 days)
        today_usage = get_daily_usage(db)
        today_requests = today_usage["request_count"]
        
        if today_requests > 0:
            # Get average requests per day for last 7 days
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            from ..models_db import GroqUsage
            
            total_requests = db.query(func.count(GroqUsage.id)).filter(
                GroqUsage.created_at >= seven_days_ago
            ).scalar() or 0
            
            avg_daily_requests = total_requests / 7.0
            
            if avg_daily_requests > 0 and today_requests > avg_daily_requests * DAILY_USAGE_SPIKE_THRESHOLD:
                alerts.append(GroqUsageAlert(
                    level="warning",
                    message=f"Daily usage spike detected: {today_requests} requests today vs {avg_daily_requests:.1f} average",
                    current_value=today_requests,
                    threshold=avg_daily_requests * DAILY_USAGE_SPIKE_THRESHOLD,
                    details={
                        "today_requests": today_requests,
                        "average_daily_requests": avg_daily_requests,
                        "spike_multiplier": today_requests / avg_daily_requests if avg_daily_requests > 0 else 0
                    }
                ))
        
    except Exception as e:
        log.error(f"Error checking Groq usage alerts: {e}")
    
    return alerts


def send_groq_alert(alert: GroqUsageAlert) -> bool:
    """
    Send Groq usage alert (logs for now, can be extended to email/Slack)
    
    Args:
        alert: GroqUsageAlert object
        
    Returns:
        True if alert was sent successfully
    """
    try:
        log.warning(f"Groq Usage Alert [{alert.level.upper()}]: {alert.message}")
        log.warning(f"Current: {alert.current_value}, Threshold: {alert.threshold}")
        
        # Send notifications if configured
        notification_sent = False
        
        # Email notification (optional)
        email_enabled = os.getenv("ASK_ALERT_EMAIL_ENABLED", "").lower() == "true"
        if email_enabled:
            email_recipients = os.getenv("ASK_ALERT_EMAIL_RECIPIENTS", "")
            if email_recipients:
                try:
                    _send_email_notification(alert, email_recipients)
                    notification_sent = True
                except Exception as e:
                    log.error(f"Failed to send email notification: {e}")
        
        # Slack notification (optional)
        slack_enabled = os.getenv("ASK_ALERT_SLACK_ENABLED", "").lower() == "true"
        if slack_enabled:
            slack_webhook_url = os.getenv("ASK_ALERT_SLACK_WEBHOOK_URL", "")
            if slack_webhook_url:
                try:
                    _send_slack_notification(alert, slack_webhook_url)
                    notification_sent = True
                except Exception as e:
                    log.error(f"Failed to send Slack notification: {e}")
        
        if not notification_sent:
            log.info("No notification channels configured. Alerts are only logged.")
        
        return True
    except Exception as e:
        log.error(f"Failed to send Groq alert: {e}")
        return False


def _send_email_notification(alert: GroqUsageAlert, recipients: str) -> bool:
    """
    Send email notification for Groq usage alert.
    
    Args:
        alert: GroqUsageAlert object
        recipients: Comma-separated list of email addresses
        
    Returns:
        True if email was sent successfully
    """
    try:
        # For now, log the email that would be sent
        # In production, integrate with email service (SendGrid, SES, etc.)
        log.info(f"Email notification would be sent to: {recipients}")
        log.info(f"Subject: Groq Usage Alert - {alert.level.upper()}")
        log.info(f"Body: {alert.message}\nCurrent: ${alert.current_value:.2f}, Threshold: ${alert.threshold:.2f}")
        
        # TODO: Implement actual email sending using your preferred email service
        # Example with SendGrid:
        # import sendgrid
        # sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        # message = sendgrid.Mail(...)
        # sg.send(message)
        
        return True
    except Exception as e:
        log.error(f"Failed to send email notification: {e}")
        return False


def _send_slack_notification(alert: GroqUsageAlert, webhook_url: str) -> bool:
    """
    Send Slack notification for Groq usage alert.
    
    Args:
        alert: GroqUsageAlert object
        webhook_url: Slack webhook URL
        
    Returns:
        True if notification was sent successfully
    """
    try:
        # Format Slack message
        color = "warning" if alert.level == "warning" else "danger"
        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"Groq Usage Alert - {alert.level.upper()}",
                    "text": alert.message,
                    "fields": [
                        {
                            "title": "Current Value",
                            "value": f"${alert.current_value:.2f}",
                            "short": True
                        },
                        {
                            "title": "Threshold",
                            "value": f"${alert.threshold:.2f}",
                            "short": True
                        }
                    ],
                    "footer": "ASK Groq Monitor",
                    "ts": int(datetime.utcnow().timestamp())
                }
            ]
        }
        
        # Send to Slack webhook
        timeout = httpx.Timeout(10.0, connect=5.0)
        with httpx.Client(timeout=timeout) as client:
            response = client.post(webhook_url, json=payload)
            response.raise_for_status()
            log.info(f"Slack notification sent successfully")
            return True
            
    except Exception as e:
        log.error(f"Failed to send Slack notification: {e}")
        return False

