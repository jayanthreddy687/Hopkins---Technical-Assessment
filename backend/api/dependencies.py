"""Dependency injection for FastAPI routes."""

from functools import lru_cache

from services import (
    DocumentService,
    LLMService,
    AnalysisService,
    ExportService
)


@lru_cache()
def get_document_service() -> DocumentService:
    """
    Get or create DocumentService instance.
    
    Returns:
        DocumentService instance
    """
    return DocumentService()


@lru_cache()
def get_llm_service() -> LLMService:
    """
    Get or create LLMService instance.
    
    Returns:
        LLMService instance
    """
    return LLMService()


@lru_cache()
def get_analysis_service() -> AnalysisService:
    """
    Get or create AnalysisService instance with dependencies.
    
    Returns:
        AnalysisService instance
    """
    document_service = get_document_service()
    llm_service = get_llm_service()
    return AnalysisService(document_service, llm_service)


@lru_cache()
def get_export_service() -> ExportService:
    """
    Get or create ExportService instance.
    
    Returns:
        ExportService instance
    """
    return ExportService()

