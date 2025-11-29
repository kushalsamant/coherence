"""
SQLAlchemy database models for ASK Research Tool
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    google_id = Column(String, unique=True, index=True)
    
    # Credits (kept for backward compatibility, but not used for access control)
    credits = Column(Integer, default=0)  # Start with 0 credits - unlimited during trial, then must upgrade
    subscription_tier = Column(String, default="trial")  # trial|week|monthly|yearly
    subscription_status = Column(String, default="inactive")  # inactive|active|cancelled
    razorpay_customer_id = Column(String, unique=True, index=True)  # Razorpay customer ID
    subscription_expires_at = Column(DateTime)
    
    # Razorpay subscription tracking
    razorpay_subscription_id = Column(String, nullable=True, index=True)  # Active subscription ID
    subscription_auto_renew = Column(Boolean, default=False)  # True if subscription, False if one-time
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Payment(Base):
    """Payment transaction history"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Razorpay details
    razorpay_payment_id = Column(String, unique=True, index=True)  # Razorpay payment_id
    razorpay_order_id = Column(String, unique=True, index=True)  # Razorpay order_id or subscription_id
    
    # Payment details
    amount = Column(Integer)  # in paise (₹1 = 100 paise)
    currency = Column(String, default="INR")
    status = Column(String)  # succeeded|pending|failed
    
    # Product
    product_type = Column(String)  # single|trial|week|monthly|yearly|one_time
    credits_added = Column(Integer, default=0)
    
    # Cost tracking
    processing_fee = Column(Integer, default=0)  # Razorpay fee in paise (2% of amount)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.razorpay_payment_id}>"


class GroqUsage(Base):
    """Groq API usage tracking"""
    __tablename__ = "groq_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Usage details
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # Cost calculation (USD)
    cost_usd = Column(String, default="0.0")  # Store as string for precision
    
    # Request metadata
    model = Column(String, default="llama-3.1-70b-versatile")
    request_type = Column(String)  # e.g., "question_generation", "answer_generation"
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<GroqUsage {self.id}: {self.total_tokens} tokens, ${self.cost_usd}>"

