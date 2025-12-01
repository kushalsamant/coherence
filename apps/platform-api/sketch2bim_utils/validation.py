"""
Enhanced validation utilities
Content-based file validation, input sanitization, and custom validators
"""
from typing import Optional, Tuple, List
from pathlib import Path
import magic
from PIL import Image
import re
from io import BytesIO

from ..exceptions import ValidationError
from loguru import logger


def validate_file_type(file_path: str, allowed_types: List[str]) -> bool:
    """
    Validate file type using magic number (content-based)
    More secure than extension checking
    
    Args:
        file_path: Path to file
        allowed_types: List of allowed MIME types (e.g., ['image/png', 'image/jpeg'])
    
    Returns:
        True if file type is allowed
    """
    try:
        mime = magic.Magic(mime=True)
        detected_type = mime.from_file(file_path)
        return detected_type in allowed_types
    except Exception as e:
        logger.warning(f"File type validation failed: {e}")
        # Fallback to extension check if magic fails
        return False


def validate_image_dimensions(
    file_path: str,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    min_width: Optional[int] = None,
    min_height: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate image dimensions
    
    Args:
        file_path: Path to image file
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        min_width: Minimum width in pixels
        min_height: Minimum height in pixels
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            
            if max_width and width > max_width:
                return False, f"Image width {width}px exceeds maximum {max_width}px"
            if max_height and height > max_height:
                return False, f"Image height {height}px exceeds maximum {max_height}px"
            if min_width and width < min_width:
                return False, f"Image width {width}px is below minimum {min_width}px"
            if min_height and height < min_height:
                return False, f"Image height {height}px is below minimum {min_height}px"
            
            return True, None
    except Exception as e:
        return False, f"Failed to read image: {str(e)}"


def validate_file_size(file_path: str, max_size_bytes: int) -> Tuple[bool, Optional[str]]:
    """
    Validate file size
    
    Args:
        file_path: Path to file
        max_size_bytes: Maximum file size in bytes
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        size = Path(file_path).stat().st_size
        if size > max_size_bytes:
            return False, f"File size {size} bytes exceeds maximum {max_size_bytes} bytes"
        return True, None
    except Exception as e:
        return False, f"Failed to check file size: {str(e)}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other attacks
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Remove dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename or "file"


def sanitize_string(input_str: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input
    
    Args:
        input_str: Input string
        max_length: Maximum length
    
    Returns:
        Sanitized string
    """
    # Remove null bytes
    input_str = input_str.replace('\x00', '')
    
    # Strip whitespace
    input_str = input_str.strip()
    
    # Limit length
    if max_length and len(input_str) > max_length:
        input_str = input_str[:max_length]
    
    return input_str


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address
    
    Returns:
        True if valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_job_id(job_id: str) -> bool:
    """
    Validate job ID format (UUID)
    
    Args:
        job_id: Job ID
    
    Returns:
        True if valid UUID format
    """
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, job_id.lower()))


def validate_upload_file(
    file_path: str,
    allowed_extensions: List[str],
    max_size_bytes: int,
    allowed_mime_types: Optional[List[str]] = None,
    is_image: bool = False,
    image_max_dimensions: Optional[Tuple[int, int]] = None
) -> Tuple[bool, Optional[str]]:
    """
    Comprehensive file validation
    
    Args:
        file_path: Path to uploaded file
        allowed_extensions: List of allowed file extensions
        max_size_bytes: Maximum file size
        allowed_mime_types: Optional list of allowed MIME types
        is_image: Whether file should be an image
        image_max_dimensions: Optional (max_width, max_height) for images
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file exists
    if not Path(file_path).exists():
        return False, "File does not exist"
    
    # Check extension
    ext = Path(file_path).suffix.lstrip('.').lower()
    if ext not in [e.lower() for e in allowed_extensions]:
        return False, f"File extension .{ext} not allowed. Allowed: {', '.join(allowed_extensions)}"
    
    # Check file size
    is_valid, error = validate_file_size(file_path, max_size_bytes)
    if not is_valid:
        return False, error
    
    # Check MIME type if provided
    if allowed_mime_types:
        try:
            if not validate_file_type(file_path, allowed_mime_types):
                return False, "File type validation failed (content-based check)"
        except Exception as e:
            logger.warning(f"MIME type validation failed: {e}")
            # Continue if magic library not available
    
    # Image-specific validation
    if is_image:
        is_valid, error = validate_image_dimensions(
            file_path,
            max_width=image_max_dimensions[0] if image_max_dimensions else None,
            max_height=image_max_dimensions[1] if image_max_dimensions else None
        )
        if not is_valid:
            return False, error
    
    return True, None

