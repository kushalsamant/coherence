"""
Groq API Service for text generation
Replaces Together AI with Groq API
"""

import os
import logging
from typing import Optional, Tuple
from groq import Groq
from datetime import datetime
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

# Groq API configuration
GROQ_API_KEY = os.getenv('ASK_GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
GROQ_MODEL = os.getenv('ASK_GROQ_MODEL', os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile'))

# Groq pricing (Llama 3.1 70B Versatile)
GROQ_INPUT_COST_PER_MILLION = 0.59  # $0.59 per 1M input tokens
GROQ_OUTPUT_COST_PER_MILLION = 0.79  # $0.79 per 1M output tokens

# Initialize Groq client
client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        log.error(f"Failed to initialize Groq client: {e}")
        client = None
else:
    log.warning("GROQ_API_KEY not set in environment variables")


def calculate_groq_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost in USD for Groq API usage
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        
    Returns:
        Cost in USD
    """
    input_cost = (input_tokens / 1_000_000) * GROQ_INPUT_COST_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * GROQ_OUTPUT_COST_PER_MILLION
    return input_cost + output_cost


def track_groq_usage(
    db: Session,
    input_tokens: int,
    output_tokens: int,
    request_type: str = "generation"
) -> None:
    """
    Track Groq API usage in database
    
    Args:
        db: Database session
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used
        request_type: Type of request (e.g., "question_generation", "answer_generation")
    """
    try:
        from ..models_db import GroqUsage
        
        total_tokens = input_tokens + output_tokens
        cost_usd = calculate_groq_cost(input_tokens, output_tokens)
        
        usage = GroqUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=str(cost_usd),
            model=GROQ_MODEL,
            request_type=request_type,
            created_at=datetime.utcnow()
        )
        
        db.add(usage)
        db.commit()
        
        log.debug(f"Tracked Groq usage: {total_tokens} tokens, ${cost_usd:.6f}")
    except Exception as e:
        log.error(f"Failed to track Groq usage: {e}")
        db.rollback()


def generate_with_groq(
    prompt: str,
    system_prompt: Optional[str] = None,
    db: Optional[Session] = None,
    request_type: str = "generation"
) -> Optional[str]:
    """
    Generate text using Groq API
    
    Args:
        prompt: User prompt for generation
        system_prompt: Optional system prompt to guide generation
        db: Optional database session for usage tracking
        request_type: Type of request for tracking purposes
        
    Returns:
        Generated text or None if generation failed
    """
    if not client:
        log.error("Groq client not initialized. Check GROQ_API_KEY environment variable.")
        return None
    
    if not prompt or not prompt.strip():
        log.error("Empty prompt provided")
        return None
    
    try:
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        if response.choices and len(response.choices) > 0:
            generated_text = response.choices[0].message.content
            
            # Track usage if database session provided
            if db and response.usage:
                input_tokens = response.usage.prompt_tokens or 0
                output_tokens = response.usage.completion_tokens or 0
                track_groq_usage(db, input_tokens, output_tokens, request_type)
            
            log.info(f"Successfully generated text with Groq API (length: {len(generated_text)})")
            return generated_text.strip()
        else:
            log.error("Groq API returned no choices")
            return None
            
    except Exception as e:
        log.error(f"Error calling Groq API: {e}")
        return None


def is_groq_available() -> bool:
    """
    Check if Groq API is available and configured
    
    Returns:
        True if Groq client is initialized, False otherwise
    """
    return client is not None


def get_groq_usage_stats(db: Session, days: int = 30) -> dict:
    """
    Get Groq usage statistics for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        Dictionary with usage statistics
    """
    try:
        from ..models_db import GroqUsage
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        usage_records = db.query(GroqUsage).filter(
            GroqUsage.created_at >= cutoff_date
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

