"""
LangChain + Gemini LLM integration service.
Handles all LLM-based operations for resume analysis and matching.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
import json
import re
from typing import Dict, Any, List

class LLMService:
    """Service for LLM-powered resume analysis and matching."""
    
    def __init__(self):
        """Initialize the Gemini LLM."""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.gemini_api_key,
            temperature=settings.llm_temperature
        )
    
    async def extract_structured_data(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured data from resume using LLM.
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dictionary with extracted information
        """
        prompt_template = """
You are an expert resume parser. Extract the following information from the resume text and return it as a JSON object.

Resume Text:
{resume_text}

Extract and return ONLY a valid JSON object with this exact structure (no additional text):
{{
    "name": "full name of the candidate",
    "email": "email address",
    "phone": "phone number",
    "skills": ["skill1", "skill2", "skill3"],
    "technical_skills": ["technical skill1", "technical skill2"],
    "soft_skills": ["soft skill1", "soft skill2"],
    "experience": [
        {{
            "company": "company name",
            "role": "job title",
            "duration": "time period"
        }}
    ],
    "education": [
        {{
            "degree": "degree name",
            "institution": "institution name",
            "year": "graduation year"
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "total_experience_years": 0
}}

If any field is not found, use null for strings, [] for arrays, or 0 for numbers.
Return ONLY the JSON object, no markdown formatting or additional text.
"""
        
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template=prompt_template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(resume_text=resume_text[:4000])  # Limit text length
            
            # Clean response - remove markdown code blocks if present
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Parse JSON
            parsed_data = json.loads(response)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {response}")
            # Return basic structure
            return {
                "name": None,
                "email": None,
                "phone": None,
                "skills": [],
                "technical_skills": [],
                "soft_skills": [],
                "experience": [],
                "education": [],
                "certifications": [],
                "total_experience_years": 0
            }
        except Exception as e:
            print(f"LLM extraction error: {e}")
            raise e
    
    async def match_resume_with_job(self, resume_text: str, job_description: str, 
                                   resume_parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match resume with job description using LLM.
        
        Args:
            resume_text: Resume text content
            job_description: Job description text
            resume_parsed_data: Parsed resume data
            
        Returns:
            Match result with score and justification
        """
        prompt_template = """
You are an expert recruiter. Compare the following candidate's resume with the job description and provide a detailed analysis.

Candidate Resume:
{resume_text}

Candidate Skills: {skills}

Job Description:
{job_description}

Provide your analysis in the following JSON format (no additional text):
{{
    "score": <number between 1-10, where 10 is perfect fit>,
    "matching_points": [
        "matching point 1",
        "matching point 2",
        "matching point 3"
    ],
    "missing_qualifications": [
        "missing qualification 1",
        "missing qualification 2"
    ],
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "justification": "2-3 sentences explaining the overall fit and recommendation"
}}

Consider:
- Technical skills match
- Experience level
- Domain knowledge
- Soft skills
- Educational background

Return ONLY the JSON object, no markdown formatting or additional text.
"""
        
        skills_str = ", ".join(resume_parsed_data.get("skills", [])[:20])
        
        prompt = PromptTemplate(
            input_variables=["resume_text", "skills", "job_description"],
            template=prompt_template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                resume_text=resume_text[:3000],
                skills=skills_str,
                job_description=job_description[:2000]
            )
            
            # Clean response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Parse JSON
            match_result = json.loads(response)
            
            # Validate score
            if 'score' in match_result:
                match_result['score'] = max(1, min(10, match_result['score']))
            
            return match_result
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in matching: {e}")
            print(f"Response was: {response}")
            # Return default structure
            return {
                "score": 5,
                "matching_points": ["Unable to analyze match"],
                "missing_qualifications": [],
                "strengths": [],
                "justification": "Analysis could not be completed due to parsing error."
            }
        except Exception as e:
            print(f"LLM matching error: {e}")
            raise e
    
    async def extract_job_requirements(self, job_description: str) -> List[str]:
        """
        Extract key requirements from job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            List of key requirements
        """
        prompt_template = """
Extract the key requirements and qualifications from this job description.
Return them as a simple JSON array of strings.

Job Description:
{job_description}

Return ONLY a JSON array like: ["requirement 1", "requirement 2", "requirement 3"]
Focus on: skills, experience, education, certifications.
"""
        
        prompt = PromptTemplate(
            input_variables=["job_description"],
            template=prompt_template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(job_description=job_description[:2000])
            response = response.strip()
            
            # Clean markdown
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            requirements = json.loads(response)
            return requirements if isinstance(requirements, list) else []
        except Exception as e:
            print(f"Error extracting requirements: {e}")
            return []


# Global LLM service instance
llm_service = LLMService()
