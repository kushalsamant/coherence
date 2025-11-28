"""
Razorpay configuration
"""

from typing import Optional
from .base import BaseSettings


class RazorpaySettings(BaseSettings):
    """Razorpay payment settings"""
    
    # Razorpay credentials
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""
    
    # Legacy aliases (for backward compatibility)
    LIVE_KEY_ID: str = ""
    LIVE_KEY_SECRET: str = ""
    
    @property
    def razorpay_key_id(self) -> str:
        """Get Razorpay key ID, checking both variable names"""
        return self.RAZORPAY_KEY_ID or self.LIVE_KEY_ID
    
    @property
    def razorpay_key_secret(self) -> str:
        """Get Razorpay key secret, checking both variable names"""
        return self.RAZORPAY_KEY_SECRET or self.LIVE_KEY_SECRET
    
    # Pricing in paise (₹1 = 100 paise)
    RAZORPAY_WEEK_AMOUNT: int = 129900
    RAZORPAY_MONTH_AMOUNT: int = 349900
    RAZORPAY_YEAR_AMOUNT: int = 2999900
    
    # Razorpay Plan IDs for subscriptions
    RAZORPAY_PLAN_WEEK: str = ""
    RAZORPAY_PLAN_MONTH: str = ""
    RAZORPAY_PLAN_YEAR: str = ""
    
    class Config:
        case_sensitive = True
        extra = "ignore"

