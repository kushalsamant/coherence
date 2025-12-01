"""
Cost tracking and metering for job processing
Tracks GPU usage, API calls, and storage costs
"""
from typing import Dict


# Cost constants (USD)
BUNNYCDN_COST_PER_GB = 0.01  # $0.01 per GB stored
BUNNYCDN_COST_PER_GB_TRANSFER = 0.005  # $0.005 per GB transferred


class CostCalculator:
    """Calculates processing costs for jobs"""
    
    def __init__(self):
        pass
    
    def calculate_storage_cost(
        self,
        file_size_bytes: int,
        storage_days: int = 7
    ) -> float:
        """
        Calculate storage cost
        
        Args:
            file_size_bytes: File size in bytes
            storage_days: Number of days stored
            
        Returns:
            Cost in USD
        """
        size_gb = file_size_bytes / (1024 ** 3)
        daily_cost = size_gb * BUNNYCDN_COST_PER_GB / 30  # Monthly cost / 30 days
        return daily_cost * storage_days
    
    def calculate_transfer_cost(
        self,
        file_size_bytes: int
    ) -> float:
        """
        Calculate CDN transfer cost
        
        Args:
            file_size_bytes: File size in bytes
            
        Returns:
            Cost in USD
        """
        size_gb = file_size_bytes / (1024 ** 3)
        return size_gb * BUNNYCDN_COST_PER_GB_TRANSFER
    
    def calculate_job_cost(
        self,
        processing_duration: float,
        file_size_bytes: int,
        gpu_type: str = "gpu",
        storage_days: int = 7,
        include_transfer: bool = True
    ) -> Dict[str, float]:
        """
        Calculate total job cost breakdown
        
        Args:
            processing_duration: Processing time in seconds (not used for cost calculation)
            file_size_bytes: Output file size
            gpu_type: GPU type used (not used for cost calculation)
            storage_days: Days to store file
            include_transfer: Include CDN transfer cost
            
        Returns:
            dict with cost breakdown
        """
        # Processing is done locally (OpenCV), so no processing cost
        processing_cost = 0.0
        storage_cost = self.calculate_storage_cost(file_size_bytes, storage_days)
        transfer_cost = self.calculate_transfer_cost(file_size_bytes) if include_transfer else 0.0
        
        total = processing_cost + storage_cost + transfer_cost
        
        return {
            "processing": processing_cost,
            "storage": storage_cost,
            "transfer": transfer_cost,
            "total": total
        }


def calculate_job_cost(
    processing_duration: float,
    file_size_bytes: int,
    gpu_type: str = "gpu",
    storage_days: int = 7
) -> Dict[str, float]:
    """
    Convenience function to calculate total job cost
    
    Args:
        processing_duration: Processing time in seconds
        file_size_bytes: Output file size
        gpu_type: GPU type
        storage_days: Storage duration
        
    Returns:
        Cost breakdown dict
    """
    calculator = CostCalculator()
    return calculator.calculate_job_cost(
        processing_duration, file_size_bytes, gpu_type, storage_days
    )

