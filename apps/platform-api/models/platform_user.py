"""
Platform User Model
User model for the platform (home site)
Manages user accounts, subscriptions, and authentication
This is the canonical User model - sketch2bim references this table
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.platform import Base


class User(Base):
    """
    User model for the platform
    
    This is the canonical User table managed by the home site.
    Sketch2BIM and other apps reference this table from the shared database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    credits = Column(Integer, nullable=True, server_default="5")
    subscription_tier = Column(String, nullable=True, server_default="trial")
    subscription_status = Column(String, nullable=True, server_default="inactive")
    razorpay_customer_id = Column(String, unique=True, index=True, nullable=True)
    razorpay_subscription_id = Column(String, index=True, nullable=True)
    subscription_auto_renew = Column(Boolean, nullable=True, server_default="false")
    subscription_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=True, server_default="true")

    # Note: Relationships to sketch2bim models (Job, Payment, etc.) are NOT defined here
    # Those relationships are defined in sketch2bim's models, which reference user_id via ForeignKey
    # This keeps the platform model clean and independent


class Payment(Base):
    """
    Payment model reference for platform subscriptions
    This is a reference to the payments table in the shared database.
    The full Payment model is in the sketch2bim repository.
    This minimal reference allows the platform to record subscription payments.
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    razorpay_payment_id = Column(String, unique=True, index=True, nullable=True)
    razorpay_order_id = Column(String, unique=True, index=True, nullable=True)
    amount = Column(Integer, nullable=True)
    currency = Column(String, nullable=True, server_default="INR")
    status = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    credits_added = Column(Integer, nullable=True, server_default="0")
    processing_fee = Column(Integer, nullable=True, server_default="0")
    created_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
