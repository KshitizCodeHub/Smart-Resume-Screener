"""
Helper Utilities
Common utility functions used across the application
"""

import re
import os
from typing import Optional
from app.config import settings


def validate_file_type(filename: str) -> bool:
    """
    Validate if file extension is allowed
    
    Args:
        filename: Name of the file
        
    Returns:
        True if file type is allowed, False otherwise
    """
    if not filename:
        return False
    
    extension = filename.rsplit('.', 1)[-1].lower()
    return extension in settings.allowed_extensions_list


def validate_file_size(file_size: int) -> bool:
    """
    Validate if file size is within allowed limit
    
    Args:
        file_size: Size of file in bytes
        
    Returns:
        True if file size is valid, False otherwise
    """
    return file_size <= settings.max_file_size_bytes


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace special characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Remove multiple spaces
    filename = re.sub(r'\s+', '_', filename)
    
    return filename


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text
    
    Args:
        text: Text to search for email
        
    Returns:
        First email found or None
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text
    
    Args:
        text: Text to search for phone number
        
    Returns:
        First phone number found or None
    """
    # Pattern for various phone formats
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-234-567-8900
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (234) 567-8900
        r'\d{10}',  # 2345678900
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
