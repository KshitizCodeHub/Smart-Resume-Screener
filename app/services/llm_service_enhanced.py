"""
Enhanced LLM Service with optimized prompts and structured output validation.
Phase 4: LLM Optimization & Prompt Engineering
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import re
from typing import Dict, Any, Optional, List
from pydantic import ValidationError
import asyncio

# Import enhanced models and prompts
from app.services.llm_models import (
    ParsedResume,
    JobMatchResult,
    RESUME_PARSER_SYSTEM_PROMPT,
    RESUME_PARSER_FEW_SHOT_EXAMPLES,
    JOB_MATCHER_SYSTEM_PROMPT,
    JOB_MATCHER_PROMPT_TEMPLATE
)
from app.config import settings

class EnhancedLLMService:
    """Enhanced LLM service with better prompts and validation."""
    
    def __init__(self):
        """Initialize the Gemini LLM with optimized settings."""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.gemini_api_key,
            temperature=0.1,  # Lower temperature for more consistent output
            max_output_tokens=8192  # Ensure enough tokens for detailed responses
        )
        
        # Configuration for retries
        self.max_retries = 3
        self.validation_enabled = True
    
    async def extract_structured_data(
        self, 
        resume_text: str, 
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Extract structured data from resume using enhanced prompts and validation.
        
        Args:
            resume_text: Raw resume text
            retry_count: Current retry attempt (for internal use)
            
        Returns:
            Dictionary with extracted and validated information
        """
        try:
            # Construct enhanced prompt with system message and few-shot examples
            prompt = f"""{RESUME_PARSER_SYSTEM_PROMPT}

{RESUME_PARSER_FEW_SHOT_EXAMPLES}

Now, parse this resume and return a valid JSON object matching the structure shown in the examples:

RESUME TEXT:
{resume_text}

IMPORTANT: Return ONLY the JSON object. No additional text, explanations, or markdown formatting.
Ensure all fields are present, even if empty. Assign a confidence_score between 0 and 1 based on:
- Resume clarity and completeness (0.3)
- Information availability (0.4)  
- Structure and formatting (0.3)
"""
            
            # Invoke LLM
            response = await asyncio.to_thread(
                self.llm.invoke,
                prompt
            )
            
            # Extract and clean JSON
            json_data = self._extract_json_from_response(response.content)
            
            # Validate with Pydantic if enabled
            if self.validation_enabled:
                try:
                    parsed_resume = ParsedResume(**json_data)
                    validated_data = parsed_resume.model_dump()
                    return validated_data
                except ValidationError as ve:
                    print(f"Validation error (attempt {retry_count + 1}): {ve}")
                    
                    # Retry with clarification if under max retries
                    if retry_count < self.max_retries:
                        clarification = self._generate_validation_clarification(ve, json_data)
                        return await self._retry_with_clarification(
                            resume_text, 
                            clarification, 
                            retry_count + 1
                        )
                    else:
                        # Return best-effort data after max retries
                        return self._sanitize_data(json_data)
            
            return json_data
            
        except Exception as e:
            print(f"Error in extract_structured_data: {str(e)}")
            
            # Retry if possible
            if retry_count < self.max_retries:
                return await self.extract_structured_data(resume_text, retry_count + 1)
            
            # Return minimal valid structure as fallback
            return self._get_fallback_resume_structure()
    
    async def match_resume_with_job(
        self,
        resume_data: Dict[str, Any],
        job_description: str,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Match resume with job description using enhanced rubric-based scoring.
        
        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            retry_count: Current retry attempt (for internal use)
            
        Returns:
            Dictionary with detailed match analysis
        """
        try:
            # Prepare candidate profile summary
            candidate_summary = self._format_candidate_profile(resume_data)
            
            # Get JSON schema for structured output
            json_schema = JobMatchResult.model_json_schema()
            schema_str = json.dumps(json_schema, indent=2)
            
            # Construct enhanced prompt
            # Helper function to safely join lists that might contain dicts
            def safe_join(items, key=None):
                if not items:
                    return "None"
                result = []
                for item in items:
                    if isinstance(item, dict):
                        if key and key in item:
                            result.append(str(item[key]))
                        else:
                            # Try to extract meaningful value from dict
                            result.append(str(item.get('name', item.get('title', str(item)))))
                    else:
                        result.append(str(item))
                return ', '.join(result) if result else "None"
            
            prompt = f"""{JOB_MATCHER_SYSTEM_PROMPT}

{JOB_MATCHER_PROMPT_TEMPLATE.format(
    candidate_name=resume_data.get('name', 'Unknown'),
    technical_skills=safe_join(resume_data.get('technical_skills', [])),
    soft_skills=safe_join(resume_data.get('soft_skills', [])),
    tools_technologies=safe_join(resume_data.get('tools_technologies', [])),
    experience_years=resume_data.get('total_experience_years', 0),
    career_level=resume_data.get('career_level', 'Unknown'),
    education=self._format_education(resume_data.get('education', [])),
    certifications=safe_join(resume_data.get('certifications', [])),
    job_description=job_description,
    json_schema=schema_str
)}

IMPORTANT: 
1. Return ONLY a valid JSON object matching the schema
2. Calculate scores using the rubric (Skills: 4pts, Experience: 3pts, Education: 1.5pts, Additional: 1.5pts)
3. Be fair and objective in your assessment
4. Provide actionable insights for the hiring team
"""
            
            # Invoke LLM
            response = await asyncio.to_thread(
                self.llm.invoke,
                prompt
            )
            
            # Extract and clean JSON
            json_data = self._extract_json_from_response(response.content)
            
            # Validate with Pydantic if enabled
            if self.validation_enabled:
                try:
                    match_result = JobMatchResult(**json_data)
                    validated_data = match_result.model_dump()
                    return validated_data
                except ValidationError as ve:
                    print(f"Match validation error (attempt {retry_count + 1}): {ve}")
                    
                    # Retry with clarification if under max retries
                    if retry_count < self.max_retries:
                        return await self.match_resume_with_job(
                            resume_data,
                            job_description,
                            retry_count + 1
                        )
                    else:
                        # Return sanitized data after max retries
                        return self._sanitize_match_data(json_data)
            
            return json_data
            
        except Exception as e:
            print(f"Error in match_resume_with_job: {str(e)}")
            
            # Retry if possible
            if retry_count < self.max_retries:
                return await self.match_resume_with_job(
                    resume_data,
                    job_description,
                    retry_count + 1
                )
            
            # Return minimal valid structure as fallback
            return self._get_fallback_match_structure()
    
    async def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """
        Extract structured requirements from job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary with extracted requirements
        """
        try:
            prompt = f"""
You are an expert job requirements analyst. Extract key information from this job description.

JOB DESCRIPTION:
{job_description}

Extract and return a JSON object with this structure:
{{
    "title": "job title",
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "experience_required": "X years",
    "education_required": "degree level",
    "responsibilities": ["responsibility1", "responsibility2"],
    "qualifications": ["qualification1", "qualification2"],
    "salary_range": "if mentioned, else null",
    "location": "location if mentioned"
}}

Return ONLY the JSON object, no additional text.
"""
            
            response = await asyncio.to_thread(
                self.llm.invoke,
                prompt
            )
            
            json_data = self._extract_json_from_response(response.content)
            return json_data
            
        except Exception as e:
            print(f"Error in extract_job_requirements: {str(e)}")
            return {
                "title": "Unknown",
                "required_skills": [],
                "preferred_skills": [],
                "experience_required": "Not specified",
                "education_required": "Not specified",
                "responsibilities": [],
                "qualifications": []
            }
    
    # ===== Helper Methods =====
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response."""
        # Remove markdown code blocks if present
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        
        # Try to find JSON object
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        
        # Try parsing the entire response
        return json.loads(response)
    
    def _format_candidate_profile(self, resume_data: Dict[str, Any]) -> str:
        """Format resume data into readable candidate profile."""
        profile_parts = []
        
        if resume_data.get('name'):
            profile_parts.append(f"Name: {resume_data['name']}")
        
        if resume_data.get('technical_skills'):
            profile_parts.append(f"Technical Skills: {', '.join(resume_data['technical_skills'])}")
        
        if resume_data.get('total_experience_years'):
            profile_parts.append(f"Experience: {resume_data['total_experience_years']} years")
        
        return '\n'.join(profile_parts)
    
    def _format_education(self, education_list: List[Dict]) -> str:
        """Format education list into readable string."""
        if not education_list:
            return "Not specified"
        
        edu_strings = []
        for edu in education_list:
            edu_str = edu.get('degree', 'Unknown Degree')
            if edu.get('institution'):
                edu_str += f" from {edu['institution']}"
            if edu.get('year'):
                edu_str += f" ({edu['year']})"
            edu_strings.append(edu_str)
        
        return '; '.join(edu_strings)
    
    def _generate_validation_clarification(
        self, 
        validation_error: ValidationError,
        original_data: Dict[str, Any]
    ) -> str:
        """Generate clarification message for validation errors."""
        errors = validation_error.errors()
        error_messages = []
        
        for error in errors:
            field = '.'.join(str(x) for x in error['loc'])
            message = error['msg']
            error_messages.append(f"- Field '{field}': {message}")
        
        return "Validation errors:\n" + '\n'.join(error_messages)
    
    async def _retry_with_clarification(
        self,
        resume_text: str,
        clarification: str,
        retry_count: int
    ) -> Dict[str, Any]:
        """Retry extraction with clarification about previous errors."""
        enhanced_prompt = f"""
Previous attempt had validation issues. Please correct these errors:

{clarification}

Now, parse this resume again with correct formatting:

{resume_text}

Return a valid JSON object following the exact structure from the examples.
"""
        
        try:
            response = await asyncio.to_thread(
                self.llm.invoke,
                enhanced_prompt
            )
            
            json_data = self._extract_json_from_response(response.content)
            
            # Validate again
            parsed_resume = ParsedResume(**json_data)
            return parsed_resume.model_dump()
            
        except Exception as e:
            print(f"Retry failed: {str(e)}")
            return self._sanitize_data(json_data if 'json_data' in locals() else {})
    
    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data to ensure it has required fields."""
        sanitized = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "location": data.get("location"),
            "technical_skills": data.get("technical_skills", []),
            "soft_skills": data.get("soft_skills", []),
            "tools_technologies": data.get("tools_technologies", []),
            "experience": data.get("experience", []),
            "education": data.get("education", []),
            "certifications": data.get("certifications", []),
            "languages": data.get("languages", ["English"]),
            "total_experience_years": data.get("total_experience_years", 0),
            "career_level": data.get("career_level"),
            "key_achievements": data.get("key_achievements", []),
            "confidence_score": data.get("confidence_score", 0.5)
        }
        return sanitized
    
    def _sanitize_match_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize match data to ensure it has required fields."""
        score = data.get("score", 5.0)
        
        return {
            "score": max(0, min(10, score)),
            "recommendation": data.get("recommendation", "Moderate Match - Recommended with Reservations"),
            "confidence_level": data.get("confidence_level", 0.7),
            "score_breakdown": data.get("score_breakdown", {
                "skills_score": score * 0.4,
                "experience_score": score * 0.3,
                "education_score": score * 0.15,
                "additional_score": score * 0.15,
                "total_score": score
            }),
            "skills_analysis": data.get("skills_analysis", {
                "matching_skills": [],
                "missing_critical_skills": [],
                "missing_preferred_skills": [],
                "bonus_skills": []
            }),
            "matching_points": data.get("matching_points", []),
            "missing_qualifications": data.get("missing_qualifications", []),
            "strengths": data.get("strengths", []),
            "concerns": data.get("concerns", []),
            "justification": data.get("justification", "Unable to generate complete analysis."),
            "interviewer_notes": data.get("interviewer_notes")
        }
    
    def _get_fallback_resume_structure(self) -> Dict[str, Any]:
        """Return minimal valid resume structure as fallback."""
        return {
            "name": None,
            "email": None,
            "phone": None,
            "location": None,
            "technical_skills": [],
            "soft_skills": [],
            "tools_technologies": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "languages": ["English"],
            "total_experience_years": 0,
            "career_level": None,
            "key_achievements": [],
            "confidence_score": 0.1
        }
    
    def _get_fallback_match_structure(self) -> Dict[str, Any]:
        """Return minimal valid match structure as fallback."""
        return {
            "score": 0,
            "recommendation": "Not Recommended",
            "confidence_level": 0.1,
            "score_breakdown": {
                "skills_score": 0,
                "experience_score": 0,
                "education_score": 0,
                "additional_score": 0,
                "total_score": 0
            },
            "skills_analysis": {
                "matching_skills": [],
                "missing_critical_skills": [],
                "missing_preferred_skills": [],
                "bonus_skills": []
            },
            "matching_points": [],
            "missing_qualifications": ["Unable to analyze"],
            "strengths": [],
            "concerns": ["Analysis failed"],
            "justification": "Unable to complete analysis due to technical error.",
            "interviewer_notes": None
        }

# Create a global instance
enhanced_llm_service = EnhancedLLMService()
