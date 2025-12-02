"""
ASK App Router
Routes for ASK: Daily Research application
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Import all ASK route modules
from . import qa_pairs, themes, stats, generate, payments, monitoring, feasibility

router = APIRouter()


@router.get("/health")
async def health_check():
    """ASK app health check"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "app": "ask"}
    )


# Include all ASK route routers
router.include_router(qa_pairs.router)
router.include_router(themes.router)
router.include_router(stats.router)
router.include_router(generate.router)
router.include_router(payments.router)
router.include_router(monitoring.router)
router.include_router(feasibility.router)
