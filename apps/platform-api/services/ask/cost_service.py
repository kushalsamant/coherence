"""
Cost Tracking Service
Tracks Groq API costs, Razorpay fees, and calculates total costs
"""

import logging
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

log = logging.getLogger(__name__)

# Razorpay fee percentage (2%)
RAZORPAY_FEE_PERCENTAGE = 0.02


def get_groq_costs(db: Session, days: int = 30) -> Dict:
    """
    Get Groq API costs for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with Groq cost breakdown
    """
    try:
        from models.ask import GroqUsage
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        usage_records = db.query(GroqUsage).filter(
            GroqUsage.created_at >= cutoff_date
        ).all()
        
        total_cost = sum(float(u.cost_usd) for u in usage_records)
        
        # Get daily breakdown
        daily_costs = {}
        for record in usage_records:
            day_key = record.created_at.date().isoformat()
            if day_key not in daily_costs:
                daily_costs[day_key] = 0.0
            daily_costs[day_key] += float(record.cost_usd)
        
        return {
            "total_cost_usd": round(total_cost, 6),
            "request_count": len(usage_records),
            "daily_breakdown": daily_costs,
            "period_days": days
        }
    except Exception as e:
        log.error(f"Failed to get Groq costs: {e}")
        return {
            "total_cost_usd": 0.0,
            "request_count": 0,
            "daily_breakdown": {},
            "period_days": days
        }


def get_payment_fees(db: Session, days: int = 30) -> Dict:
    """
    Get Razorpay processing fees for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with payment fee breakdown
    """
    try:
        from models.ask import Payment
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all successful payments in the period
        payments = db.query(Payment).filter(
            Payment.status == "succeeded",
            Payment.created_at >= cutoff_date
        ).all()
        
        total_fees = sum(p.processing_fee or 0 for p in payments)
        total_revenue = sum(p.amount or 0 for p in payments)
        
        # Calculate fees if not already stored
        calculated_fees = 0
        for payment in payments:
            if not payment.processing_fee and payment.amount:
                # Calculate 2% fee
                fee = int(payment.amount * RAZORPAY_FEE_PERCENTAGE)
                calculated_fees += fee
        
        total_fees_paise = total_fees + calculated_fees
        total_fees_usd = total_fees_paise / 100.0 * 0.012  # Approximate conversion (₹1 ≈ $0.012)
        total_revenue_usd = total_revenue / 100.0 * 0.012
        
        # Get daily breakdown
        daily_fees = {}
        daily_revenue = {}
        for payment in payments:
            day_key = payment.created_at.date().isoformat()
            fee = payment.processing_fee or int((payment.amount or 0) * RAZORPAY_FEE_PERCENTAGE)
            
            if day_key not in daily_fees:
                daily_fees[day_key] = 0
                daily_revenue[day_key] = 0
            
            daily_fees[day_key] += fee
            daily_revenue[day_key] += payment.amount or 0
        
        return {
            "total_fees_paise": total_fees_paise,
            "total_fees_usd": round(total_fees_usd, 2),
            "total_revenue_paise": total_revenue,
            "total_revenue_usd": round(total_revenue_usd, 2),
            "fee_percentage": RAZORPAY_FEE_PERCENTAGE * 100,
            "payment_count": len(payments),
            "daily_fees": daily_fees,
            "daily_revenue": daily_revenue,
            "period_days": days
        }
    except Exception as e:
        log.error(f"Failed to get payment fees: {e}")
        return {
            "total_fees_paise": 0,
            "total_fees_usd": 0.0,
            "total_revenue_paise": 0,
            "total_revenue_usd": 0.0,
            "fee_percentage": RAZORPAY_FEE_PERCENTAGE * 100,
            "payment_count": 0,
            "daily_fees": {},
            "daily_revenue": {},
            "period_days": days
        }


def get_total_costs(db: Session, days: int = 30) -> Dict:
    """
    Get total costs breakdown (Groq + Payment fees)
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with total cost breakdown
    """
    try:
        groq_costs = get_groq_costs(db, days=days)
        payment_fees = get_payment_fees(db, days=days)
        
        total_cost_usd = groq_costs["total_cost_usd"] + payment_fees["total_fees_usd"]
        
        return {
            "period_days": days,
            "groq_costs": groq_costs,
            "payment_fees": payment_fees,
            "total_cost_usd": round(total_cost_usd, 2),
            "breakdown": {
                "groq_percentage": round((groq_costs["total_cost_usd"] / total_cost_usd * 100) if total_cost_usd > 0 else 0, 2),
                "payment_fees_percentage": round((payment_fees["total_fees_usd"] / total_cost_usd * 100) if total_cost_usd > 0 else 0, 2)
            }
        }
    except Exception as e:
        log.error(f"Failed to get total costs: {e}")
        return {
            "period_days": days,
            "groq_costs": {"total_cost_usd": 0.0},
            "payment_fees": {"total_fees_usd": 0.0},
            "total_cost_usd": 0.0,
            "breakdown": {}
        }


def get_cost_summary(db: Session) -> Dict:
    """
    Get comprehensive cost and usage summary
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with complete summary
    """
    try:
        # Get current month costs
        now = datetime.utcnow()
        days_in_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        days_elapsed = now.day
        
        monthly_costs = get_total_costs(db, days=days_elapsed)
        
        # Project monthly total
        projected_monthly = {}
        if days_elapsed > 0:
            for key in ["total_cost_usd", "groq_costs", "payment_fees"]:
                if key in monthly_costs:
                    if isinstance(monthly_costs[key], dict):
                        projected_monthly[key] = {
                            k: round(v * days_in_month.day / days_elapsed, 2) if isinstance(v, (int, float)) else v
                            for k, v in monthly_costs[key].items()
                        }
                    else:
                        projected_monthly[key] = round(monthly_costs[key] * days_in_month.day / days_elapsed, 2)
        
        # Get usage stats
        from ..services.groq_service import get_groq_usage_stats
        usage_stats = get_groq_usage_stats(db, days=30)
        
        # Get alerts
        from ..utils.groq_monitor import check_groq_usage_alerts
        alerts = check_groq_usage_alerts(db)
        
        return {
            "current_month": {
                "days_elapsed": days_elapsed,
                "days_total": days_in_month.day,
                "costs": monthly_costs,
                "projected": projected_monthly
            },
            "usage": usage_stats,
            "alerts": {
                "count": len(alerts),
                "critical": sum(1 for a in alerts if a.level == "critical"),
                "warnings": sum(1 for a in alerts if a.level == "warning"),
                "active_alerts": [a.to_dict() for a in alerts[:5]]  # Top 5 alerts
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        log.error(f"Failed to get cost summary: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

