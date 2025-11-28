"""
Payment model utilities
"""

from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class PaymentModel:
    """
    Base payment model structure.
    Apps should create their own Payment model inheriting from this pattern.
    """
    
    # Common fields (apps should implement these in their SQLAlchemy models)
    # id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # stripe_payment_intent_id = Column(String, unique=True, index=True)  # Stores Razorpay payment_id
    # stripe_checkout_session_id = Column(String, unique=True, index=True)  # Stores Razorpay order_id or subscription_id
    # amount = Column(Integer)  # in paise
    # currency = Column(String, default="INR")
    # status = Column(String)  # succeeded|pending|failed
    # product_type = Column(String)  # single|trial|week|month|year|one_time
    # credits_added = Column(Integer, default=0)
    # processing_fee = Column(Integer, default=0)  # Razorpay fee in paise
    # created_at = Column(DateTime, default=datetime.utcnow)
    # completed_at = Column(DateTime)
    
    pass

