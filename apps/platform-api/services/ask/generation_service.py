"""
Generation Service for triggering content generation
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent.parent
MAIN_SCRIPT = BASE_DIR / "main.py"
MAIN_TEXT_ONLY_SCRIPT = BASE_DIR / "main_text_only.py"


def trigger_generation(theme: Optional[str] = None, text_only: bool = False) -> dict:
    """
    Trigger content generation by calling the Python script
    
    Args:
        theme: Optional theme to generate for
        text_only: Whether to use text-only mode
        
    Returns:
        Dictionary with success status and message
    """
    try:
        script = MAIN_TEXT_ONLY_SCRIPT if text_only else MAIN_SCRIPT
        
        if not script.exists():
            return {
                "success": False,
                "message": f"Generation script not found: {script}"
            }
        
        # Build command
        cmd = ["python", str(script)]
        
        # Run the script
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Content generation completed successfully",
                "output": result.stdout
            }
        else:
            return {
                "success": False,
                "message": "Content generation failed",
                "error": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Content generation timed out"
        }
    except Exception as e:
        log.error(f"Error triggering generation: {e}")
        return {
            "success": False,
            "message": f"Error triggering generation: {str(e)}"
        }

