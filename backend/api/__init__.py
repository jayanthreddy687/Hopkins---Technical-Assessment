"""API module for route definitions and dependencies."""

from .dependencies import get_document_service, get_llm_service, get_analysis_service, get_export_service
from .routes import router

__all__ = [
    "router",
    "get_document_service",
    "get_llm_service",
    "get_analysis_service",
    "get_export_service"
]

