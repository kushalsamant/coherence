"""
FastAPI Backend Server for {{APP_DISPLAY_NAME}}
{{APP_DESCRIPTION}}
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

from .config import settings
from .database import init_db
from .routes import example  # Import your routes here
# from .routes import payments, users, etc.

from shared_backend.api.factory import create_app
from shared_backend.api.middleware import setup_cors_middleware, setup_standard_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} Backend")
    logger.info(f"Environment: {settings.APP_ENV}")
    
    # Initialize database
    try:
        init_db()
        logger.success("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Continue startup even if DB init fails (for development)
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME} Backend")


# Create FastAPI app using factory
app = create_app(
    app_name=settings.APP_NAME,
    version="1.0.0",
    description="{{APP_DESCRIPTION}}",
    cors_origins=settings.cors_origins_list,
    lifespan=lifespan,
    enable_docs=settings.DEBUG,
    enable_error_handlers=True,
    debug=settings.DEBUG,
)

# Include routers
app.include_router(example.router, prefix="/api", tags=["example"])

# Add more routes here:
# app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)

