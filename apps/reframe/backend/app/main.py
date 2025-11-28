"""
FastAPI Backend Server for Reframe
Provides REST API endpoint for text reframing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import get_settings
from .routes import reframe

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for AI-powered text reframing with multiple human tones",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reframe.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": settings.APP_NAME, "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": "1.0.0"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

