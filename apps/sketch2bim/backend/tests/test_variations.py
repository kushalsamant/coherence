"""
Tests for layout variations functionality
Tests the layout variation generation and routes
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Job, LayoutVariation
from app.ai.layout_generator import generate_layout_variations




@pytest.fixture
def test_job(db: Session, test_user):
    """Create a test job with plan data"""
    plan_data = {
        "rooms": [
            {
                "id": "room1",
                "polygon": [[0, 0], [100, 0], [100, 50], [0, 50]],
                "area": 5000,
                "type": "bedroom"
            },
            {
                "id": "room2",
                "polygon": [[100, 0], [200, 0], [200, 50], [100, 50]],
                "area": 5000,
                "type": "living"
            }
        ],
        "walls": [
            {"id": "wall1", "start": [0, 0], "end": [200, 0]},
            {"id": "wall2", "start": [0, 0], "end": [0, 50]}
        ],
        "openings": []
    }
    
    job = Job(
        id="test-job-123",
        user_id=test_user.id,
        status="completed",
        plan_data=plan_data,
        detection_confidence=0.85
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def test_generate_layout_variations():
    """Test layout variation generation function"""
    original_plan_data = {
        "rooms": [
            {
                "id": "room1",
                "polygon": [[0, 0], [100, 0], [100, 50], [0, 50]],
                "area": 5000
            },
            {
                "id": "room2",
                "polygon": [[100, 0], [200, 0], [200, 50], [100, 50]],
                "area": 5000
            }
        ],
        "walls": [],
        "openings": []
    }
    
    variations = generate_layout_variations(
        original_plan_data=original_plan_data,
        num_variations=3
    )
    
    assert len(variations) == 3
    for variation in variations:
        assert "plan_data" in variation
        assert "confidence" in variation
        assert "variation_number" in variation
        assert "rooms" in variation["plan_data"]
        assert len(variation["plan_data"]["rooms"]) == 2  # Same number of rooms


def test_generate_variations_no_rooms():
    """Test variation generation with no rooms"""
    original_plan_data = {
        "rooms": [],
        "walls": [],
        "openings": []
    }
    
    variations = generate_layout_variations(
        original_plan_data=original_plan_data,
        num_variations=3
    )
    
    # Should return empty list when no rooms
    assert len(variations) == 0


def test_create_variations_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test POST /variations/jobs/{job_id}/variations endpoint"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post(
            f"/api/v1/variations/jobs/{test_job.id}/variations",
            headers=auth_headers,
            json={"num_variations": 2}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Verify variations were created in database
        variations = db.query(LayoutVariation).filter(
            LayoutVariation.job_id == test_job.id
        ).all()
        assert len(variations) == 2
    finally:
        app.dependency_overrides.clear()


def test_list_variations_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test GET /variations/jobs/{job_id}/variations endpoint"""
    # Create some variations first
    variation1 = LayoutVariation(
        id="var1",
        job_id=test_job.id,
        user_id=test_user.id,
        variation_number=1,
        plan_data={"rooms": []},
        confidence=0.7
    )
    variation2 = LayoutVariation(
        id="var2",
        job_id=test_job.id,
        user_id=test_user.id,
        variation_number=2,
        plan_data={"rooms": []},
        confidence=0.8
    )
    db.add(variation1)
    db.add(variation2)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get(
            f"/api/v1/variations/jobs/{test_job.id}/variations",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["variation_number"] in [1, 2]
        assert data[1]["variation_number"] in [1, 2]
    finally:
        app.dependency_overrides.clear()


def test_get_variation_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test GET /variations/{variation_id} endpoint"""
    variation = LayoutVariation(
        id="var-test",
        job_id=test_job.id,
        user_id=test_user.id,
        variation_number=1,
        plan_data={"rooms": []},
        confidence=0.75
    )
    db.add(variation)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get(
            f"/api/v1/variations/{variation.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == variation.id
        assert data["confidence"] == 0.75
    finally:
        app.dependency_overrides.clear()


def test_delete_variation_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test DELETE /variations/{variation_id} endpoint"""
    variation = LayoutVariation(
        id="var-delete",
        job_id=test_job.id,
        user_id=test_user.id,
        variation_number=1,
        plan_data={"rooms": []},
        confidence=0.75
    )
    db.add(variation)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.delete(
            f"/api/v1/variations/{variation.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        # Verify variation was deleted
        deleted = db.query(LayoutVariation).filter(
            LayoutVariation.id == variation.id
        ).first()
        assert deleted is None
    finally:
        app.dependency_overrides.clear()

