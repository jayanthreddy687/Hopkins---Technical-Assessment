"""Pydantic schemas for request/response validation."""

from typing import List, Dict
from pydantic import BaseModel, Field

from core.constants import DocumentCategory


class CategoryCounts(BaseModel):
    """Counts for facts and red flags in a category."""
    
    facts: int = Field(default=0, ge=0, description="Number of key facts")
    red_flags: int = Field(default=0, ge=0, alias="red_flags", description="Number of red flags")
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True


class AggregateCounts(BaseModel):
    """Aggregated counts across all categories."""
    
    financial: CategoryCounts = Field(default_factory=CategoryCounts)
    legal: CategoryCounts = Field(default_factory=CategoryCounts)
    operations: CategoryCounts = Field(default_factory=CategoryCounts)
    commercial: CategoryCounts = Field(default_factory=CategoryCounts)
    other: CategoryCounts = Field(default_factory=CategoryCounts)


class DocumentAnalysis(BaseModel):
    """Analysis result for a single document."""
    
    doc: str = Field(..., description="Document filename")
    category: DocumentCategory = Field(..., description="Document category")
    facts: List[str] = Field(default_factory=list, description="Key facts extracted")
    red_flags: List[str] = Field(
        default_factory=list,
        alias="red_flags",
        description="Red flags identified"
    )
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True
        use_enum_values = True


class AnalysisResponse(BaseModel):
    """Response model for document analysis."""
    
    docs: List[DocumentAnalysis] = Field(
        default_factory=list,
        description="List of analyzed documents"
    )
    aggregate: AggregateCounts = Field(
        default_factory=AggregateCounts,
        description="Aggregated counts"
    )
    summary_text: str = Field(
        alias="summaryText",
        default="",
        description="Executive summary"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="Processing errors"
    )
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str = Field(..., description="Error message")
    details: str = Field(default="", description="Detailed error information")
    error_code: str = Field(default="", description="Error code")

