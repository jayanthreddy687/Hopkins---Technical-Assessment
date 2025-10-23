"""Application configuration and settings management."""

import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    app_name: str = "VDR Lite + LLM"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Settings
    cors_origins: List[str] = [
        "http://localhost:8080",
        "http://localhost:5173"
    ]
    
    # LLM Configuration
    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        "AIzaSyDiiZwmkPg_rzRJUneZb13JFUzIt2gEK-0"
    )
    gemini_model: str = "gemini-2.5-flash-lite"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 700
    llm_summary_max_tokens: int = 500  # As per instructions: ~500 for final narrative
    llm_retry_attempts: int = 2
    
    # Document Processing Configuration
    max_text_length: int = 15000
    max_excel_rows: int = 200
    max_csv_rows: int = 200
    max_column_values: int = 10
    
    # File Processing Configuration
    allowed_extensions: List[str] = [".txt", ".csv", ".xlsx", ".xls", ".docx"]
    excluded_extensions: List[str] = [".json", ".pdf"]
    max_file_size_mb: int = 100
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


settings = get_settings()

