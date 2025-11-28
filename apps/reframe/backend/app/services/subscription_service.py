"""
Subscription Service for Reframe
Handles subscription logic and status management
"""
from typing import Dict, Optional
from datetime import datetime, timedelta


# Subscription tier durations in days
SUBSCRIPTION_DURATIONS = {
    "trial": 7,
    "daily": 1,
    "week": 1,  # Week is same as daily (1 day pass)
    "monthly": 30,
    "yearly": 365,
}

# Paid subscription tiers
PAID_TIERS = {"daily", "monthly", "yearly"}


def calculate_expiry(tier: str, reference_date: Optional[datetime] = None) -> Optional[str]:
    """Calculate expiry date for a subscription tier"""
    days = SUBSCRIPTION_DURATIONS.get(tier.lower())
    if not days:
        return None
    
    start = reference_date or datetime.utcnow()
    expiry = start + timedelta(days=days)
    return expiry.isoformat()


def is_paid_tier(tier: Optional[str]) -> bool:
    """Check if a tier is a paid tier"""
    if not tier:
        return False
    return tier.lower() in PAID_TIERS


def is_active_trial(metadata: Dict) -> bool:
    """Check if user has an active trial period"""
    if metadata.get("subscription_tier") != "trial":
        return False
    if metadata.get("subscription_status") != "active":
        return False
    if not metadata.get("subscription_expires_at"):
        return False
    
    try:
        expiry = datetime.fromisoformat(metadata["subscription_expires_at"].replace("Z", "+00:00"))
        return expiry > datetime.utcnow()
    except (ValueError, KeyError):
        return False


def has_active_subscription(metadata: Dict) -> bool:
    """Check if user has an active subscription (trial or paid tier)"""
    # Check if user is in active trial
    if is_active_trial(metadata):
        return True
    
    # Check if user has active paid tier subscription
    tier = metadata.get("subscription_tier")
    if is_paid_tier(tier):
        if metadata.get("subscription_status") != "active":
            return False
        if not metadata.get("subscription_expires_at"):
            return False
        
        try:
            expiry = datetime.fromisoformat(metadata["subscription_expires_at"].replace("Z", "+00:00"))
            is_expired = expiry <= datetime.utcnow()
            
            # If auto-renew is enabled, consider it active even if slightly expired
            # (webhook will update expiry)
            if is_expired and metadata.get("subscription_auto_renew") and metadata.get("razorpay_subscription_id"):
                return True  # Still active, waiting for renewal webhook
            
            return not is_expired
        except (ValueError, KeyError):
            return False
    
    return False


def ensure_subscription_status(metadata: Dict) -> Dict:
    """Ensure subscription status matches expiry date"""
    expires_at = metadata.get("subscription_expires_at")
    if expires_at:
        try:
            expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            now = datetime.utcnow()
            
            if expiry < now:
                # If it's a subscription with auto-renew, don't downgrade yet
                # The webhook will update the expiry date
                if metadata.get("subscription_auto_renew") and metadata.get("razorpay_subscription_id"):
                    return metadata  # Keep status, webhook will update
                
                # One-time payment expired or subscription cancelled
                updated = metadata.copy()
                updated.update({
                    "subscription_tier": "trial",
                    "subscription_status": "expired",
                    "subscription_expires_at": None,
                    "subscription_auto_renew": False,
                    "razorpay_subscription_id": None,
                })
                return updated
        except (ValueError, KeyError):
            pass
    
    return metadata

