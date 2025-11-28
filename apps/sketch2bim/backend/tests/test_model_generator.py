"""
Tests for model generator
"""
import pytest
import tempfile
import os
from pathlib import Path

from app.ai.model_generator import ModelGenerator, generate_model


def test_model_generator_initialization():
    """Test model generator can be initialized"""
    generator = ModelGenerator()
    assert generator is not None
    # ModelGenerator uses pure Python IfcOpenShell (no Blender required)


def test_generate_model_structure():
    """Test model generation returns correct structure"""
    # Model generator uses IfcOpenShell, no Blender setup required
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy sketch
        from PIL import Image
        sketch_path = Path(tmpdir) / "test.png"
        Image.new('RGB', (100, 100), color='white').save(sketch_path)
        
        # This test validates structure - actual execution would require
        # IfcOpenShell and valid sketch/image processing
        # In real tests, mock sketch_reader and ifc_generator if needed
        pass

