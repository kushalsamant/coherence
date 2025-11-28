"""
Pytest configuration and shared fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.models import User, Job, LayoutVariation, Iteration
from app.main import app
from app.auth import create_access_token


# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a test database session"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def test_user(db: Session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        name="Test User",
        credits=100,
        subscription_tier="pro",
        subscription_expires_at=None
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create auth headers for test user"""
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

