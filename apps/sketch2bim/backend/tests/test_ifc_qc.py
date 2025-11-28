"""
Tests for IFC quality control module
"""
import pytest
import tempfile
import os
from pathlib import Path

from app.ai.ifc_qc import validate_ifc, write_qc_report, QCReport


def test_validate_ifc_nonexistent():
    """Test validation of non-existent file"""
    report = validate_ifc("/nonexistent/file.ifc")
    assert report.valid is False
    assert len(report.errors) > 0
    assert any("does not exist" in e.message for e in report.errors)


def test_validate_ifc_empty_file():
    """Test validation of empty file"""
    with tempfile.NamedTemporaryFile(suffix='.ifc', delete=False) as f:
        f.write(b"")
        temp_path = f.name
    
    try:
        report = validate_ifc(temp_path)
        assert report.valid is False
        assert report.file_size == 0
    finally:
        os.unlink(temp_path)


def test_write_qc_report():
    """Test QC report generation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        report = QCReport(
            valid=True,
            confidence_score=85.0,
            errors=[],
            warnings=[],
            info=[],
            file_size=1000,
            element_counts={"IfcWall": 10},
            validation_timestamp="2025-01-01T00:00:00"
        )
        
        report_path = write_qc_report("test_job", report, tmpdir)
        
        assert os.path.exists(report_path)
        assert report_path.endswith("_qc_report.json")
        
        # Check text report also exists
        txt_path = report_path.replace(".json", ".txt")
        assert os.path.exists(txt_path)

