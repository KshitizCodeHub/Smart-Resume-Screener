"""
Resume-job matching service.
Orchestrates the matching process between resumes and job descriptions.
Enhanced with Phase 4 LLM optimization.
"""
from typing import Dict, Any, List
from app.services.llm_service import llm_service  # Original service (backup)
from app.services.llm_service_enhanced import enhanced_llm_service  # Enhanced Phase 4 service
from app.database.mongodb import ResumeDB, JobDB, MatchDB

class MatcherService:
    """Service for matching resumes with job descriptions."""
    
    @staticmethod
    async def match_single_resume(resume_id: str, job_id: str) -> Dict[str, Any]:
        """
        Match a single resume with a job description.
        
        Args:
            resume_id: Resume document ID
            job_id: Job document ID
            
        Returns:
            Match result dictionary
        """
        # Fetch resume and job from database
        resume = await ResumeDB.get_resume(resume_id)
        job = await JobDB.get_job(job_id)
        
        if not resume:
            raise ValueError(f"Resume not found: {resume_id}")
        if not job:
            raise ValueError(f"Job not found: {job_id}")
        
        # Perform Enhanced LLM-based matching (Phase 4 optimization)
        match_result = await enhanced_llm_service.match_resume_with_job(
            resume_data=resume.get("parsed_data", {}),
            job_description=job.get("description", "")
        )
        
        # Prepare match document with enhanced analysis
        match_data = {
            "resume_id": resume_id,
            "job_id": job_id,
            "candidate_name": resume.get("parsed_data", {}).get("name", "Unknown"),
            "score": match_result.get("score", 0),
            "recommendation": match_result.get("recommendation", "Moderate Match"),
            "confidence_level": match_result.get("confidence_level", 0.7),
            "score_breakdown": match_result.get("score_breakdown", {}),
            "skills_analysis": match_result.get("skills_analysis", {}),
            "matching_points": match_result.get("matching_points", []),
            "missing_qualifications": match_result.get("missing_qualifications", []),
            "strengths": match_result.get("strengths", []),
            "concerns": match_result.get("concerns", []),
            "justification": match_result.get("justification", ""),
            "interviewer_notes": match_result.get("interviewer_notes"),
            "resume_filename": resume.get("filename", ""),
            "job_title": job.get("title", "")
        }
        
        # Save match to database
        match_id = await MatchDB.create_match(match_data)
        match_data["_id"] = match_id
        
        return match_data
    
    @staticmethod
    async def match_all_resumes_with_job(job_id: str) -> List[Dict[str, Any]]:
        """
        Match all resumes with a specific job description.
        
        Args:
            job_id: Job document ID
            
        Returns:
            List of match results, sorted by score (highest first)
        """
        # Get all resumes
        resumes = await ResumeDB.get_all_resumes()
        
        if not resumes:
            return []
        
        # Match each resume
        matches = []
        for resume in resumes:
            try:
                match_result = await MatcherService.match_single_resume(
                    resume_id=resume["_id"],
                    job_id=job_id
                )
                matches.append(match_result)
            except Exception as e:
                print(f"Error matching resume {resume['_id']}: {e}")
                continue
        
        # Sort by score (descending)
        matches.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return matches
    
    @staticmethod
    async def get_top_candidates(job_id: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get top N candidates for a job.
        
        Args:
            job_id: Job document ID
            top_n: Number of top candidates to return
            
        Returns:
            List of top candidates
        """
        matches = await MatchDB.get_matches_by_job(job_id)
        return matches[:top_n]
