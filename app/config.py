"""
Configuration Management for Smart Resume Screener
Loads environment variables and provides centralized configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application Settings"""
    
    # MongoDB Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "resume_screener"
    
    # Google Gemini API
    gemini_api_key: str
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000"
    
    # File Upload Settings
    max_file_size_mb: int = 10
    allowed_extensions: str = "pdf,docx,txt"
    
    # LLM Settings
    llm_model: str = "gemini-2.5-flash"  # Using stable Gemini 2.5 Flash model
    llm_temperature: float = 0.3
    max_tokens: int = 2048
    
    # Computed Properties
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert comma-separated extensions to list"""
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes"""
        return self.max_file_size_mb * 1024 * 1024
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure uploads directory exists
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
