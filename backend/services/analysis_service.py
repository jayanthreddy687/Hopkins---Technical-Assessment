"""Service for orchestrating document analysis workflow."""

import os
from typing import List, Optional
from pathlib import Path

from core.logging import get_logger
from core.constants import DocumentCategory
from models.schemas import (
    DocumentAnalysis,
    AggregateCounts,
    CategoryCounts,
    AnalysisResponse
)
from services.document_service import DocumentService
from services.llm_service import LLMService
from utils.file_utils import is_allowed_file
from utils.text_utils import truncate_text
from config import settings

logger = get_logger(__name__)


class AnalysisService:
    """
    Service for orchestrating the complete document analysis workflow.
    
    Coordinates document extraction, categorization, LLM analysis,
    and result aggregation.
    """
    
    def __init__(
        self,
        document_service: DocumentService,
        llm_service: LLMService
    ):
        """
        Initialize analysis service with dependencies.
        
        Args:
            document_service: Service for document processing
            llm_service: Service for LLM analysis
        """
        self.document_service = document_service
        self.llm_service = llm_service
    
    async def analyze_directory(
        self,
        directory_path: str
    ) -> AnalysisResponse:
        """
        Analyze all documents in a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            Complete analysis response with all results
        """
        logger.info(f"Starting analysis of directory: {directory_path}")
        
        # Initialize results
        documents = []
        errors = []
        aggregate = AggregateCounts()
        
        # Get all files
        file_paths = self._get_processable_files(directory_path)
        total_files = len(file_paths)
        
        logger.info(f"Found {total_files} processable files")
        
        # Process each file
        for idx, file_path in enumerate(file_paths, 1):
            filename = os.path.basename(file_path)
            logger.info(f"Analysing {idx} of {total_files}: {filename}")
            
            try:
                # Process single document
                analysis = await self._process_document(file_path)
                
                if analysis:
                    documents.append(analysis)
                    self._update_aggregate(aggregate, analysis)
                else:
                    errors.append(f"Failed to analyze: {filename}")
                    
            except Exception as e:
                error_msg = f"Error processing {filename}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
        
        # Generate executive summary
        logger.info("Generating executive summary")
        summary_text = await self.llm_service.generate_summary(
            [doc.dict() for doc in documents]
        )
        
        logger.info(
            f"Analysis complete: {len(documents)} documents processed, "
            f"{len(errors)} errors"
        )
        
        return AnalysisResponse(
            docs=documents,
            aggregate=aggregate,
            summaryText=summary_text,
            errors=errors
        )
    
    async def _process_document(
        self,
        file_path: str
    ) -> Optional[DocumentAnalysis]:
        """
        Process a single document through the analysis pipeline.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Document analysis result or None if processing fails
        """
        filename = os.path.basename(file_path)
        
        # Extract text
        text = self.document_service.extract_text(file_path)
        if not text:
            logger.warning(f"Could not extract text from: {filename}")
            return None
        
        logger.debug(f"Extracted {len(text)} characters from {filename}")
        
        # Truncate text
        text = truncate_text(text)
        
        # Categorize document
        category = self.document_service.categorize_document(filename, text)
        logger.debug(f"Categorized {filename} as: {category.value}")
        
        # Analyze with LLM
        analysis_dict = await self.llm_service.analyze_document(
            filename,
            category,
            text
        )
        
        if not analysis_dict:
            logger.warning(f"LLM analysis failed for: {filename}")
            return None
        
        # Convert to Pydantic model
        try:
            return DocumentAnalysis(**analysis_dict)
        except Exception as e:
            logger.error(f"Failed to create DocumentAnalysis for {filename}: {e}")
            return None
    
    def _get_processable_files(self, directory_path: str) -> List[str]:
        """
        Get list of files that can be processed.
        
        Args:
            directory_path: Directory to search
            
        Returns:
            List of file paths
        """
        file_paths = []
        
        for root, _, files in os.walk(directory_path):
            for filename in files:
                if is_allowed_file(filename):
                    file_path = os.path.join(root, filename)
                    file_paths.append(file_path)
                else:
                    logger.debug(f"Skipping file: {filename}")
        
        return file_paths
    
    def _update_aggregate(
        self,
        aggregate: AggregateCounts,
        analysis: DocumentAnalysis
    ) -> None:
        """
        Update aggregate counts with a document's analysis.
        
        Args:
            aggregate: Aggregate counts object to update
            analysis: Document analysis to aggregate
        """
        # Category is already a string due to use_enum_values = True in schema
        category = analysis.category if isinstance(analysis.category, str) else analysis.category.value
        category_counts = getattr(aggregate, category, None)
        
        if category_counts:
            category_counts.facts += len(analysis.facts)
            category_counts.red_flags += len(analysis.red_flags)

