"""
Cost Tracking Service for Reframe
Tracks Groq API costs, Razorpay fees, and calculates total costs
Uses Redis for storage (Upstash Redis REST API)
"""

import logging
import asyncio
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .redis_service import get_redis_service

log = logging.getLogger(__name__)

# Razorpay fee percentage (2%)
RAZORPAY_FEE_PERCENTAGE = 0.02

# Groq pricing for Reframe (Llama 3.1 8B Instant)
GROQ_8B_INPUT_COST_PER_MILLION = 0.05  # $0.05 per 1M input tokens
GROQ_8B_OUTPUT_COST_PER_MILLION = 0.08  # $0.08 per 1M output tokens


def calculate_groq_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost in USD for Groq API usage (8B model)
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        
    Returns:
        Cost in USD
    """
    input_cost = (input_tokens / 1_000_000) * GROQ_8B_INPUT_COST_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * GROQ_8B_OUTPUT_COST_PER_MILLION
    return input_cost + output_cost


async def _get_groq_costs_async(days: int = 30) -> Dict:
    """
    Get Groq API costs for the last N days from Redis
    
    Reads from Redis keys created by groq_monitor.py:
    - Daily keys: groq:usage:daily:{YYYY-MM-DD}:cost, groq:usage:daily:{YYYY-MM-DD}:requests
    - Monthly keys: groq:usage:monthly:{YYYY-MM}:cost, groq:usage:monthly:{YYYY-MM}:requests
    
    Data retention: 30 days for daily keys, 90 days for monthly keys
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary with Groq cost breakdown
    """
    try:
        redis = get_redis_service()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        total_cost = 0.0
        total_requests = 0
        daily_breakdown = {}
        
        # Iterate through each day in the range
        current_date = cutoff_date.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            daily_key = f"groq:usage:daily:{date_key}"
            
            # Get daily metrics from Redis
            cost_str = await redis.get(f"{daily_key}:cost")
            requests_str = await redis.get(f"{daily_key}:requests")
            input_tokens_str = await redis.get(f"{daily_key}:input_tokens")
            output_tokens_str = await redis.get(f"{daily_key}:output_tokens")
            
            daily_cost = float(cost_str) if cost_str else 0.0
            daily_requests = int(requests_str) if requests_str else 0
            
            if daily_cost > 0 or daily_requests > 0:
                total_cost += daily_cost
                total_requests += daily_requests
                daily_breakdown[date_key] = {
                    "cost_usd": round(daily_cost, 6),
                    "requests": daily_requests,
                    "input_tokens": int(input_tokens_str) if input_tokens_str else 0,
                    "output_tokens": int(output_tokens_str) if output_tokens_str else 0
                }
            
            current_date += timedelta(days=1)
        
        return {
            "total_cost_usd": round(total_cost, 6),
            "request_count": total_requests,
            "daily_breakdown": daily_breakdown,
            "period_days": days
        }
    except Exception as e:
        log.error(f"Failed to get Groq costs from Redis: {e}")
        return {
            "total_cost_usd": 0.0,
            "request_count": 0,
            "daily_breakdown": {},
            "period_days": days
        }


def get_groq_costs(db: Session, days: int = 30) -> Dict:
    """
    Get Groq API costs for the last N days from Redis
    
    Synchronous wrapper for async Redis operations.
    Reads from Redis keys created by groq_monitor.py.
    
    Redis key structure:
    - Daily: groq:usage:daily:{YYYY-MM-DD}:cost, groq:usage:daily:{YYYY-MM-DD}:requests
    - Data retention: 30 days for daily keys
    
    Args:
        db: Database session (kept for API compatibility, not used - Reframe uses Redis)
        days: Number of days to look back
        
    Returns:
        Dictionary with Groq cost breakdown:
        - total_cost_usd: Total cost in USD
        - request_count: Total number of requests
        - daily_breakdown: Dictionary mapping dates to daily costs and metrics
        - period_days: Number of days analyzed
    """
    try:
        # Run async function in sync context
        # asyncio.run() creates a new event loop, which works for sync callers
        return asyncio.run(_get_groq_costs_async(days))
    except Exception as e:
        log.error(f"Failed to get Groq costs: {e}")
        return {
            "total_cost_usd": 0.0,
            "request_count": 0,
            "daily_breakdown": {},
            "period_days": days
        }


async def _get_payment_fees_async(days: int = 30) -> Dict:
    """
    Get Razorpay processing fees for the last N days from Redis
    
    Reads from Redis keys created by Next.js webhook handler:
    - Daily keys: payment:fees:daily:{YYYY-MM-DD}, payment:revenue:daily:{YYYY-MM-DD}, payment:count:daily:{YYYY-MM-DD}
    - Monthly keys: payment:fees:monthly:{YYYY-MM}, payment:revenue:monthly:{YYYY-MM}, payment:count:monthly:{YYYY-MM}
    
    Data retention: 30 days for daily keys, 90 days for monthly keys
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary with payment fee breakdown
    """
    try:
        redis = get_redis_service()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        total_fees_paise = 0
        total_revenue_paise = 0
        total_payment_count = 0
        daily_fees = {}
        daily_revenue = {}
        
        # Iterate through each day in the range
        current_date = cutoff_date.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            
            # Get daily metrics from Redis
            fees_str = await redis.get(f"payment:fees:daily:{date_key}")
            revenue_str = await redis.get(f"payment:revenue:daily:{date_key}")
            count_str = await redis.get(f"payment:count:daily:{date_key}")
            
            daily_fees_paise = int(fees_str) if fees_str else 0
            daily_revenue_paise = int(revenue_str) if revenue_str else 0
            daily_count = int(count_str) if count_str else 0
            
            if daily_fees_paise > 0 or daily_revenue_paise > 0 or daily_count > 0:
                total_fees_paise += daily_fees_paise
                total_revenue_paise += daily_revenue_paise
                total_payment_count += daily_count
                daily_fees[date_key] = daily_fees_paise
                daily_revenue[date_key] = daily_revenue_paise
            
            current_date += timedelta(days=1)
        
        # Convert to USD (₹1 ≈ $0.012)
        INR_TO_USD = 0.012
        total_fees_usd = total_fees_paise / 100.0 * INR_TO_USD
        total_revenue_usd = total_revenue_paise / 100.0 * INR_TO_USD
        
        return {
            "total_fees_paise": total_fees_paise,
            "total_fees_usd": round(total_fees_usd, 2),
            "total_revenue_paise": total_revenue_paise,
            "total_revenue_usd": round(total_revenue_usd, 2),
            "fee_percentage": RAZORPAY_FEE_PERCENTAGE * 100,
            "payment_count": total_payment_count,
            "daily_fees": daily_fees,
            "daily_revenue": daily_revenue,
            "period_days": days
        }
    except Exception as e:
        log.error(f"Failed to get payment fees from Redis: {e}")
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


def get_payment_fees(db: Session, days: int = 30) -> Dict:
    """
    Get Razorpay processing fees for the last N days from Redis
    
    Synchronous wrapper for async Redis operations.
    Reads from Redis keys created by Next.js webhook handler.
    
    Redis key structure:
    - Daily: payment:fees:daily:{YYYY-MM-DD}, payment:revenue:daily:{YYYY-MM-DD}, payment:count:daily:{YYYY-MM-DD}
    - Data retention: 30 days for daily keys
    
    Args:
        db: Database session (kept for API compatibility, not used - Reframe uses Redis)
        days: Number of days to look back
        
    Returns:
        Dictionary with payment fee breakdown:
        - total_fees_paise: Total fees in paise
        - total_fees_usd: Total fees in USD
        - total_revenue_paise: Total revenue in paise
        - total_revenue_usd: Total revenue in USD
        - fee_percentage: Fee percentage (2.0)
        - payment_count: Total number of payments
        - daily_fees: Dictionary mapping dates to daily fees
        - daily_revenue: Dictionary mapping dates to daily revenue
        - period_days: Number of days analyzed
    """
    try:
        # Run async function in sync context
        # asyncio.run() creates a new event loop, which works for sync callers
        return asyncio.run(_get_payment_fees_async(days))
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

