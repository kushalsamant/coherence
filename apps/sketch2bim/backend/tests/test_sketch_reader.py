"""
Tests for sketch reader modules
"""
import pytest
import tempfile
import os
from PIL import Image
import numpy as np

from app.ai.sketch_reader import OpenCVReader, HybridReader, get_sketch_reader


def test_opencv_reader():
    """Test OpenCV-based sketch reading"""
    # Create a simple test image
    img = Image.new('RGB', (200, 200), color='white')
    # Draw some lines (simplified)
    pixels = img.load()
    for i in range(200):
        pixels[i, 100] = (0, 0, 0)  # Horizontal line
        pixels[100, i] = (0, 0, 0)  # Vertical line
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img.save(f.name)
        temp_path = f.name
    
    try:
        reader = OpenCVReader()
        result = reader.read_sketch(temp_path)
        
        assert "rooms" in result
        assert "walls" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_get_sketch_reader():
    """Test factory function"""
    reader = get_sketch_reader()
    assert reader is not None

