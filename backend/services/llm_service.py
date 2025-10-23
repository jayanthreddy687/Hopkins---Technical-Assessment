"""Service for LLM-based document analysis."""

import json
from typing import Optional, Dict, Any, List
import google.generativeai as genai

from core.logging import get_logger
from core.constants import (
    DocumentCategory,
    DOCUMENT_ANALYSIS_PROMPT_TEMPLATE,
    SUMMARY_GENERATION_PROMPT_TEMPLATE,
    RETRY_ANALYSIS_PROMPT_TEMPLATE
)
from core.exceptions import LLMAnalysisError
from config import settings
from utils.text_utils import clean_json_response

logger = get_logger(__name__)


class LLMService:
    """
    Service for LLM-powered document analysis and summarization.
    
    Uses Google's Gemini API for natural language understanding
    and structured data extraction.
    """
    
    def __init__(self):
        """Initialize LLM service with Gemini configuration."""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.generation_config = genai.types.GenerationConfig(
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_tokens,
        )
        logger.info(f"LLMService initialized with model: {settings.gemini_model}")
    
    async def analyze_document(
        self,
        filename: str,
        category: DocumentCategory,
        text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze a single document using LLM.
        
        Extracts key facts and identifies red flags from the document.
        
        Args:
            filename: Name of the document
            category: Categorized document type
            text: Document content
            
        Returns:
            Analysis result dictionary or None if analysis fails
        """
        logger.info(f"Starting LLM analysis for '{filename}' (category: {category})")
        
        try:
            # Generate prompt from template
            prompt = DOCUMENT_ANALYSIS_PROMPT_TEMPLATE.format(
                filename=filename,
                category=category.value,
                text=text
            )
            
            # Call LLM API
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Parse and validate response
            result = self._parse_analysis_response(response.text, filename)
            
            if result:
                logger.info(
                    f"Analysis complete for '{filename}': "
                    f"{len(result.get('facts', []))} facts, "
                    f"{len(result.get('red_flags', []))} red flags"
                )
                return result
            
            # Retry if initial parsing failed
            logger.warning(f"Initial analysis failed for '{filename}', retrying...")
            return await self._retry_analysis(filename, category, text)
            
        except Exception as e:
            logger.error(f"Error analyzing '{filename}': {str(e)}", exc_info=True)
            self._log_api_errors(e)
            return None
    
    def _parse_analysis_response(
        self,
        response_text: str,
        filename: str
    ) -> Optional[Dict[str, Any]]:
        """
        Parse and validate LLM analysis response.
        
        Args:
            response_text: Raw response from LLM
            filename: Document filename for logging
            
        Returns:
            Parsed analysis dictionary or None if invalid
        """
        try:
            # Clean response text
            content = clean_json_response(response_text)
            
            # Parse JSON
            result = json.loads(content)
            
            # Validate required fields
            required_fields = ["doc", "category", "facts", "red_flags"]
            if all(field in result for field in required_fields):
                return result
            
            logger.warning(
                f"Invalid response structure for '{filename}': "
                f"missing required fields"
            )
            return None
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error for '{filename}': {str(e)}")
            logger.debug(f"Failed content: {response_text[:200]}")
            return None
    
    async def _retry_analysis(
        self,
        filename: str,
        category: DocumentCategory,
        text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retry document analysis with more specific instructions.
        
        Args:
            filename: Name of the document
            category: Document category
            text: Document content (truncated for retry)
            
        Returns:
            Analysis result dictionary or None if retry fails
        """
        logger.info(f"Retry attempt for '{filename}'")
        
        try:
            # Use truncated text for retry to avoid token limits
            truncated_text = text[:1000]
            
            # Generate retry prompt
            prompt = RETRY_ANALYSIS_PROMPT_TEMPLATE.format(
                filename=filename,
                category=category.value,
                text=truncated_text
            )
            
            # Shorter token limit for retry
            retry_config = genai.types.GenerationConfig(
                temperature=0,
                max_output_tokens=500,
            )
            
            response = self.model.generate_content(prompt, generation_config=retry_config)
            result = self._parse_analysis_response(response.text, filename)
            
            if result:
                logger.info(f"Retry successful for '{filename}'")
                return result
            
            logger.error(f"Retry failed for '{filename}': invalid response")
            return None
            
        except Exception as e:
            logger.error(f"Retry exception for '{filename}': {str(e)}", exc_info=True)
            return None
    
    async def generate_summary(self, analyses: List[Dict[str, Any]]) -> str:
        """
        Generate executive summary from document analyses.
        
        Args:
            analyses: List of document analysis results
            
        Returns:
            Executive summary text
        """
        logger.info(f"Generating executive summary from {len(analyses)} documents")
        
        try:
            # Prepare analyses as JSON
            analyses_json = json.dumps(analyses, indent=2)
            
            # Generate prompt
            prompt = SUMMARY_GENERATION_PROMPT_TEMPLATE.format(
                analysis_json=analyses_json
            )
            
            # Use separate config for summary generation (500 tokens as per instructions)
            summary_config = genai.types.GenerationConfig(
                temperature=settings.llm_temperature,
                max_output_tokens=settings.llm_summary_max_tokens,
            )
            
            # Call LLM
            response = self.model.generate_content(
                prompt,
                generation_config=summary_config
            )
            
            summary = response.text.strip()
            logger.info(f"Executive summary generated ({len(summary)} characters)")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}", exc_info=True)
            self._log_api_errors(e)
            return "Summary generation failed. Please review individual document analyses."
    
    def _log_api_errors(self, error: Exception) -> None:
        """
        Log specific API errors with helpful messages.
        
        Args:
            error: Exception from API call
        """
        error_msg = str(error).lower()
        
        if "quota" in error_msg or "rate limit" in error_msg:
            logger.error(
                "⚠️  API QUOTA EXCEEDED - Check your Gemini API quota and billing"
            )
        elif "api key" in error_msg or "authentication" in error_msg:
            logger.error(
                "⚠️  API KEY ERROR - Check your GEMINI_API_KEY environment variable"
            )
        elif "invalid" in error_msg:
            logger.error(
                "⚠️  INVALID REQUEST - Check API parameters and model availability"
            )

