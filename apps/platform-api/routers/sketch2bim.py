"""
Sketch2BIM App Router
Routes for Sketch-to-BIM conversion application
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Import Sketch2BIM route modules
from routers.sketch2bim import (
    admin, auth, extraction, generate, iterations, 
    logs, monitoring, payments, referrals, variations
)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Sketch2BIM app health check"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "app": "sketch2bim"}
    )


# Include all Sketch2BIM route routers
router.include_router(auth.router)
router.include_router(generate.router)
router.include_router(extraction.router)
router.include_router(iterations.router)
router.include_router(variations.router)
router.include_router(payments.router)
router.include_router(referrals.router)
router.include_router(monitoring.router)
router.include_router(admin.router)
router.include_router(logs.router)

