"""
Groq Usage Monitoring for Reframe
Tracks token usage and costs, stores in Redis
"""
import os
from datetime import datetime
from typing import Optional
from .redis_service import get_redis_service


# Groq pricing for llama-3.1-8b-instant (Reframe model)
GROQ_INPUT_COST_PER_MILLION = 0.05  # $0.05 per 1M input tokens
GROQ_OUTPUT_COST_PER_MILLION = 0.08  # $0.08 per 1M output tokens

# Alert thresholds (monthly only)
MONTHLY_COST_THRESHOLD = float(os.getenv("REFRAME_GROQ_MONTHLY_COST_THRESHOLD", os.getenv("GROQ_MONTHLY_COST_THRESHOLD", "50.0")))  # $50/month


def calculate_groq_cost(input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD for Groq API usage"""
    input_cost = (input_tokens / 1_000_000) * GROQ_INPUT_COST_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * GROQ_OUTPUT_COST_PER_MILLION
    return input_cost + output_cost


async def track_groq_usage(
    input_tokens: int,
    output_tokens: int,
    request_type: str = "reframe"
) -> None:
    """Track Groq API usage in Redis"""
    try:
        redis = get_redis_service()
        now = datetime.utcnow()
        date_key = now.strftime("%Y-%m-%d")  # YYYY-MM-DD
        month_key = f"{now.year}-{now.month:02d}"  # YYYY-MM
        
        total_tokens = input_tokens + output_tokens
        cost = calculate_groq_cost(input_tokens, output_tokens)
        
        # Track daily usage
        daily_key = f"groq:usage:daily:{date_key}"
        await redis.incrby(f"{daily_key}:requests", 1)
        await redis.incrby(f"{daily_key}:input_tokens", input_tokens)
        await redis.incrby(f"{daily_key}:output_tokens", output_tokens)
        await redis.incrbyfloat(f"{daily_key}:cost", cost)
        
        # Track monthly usage
        monthly_key = f"groq:usage:monthly:{month_key}"
        await redis.incrby(f"{monthly_key}:requests", 1)
        await redis.incrby(f"{monthly_key}:input_tokens", input_tokens)
        await redis.incrby(f"{monthly_key}:output_tokens", output_tokens)
        await redis.incrbyfloat(f"{monthly_key}:cost", cost)
        
        # Set expiration (30 days for daily, 90 days for monthly)
        await redis.expire(daily_key, 30 * 24 * 60 * 60)
        await redis.expire(monthly_key, 90 * 24 * 60 * 60)
        
        # Store individual request for detailed tracking
        import random
        import time
        request_key = f"groq:request:{int(time.time() * 1000)}:{random.randint(100000, 999999)}"
        await redis.hset(request_key, "input_tokens", str(input_tokens))
        await redis.hset(request_key, "output_tokens", str(output_tokens))
        await redis.hset(request_key, "total_tokens", str(total_tokens))
        await redis.hset(request_key, "cost", str(cost))
        await redis.hset(request_key, "request_type", request_type)
        await redis.hset(request_key, "timestamp", now.isoformat())
        await redis.expire(request_key, 30 * 24 * 60 * 60)  # 30 days
        
        # Check for alerts
        await _check_and_alert(redis, date_key, month_key)
    except Exception as error:
        print(f"Failed to track Groq usage: {error}")
        # Don't throw - tracking failure shouldn't break the request


async def _check_and_alert(redis, date_key: str, month_key: str) -> None:
    """Check usage and send alerts if thresholds exceeded"""
    try:
        daily_key = f"groq:usage:daily:{date_key}"
        monthly_key = f"groq:usage:monthly:{month_key}"
        
        monthly_cost_str = await redis.get(f"{monthly_key}:cost")
        monthly_cost = float(monthly_cost_str) if monthly_cost_str else 0.0
        
        # Check monthly threshold
        if monthly_cost > MONTHLY_COST_THRESHOLD:
            alert_key = f"groq:alert:monthly:{month_key}"
            already_alerted = await redis.get(alert_key)
            
            if not already_alerted:
                print(f"[GROQ ALERT] Monthly cost (${monthly_cost:.2f}) exceeds threshold (${MONTHLY_COST_THRESHOLD})")
                await redis.set(alert_key, "1")
                await redis.expire(alert_key, 30 * 24 * 60 * 60)  # Alert once per month
    except Exception as error:
        print(f"Failed to check alerts: {error}")

