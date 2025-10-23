"""Core module for exceptions, constants, and utilities."""

from .exceptions import (
    VDRException,
    DocumentProcessingError,
    LLMAnalysisError,
    FileValidationError
)
from .constants import (
    DocumentCategory,
    AnalysisStatus,
    CATEGORY_KEYWORDS
)

__all__ = [
    "VDRException",
    "DocumentProcessingError",
    "LLMAnalysisError",
    "FileValidationError",
    "DocumentCategory",
    "AnalysisStatus",
    "CATEGORY_KEYWORDS"
]

