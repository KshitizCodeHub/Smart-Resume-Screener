"""
API routes for Smart Resume Screener.
Handles all HTTP endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
from datetime import datetime

from app.services.pdf_parser import DocumentParser
from app.services.text_extractor import TextExtractor
from app.services.llm_service import llm_service  # Original service (backup)
from app.services.llm_service_enhanced import enhanced_llm_service  # Enhanced Phase 4 service
from app.services.matcher import MatcherService
from app.database.mongodb import ResumeDB, JobDB, MatchDB
from app.api.schemas import (
    ResumeResponse, ResumeListResponse,
    JobCreateRequest, JobResponse, JobListResponse,
    MatchRequest, MatchResult, MatchListResponse,
    MessageResponse, ErrorResponse, HealthResponse
)
from app.config import settings

router = APIRouter()

# Health Check
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }

# Resume Endpoints
@router.post("/api/upload-resume", response_model=MessageResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and process a resume file.
    Supports PDF, DOCX, and TXT formats.
    """
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext.replace('.', '') not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {settings.allowed_extensions}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.max_file_size_mb}MB"
            )
        
        # Parse document
        text_content = DocumentParser.parse_file(file.filename, file_content)
        
        if not text_content or len(text_content) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract meaningful text from file"
            )
        
        # Extract basic info
        extractor = TextExtractor()
        name = extractor.extract_name(text_content)
        email = extractor.extract_email(text_content)
        phone = extractor.extract_phone(text_content)
        basic_skills = extractor.extract_skills_basic(text_content)
        
        # Use Enhanced LLM to extract structured data (Phase 4 optimization)
        parsed_data = await enhanced_llm_service.extract_structured_data(text_content)
        
        # Merge basic extraction with LLM results
        if not parsed_data.get("name"):
            parsed_data["name"] = name
        if not parsed_data.get("email"):
            parsed_data["email"] = email
        if not parsed_data.get("phone"):
            parsed_data["phone"] = phone
        if not parsed_data.get("skills"):
            parsed_data["skills"] = basic_skills
        
        # Save to database
        resume_data = {
            "filename": file.filename,
            "text_content": text_content,
            "parsed_data": parsed_data
        }
        
        resume_id = await ResumeDB.create_resume(resume_data)
        
        return {
            "message": f"Resume uploaded successfully. ID: {resume_id}",
            "success": True
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error uploading resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/resumes", response_model=ResumeListResponse)
async def get_all_resumes():
    """Get all uploaded resumes."""
    try:
        resumes = await ResumeDB.get_all_resumes()
        return {
            "resumes": resumes,
            "total": len(resumes)
        }
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str):
    """Get a specific resume by ID."""
    try:
        resume = await ResumeDB.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/resumes/{resume_id}", response_model=MessageResponse)
async def delete_resume(resume_id: str):
    """Delete a resume by ID."""
    try:
        success = await ResumeDB.delete_resume(resume_id)
        if not success:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {
            "message": "Resume deleted successfully",
            "success": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error deleting resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Job Endpoints
@router.post("/api/upload-job", response_model=MessageResponse)
async def create_job(job: JobCreateRequest):
    """Create a new job description."""
    try:
        # Extract requirements using Enhanced LLM if not provided (Phase 4 optimization)
        if not job.requirements:
            requirements = await enhanced_llm_service.extract_job_requirements(job.description)
            job.requirements = requirements
        
        job_data = {
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements
        }
        
        job_id = await JobDB.create_job(job_data)
        
        return {
            "message": f"Job description created successfully. ID: {job_id}",
            "success": True
        }
    except Exception as e:
        print(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/jobs", response_model=JobListResponse)
async def get_all_jobs():
    """Get all job descriptions."""
    try:
        jobs = await JobDB.get_all_jobs()
        return {
            "jobs": jobs,
            "total": len(jobs)
        }
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get a specific job by ID."""
    try:
        job = await JobDB.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/jobs/{job_id}", response_model=MessageResponse)
async def delete_job(job_id: str):
    """Delete a job by ID."""
    try:
        success = await JobDB.delete_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return {
            "message": "Job deleted successfully",
            "success": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Matching Endpoints
@router.post("/api/match", response_model=MatchListResponse)
async def match_resumes_with_job(match_request: MatchRequest):
    """
    Match resumes with a job description.
    If resume_ids is provided, matches only those resumes.
    Otherwise, matches all resumes.
    """
    try:
        job = await JobDB.get_job(match_request.job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if match_request.resume_ids:
            # Match specific resumes
            matches = []
            for resume_id in match_request.resume_ids:
                try:
                    match = await MatcherService.match_single_resume(resume_id, match_request.job_id)
                    matches.append(match)
                except Exception as e:
                    print(f"Error matching resume {resume_id}: {e}")
                    continue
            matches.sort(key=lambda x: x.get("score", 0), reverse=True)
        else:
            # Match all resumes
            matches = await MatcherService.match_all_resumes_with_job(match_request.job_id)
        
        return {
            "matches": matches,
            "total": len(matches),
            "job_id": match_request.job_id,
            "job_title": job.get("title")
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error matching resumes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/matches/{job_id}", response_model=MatchListResponse)
async def get_matches_for_job(job_id: str):
    """Get all saved matches for a specific job."""
    try:
        job = await JobDB.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        matches = await MatchDB.get_matches_by_job(job_id)
        
        return {
            "matches": matches,
            "total": len(matches),
            "job_id": job_id,
            "job_title": job.get("title")
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))
