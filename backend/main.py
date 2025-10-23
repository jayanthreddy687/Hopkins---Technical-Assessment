"""
Main application entry point for VDR Lite + LLM.

This application provides API endpoints for analyzing due diligence documents
using AI-powered analysis with Google's Gemini LLM.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from core.logging import setup_logging, get_logger
from api.routes import router

# Configure application logging
setup_logging(level="INFO" if not settings.debug else "DEBUG")
logger = get_logger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered virtual data room document analysis",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

logger.info(
    f"{settings.app_name} v{settings.app_version} initialized successfully"
)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Application starting up...")
    logger.info(f"CORS origins: {settings.cors_origins}")
    logger.info(f"LLM Model: {settings.gemini_model}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(
        f"Starting server on {settings.host}:{settings.port}"
    )
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info" if not settings.debug else "debug"
    )
