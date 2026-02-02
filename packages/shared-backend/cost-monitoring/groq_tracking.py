"""
Groq API usage tracking utilities
"""

import os
import logging
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

# Groq pricing (Llama 3.1 70B Versatile)
GROQ_INPUT_COST_PER_MILLION = 0.59  # $0.59 per 1M input tokens
GROQ_OUTPUT_COST_PER_MILLION = 0.79  # $0.79 per 1M output tokens

# Groq pricing for Llama 3.1 8B Instant
GROQ_8B_INPUT_COST_PER_MILLION = 0.05  # $0.05 per 1M input tokens
GROQ_8B_OUTPUT_COST_PER_MILLION = 0.08  # $0.08 per 1M output tokens


def calculate_groq_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "llama-3.1-70b-versatile"
) -> float:
    """
    Calculate cost in USD for Groq API usage.
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Groq model name
        
    Returns:
        Cost in USD
    """
    # Use 8B pricing for instant models, 70B for versatile
    if "8b" in model.lower() or "instant" in model.lower():
        input_cost = (input_tokens / 1_000_000) * GROQ_8B_INPUT_COST_PER_MILLION
        output_cost = (output_tokens / 1_000_000) * GROQ_8B_OUTPUT_COST_PER_MILLION
    else:
        input_cost = (input_tokens / 1_000_000) * GROQ_INPUT_COST_PER_MILLION
        output_cost = (output_tokens / 1_000_000) * GROQ_OUTPUT_COST_PER_MILLION
    
    return input_cost + output_cost


def track_groq_usage(
    db: Session,
    GroqUsageModel,
    input_tokens: int,
    output_tokens: int,
    request_type: str = "generation",
    model: str = "llama-3.1-70b-versatile"
) -> None:
    """
    Track Groq API usage in database.
    
    Args:
        db: Database session
        GroqUsageModel: SQLAlchemy GroqUsage model class
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used
        request_type: Type of request (e.g., "question_generation", "answer_generation")
        model: Groq model name
    """
    try:
        total_tokens = input_tokens + output_tokens
        cost_usd = calculate_groq_cost(input_tokens, output_tokens, model)
        
        usage = GroqUsageModel(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=str(cost_usd),
            model=model,
            request_type=request_type,
            created_at=datetime.utcnow()
        )
        
        db.add(usage)
        db.commit()
        
        log.debug(f"Tracked Groq usage: {total_tokens} tokens, ${cost_usd:.6f}")
    except Exception as e:
        log.error(f"Failed to track Groq usage: {e}")
        db.rollback()


def get_groq_usage_stats(
    db: Session,
    GroqUsageModel,
    days: int = 30
) -> dict:
    """
    Get Groq usage statistics for the last N days.
    
    Args:
        db: Database session
        GroqUsageModel: SQLAlchemy GroqUsage model class
        days: Number of days to look back
        
    Returns:
        Dictionary with usage statistics
    """
    try:
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        usage_records = db.query(GroqUsageModel).filter(
            GroqUsageModel.created_at >= cutoff_date
        ).all()
        
        total_input_tokens = sum(u.input_tokens for u in usage_records)
        total_output_tokens = sum(u.output_tokens for u in usage_records)
        total_tokens = sum(u.total_tokens for u in usage_records)
        total_cost = sum(float(u.cost_usd) for u in usage_records)
        
        return {
            "period_days": days,
            "request_count": len(usage_records),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "average_cost_per_request": round(total_cost / len(usage_records), 6) if usage_records else 0.0
        }
    except Exception as e:
        log.error(f"Failed to get Groq usage stats: {e}")
        return {
            "period_days": days,
            "request_count": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "average_cost_per_request": 0.0
        }

