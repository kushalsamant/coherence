"""
Common test fixtures for backend tests
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Import base models
from shared_backend.database.models import Base


@pytest.fixture
def db_engine():
    """
    Create an in-memory SQLite database for testing
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """
    Create a database session for testing
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user_data():
    """
    Sample user data for testing
    """
    return {
        "email": "test@example.com",
        "name": "Test User",
        "google_id": "google_123",
        "subscription_tier": "trial",
        "subscription_status": "active",
        "subscription_expires_at": datetime.utcnow() + timedelta(days=7),
        "razorpay_customer_id": "cust_test123",
        "razorpay_subscription_id": None,
        "subscription_auto_renew": False,
        "is_active": True,
    }


@pytest.fixture
def test_user(db_session, test_user_data):
    """
    Create a test user in the database
    """
    from shared_backend.database.models import BaseUser
    
    # Create a concrete User class for testing
    class TestUser(BaseUser, Base):
        __tablename__ = "users"
    
    user = TestUser(**test_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_payment_data(test_user):
    """
    Sample payment data for testing
    """
    return {
        "user_id": test_user.id,
        "razorpay_payment_id": "pay_test123",
        "razorpay_order_id": "order_test123",
        "amount": 29900,  # ₹299 in paise
        "currency": "INR",
        "status": "succeeded",
        "product_type": "monthly",
        "credits_added": 0,
        "processing_fee": 2600,  # 2% of amount
        "completed_at": datetime.utcnow(),
    }


@pytest.fixture
def test_payment(db_session, test_payment_data):
    """
    Create a test payment in the database
    """
    from shared_backend.database.models import BasePayment
    
    # Create a concrete Payment class for testing
    class TestPayment(BasePayment, Base):
        __tablename__ = "payments"
    
    payment = TestPayment(**test_payment_data)
    db_session.add(payment)
    db_session.commit()
    db_session.refresh(payment)
    return payment


@pytest.fixture
def authenticated_client(test_user):
    """
    Create an authenticated test client
    """
    from fastapi.testclient import TestClient
    
    # This is a placeholder - apps should override this with their actual app
    def get_client(app):
        client = TestClient(app)
        # Add authentication token to client
        # client.headers["Authorization"] = f"Bearer {token}"
        return client
    
    return get_client

