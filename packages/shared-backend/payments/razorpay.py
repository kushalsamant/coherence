"""
Razorpay client and webhook utilities
"""

import logging
import razorpay
from typing import Optional
from ..config.base import get_settings

log = logging.getLogger(__name__)

# Global Razorpay client (lazy initialization)
_razorpay_client: Optional[razorpay.Client] = None


def get_razorpay_client() -> Optional[razorpay.Client]:
    """
    Get or create Razorpay client instance.
    
    Returns:
        Razorpay client or None if not configured
    """
    global _razorpay_client
    
    if _razorpay_client is not None:
        return _razorpay_client
    
    try:
        settings = get_settings()
        key_id = settings.razorpay_key_id if hasattr(settings, 'razorpay_key_id') else None
        key_secret = settings.razorpay_key_secret if hasattr(settings, 'razorpay_key_secret') else None
    except Exception:
        # Fallback to environment variables
        # Note: This shared package uses unprefixed variables for cross-app compatibility
        # Apps should set prefixed variables (ASK_RAZORPAY_KEY_ID, etc.) in their .env files
        import os
        key_id = os.getenv("RAZORPAY_KEY_ID") or os.getenv("LIVE_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET") or os.getenv("LIVE_KEY_SECRET")
    
    if not key_id or not key_secret:
        log.warning("Razorpay credentials not configured")
        return None
    
    try:
        _razorpay_client = razorpay.Client(auth=(key_id, key_secret))
        return _razorpay_client
    except Exception as e:
        log.error(f"Failed to initialize Razorpay client: {e}")
        return None


def verify_webhook_signature(payload: str, signature: str, webhook_secret: Optional[str] = None) -> bool:
    """
    Verify Razorpay webhook signature.
    
    Args:
        payload: Webhook payload string
        signature: Webhook signature from header
        webhook_secret: Optional webhook secret (uses settings if not provided)
        
    Returns:
        True if signature is valid, False otherwise
    """
    client = get_razorpay_client()
    if not client:
        return False
    
    try:
        settings = get_settings()
        secret = webhook_secret or (getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', None) if hasattr(settings, 'RAZORPAY_WEBHOOK_SECRET') else None)
    except Exception:
        # Fallback to environment variable
        # Note: This shared package uses unprefixed variables for cross-app compatibility
        import os
        secret = webhook_secret or os.getenv("RAZORPAY_WEBHOOK_SECRET")
    
    if not secret:
        log.warning("Razorpay webhook secret not configured")
        return False
    
    try:
        client.utility.verify_webhook_signature(
            payload,
            signature,
            secret
        )
        return True
    except Exception as e:
        log.error(f"Webhook signature verification failed: {e}")
        return False

