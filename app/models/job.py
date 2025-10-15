"""
Job Description Data Models
Defines the structure for job posting data
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class JobRequirements(BaseModel):
    """Structured job requirements"""
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)


class Job(BaseModel):
    """Job description document model for MongoDB"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    company: Optional[str] = None
    description: str
    requirements: Optional[JobRequirements] = None
    location: Optional[str] = None
    job_type: Optional[str] = None  # Full-time, Part-time, Contract
    created_date: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class MatchResult(BaseModel):
    """Result of resume-job matching"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    resume_id: str
    job_id: str
    candidate_name: Optional[str] = None
    score: float  # 1-10 scale
    matching_points: List[str] = Field(default_factory=list)
    missing_qualifications: List[str] = Field(default_factory=list)
    justification: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
