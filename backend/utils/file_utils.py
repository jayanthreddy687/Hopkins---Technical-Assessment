"""File handling utility functions."""

import os
import zipfile
from typing import List
from pathlib import Path

from core.exceptions import FileValidationError
from core.logging import get_logger
from config import settings

logger = get_logger(__name__)


def get_file_extension(filename: str) -> str:
    """
    Get file extension in lowercase.
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension (including the dot)
    """
    return os.path.splitext(filename)[1].lower()


def is_allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed for processing.
    
    Args:
        filename: Name of the file
        
    Returns:
        True if file is allowed, False otherwise
    """
    ext = get_file_extension(filename)
    
    # Skip explicitly excluded extensions
    if ext in settings.excluded_extensions:
        return False
    
    # Allow explicitly allowed extensions
    if ext in settings.allowed_extensions:
        return True
    
    return False


def validate_zip_file(file_path: str) -> bool:
    """
    Validate that a file is a valid ZIP archive.
    
    Args:
        file_path: Path to the ZIP file
        
    Returns:
        True if valid ZIP file
        
    Raises:
        FileValidationError: If file is not a valid ZIP
    """
    if not os.path.exists(file_path):
        raise FileValidationError(
            filename=file_path,
            reason="File does not exist"
        )
    
    if not zipfile.is_zipfile(file_path):
        raise FileValidationError(
            filename=file_path,
            reason="File is not a valid ZIP archive"
        )
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Test ZIP integrity
            zip_ref.testzip()
        return True
    except zipfile.BadZipFile as e:
        raise FileValidationError(
            filename=file_path,
            reason=f"Corrupted ZIP file: {str(e)}"
        )


def extract_zip_file(zip_path: str, extract_dir: str) -> List[str]:
    """
    Extract ZIP file and return list of extracted file paths.
    
    Args:
        zip_path: Path to the ZIP file
        extract_dir: Directory to extract files to
        
    Returns:
        List of extracted file paths
        
    Raises:
        FileValidationError: If extraction fails
    """
    try:
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            extracted_files = zip_ref.namelist()
            
        logger.info(f"Extracted {len(extracted_files)} files from ZIP")
        
        # Return full paths
        return [
            os.path.join(extract_dir, filename)
            for filename in extracted_files
            if os.path.isfile(os.path.join(extract_dir, filename))
        ]
        
    except Exception as e:
        raise FileValidationError(
            filename=zip_path,
            reason=f"Failed to extract ZIP: {str(e)}"
        )


def get_all_files_in_directory(directory: str) -> List[str]:
    """
    Recursively get all files in a directory.
    
    Args:
        directory: Root directory to search
        
    Returns:
        List of file paths
    """
    file_paths = []
    
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    
    return file_paths

