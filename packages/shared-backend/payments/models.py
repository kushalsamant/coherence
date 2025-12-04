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
    # razorpay_payment_id = Column(String, unique=True, index=True)  # Razorpay payment_id
    # razorpay_order_id = Column(String, unique=True, index=True)  # Razorpay order_id or subscription_id
    # amount = Column(Integer)  # in paise
    # currency = Column(String, default="INR")
    # status = Column(String)  # succeeded|pending|failed
    # product_type = Column(String)  # single|trial|weekly|monthly|yearly|one_time
    # credits_added = Column(Integer, default=0)
    # processing_fee = Column(Integer, default=0)  # Razorpay fee in paise
    # created_at = Column(DateTime, default=datetime.utcnow)
    # completed_at = Column(DateTime)
    
    pass

