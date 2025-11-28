"""
Subscription utility functions for tier durations and status management.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

SUBSCRIPTION_DURATIONS = {
    "trial": timedelta(days=7),
    "week": timedelta(days=7),
    "month": timedelta(days=30),
    "year": timedelta(days=365),
}

PAID_TIERS = {"week", "month", "year"}


def calculate_expiry(tier: str, reference: Optional[datetime] = None) -> Optional[datetime]:
    """Return expiry datetime for a tier."""
    duration = SUBSCRIPTION_DURATIONS.get(tier)
    if not duration:
        return None
    start = reference or datetime.utcnow()
    return start + duration


def is_paid_tier(tier: Optional[str]) -> bool:
    return tier in PAID_TIERS


def is_active_trial(user) -> bool:
    """
    Check if user is in active trial period.
    Returns True if user has trial tier, active status, and hasn't expired.
    """
    if user.subscription_tier != "trial":
        return False
    if user.subscription_status != "active":
        return False
    if not user.subscription_expires_at:
        return False
    return user.subscription_expires_at > datetime.utcnow()


def has_active_subscription(user) -> bool:
    """
    Check if user has an active subscription (trial or paid tier).
    Returns True if:
    - User is in active trial, OR
    - User has paid tier and subscription is active and not expired.
    This replaces all credit-based access checks.
    """
    # Check if user is in active trial
    if is_active_trial(user):
        return True
    
    # Check if user has active paid tier subscription
    if is_paid_tier(user.subscription_tier):
        if user.subscription_status != "active":
            return False
        if not user.subscription_expires_at:
            return False
        return user.subscription_expires_at > datetime.utcnow()
    
    # No active subscription
    return False


def ensure_subscription_status(user, db: Optional[Session] = None) -> None:
    """
    Ensure user's subscription status matches expiry.
    Downgrade to trial if expired.
    For subscriptions, check if still active in Razorpay.
    """
    # Check if subscription expired
    if user.subscription_expires_at and user.subscription_expires_at < datetime.utcnow():
        # If it's a subscription (auto_renew), check if it's still active
        if user.subscription_auto_renew and user.razorpay_subscription_id:
            # Subscription might have been renewed - don't downgrade yet
            # The webhook will update the expiry date
            return
        
        # One-time payment expired or subscription cancelled
        user.subscription_tier = "trial"
        user.subscription_status = "expired"
        user.subscription_expires_at = None
        user.razorpay_subscription_id = None
        user.subscription_auto_renew = False
        user.credits = 0  # No free credits after trial expires - users must upgrade
        if db:
            db.commit()

