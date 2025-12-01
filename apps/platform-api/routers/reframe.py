"""
Reframe App Router
Routes for Reframe text rewriting application
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Import Reframe route module
from routers.reframe import reframe as reframe_routes

router = APIRouter()


@router.get("/health")
async def health_check():
    """Reframe app health check"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "app": "reframe"}
    )


# Include Reframe routes
router.include_router(reframe_routes.router, prefix="/reframe")

