"""
Phase 4: LLM Enhancement Testing Script
Tests and compares original vs enhanced LLM service performance.
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Import both services for comparison
from app.services.llm_service import llm_service as original_service
from app.services.llm_service_enhanced import enhanced_llm_service

# Sample test resumes
SAMPLE_RESUMES = [
    """
    John Smith
    Email: john.smith@email.com | Phone: (555) 123-4567
    Location: San Francisco, CA
    
    PROFESSIONAL SUMMARY
    Senior Full Stack Developer with 8 years of experience building scalable web applications.
    
    WORK EXPERIENCE
    Senior Software Engineer | Tech Corp | Jan 2020 - Present
    - Led development of microservices architecture using Python and FastAPI
    - Managed team of 5 developers
    - Reduced deployment time by 60% through CI/CD automation
    
    Software Engineer | StartupXYZ | Jun 2017 - Dec 2019
    - Developed RESTful APIs using Flask and PostgreSQL
    - Implemented real-time features using WebSockets
    
    EDUCATION
    BS Computer Science | MIT | 2017
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, TypeScript, SQL
    Frameworks: FastAPI, Flask, React, Node.js
    Tools: Docker, Kubernetes, AWS, MongoDB, PostgreSQL
    
    CERTIFICATIONS
    - AWS Certified Solutions Architect
    - MongoDB Certified Developer
    """,
    
    """
    Sarah Johnson
    sarah.j@email.com | 555-987-6543 | New York, NY
    
    EXPERIENCE
    Data Scientist at AI Corp (2021-Present)
    - Built ML models for customer churn prediction (95% accuracy)
    - Developed data pipelines using Python and Apache Spark
    
    Junior Data Analyst at Analytics Inc (2019-2021)
    - Created dashboards using Tableau and Power BI
    - Performed statistical analysis on large datasets
    
    EDUCATION
    MS Data Science, Stanford University, 2019
    BS Mathematics, UCLA, 2017
    
    SKILLS
    Python (NumPy, Pandas, Scikit-learn, TensorFlow)
    SQL, R, Tableau, Power BI, Apache Spark
    Machine Learning, Statistical Analysis, Data Visualization
    """,
    
    """
    Michael Chen
    michael.chen@tech.com
    
    Junior Developer looking for opportunities
    
    Experience:
    Intern at WebDev Agency (6 months)
    - Worked on WordPress websites
    - Basic HTML, CSS, JavaScript
    
    Education:
    Currently pursuing BS Computer Science (Expected 2024)
    State University
    
    Skills:
    HTML, CSS, JavaScript, React basics, Git
    """
]

SAMPLE_JOB_DESCRIPTION = """
Senior Backend Engineer

We are looking for a Senior Backend Engineer to join our growing team.

Required Skills:
- 5+ years of Python development experience
- Strong experience with FastAPI or Flask
- Database design (PostgreSQL, MongoDB)
- Docker and Kubernetes
- RESTful API design
- Cloud platforms (AWS, GCP, or Azure)

Preferred Qualifications:
- Microservices architecture experience
- CI/CD pipeline setup
- Team leadership experience
- BS in Computer Science or related field

Responsibilities:
- Design and develop scalable backend services
- Mentor junior developers
- Participate in code reviews
- Optimize application performance
"""

async def test_resume_parsing():
    """Test resume parsing with both services."""
    print("\n" + "="*80)
    print("PHASE 4 TEST: Resume Parsing Comparison")
    print("="*80)
    
    results = {
        "original": [],
        "enhanced": []
    }
    
    for idx, resume_text in enumerate(SAMPLE_RESUMES, 1):
        print(f"\n--- Testing Resume {idx} ---")
        
        # Test original service
        try:
            print("Testing ORIGINAL service...")
            start = datetime.now()
            original_result = await original_service.extract_structured_data(resume_text)
            original_time = (datetime.now() - start).total_seconds()
            
            results["original"].append({
                "resume": idx,
                "success": True,
                "time": original_time,
                "fields_extracted": len([k for k, v in original_result.items() if v]),
                "has_confidence": "confidence_score" in original_result,
                "data": original_result
            })
            print(f"  ✓ Success in {original_time:.2f}s")
            print(f"  ✓ Fields extracted: {results['original'][-1]['fields_extracted']}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            results["original"].append({
                "resume": idx,
                "success": False,
                "error": str(e)
            })
        
        # Test enhanced service
        try:
            print("Testing ENHANCED service...")
            start = datetime.now()
            enhanced_result = await enhanced_llm_service.extract_structured_data(resume_text)
            enhanced_time = (datetime.now() - start).total_seconds()
            
            results["enhanced"].append({
                "resume": idx,
                "success": True,
                "time": enhanced_time,
                "fields_extracted": len([k for k, v in enhanced_result.items() if v]),
                "has_confidence": "confidence_score" in enhanced_result,
                "has_career_level": "career_level" in enhanced_result and enhanced_result["career_level"],
                "technical_skills_count": len(enhanced_result.get("technical_skills", [])),
                "soft_skills_count": len(enhanced_result.get("soft_skills", [])),
                "data": enhanced_result
            })
            print(f"  ✓ Success in {enhanced_time:.2f}s")
            print(f"  ✓ Fields extracted: {results['enhanced'][-1]['fields_extracted']}")
            print(f"  ✓ Confidence: {enhanced_result.get('confidence_score', 'N/A')}")
            print(f"  ✓ Career Level: {enhanced_result.get('career_level', 'N/A')}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            results["enhanced"].append({
                "resume": idx,
                "success": False,
                "error": str(e)
            })
    
    return results

async def test_job_matching():
    """Test job matching with both services."""
    print("\n" + "="*80)
    print("PHASE 4 TEST: Job Matching Comparison")
    print("="*80)
    
    # First parse the resumes with enhanced service
    print("\nParsing resumes...")
    parsed_resumes = []
    for idx, resume_text in enumerate(SAMPLE_RESUMES, 1):
        try:
            parsed = await enhanced_llm_service.extract_structured_data(resume_text)
            parsed_resumes.append(parsed)
            print(f"  ✓ Resume {idx} parsed")
        except Exception as e:
            print(f"  ✗ Resume {idx} failed: {str(e)}")
            parsed_resumes.append({})
    
    # Test matching with enhanced service
    results = {
        "enhanced": []
    }
    
    print(f"\nMatching {len(parsed_resumes)} resumes with job description...")
    
    for idx, resume_data in enumerate(parsed_resumes, 1):
        if not resume_data:
            print(f"\n--- Resume {idx}: Skipped (parsing failed) ---")
            continue
            
        print(f"\n--- Resume {idx}: {resume_data.get('name', 'Unknown')} ---")
        
        try:
            print("Testing ENHANCED matching service...")
            start = datetime.now()
            match_result = await enhanced_llm_service.match_resume_with_job(
                resume_data=resume_data,
                job_description=SAMPLE_JOB_DESCRIPTION
            )
            match_time = (datetime.now() - start).total_seconds()
            
            results["enhanced"].append({
                "resume": idx,
                "candidate": resume_data.get("name", "Unknown"),
                "success": True,
                "time": match_time,
                "score": match_result.get("score", 0),
                "recommendation": match_result.get("recommendation", "Unknown"),
                "confidence": match_result.get("confidence_level", 0),
                "has_breakdown": "score_breakdown" in match_result,
                "has_skills_analysis": "skills_analysis" in match_result,
                "data": match_result
            })
            
            print(f"  ✓ Success in {match_time:.2f}s")
            print(f"  ✓ Score: {match_result.get('score', 0):.2f}/10")
            print(f"  ✓ Recommendation: {match_result.get('recommendation', 'N/A')}")
            print(f"  ✓ Confidence: {match_result.get('confidence_level', 0):.2%}")
            
            # Show score breakdown
            breakdown = match_result.get("score_breakdown", {})
            if breakdown:
                print(f"  ✓ Skills: {breakdown.get('skills_score', 0):.2f}/4")
                print(f"  ✓ Experience: {breakdown.get('experience_score', 0):.2f}/3")
                print(f"  ✓ Education: {breakdown.get('education_score', 0):.2f}/1.5")
                print(f"  ✓ Additional: {breakdown.get('additional_score', 0):.2f}/1.5")
            
            # Show skills analysis
            skills = match_result.get("skills_analysis", {})
            if skills:
                matching = skills.get("matching_skills", [])
                missing = skills.get("missing_critical_skills", [])
                print(f"  ✓ Matching Skills: {len(matching)}")
                print(f"  ✓ Missing Critical: {len(missing)}")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            results["enhanced"].append({
                "resume": idx,
                "success": False,
                "error": str(e)
            })
    
    return results

async def generate_comparison_report(parsing_results: Dict, matching_results: Dict):
    """Generate a comprehensive comparison report."""
    print("\n" + "="*80)
    print("PHASE 4: ENHANCEMENT ANALYSIS REPORT")
    print("="*80)
    
    # Parsing Analysis
    print("\n### RESUME PARSING COMPARISON ###\n")
    
    original_success = sum(1 for r in parsing_results["original"] if r.get("success"))
    enhanced_success = sum(1 for r in parsing_results["enhanced"] if r.get("success"))
    
    print(f"Success Rate:")
    print(f"  Original: {original_success}/{len(parsing_results['original'])} ({original_success/len(parsing_results['original'])*100:.0f}%)")
    print(f"  Enhanced: {enhanced_success}/{len(parsing_results['enhanced'])} ({enhanced_success/len(parsing_results['enhanced'])*100:.0f}%)")
    
    if original_success > 0:
        avg_orig_time = sum(r.get("time", 0) for r in parsing_results["original"] if r.get("success")) / original_success
        avg_orig_fields = sum(r.get("fields_extracted", 0) for r in parsing_results["original"] if r.get("success")) / original_success
    else:
        avg_orig_time = 0
        avg_orig_fields = 0
    
    if enhanced_success > 0:
        avg_enh_time = sum(r.get("time", 0) for r in parsing_results["enhanced"] if r.get("success")) / enhanced_success
        avg_enh_fields = sum(r.get("fields_extracted", 0) for r in parsing_results["enhanced"] if r.get("success")) / enhanced_success
    else:
        avg_enh_time = 0
        avg_enh_fields = 0
    
    print(f"\nAverage Response Time:")
    print(f"  Original: {avg_orig_time:.2f}s")
    print(f"  Enhanced: {avg_enh_time:.2f}s")
    
    print(f"\nAverage Fields Extracted:")
    print(f"  Original: {avg_orig_fields:.1f}")
    print(f"  Enhanced: {avg_enh_fields:.1f}")
    
    enhanced_with_confidence = sum(1 for r in parsing_results["enhanced"] if r.get("has_confidence"))
    enhanced_with_career = sum(1 for r in parsing_results["enhanced"] if r.get("has_career_level"))
    
    print(f"\nEnhanced Features:")
    print(f"  Confidence Scores: {enhanced_with_confidence}/{enhanced_success}")
    print(f"  Career Level Classification: {enhanced_with_career}/{enhanced_success}")
    
    # Matching Analysis
    print("\n### JOB MATCHING ANALYSIS ###\n")
    
    match_success = sum(1 for r in matching_results["enhanced"] if r.get("success"))
    
    print(f"Success Rate: {match_success}/{len(matching_results['enhanced'])} ({match_success/len(matching_results['enhanced'])*100:.0f}%)")
    
    if match_success > 0:
        avg_match_time = sum(r.get("time", 0) for r in matching_results["enhanced"] if r.get("success")) / match_success
        avg_score = sum(r.get("score", 0) for r in matching_results["enhanced"] if r.get("success")) / match_success
        avg_confidence = sum(r.get("confidence", 0) for r in matching_results["enhanced"] if r.get("success")) / match_success
        
        print(f"\nAverage Response Time: {avg_match_time:.2f}s")
        print(f"Average Match Score: {avg_score:.2f}/10")
        print(f"Average Confidence: {avg_confidence:.2%}")
        
        with_breakdown = sum(1 for r in matching_results["enhanced"] if r.get("has_breakdown"))
        with_skills = sum(1 for r in matching_results["enhanced"] if r.get("has_skills_analysis"))
        
        print(f"\nStructured Output:")
        print(f"  Score Breakdown: {with_breakdown}/{match_success}")
        print(f"  Skills Analysis: {with_skills}/{match_success}")
    
    # Individual Match Results
    print("\n### CANDIDATE RANKING ###\n")
    
    successful_matches = [r for r in matching_results["enhanced"] if r.get("success")]
    successful_matches.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    for rank, match in enumerate(successful_matches, 1):
        print(f"{rank}. {match.get('candidate', 'Unknown')}")
        print(f"   Score: {match.get('score', 0):.2f}/10 | {match.get('recommendation', 'N/A')}")
    
    # Key Improvements
    print("\n### KEY IMPROVEMENTS ###\n")
    
    improvements = [
        "✓ Structured Pydantic validation for consistent output",
        "✓ Few-shot learning examples for better accuracy",
        "✓ Confidence scoring for reliability assessment",
        "✓ Career level classification",
        "✓ Skills categorization (technical vs soft vs tools)",
        "✓ Rubric-based scoring (Skills 40%, Experience 30%, Education 15%, Additional 15%)",
        "✓ Detailed score breakdown by category",
        "✓ Skills analysis (matching/missing/bonus)",
        "✓ Recommendation strength classification",
        "✓ Automatic retry logic with clarifications",
        "✓ Fallback structures for error handling"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")
    
    # Save detailed results to file
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "parsing_results": parsing_results,
        "matching_results": matching_results,
        "summary": {
            "parsing": {
                "original_success_rate": f"{original_success}/{len(parsing_results['original'])}",
                "enhanced_success_rate": f"{enhanced_success}/{len(parsing_results['enhanced'])}",
                "avg_original_time": avg_orig_time,
                "avg_enhanced_time": avg_enh_time
            },
            "matching": {
                "success_rate": f"{match_success}/{len(matching_results['enhanced'])}",
                "avg_score": avg_score if match_success > 0 else 0,
                "avg_confidence": avg_confidence if match_success > 0 else 0
            }
        }
    }
    
    with open("phase4_test_results.json", "w") as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print("\n✓ Detailed results saved to: phase4_test_results.json")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

async def main():
    """Run all tests."""
    print("\n🚀 Starting Phase 4 LLM Enhancement Tests...")
    
    try:
        # Test parsing
        parsing_results = await test_resume_parsing()
        
        # Test matching
        matching_results = await test_job_matching()
        
        # Generate report
        await generate_comparison_report(parsing_results, matching_results)
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
