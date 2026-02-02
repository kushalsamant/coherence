"""
FastAPI application factory
Creates FastAPI apps with standard configuration
"""
from fastapi import FastAPI
from typing import List, Optional, Callable, Any
from contextlib import asynccontextmanager
from .middleware import setup_cors_middleware, setup_standard_error_handlers


def create_app(
    app_name: str,
    version: str = "1.0.0",
    description: Optional[str] = None,
    cors_origins: Optional[List[str]] = None,
    lifespan: Optional[Callable] = None,
    enable_docs: bool = True,
    enable_error_handlers: bool = True,
    include_correlation: bool = False,
    debug: bool = False,
    **fastapi_kwargs
) -> FastAPI:
    """
    Create a FastAPI application with standard configuration
    
    Args:
        app_name: Name of the application
        version: API version
        description: API description
        cors_origins: List of allowed CORS origins (defaults to empty list)
        lifespan: Optional lifespan context manager for startup/shutdown
        enable_docs: Whether to enable OpenAPI docs (disabled in production by default)
        enable_error_handlers: Whether to enable standard error handlers
        include_correlation: Whether to include correlation IDs in error responses
        debug: Whether to include debug information in errors
        **fastapi_kwargs: Additional arguments to pass to FastAPI constructor
    
    Returns:
        Configured FastAPI application instance
    """
    # Build FastAPI constructor arguments
    app_kwargs = {
        "title": app_name,
        "version": version,
        **fastapi_kwargs
    }
    
    if description:
        app_kwargs["description"] = description
    
    if lifespan:
        app_kwargs["lifespan"] = lifespan
    
    # Conditionally enable docs based on debug mode
    if not enable_docs or not debug:
        app_kwargs["docs_url"] = None
        app_kwargs["redoc_url"] = None
    elif enable_docs and debug:
        app_kwargs["docs_url"] = "/docs"
        app_kwargs["redoc_url"] = "/redoc"
    
    # Create app
    app = FastAPI(**app_kwargs)
    
    # Setup CORS
    if cors_origins is None:
        cors_origins = []
    setup_cors_middleware(app, cors_origins=cors_origins)
    
    # Setup error handlers
    if enable_error_handlers:
        setup_standard_error_handlers(
            app,
            include_correlation=include_correlation,
            debug=debug
        )
    
    # Add standard health check endpoints
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {"message": app_name, "version": version}
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "service": app_name,
                "version": version,
            },
        )
    
    return app

