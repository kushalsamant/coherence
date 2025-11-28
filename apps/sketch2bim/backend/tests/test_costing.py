"""
Tests for cost calculation
"""
import pytest
from app.utils.costing import (
    estimate_gpu_cost,
    calculate_job_cost,
    CostCalculator
)


def test_estimate_gpu_cost():
    """Test GPU cost estimation"""
    cost = estimate_gpu_cost(60.0, "gpu")  # 60 seconds
    assert cost > 0
    assert cost < 1.0  # Should be reasonable


def test_calculate_job_cost():
    """Test full job cost calculation"""
    cost_breakdown = calculate_job_cost(
        processing_duration=60.0,
        file_size_bytes=1024 * 1024,  # 1MB
        gpu_type="gpu",
        storage_days=7
    )
    
    assert "processing" in cost_breakdown
    assert "storage" in cost_breakdown
    assert "transfer" in cost_breakdown
    assert "total" in cost_breakdown
    assert cost_breakdown["total"] > 0


def test_cost_calculator():
    """Test CostCalculator class"""
    calculator = CostCalculator()
    
    # Test storage cost
    storage_cost = calculator.calculate_storage_cost(1024 * 1024 * 100, 7)  # 100MB for 7 days
    assert storage_cost >= 0
    
    # Test transfer cost
    transfer_cost = calculator.calculate_transfer_cost(1024 * 1024 * 10)  # 10MB
    assert transfer_cost >= 0

