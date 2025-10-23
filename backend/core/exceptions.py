"""Custom exceptions for the VDR application."""

from typing import Optional


class VDRException(Exception):
    """Base exception for VDR application."""
    
    def __init__(
        self,
        message: str,
        details: Optional[str] = None,
        error_code: Optional[str] = None
    ):
        """
        Initialize VDR exception.
        
        Args:
            message: Human-readable error message
            details: Additional error details
            error_code: Unique error code for tracking
        """
        self.message = message
        self.details = details
        self.error_code = error_code
        super().__init__(self.message)


class DocumentProcessingError(VDRException):
    """Raised when document processing fails."""
    
    def __init__(self, filename: str, reason: str):
        """
        Initialize document processing error.
        
        Args:
            filename: Name of the file that failed processing
            reason: Reason for failure
        """
        message = f"Failed to process document: {filename}"
        super().__init__(message, details=reason, error_code="DOC_PROCESS_ERROR")
        self.filename = filename


class LLMAnalysisError(VDRException):
    """Raised when LLM analysis fails."""
    
    def __init__(self, filename: str, reason: str):
        """
        Initialize LLM analysis error.
        
        Args:
            filename: Name of the file that failed analysis
            reason: Reason for failure
        """
        message = f"Failed to analyze document with LLM: {filename}"
        super().__init__(message, details=reason, error_code="LLM_ANALYSIS_ERROR")
        self.filename = filename


class FileValidationError(VDRException):
    """Raised when file validation fails."""
    
    def __init__(self, filename: str, reason: str):
        """
        Initialize file validation error.
        
        Args:
            filename: Name of the invalid file
            reason: Reason for validation failure
        """
        message = f"File validation failed: {filename}"
        super().__init__(message, details=reason, error_code="FILE_VALIDATION_ERROR")
        self.filename = filename

