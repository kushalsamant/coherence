"""
Storage usage monitoring
Tracks BunnyCDN storage usage and calculates cost estimates
"""
from typing import Dict, Any, Optional
import requests
from ..config import settings
from loguru import logger
from ..utils.costing import BUNNYCDN_COST_PER_GB, BUNNYCDN_COST_PER_GB_TRANSFER

# BunnyCDN API endpoint for storage statistics
BUNNYCDN_STATS_API = "https://api.bunny.net/storagezone/{zone_id}/statistics"


def get_storage_usage() -> Dict[str, Any]:
    """
    Get BunnyCDN storage usage
    
    Returns:
        dict with size_gb, size_tb, cost_estimate, file_count, status
    """
    try:
        if not settings.BUNNY_STORAGE_ZONE or not settings.BUNNY_ACCESS_KEY:
            return {
                "size_gb": 0,
                "size_tb": 0,
                "cost_estimate_usd": 0,
                "file_count": 0,
                "status": "error",
                "error": "BunnyCDN not configured"
            }
        
        # Query BunnyCDN API for storage statistics
        # Note: BunnyCDN API may require different endpoint structure
        # This is a placeholder - actual API may vary
        headers = {
            "AccessKey": settings.BUNNY_ACCESS_KEY,
            "Accept": "application/json"
        }
        
        # Try to get storage zone statistics
        # BunnyCDN API endpoint structure may vary
        stats_url = f"https://api.bunny.net/storagezone/{settings.BUNNY_STORAGE_ZONE}/statistics"
        
        try:
            response = requests.get(stats_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract storage information (API structure may vary)
                # These fields are placeholders - adjust based on actual API response
                storage_bytes = data.get("StorageUsed", 0) or data.get("storage_used", 0) or 0
                file_count = data.get("FileCount", 0) or data.get("file_count", 0) or 0
                
                size_gb = storage_bytes / (1024 ** 3)
                size_tb = size_gb / 1024
                
                # Calculate cost estimate (storage + transfer)
                # Storage cost: $0.01 per GB per month
                storage_cost_monthly = size_gb * BUNNYCDN_COST_PER_GB
                
                # Transfer cost (estimate based on typical usage)
                # This would need actual transfer data from API
                transfer_gb_estimate = size_gb * 0.1  # Estimate 10% of storage as transfer
                transfer_cost_monthly = transfer_gb_estimate * BUNNYCDN_COST_PER_GB_TRANSFER
                
                total_cost_estimate = storage_cost_monthly + transfer_cost_monthly
                
                return {
                    "size_gb": round(size_gb, 2),
                    "size_tb": round(size_tb, 4),
                    "size_bytes": storage_bytes,
                    "cost_estimate_usd": round(total_cost_estimate, 2),
                    "storage_cost_usd": round(storage_cost_monthly, 2),
                    "transfer_cost_estimate_usd": round(transfer_cost_monthly, 2),
                    "file_count": file_count,
                    "status": "ok"
                }
            else:
                logger.warning(f"BunnyCDN API returned status {response.status_code}: {response.text}")
                # Fallback: estimate from database
                return _estimate_storage_from_database()
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"BunnyCDN API request failed: {e}")
            # Fallback: estimate from database
            return _estimate_storage_from_database()
            
    except Exception as e:
        logger.error(f"Error getting storage usage: {e}")
        return {
            "size_gb": 0,
            "size_tb": 0,
            "cost_estimate_usd": 0,
            "file_count": 0,
            "status": "error",
            "error": str(e)
        }


def _estimate_storage_from_database() -> Dict[str, Any]:
    """
    Estimate storage usage from database job records
    Fallback when BunnyCDN API is unavailable
    """
    try:
        from ..database import SessionLocal
        from ..models import Job
        from sqlalchemy import func
        
        db = SessionLocal()
        try:
            # Count jobs with files
            jobs_with_files = db.query(func.count(Job.id)).filter(
                (Job.ifc_url.isnot(None)) | (Job.dwg_url.isnot(None))
            ).scalar() or 0
            
            # Estimate average file size (IFC files are typically 1-10MB)
            # This is a rough estimate
            avg_file_size_mb = 5  # 5MB average
            total_size_gb = (jobs_with_files * avg_file_size_mb) / 1024
            
            storage_cost_monthly = total_size_gb * BUNNYCDN_COST_PER_GB
            transfer_cost_estimate = (total_size_gb * 0.1) * BUNNYCDN_COST_PER_GB_TRANSFER
            
            return {
                "size_gb": round(total_size_gb, 2),
                "size_tb": round(total_size_gb / 1024, 4),
                "size_bytes": int(total_size_gb * (1024 ** 3)),
                "cost_estimate_usd": round(storage_cost_monthly + transfer_cost_estimate, 2),
                "storage_cost_usd": round(storage_cost_monthly, 2),
                "transfer_cost_estimate_usd": round(transfer_cost_estimate, 2),
                "file_count": jobs_with_files * 2,  # Estimate 2 files per job (IFC + DWG)
                "status": "estimated",
                "note": "Estimated from database (BunnyCDN API unavailable)"
            }
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error estimating storage from database: {e}")
        return {
            "size_gb": 0,
            "size_tb": 0,
            "cost_estimate_usd": 0,
            "file_count": 0,
            "status": "error",
            "error": str(e)
        }

