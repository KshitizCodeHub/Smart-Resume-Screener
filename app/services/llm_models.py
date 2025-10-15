"""
Enhanced LLM Service with optimized prompts and structured output.
Phase 4: LLM Optimization & Prompt Engineering
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

# ===== Enums for structured data =====

class CareerLevel(str, Enum):
    """Career level classification"""
    ENTRY = "Entry Level"
    JUNIOR = "Junior"
    MID = "Mid-Level"
    SENIOR = "Senior"
    LEAD = "Lead/Principal"
    EXECUTIVE = "Executive"

class RecommendationStrength(str, Enum):
    """Job match recommendation strength"""
    STRONG = "Strong Match - Highly Recommended"
    MODERATE = "Moderate Match - Recommended with Reservations"
    WEAK = "Weak Match - Not Ideal"
    NOT_RECOMMENDED = "Not Recommended"

# ===== Pydantic Models for Structured Output =====

class Experience(BaseModel):
    """Work experience entry"""
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job title/role")
    duration: str = Field(..., description="Time period (e.g., 'Jan 2020 - Dec 2022')")
    description: Optional[str] = Field(None, description="Brief description of responsibilities")

class Education(BaseModel):
    """Education entry"""
    degree: str = Field(..., description="Degree name")
    institution: str = Field(..., description="Institution name")
    year: Optional[str] = Field(None, description="Graduation year or expected year")
    field: Optional[str] = Field(None, description="Field of study")

class ParsedResume(BaseModel):
    """Structured resume data with validation"""
    name: Optional[str] = Field(None, description="Full name of candidate")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location or city")
    
    # Skills categorization
    technical_skills: List[str] = Field(default_factory=list, description="Technical/hard skills")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills")
    tools_technologies: List[str] = Field(default_factory=list, description="Tools and technologies")
    
    # Experience and education
    experience: List[Experience] = Field(default_factory=list, description="Work experience")
    education: List[Education] = Field(default_factory=list, description="Education background")
    
    # Additional information
    certifications: List[str] = Field(default_factory=list, description="Professional certifications")
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    total_experience_years: float = Field(0, ge=0, description="Total years of experience")
    career_level: Optional[CareerLevel] = Field(None, description="Career level classification")
    
    # Metadata
    key_achievements: List[str] = Field(default_factory=list, description="Notable achievements")
    confidence_score: float = Field(0.8, ge=0, le=1, description="Confidence in extraction accuracy")

    @validator('total_experience_years')
    def validate_experience_years(cls, v):
        """Ensure experience years is reasonable"""
        return min(v, 50)  # Cap at 50 years

class SkillsBreakdown(BaseModel):
    """Detailed skills comparison"""
    matching_skills: List[str] = Field(default_factory=list, description="Skills that match requirements")
    missing_critical_skills: List[str] = Field(default_factory=list, description="Required skills candidate lacks")
    missing_preferred_skills: List[str] = Field(default_factory=list, description="Preferred skills candidate lacks")
    bonus_skills: List[str] = Field(default_factory=list, description="Additional valuable skills")

class ScoreBreakdown(BaseModel):
    """Detailed score breakdown by category"""
    skills_score: float = Field(..., ge=0, le=10, description="Skills match score (out of 4)")
    experience_score: float = Field(..., ge=0, le=10, description="Experience match score (out of 3)")
    education_score: float = Field(..., ge=0, le=10, description="Education match score (out of 1.5)")
    additional_score: float = Field(..., ge=0, le=10, description="Additional qualifications score (out of 1.5)")
    total_score: float = Field(..., ge=0, le=10, description="Total weighted score (out of 10)")

class JobMatchResult(BaseModel):
    """Enhanced job match result with detailed analysis"""
    # Overall assessment
    score: float = Field(..., ge=0, le=10, description="Overall match score (0-10)")
    recommendation: RecommendationStrength = Field(..., description="Recommendation strength")
    confidence_level: float = Field(..., ge=0, le=1, description="Confidence in this assessment")
    
    # Detailed breakdown
    score_breakdown: ScoreBreakdown = Field(..., description="Score breakdown by category")
    skills_analysis: SkillsBreakdown = Field(..., description="Detailed skills comparison")
    
    # Qualitative analysis
    matching_points: List[str] = Field(default_factory=list, description="Key matching qualifications")
    missing_qualifications: List[str] = Field(default_factory=list, description="Missing qualifications")
    strengths: List[str] = Field(default_factory=list, description="Candidate's strengths")
    concerns: List[str] = Field(default_factory=list, description="Potential concerns or gaps")
    
    # Summary
    justification: str = Field(..., description="Detailed justification for the score and recommendation")
    interviewer_notes: Optional[str] = Field(None, description="Suggested interview focus areas")

    @validator('score')
    def validate_score(cls, v):
        """Ensure score is in valid range"""
        return max(0, min(10, v))

# ===== Enhanced Prompts =====

RESUME_PARSER_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) resume parser with years of experience in HR and recruitment. Your job is to extract structured, accurate information from resumes.

CRITICAL RULES:
1. Extract ONLY information explicitly stated in the resume
2. DO NOT hallucinate or invent information
3. If a field is not found, use null or empty array
4. Categorize skills accurately (technical vs soft vs tools)
5. Calculate total experience by summing all job durations
6. Classify career level based on experience and roles
7. Assign confidence score based on resume clarity and completeness

SKILL CATEGORIZATION GUIDE:
- Technical Skills: Programming languages, frameworks, methodologies
- Soft Skills: Leadership, communication, teamwork, problem-solving
- Tools & Technologies: Software, platforms, databases, cloud services

CAREER LEVEL CLASSIFICATION:
- Entry Level: 0-1 years, internships, recent graduate
- Junior: 1-3 years, developing skills
- Mid-Level: 3-7 years, independent contributor
- Senior: 7-12 years, mentoring others, expert
- Lead/Principal: 12+ years, leading teams/projects
- Executive: C-level, VP, Director positions"""

RESUME_PARSER_FEW_SHOT_EXAMPLES = """
EXAMPLE 1:
Input Resume: "John Doe | john@email.com | (555) 123-4567 | New York, NY

EXPERIENCE
Senior Software Engineer at Tech Corp (Jan 2020 - Present)
- Led team of 5 developers building cloud-native applications
- Implemented microservices architecture using Python and Docker
- Reduced deployment time by 60%

Software Engineer at StartupXYZ (Jun 2017 - Dec 2019)
- Developed RESTful APIs using Flask and PostgreSQL
- Collaborated with product team on feature development

EDUCATION
BS Computer Science, MIT, 2017

SKILLS
Languages: Python, JavaScript, SQL
Frameworks: Flask, FastAPI, React
Tools: Docker, Kubernetes, AWS
Soft Skills: Team Leadership, Agile Methodologies

CERTIFICATIONS
AWS Certified Solutions Architect"

Output JSON:
{
  "name": "John Doe",
  "email": "john@email.com",
  "phone": "(555) 123-4567",
  "location": "New York, NY",
  "technical_skills": ["Python", "JavaScript", "SQL", "Flask", "FastAPI", "React"],
  "soft_skills": ["Team Leadership", "Agile Methodologies"],
  "tools_technologies": ["Docker", "Kubernetes", "AWS", "PostgreSQL"],
  "experience": [
    {
      "company": "Tech Corp",
      "role": "Senior Software Engineer",
      "duration": "Jan 2020 - Present",
      "description": "Led team of 5 developers building cloud-native applications"
    },
    {
      "company": "StartupXYZ",
      "role": "Software Engineer",
      "duration": "Jun 2017 - Dec 2019",
      "description": "Developed RESTful APIs using Flask and PostgreSQL"
    }
  ],
  "education": [
    {
      "degree": "BS Computer Science",
      "institution": "MIT",
      "year": "2017",
      "field": "Computer Science"
    }
  ],
  "certifications": ["AWS Certified Solutions Architect"],
  "languages": ["English"],
  "total_experience_years": 7.5,
  "career_level": "Senior",
  "key_achievements": ["Reduced deployment time by 60%", "Led team of 5 developers"],
  "confidence_score": 0.95
}
"""

JOB_MATCHER_SYSTEM_PROMPT = """You are an expert technical recruiter with deep understanding of job requirements and candidate evaluation. Your task is to match candidates with job descriptions using a structured, fair, and transparent scoring system.

SCORING RUBRIC (Total: 10 points):
1. SKILLS MATCH (4 points / 40%):
   - All critical skills present: 4 points
   - Most critical skills present: 3 points
   - Some critical skills present: 2 points
   - Few critical skills present: 1 point
   - No critical skills present: 0 points

2. EXPERIENCE RELEVANCE (3 points / 30%):
   - Experience level matches perfectly: 3 points
   - Experience level close (±2 years): 2 points
   - Experience level somewhat relevant: 1 point
   - Experience level not relevant: 0 points

3. EDUCATION ALIGNMENT (1.5 points / 15%):
   - Education perfectly matches requirements: 1.5 points
   - Education partially matches: 1 point
   - Education somewhat relevant: 0.5 points
   - Education not relevant: 0 points

4. ADDITIONAL QUALIFICATIONS (1.5 points / 15%):
   - Certifications, languages, achievements, projects
   - Exceptional additional qualifications: 1.5 points
   - Good additional qualifications: 1 point
   - Some additional qualifications: 0.5 points
   - No additional qualifications: 0 points

RECOMMENDATION GUIDELINES:
- 8.5-10: Strong Match - Highly Recommended (Top 10% candidates)
- 6.5-8.4: Moderate Match - Recommended with Reservations (Interview with specific focus)
- 4.5-6.4: Weak Match - Not Ideal (Only if pool is limited)
- 0-4.4: Not Recommended (Does not meet minimum requirements)

ANALYSIS PROCESS:
1. Identify required vs preferred skills
2. Compare candidate skills with requirements
3. Evaluate experience level and relevance
4. Assess education background
5. Consider additional qualifications
6. Calculate weighted score
7. Determine recommendation strength
8. Provide actionable insights"""

JOB_MATCHER_PROMPT_TEMPLATE = """
Analyze this candidate for the given job position using the scoring rubric.

CANDIDATE PROFILE:
Name: {candidate_name}
Technical Skills: {technical_skills}
Soft Skills: {soft_skills}
Tools & Technologies: {tools_technologies}
Total Experience: {experience_years} years
Career Level: {career_level}
Education: {education}
Certifications: {certifications}

JOB REQUIREMENTS:
{job_description}

ANALYSIS STEPS:
1. Extract required and preferred skills from job description
2. Compare candidate's skills with requirements (matching/missing/bonus)
3. Evaluate experience level fit
4. Assess education relevance
5. Calculate scores per category
6. Provide detailed justification

Return your analysis as a valid JSON object matching this structure:
{json_schema}

Be thorough, fair, and provide actionable insights for the hiring team."""

