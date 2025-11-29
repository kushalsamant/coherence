"""
SQLAlchemy database models
Extends base models from shared-backend
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from shared_backend.database.models import BaseUser, BasePayment


class User(BaseUser, Base):
    """
    User model - extends BaseUser from shared-backend
    Add app-specific fields here if needed
    """
    __tablename__ = "users"
    
    # Relationships
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Payment(BasePayment, Base):
    """
    Payment model - extends BasePayment from shared-backend
    Add app-specific fields here if needed
    """
    __tablename__ = "payments"
    
    # Relationships
    user = relationship("User", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.id} - {self.amount}>"

