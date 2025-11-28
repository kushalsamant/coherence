"""
Tests for iterations functionality
Tests the IFC file versioning and editing routes
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Job, Iteration




@pytest.fixture
def test_job(db: Session, test_user):
    """Create a test job with IFC URL and plan data"""
    plan_data = {
        "rooms": [
            {
                "id": "room1",
                "polygon": [[0, 0], [100, 0], [100, 50], [0, 50]],
                "area": 5000
            }
        ],
        "walls": [],
        "openings": []
    }
    
    job = Job(
        id="test-job-iter",
        user_id=test_user.id,
        status="completed",
        plan_data=plan_data,
        ifc_url="https://example.com/test.ifc",
        sketch_filename="test.png"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def test_create_iteration_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test POST /iterations/jobs/{job_id}/iterations endpoint"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post(
            f"/api/v1/iterations/jobs/{test_job.id}/iterations",
            headers=auth_headers,
            json={
                "name": "Test Iteration",
                "notes": "Testing iteration creation",
                "changes_json": {
                    "moved_elements": [],
                    "resized_rooms": []
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Iteration"
        assert data["notes"] == "Testing iteration creation"
        assert data["job_id"] == test_job.id
        
        # Verify iteration was created in database
        iteration = db.query(Iteration).filter(
            Iteration.id == data["id"]
        ).first()
        assert iteration is not None
    finally:
        app.dependency_overrides.clear()


def test_list_iterations_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test GET /iterations/jobs/{job_id}/iterations endpoint"""
    # Create some iterations first
    iteration1 = Iteration(
        id="iter1",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/iter1.ifc",
        ifc_filename="iter1.ifc",
        name="Iteration 1",
        changes_json={}
    )
    iteration2 = Iteration(
        id="iter2",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/iter2.ifc",
        ifc_filename="iter2.ifc",
        name="Iteration 2",
        changes_json={}
    )
    db.add(iteration1)
    db.add(iteration2)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get(
            f"/api/v1/iterations/jobs/{test_job.id}/iterations",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] in ["iter1", "iter2"]
        assert data[1]["id"] in ["iter1", "iter2"]
    finally:
        app.dependency_overrides.clear()


def test_get_iteration_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test GET /iterations/{iteration_id} endpoint"""
    iteration = Iteration(
        id="iter-get",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/iter.ifc",
        ifc_filename="iter.ifc",
        name="Test Iteration",
        changes_json={"moved_elements": []}
    )
    db.add(iteration)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get(
            f"/api/v1/iterations/{iteration.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == iteration.id
        assert data["name"] == "Test Iteration"
    finally:
        app.dependency_overrides.clear()


def test_update_iteration_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test PATCH /iterations/{iteration_id} endpoint"""
    iteration = Iteration(
        id="iter-update",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/iter.ifc",
        ifc_filename="iter.ifc",
        name="Original Name",
        changes_json={}
    )
    db.add(iteration)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.patch(
            f"/api/v1/iterations/{iteration.id}",
            headers=auth_headers,
            json={
                "name": "Updated Name",
                "notes": "Updated notes",
                "changes_json": {"moved_elements": [{"element_id": "wall1"}]}
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["notes"] == "Updated notes"
        assert "moved_elements" in data["changes_json"]
    finally:
        app.dependency_overrides.clear()


def test_delete_iteration_endpoint(client, test_user, test_job, auth_headers, db: Session):
    """Test DELETE /iterations/{iteration_id} endpoint"""
    iteration = Iteration(
        id="iter-delete",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/iter.ifc",
        ifc_filename="iter.ifc",
        name="To Delete",
        changes_json={}
    )
    db.add(iteration)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.delete(
            f"/api/v1/iterations/{iteration.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        # Verify iteration was deleted
        deleted = db.query(Iteration).filter(
            Iteration.id == iteration.id
        ).first()
        assert deleted is None
    finally:
        app.dependency_overrides.clear()


def test_create_iteration_with_parent(client, test_user, test_job, auth_headers, db: Session):
    """Test creating iteration with parent iteration"""
    parent = Iteration(
        id="parent-iter",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/parent.ifc",
        ifc_filename="parent.ifc",
        name="Parent Iteration",
        changes_json={}
    )
    db.add(parent)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post(
            f"/api/v1/iterations/jobs/{test_job.id}/iterations",
            headers=auth_headers,
            json={
                "parent_iteration_id": parent.id,
                "name": "Child Iteration",
                "changes_json": {}
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["parent_iteration_id"] == parent.id
    finally:
        app.dependency_overrides.clear()


def test_delete_iteration_with_children(client, test_user, test_job, auth_headers, db: Session):
    """Test that deletion fails if iteration has children"""
    parent = Iteration(
        id="parent-with-child",
        job_id=test_job.id,
        user_id=test_user.id,
        ifc_url="https://example.com/parent.ifc",
        ifc_filename="parent.ifc",
        name="Parent",
        changes_json={}
    )
    child = Iteration(
        id="child-iter",
        job_id=test_job.id,
        user_id=test_user.id,
        parent_iteration_id=parent.id,
        ifc_url="https://example.com/child.ifc",
        ifc_filename="child.ifc",
        name="Child",
        changes_json={}
    )
    db.add(parent)
    db.add(child)
    db.commit()
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.delete(
            f"/api/v1/iterations/{parent.id}",
            headers=auth_headers
        )
        
        # Should fail because parent has children
        assert response.status_code == 400
    finally:
        app.dependency_overrides.clear()

