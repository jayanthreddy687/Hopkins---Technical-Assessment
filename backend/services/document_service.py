"""Service for document processing and text extraction."""

import os
from typing import Optional
from docx import Document
import pandas as pd
from pypdf import PdfReader

from core.logging import get_logger
from core.constants import DocumentCategory, CATEGORY_KEYWORDS
from core.exceptions import DocumentProcessingError
from config import settings

logger = get_logger(__name__)


class DocumentService:
    """
    Service for extracting and processing document content.
    
    Handles various document formats (TXT, CSV, XLSX, DOCX) and
    provides categorization based on content analysis.
    """
    
    def __init__(self):
        """Initialize document service with category keywords."""
        self.keywords = CATEGORY_KEYWORDS
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from various document formats.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content or None if extraction fails
            
        Raises:
            DocumentProcessingError: If document processing fails
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            filename = os.path.basename(file_path)
            
            logger.debug(f"Extracting text from {filename} (type: {file_ext})")
            
            # Route to appropriate extraction method
            extractors = {
                '.txt': self._extract_txt_text,
                '.csv': self._extract_csv_text,
                '.xlsx': self._extract_excel_text,
                '.xls': self._extract_excel_text,
                '.docx': self._extract_docx_text,
                '.pdf': self._extract_pdf_text
            }
            
            extractor = extractors.get(file_ext)
            if not extractor:
                logger.warning(f"No extractor found for {file_ext}")
                return None
            
            text = extractor(file_path)
            
            if text:
                logger.info(
                    f"Successfully extracted {len(text)} characters from {filename}"
                )
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise DocumentProcessingError(
                filename=os.path.basename(file_path),
                reason=str(e)
            )
    
    def _extract_txt_text(self, file_path: str) -> str:
        """
        Extract text from TXT files.
        
        Args:
            file_path: Path to the TXT file
            
        Returns:
            Extracted text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding
            logger.warning(f"UTF-8 decode failed, trying latin-1: {file_path}")
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    def _extract_docx_text(self, file_path: str) -> str:
        """
        Extract text from DOCX files.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Extracted text content
        """
        doc = Document(file_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """
        Extract text from PDF files.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            return '\n'.join(text_parts)
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {str(e)}")
            return ""
    
    def _extract_excel_text(self, file_path: str) -> str:
        """
        Extract text from Excel files.
        
        Reads the first sheet and limits rows for performance.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Extracted text content as formatted string
        """
        try:
            df = pd.read_excel(file_path, nrows=settings.max_excel_rows)
            return self._dataframe_to_text(df)
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {str(e)}")
            return ""
    
    def _extract_csv_text(self, file_path: str) -> str:
        """
        Extract text from CSV files.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Extracted text content as formatted string
        """
        try:
            df = pd.read_csv(file_path, nrows=settings.max_csv_rows)
            return self._dataframe_to_text(df)
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            return ""
    
    def _dataframe_to_text(self, df: pd.DataFrame) -> str:
        """
        Convert DataFrame to text representation.
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Text representation of the DataFrame
        """
        text_parts = []
        
        for column in df.columns:
            values = df[column].dropna().astype(str).tolist()
            limited_values = values[:settings.max_column_values]
            text_parts.append(f"{column}: {', '.join(limited_values)}")
        
        return '\n'.join(text_parts)
    
    def categorize_document(self, filename: str, text: str) -> DocumentCategory:
        """
        Categorize document based on filename and content.
        
        Uses keyword matching to determine the most likely category.
        
        Args:
            filename: Name of the document
            text: Document content
            
        Returns:
            Document category
        """
        # Analyze first 300 characters
        sample_text = text[:300].lower()
        filename_lower = filename.lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.keywords.items():
            score = 0
            for keyword in keywords:
                # Score both content and filename matches
                score += sample_text.count(keyword)
                score += filename_lower.count(keyword) * 2  # Weight filename higher
            
            category_scores[category] = score
        
        # Return category with highest score
        if category_scores and max(category_scores.values()) > 0:
            best_category = max(category_scores, key=category_scores.get)
            logger.debug(
                f"Categorized '{filename}' as {best_category} "
                f"(score: {category_scores[best_category]})"
            )
            return DocumentCategory(best_category)
        
        logger.debug(f"No category match for '{filename}', using OTHER")
        return DocumentCategory.OTHER

