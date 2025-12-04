"""
Razorpay configuration
"""

import os
from typing import Optional
from .base import BaseSettings


class RazorpaySettings(BaseSettings):
    """Razorpay payment settings
    
    Note: This is a shared base class. Individual apps should extend this
    and read from prefixed environment variables (e.g., ASK_RAZORPAY_*).
    This class uses unprefixed variables for shared functionality.
    """
    
    # Razorpay credentials
    # Note: Apps should set prefixed variables (ASK_RAZORPAY_KEY_ID, etc.)
    # but this shared class uses unprefixed for cross-app compatibility
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""
    
    @property
    def razorpay_key_id(self) -> str:
        """Get Razorpay key ID"""
        return self.RAZORPAY_KEY_ID
    
    @property
    def razorpay_key_secret(self) -> str:
        """Get Razorpay key secret"""
        return self.RAZORPAY_KEY_SECRET
    
    # Pricing in paise (₹1 = 100 paise)
    # Shared across all projects - uses unprefixed variables
    # Apps can override with prefixed variables in their config
    RAZORPAY_WEEK_AMOUNT: int = int(os.getenv("RAZORPAY_WEEK_AMOUNT", "129900"))
    RAZORPAY_MONTH_AMOUNT: int = int(os.getenv("RAZORPAY_MONTH_AMOUNT", "349900"))
    RAZORPAY_YEAR_AMOUNT: int = int(os.getenv("RAZORPAY_YEAR_AMOUNT", "2999900"))
    
    # Razorpay Plan IDs for subscriptions
    # Shared across all projects - uses unprefixed variables
    RAZORPAY_PLAN_WEEKLY: str = os.getenv("RAZORPAY_PLAN_WEEKLY", "")
    RAZORPAY_PLAN_MONTHLY: str = os.getenv("RAZORPAY_PLAN_MONTHLY", "")
    RAZORPAY_PLAN_YEARLY: str = os.getenv("RAZORPAY_PLAN_YEARLY", "")
    
    class Config:
        case_sensitive = True
        extra = "ignore"

