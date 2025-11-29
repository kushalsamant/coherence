"""
Cost Tracking Service for Sketch2BIM
Tracks BunnyCDN storage/transfer costs, Razorpay fees, and calculates total costs
"""

import logging
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

log = logging.getLogger(__name__)

# Razorpay fee percentage (2%)
RAZORPAY_FEE_PERCENTAGE = 0.02

# BunnyCDN costs (from costing.py)
BUNNYCDN_COST_PER_GB = 0.01  # $0.01 per GB stored
BUNNYCDN_COST_PER_GB_TRANSFER = 0.005  # $0.005 per GB transferred


def get_bunnycdn_costs(db: Session, days: int = 30) -> Dict:
    """
    Get BunnyCDN storage and transfer costs for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with BunnyCDN cost breakdown
    """
    try:
        from ..models import Job
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all jobs in the period
        jobs = db.query(Job).filter(
            Job.created_at >= cutoff_date
        ).all()
        
        total_storage_cost = 0.0
        total_transfer_cost = 0.0
        
        # Calculate costs for each job
        for job in jobs:
            if job.output_file_size:
                # Storage cost (assuming 7 days average storage)
                size_gb = job.output_file_size / (1024 ** 3)
                daily_storage_cost = size_gb * BUNNYCDN_COST_PER_GB / 30
                total_storage_cost += daily_storage_cost * 7  # 7 days average
            
            if job.output_file_size:
                # Transfer cost (assuming file is downloaded once)
                size_gb = job.output_file_size / (1024 ** 3)
                total_transfer_cost += size_gb * BUNNYCDN_COST_PER_GB_TRANSFER
        
        return {
            "total_storage_cost_usd": round(total_storage_cost, 6),
            "total_transfer_cost_usd": round(total_transfer_cost, 6),
            "total_cost_usd": round(total_storage_cost + total_transfer_cost, 6),
            "job_count": len(jobs),
            "period_days": days
        }
    except Exception as e:
        log.error(f"Failed to get BunnyCDN costs: {e}")
        return {
            "total_storage_cost_usd": 0.0,
            "total_transfer_cost_usd": 0.0,
            "total_cost_usd": 0.0,
            "job_count": 0,
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
        from ..models import Payment
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all successful payments in the period
        payments = db.query(Payment).filter(
            Payment.status == "succeeded",
            Payment.created_at >= cutoff_date
        ).all()
        
        total_fees = sum(p.processing_fee or 0 for p in payments)
        total_revenue = sum(p.amount or 0 for p in payments)
        
        # Calculate fees if not already stored (for backward compatibility)
        calculated_fees = 0
        for payment in payments:
            if not payment.processing_fee and payment.amount:
                # Calculate 2% fee
                fee = int(payment.amount * RAZORPAY_FEE_PERCENTAGE)
                calculated_fees += fee
        
        total_fees_paise = total_fees + calculated_fees
        total_fees_usd = total_fees_paise / 100.0 * 0.012  # Approximate conversion (₹1 ≈ $0.012)
        total_revenue_usd = total_revenue / 100.0 * 0.012
        
        return {
            "total_fees_paise": total_fees_paise,
            "total_fees_usd": round(total_fees_usd, 2),
            "total_revenue_paise": total_revenue,
            "total_revenue_usd": round(total_revenue_usd, 2),
            "fee_percentage": RAZORPAY_FEE_PERCENTAGE * 100,
            "payment_count": len(payments),
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
            "period_days": days
        }


def get_total_costs(db: Session, days: int = 30) -> Dict:
    """
    Get total costs breakdown (BunnyCDN + Payment fees)
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with total cost breakdown
    """
    try:
        bunnycdn_costs = get_bunnycdn_costs(db, days=days)
        payment_fees = get_payment_fees(db, days=days)
        
        total_cost_usd = bunnycdn_costs["total_cost_usd"] + payment_fees["total_fees_usd"]
        
        return {
            "period_days": days,
            "bunnycdn_costs": bunnycdn_costs,
            "payment_fees": payment_fees,
            "total_cost_usd": round(total_cost_usd, 2),
            "breakdown": {
                "bunnycdn_percentage": round((bunnycdn_costs["total_cost_usd"] / total_cost_usd * 100) if total_cost_usd > 0 else 0, 2),
                "payment_fees_percentage": round((payment_fees["total_fees_usd"] / total_cost_usd * 100) if total_cost_usd > 0 else 0, 2)
            }
        }
    except Exception as e:
        log.error(f"Failed to get total costs: {e}")
        return {
            "period_days": days,
            "bunnycdn_costs": {"total_cost_usd": 0.0},
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
            for key in ["total_cost_usd", "bunnycdn_costs", "payment_fees"]:
                if key in monthly_costs:
                    if isinstance(monthly_costs[key], dict):
                        projected_monthly[key] = {
                            k: round(v * days_in_month.day / days_elapsed, 2) if isinstance(v, (int, float)) else v
                            for k, v in monthly_costs[key].items()
                        }
                    else:
                        projected_monthly[key] = round(monthly_costs[key] * days_in_month.day / days_elapsed, 2)
        
        return {
            "current_month": {
                "days_elapsed": days_elapsed,
                "days_total": days_in_month.day,
                "costs": monthly_costs,
                "projected": projected_monthly
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        log.error(f"Failed to get cost summary: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

