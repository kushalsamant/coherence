"""
Base database models
Apps should create their own models inheriting from these patterns.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class BaseUser(Base):
    """
    Base User model structure.
    Apps should create their own User model with app-specific fields.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    google_id = Column(String, unique=True, index=True)
    
    # Credits (kept for backward compatibility)
    credits = Column(Integer, default=0)
    
    # Subscription
    subscription_tier = Column(String, default="trial")
    subscription_status = Column(String, default="inactive")
    stripe_customer_id = Column(String, unique=True, index=True)  # Reused for Razorpay customer ID
    subscription_expires_at = Column(DateTime)
    
    # Razorpay subscription tracking
    razorpay_subscription_id = Column(String, nullable=True, index=True)
    subscription_auto_renew = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)


class BasePayment(Base):
    """
    Base Payment model structure.
    Apps should create their own Payment model with app-specific relationships.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Razorpay details (reusing Stripe field names for backward compatibility)
    stripe_payment_intent_id = Column(String, unique=True, index=True)  # Stores Razorpay payment_id
    stripe_checkout_session_id = Column(String, unique=True, index=True)  # Stores Razorpay order_id or subscription_id
    
    # Payment details
    amount = Column(Integer)  # in paise (₹1 = 100 paise)
    currency = Column(String, default="INR")
    status = Column(String)  # succeeded|pending|failed
    
    # Product
    product_type = Column(String)  # single|trial|week|month|year|one_time
    credits_added = Column(Integer, default=0)
    
    # Cost tracking
    processing_fee = Column(Integer, default=0)  # Razorpay fee in paise (2% of amount)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

