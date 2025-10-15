"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

# Resume Schemas
class ResumeParsedData(BaseModel):
    """Parsed resume data structure."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    certifications: List[str] = []
    total_experience_years: int = 0
    
    @field_validator('education', mode='before')
    @classmethod
    def clean_education(cls, v):
        """Clean education data and convert None values to empty strings."""
        if not v:
            return []
        result = []
        for edu in v:
            if isinstance(edu, dict):
                # Convert None values to empty strings
                cleaned_edu = {
                    key: (value if value is not None else "")
                    for key, value in edu.items()
                }
                result.append(cleaned_edu)
            else:
                result.append(edu)
        return result
    
    @field_validator('experience', mode='before')
    @classmethod
    def clean_experience(cls, v):
        """Clean experience data and convert None values to empty strings."""
        if not v:
            return []
        result = []
        for exp in v:
            if isinstance(exp, dict):
                # Convert None values to empty strings
                cleaned_exp = {
                    key: (value if value is not None else "")
                    for key, value in exp.items()
                }
                result.append(cleaned_exp)
            else:
                result.append(exp)
        return result
    
    @field_validator('total_experience_years', mode='before')
    @classmethod
    def round_experience(cls, v):
        """Convert float experience to integer."""
        if v is None:
            return 0
        return int(round(float(v)))
    
    @field_validator('certifications', mode='before')
    @classmethod
    def convert_certifications(cls, v):
        """Convert certifications from dict to string if needed."""
        if not v:
            return []
        result = []
        for cert in v:
            if isinstance(cert, dict):
                # Old format: {name, issuer, year}
                name = cert.get('name', 'Unknown')
                issuer = cert.get('issuer', '')
                year = cert.get('year', '')
                if issuer and year:
                    result.append(f"{name} ({issuer}, {year})")
                elif issuer:
                    result.append(f"{name} ({issuer})")
                else:
                    result.append(name)
            else:
                result.append(str(cert))
        return result

class ResumeResponse(BaseModel):
    """Resume response schema."""
    id: str = Field(alias="_id")
    filename: str
    text_content: str
    parsed_data: ResumeParsedData
    upload_date: str
    
    class Config:
        populate_by_name = True

class ResumeListResponse(BaseModel):
    """List of resumes response."""
    resumes: List[ResumeResponse]
    total: int

# Job Schemas
class JobCreateRequest(BaseModel):
    """Job creation request schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    requirements: List[str] = []

class JobResponse(BaseModel):
    """Job response schema."""
    id: str = Field(alias="_id")
    title: str
    description: str
    requirements: List[str]
    created_date: str
    
    @field_validator('requirements', mode='before')
    @classmethod
    def convert_requirements(cls, v):
        """Convert requirements from dict to string list if needed."""
        if not v:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, dict):
            # Old format: dict with required_skills, preferred_skills, etc.
            result = []
            required_skills = v.get('required_skills', [])
            preferred_skills = v.get('preferred_skills', [])
            experience = v.get('experience_required', '')
            education = v.get('education_required', '')
            responsibilities = v.get('responsibilities', [])
            
            if required_skills:
                result.append(f"Required Skills: {', '.join(required_skills)}")
            if preferred_skills:
                result.append(f"Preferred Skills: {', '.join(preferred_skills)}")
            if experience:
                result.append(f"Experience: {experience}")
            if education:
                result.append(f"Education: {education}")
            if responsibilities:
                result.extend([f"Responsibility: {r}" for r in responsibilities[:3]])  # Limit to 3
            
            return result if result else ["See job description for requirements"]
        return [str(v)]
    
    class Config:
        populate_by_name = True

class JobListResponse(BaseModel):
    """List of jobs response."""
    jobs: List[JobResponse]
    total: int

# Match Schemas
class MatchRequest(BaseModel):
    """Match request schema."""
    job_id: str = Field(..., description="Job ID to match resumes against")
    resume_ids: Optional[List[str]] = Field(None, description="Specific resume IDs to match (optional, matches all if not provided)")

class MatchResult(BaseModel):
    """Single match result."""
    id: str = Field(alias="_id")
    resume_id: str
    job_id: str
    candidate_name: str
    score: float = Field(..., ge=0, le=10)  # Allow 0 for no match cases
    matching_points: List[str]
    missing_qualifications: List[str]
    strengths: List[str]
    justification: str
    resume_filename: str
    job_title: str
    timestamp: str
    
    class Config:
        populate_by_name = True

class MatchListResponse(BaseModel):
    """List of match results."""
    matches: List[MatchResult]
    total: int
    job_id: str
    job_title: Optional[str] = None

# Generic Response Schemas
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    success: bool = False

# Health Check
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    database: str = "connected"
