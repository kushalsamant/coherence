"""
Utility functions for file storage, signing, and helpers
"""
import hashlib
import time
from typing import Optional
from pathlib import Path
import requests
from datetime import datetime
import uuid

from ..config import settings


# ============================================================================
# BunnyCDN Functions
# ============================================================================

def upload_to_bunny(file_path: str, remote_path: str) -> str:
    """
    Upload file to BunnyCDN storage
    
    Args:
        file_path: Local file path to upload
        remote_path: Remote path in storage zone (e.g., "jobs/abc123/model.ifc")
    
    Returns:
        Public CDN URL
    """
    storage_url = f"https://{settings.BUNNY_REGION}/{settings.BUNNY_STORAGE_ZONE}/{remote_path}"
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    headers = {
        "AccessKey": settings.BUNNY_ACCESS_KEY,
        "Content-Type": "application/octet-stream"
    }
    
    response = requests.put(
        storage_url,
        headers=headers,
        data=file_data,
        timeout=300
    )
    
    if response.status_code not in [200, 201]:
        raise Exception(f"BunnyCDN upload failed: {response.text}")
    
    # Return CDN URL
    cdn_url = f"https://{settings.BUNNY_CDN_HOSTNAME}/{remote_path}"
    return cdn_url


def create_signed_bunny_url(url: str, expiry_seconds: Optional[int] = None) -> str:
    """
    Create signed URL with expiration for BunnyCDN
    
    Args:
        url: Base CDN URL
        expiry_seconds: Seconds until expiration (default: from settings)
    
    Returns:
        Signed URL with token and expiration
    """
    if not settings.BUNNY_SIGNED_URL_KEY:
        # If no signing key, return plain URL
        return url
    
    if expiry_seconds is None:
        expiry_seconds = settings.BUNNY_SIGNED_URL_EXPIRY
    
    # Calculate expiration timestamp
    expires = int(time.time()) + expiry_seconds
    
    # Parse URL to get path
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path
    
    # Create signature: md5(key + path + expires)
    sign_string = f"{settings.BUNNY_SIGNED_URL_KEY}{path}{expires}"
    token = hashlib.md5(sign_string.encode()).hexdigest()
    
    # Append token and expiration to URL
    signed_url = f"{url}?token={token}&expires={expires}"
    
    return signed_url


def delete_from_bunny(remote_path: str) -> bool:
    """
    Delete file from BunnyCDN storage
    
    Args:
        remote_path: Remote path in storage zone
    
    Returns:
        True if successful
    """
    storage_url = f"https://{settings.BUNNY_REGION}/{settings.BUNNY_STORAGE_ZONE}/{remote_path}"
    
    headers = {
        "AccessKey": settings.BUNNY_ACCESS_KEY
    }
    
    response = requests.delete(storage_url, headers=headers, timeout=30)
    
    return response.status_code in [200, 204]


def download_from_bunny(remote_path: str, local_path: str) -> bool:
    """
    Download file from BunnyCDN storage to local path
    
    Args:
        remote_path: Remote path in storage zone (e.g., "temp/jobs/abc123/sketch.png")
        local_path: Local file path to save downloaded file
    
    Returns:
        True if successful
    """
    cdn_url = f"https://{settings.BUNNY_CDN_HOSTNAME}/{remote_path}"
    
    try:
        response = requests.get(cdn_url, timeout=300, stream=True)
        response.raise_for_status()
        
        # Ensure parent directory exists
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        from loguru import logger
        logger.error(f"Failed to download from BunnyCDN: {remote_path} -> {local_path}: {e}")
        return False


def upload_bytes_to_bunny(file_data: bytes, remote_path: str) -> str:
    """
    Upload file data (bytes) directly to BunnyCDN storage
    
    Args:
        file_data: File data as bytes
        remote_path: Remote path in storage zone (e.g., "temp/jobs/abc123/sketch.png")
    
    Returns:
        Public CDN URL
    """
    storage_url = f"https://{settings.BUNNY_REGION}/{settings.BUNNY_STORAGE_ZONE}/{remote_path}"
    
    headers = {
        "AccessKey": settings.BUNNY_ACCESS_KEY,
        "Content-Type": "application/octet-stream"
    }
    
    response = requests.put(
        storage_url,
        headers=headers,
        data=file_data,
        timeout=300
    )
    
    if response.status_code not in [200, 201]:
        raise Exception(f"BunnyCDN upload failed: {response.text}")
    
    # Return CDN URL
    cdn_url = f"https://{settings.BUNNY_CDN_HOSTNAME}/{remote_path}"
    return cdn_url


def generate_temp_path(job_id: str, filename: str) -> str:
    """
    Generate temporary storage path for processing files
    
    Args:
        job_id: Job UUID
        filename: Filename
    
    Returns:
        Remote path like "temp/jobs/abc123/sketch.png"
    """
    return f"temp/jobs/{job_id}/{filename}"


def upload_checkpoint(file_path: str, job_id: str, checkpoint_type: str) -> Optional[str]:
    """
    Upload intermediate file as checkpoint to BunnyCDN temp storage
    
    Args:
        file_path: Local file path to upload
        job_id: Job UUID
        checkpoint_type: Type of checkpoint (ifc, dwg, obj, rvt, preview)
    
    Returns:
        CDN URL or None if upload failed
    """
    from loguru import logger
    
    if not Path(file_path).exists():
        logger.warning(f"Checkpoint file does not exist: {file_path}")
        return None
    
    # Generate checkpoint filename
    checkpoint_filenames = {
        "ifc": "checkpoint_ifc.ifc",
        "dwg": "checkpoint_dwg.dwg",
        "obj": "checkpoint_obj.obj",
        "rvt": "checkpoint_rvt.rvt.ifc",
        "preview": "checkpoint_preview.png"
    }
    
    filename = checkpoint_filenames.get(checkpoint_type)
    if not filename:
        logger.warning(f"Unknown checkpoint type: {checkpoint_type}")
        return None
    
    remote_path = generate_temp_path(job_id, filename)
    
    try:
        cdn_url = upload_to_bunny(file_path, remote_path)
        logger.info(f"Checkpoint uploaded: {checkpoint_type} -> {cdn_url}")
        return cdn_url
    except Exception as e:
        logger.error(f"Failed to upload checkpoint {checkpoint_type}: {e}")
        return None


def get_checkpoint_remote_path(job_id: str, checkpoint_type: str) -> Optional[str]:
    """
    Get remote path for a checkpoint file
    
    Args:
        job_id: Job UUID
        checkpoint_type: Type of checkpoint (ifc, dwg, obj, rvt, preview)
    
    Returns:
        Remote path or None if invalid type
    """
    checkpoint_filenames = {
        "ifc": "checkpoint_ifc.ifc",
        "dwg": "checkpoint_dwg.dwg",
        "obj": "checkpoint_obj.obj",
        "rvt": "checkpoint_rvt.rvt.ifc",
        "preview": "checkpoint_preview.png"
    }
    
    filename = checkpoint_filenames.get(checkpoint_type)
    if not filename:
        return None
    
    return generate_temp_path(job_id, filename)


def download_checkpoint(job_id: str, checkpoint_type: str, local_path: str) -> bool:
    """
    Download checkpoint file from BunnyCDN
    
    Args:
        job_id: Job UUID
        checkpoint_type: Type of checkpoint (ifc, dwg, obj, rvt, preview)
        local_path: Local file path to save
    
    Returns:
        True if successful
    """
    remote_path = get_checkpoint_remote_path(job_id, checkpoint_type)
    if not remote_path:
        return False
    
    return download_from_bunny(remote_path, local_path)


# ============================================================================
# File Helpers
# ============================================================================

def generate_job_id() -> str:
    """Generate unique job ID"""
    return str(uuid.uuid4())


def get_file_extension(filename: str) -> str:
    """Get file extension without dot"""
    return Path(filename).suffix.lstrip('.').lower()


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    ext = get_file_extension(filename)
    return ext in settings.allowed_extensions_list


def generate_remote_path(job_id: str, filename: str) -> str:
    """
    Generate remote storage path for job files
    
    Args:
        job_id: Job UUID
        filename: Original filename
    
    Returns:
        Remote path like "jobs/2024/11/abc123/filename.ifc"
    """
    now = datetime.utcnow()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    
    return f"jobs/{year}/{month}/{job_id}/{filename}"


# ============================================================================
# Processing Helpers
# ============================================================================

# ============================================================================
# Rate Limiting
# ============================================================================

async def check_rate_limit(user_id: int, limit_per_minute: int = None, limit_per_hour: int = None) -> bool:
    """
    Check if user is within rate limit
    Uses Upstash Redis REST API for distributed rate limiting
    
    Args:
        user_id: User ID
        limit_per_minute: Rate limit per minute (default: settings)
        limit_per_hour: Rate limit per hour (default: settings)
    
    Returns:
        True if within limit
    """
    if limit_per_minute is None:
        limit_per_minute = settings.RATE_LIMIT_PER_MINUTE
    if limit_per_hour is None:
        limit_per_hour = settings.RATE_LIMIT_PER_HOUR
    
    try:
        # Use Upstash Redis REST API
        from ..services.redis_service import get_redis_service
        redis_service = get_redis_service()
        
        # Track Redis command usage
        from ..monitoring.redis_monitor import increment_redis_command_count
        
        minute_key = f"rate_limit:minute:{user_id}"
        hour_key = f"rate_limit:hour:{user_id}"
        
        minute_count = await redis_service.get(minute_key)
        increment_redis_command_count()  # Track GET command
        
        hour_count = await redis_service.get(hour_key)
        increment_redis_command_count()  # Track GET command
        
        # Minute window
        if minute_count is None:
            await redis_service.setex(minute_key, 60, "1")
            increment_redis_command_count()  # Track SETEX command
        else:
            if int(minute_count) >= limit_per_minute:
                return False
            await redis_service.incr(minute_key)
            increment_redis_command_count()  # Track INCR command
        
        # Hour window
        if hour_count is None:
            await redis_service.setex(hour_key, 3600, "1")
            increment_redis_command_count()  # Track SETEX command
        else:
            if int(hour_count) >= limit_per_hour:
                return False
            await redis_service.incr(hour_key)
            increment_redis_command_count()  # Track INCR command
        
        return True
    
    except Exception as e:
        from loguru import logger
        logger.warning(f"Rate limit check failed: {e}")
        return True  # Fail open


# ============================================================================
# Logging
# ============================================================================

def log_job_event(job_id: str, event: str, data: dict = None):
    """Log job event for monitoring"""
    from loguru import logger
    
    log_data = {
        "job_id": job_id,
        "event": event,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data:
        log_data.update(data)
    
    logger.info(f"Job event: {event}", **log_data)


# ============================================================================
# Import validation functions
# ============================================================================

from .validation import sanitize_filename, validate_upload_file
