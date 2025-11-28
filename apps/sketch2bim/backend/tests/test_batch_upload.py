"""
Tests for batch upload functionality
Tests the POST /generate/batch-upload endpoint
"""
import pytest
import tempfile
import os
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Job
from app.auth import create_access_token


@pytest.fixture
def test_image_files():
    """Create test image files"""
    files = []
    temp_paths = []
    
    for i in range(3):
        # Create a simple test image
        img = Image.new('RGB', (200, 200), color='white')
        pixels = img.load()
        # Draw some lines
        for j in range(200):
            pixels[j, 100] = (0, 0, 0)  # Horizontal line
            pixels[100, j] = (0, 0, 0)  # Vertical line
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file.name)
        temp_paths.append(temp_file.name)
        files.append(('files', (f'test_{i}.png', open(temp_file.name, 'rb'), 'image/png')))
    
    yield files
    
    # Cleanup
    for file_tuple in files:
        if len(file_tuple) == 3:
            file_tuple[1][1].close()
    for path in temp_paths:
        if os.path.exists(path):
            os.unlink(path)


def test_batch_upload_success(client, test_user, auth_headers, test_image_files, db: Session):
    """Test successful batch upload"""
    # Override get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post(
            "/api/v1/generate/batch-upload",
            headers=auth_headers,
            files=test_image_files,
            data={"project_type": "architecture"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "batch_id" in data
        assert "job_ids" in data
        assert len(data["job_ids"]) == 3
        assert data["total_jobs"] == 3
        
        # Verify jobs were created in database
        jobs = db.query(Job).filter(Job.user_id == test_user.id).all()
        assert len(jobs) == 3
        
        # Verify all jobs have correct status
        for job in jobs:
            assert job.status == "queued"
            assert job.project_type == "architecture"
    finally:
        app.dependency_overrides.clear()


def test_batch_upload_invalid_file_type(client, test_user, auth_headers, db: Session):
    """Test batch upload with invalid file type"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        # Create a text file (invalid)
        temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w')
        temp_file.write("not an image")
        temp_file.close()
        
        files = [('files', ('test.txt', open(temp_file.name, 'rb'), 'text/plain'))]
        
        response = client.post(
            "/api/v1/generate/batch-upload",
            headers=auth_headers,
            files=files,
            data={"project_type": "architecture"}
        )
        
        assert response.status_code == 400
        files[0][1][1].close()
        os.unlink(temp_file.name)
    finally:
        app.dependency_overrides.clear()


def test_batch_upload_requires_subscription(client, test_user, db: Session):
    """Test that batch upload requires active subscription"""
    # Set user to free tier (no subscription)
    test_user.subscription_tier = None
    test_user.subscription_expires_at = None
    db.commit()
    
    token = create_access_token({"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        # Create a test image file
        img = Image.new('RGB', (200, 200), color='white')
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file.name)
        
        files = [('files', ('test.png', open(temp_file.name, 'rb'), 'image/png'))]
        
        response = client.post(
            "/api/v1/generate/batch-upload",
            headers=headers,
            files=files,
            data={"project_type": "architecture"}
        )
        
        # Should require subscription
        assert response.status_code in [403, 401]  # Forbidden or Unauthorized
        
        files[0][1][1].close()
        os.unlink(temp_file.name)
    finally:
        app.dependency_overrides.clear()


def test_batch_upload_empty_files(client, test_user, auth_headers, db: Session):
    """Test batch upload with no files"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post(
            "/api/v1/generate/batch-upload",
            headers=auth_headers,
            files=[],
            data={"project_type": "architecture"}
        )
        
        # Should return error for empty files
        assert response.status_code in [400, 422]  # Bad Request or Validation Error
    finally:
        app.dependency_overrides.clear()

