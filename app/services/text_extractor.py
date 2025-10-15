"""
Text extraction and preprocessing service.
Extracts structured information from resume text.
"""
import re
from typing import Dict, List, Optional

class TextExtractor:
    """Extract structured data from resume text."""
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email address from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text."""
        # Match various phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}',
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """
        Extract name from resume (usually first line or before contact info).
        This is a simple heuristic - can be improved with NER.
        """
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Name is usually 2-4 words, capitalized
            if line and len(line.split()) <= 4 and line[0].isupper():
                # Avoid lines with common keywords
                keywords = ['resume', 'cv', 'curriculum', 'vitae', 'email', 'phone', 'address']
                if not any(keyword in line.lower() for keyword in keywords):
                    return line
        return None
    
    @staticmethod
    def extract_skills_basic(text: str) -> List[str]:
        """
        Basic skill extraction using keyword matching.
        This will be enhanced by LLM extraction.
        """
        # Common technical skills
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'fastapi', 'sql', 'mongodb',
            'postgresql', 'mysql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'ci/cd', 'machine learning', 'deep learning', 'nlp', 'data analysis',
            'html', 'css', 'rest api', 'graphql', 'microservices', 'agile', 'scrum'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    @staticmethod
    def extract_experience_years(text: str) -> Optional[int]:
        """Extract years of experience from text."""
        # Look for patterns like "5 years", "5+ years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        return None
    
    @staticmethod
    def extract_education_keywords(text: str) -> List[str]:
        """Extract education-related information."""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'diploma', 'degree',
            'b.tech', 'm.tech', 'b.e', 'm.e', 'bsc', 'msc', 'mba', 'bba'
        ]
        
        text_lower = text.lower()
        found_education = []
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            for keyword in education_keywords:
                if keyword in line_lower:
                    found_education.append(line.strip())
                    break
        
        return found_education[:5]  # Limit to 5 entries
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:()\-@+#]', '', text)
        return text.strip()
