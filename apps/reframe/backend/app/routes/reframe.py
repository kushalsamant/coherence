"""
Reframe API Route
Main endpoint for text reframing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ..models import ReframeRequest, ReframeResponse, ErrorResponse
from ..auth import get_current_user_id, get_current_user_email
from ..services.user_metadata_service import (
    get_user_metadata,
    initialize_user_trial,
    set_user_metadata,
    get_usage,
    increment_usage,
)
from ..services.subscription_service import (
    has_active_subscription,
    ensure_subscription_status,
)
from ..services.tone_service import can_user_access_tone
from ..services.groq_service import reframe_text
from ..services.groq_monitor import track_groq_usage
import os

router = APIRouter()

FREE_LIMIT = int(os.getenv("REFRAME_FREE_LIMIT", os.getenv("FREE_LIMIT", "5")))


@router.post("/api/reframe", response_model=ReframeResponse)
async def reframe(
    request: ReframeRequest,
    user_id: str = Depends(get_current_user_id),
    user_email: Optional[str] = Depends(get_current_user_email),
):
    """
    Reframe text using AI with specified tone
    
    Requires authentication via NextAuth JWT token.
    """
    # Get user metadata and initialize trial if needed
    metadata = await get_user_metadata(user_id)
    if not metadata:
        if user_email:
            await initialize_user_trial(user_id, user_email)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize user: email not available",
            )
        metadata = await get_user_metadata(user_id)
    
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize user",
        )
    
    # Ensure subscription status is up to date
    metadata = ensure_subscription_status(metadata)
    if metadata.get("subscription_status") == "expired" and not metadata.get("subscription_expires_at"):
        await set_user_metadata(user_id, metadata)
    
    # Check if user has active subscription (trial or paid)
    has_active_sub = has_active_subscription(metadata)
    subscription_tier = metadata.get("subscription_tier")
    
    # Validate tone parameter
    selected_tone = request.tone or "conversational"
    
    # Legacy: Check subscription field for backward compatibility
    legacy_subscription = metadata.get("subscription")
    if not can_user_access_tone(selected_tone, subscription_tier or legacy_subscription):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium tone! Upgrade to unlock Enthusiastic, Empathetic, and Witty tones.",
        )
    
    # Usage tracking - only track for free users after trial expires
    usage = 0
    usage_key = ""
    
    if has_active_sub:
        # User has active subscription (trial or paid) - unlimited access
        # No usage tracking needed
        pass
    else:
        # Free user after trial expired - check 5 request limit
        usage = await get_usage(user_id)
        
        if usage >= FREE_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Free limit reached. Upgrade to unlock unlimited requests!",
            )
    
    try:
        # Call Groq API
        result = await reframe_text(
            text=request.text,
            tone=selected_tone,
            generation=request.generation or "any"
        )
        
        output = result["output"]
        groq_usage = result["usage"]
        
        # Track Groq usage (tokens and cost)
        if groq_usage:
            await track_groq_usage(
                groq_usage.get("prompt_tokens", 0),
                groq_usage.get("completion_tokens", 0),
                "reframe"
            )
        
        # Update usage only for free users (after trial expired)
        if not has_active_sub:
            usage = await increment_usage(user_id)
        
        return ReframeResponse(
            output=output,
            usage=usage if not has_active_sub else None  # Only return usage for free tier
        )
    except HTTPException:
        raise
    except Exception as err:
        print(f"Groq API error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err) if str(err) else "Reframing failed",
        )

