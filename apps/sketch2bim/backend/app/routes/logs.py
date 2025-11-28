from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

router = APIRouter(prefix="/logs", tags=["logs"])


class ClientErrorPayload(BaseModel):
    message: str
    stack: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


@router.post("/client-error", status_code=status.HTTP_204_NO_CONTENT)
async def capture_client_error(payload: ClientErrorPayload):
    """
    Capture client-side errors reported from the frontend.
    """
    logger.error(
        "Client error reported: {message}",
        message=payload.message,
        stack=payload.stack,
        context=payload.context,
        timestamp=payload.timestamp,
    )
    return None

