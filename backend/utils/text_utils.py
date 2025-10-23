"""Text processing utility functions."""

import re
from typing import Optional

from config import settings


def truncate_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (defaults to settings value)
        
    Returns:
        Truncated text
    """
    if max_length is None:
        max_length = settings.max_text_length
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length]


def clean_json_response(content: str) -> str:
    """
    Clean JSON response by removing markdown code blocks.
    
    Args:
        content: Raw response content
        
    Returns:
        Cleaned JSON string
    """
    content = content.strip()
    
    # Remove markdown code block markers
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    
    if content.endswith("```"):
        content = content[:-3]
    
    return content.strip()


def extract_json_from_markdown(content: str) -> Optional[str]:
    """
    Extract JSON from markdown code blocks.
    
    Args:
        content: Content that may contain JSON in markdown
        
    Returns:
        Extracted JSON string or None
    """
    # Try to find JSON in code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, content, re.DOTALL)
    
    if match:
        return match.group(1)
    
    # If no code block, try to find raw JSON
    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, content, re.DOTALL)
    
    if match:
        return match.group(0)
    
    return None

