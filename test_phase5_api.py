"""
Phase 5: Comprehensive API Testing Suite
Tests all endpoints and functionality of the Smart Resume Screener.
"""
import httpx
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 30.0

# Test data storage
test_data = {
    "resume_ids": [],
    "job_ids": [],
    "match_ids": []
}

# Test results
results = {
    "passed": 0,
    "failed": 0,
    "total": 0,
    "tests": []
}

def log_test(name: str, passed: bool, message: str = ""):
    """Log test result."""
    results["total"] += 1
    if passed:
        results["passed"] += 1
        status = "✅ PASSED"
    else:
        results["failed"] += 1
        status = "❌ FAILED"
    
    results["tests"].append({
        "name": name,
        "passed": passed,
        "message": message
    })
    
    print(f"{status} - {name}")
    if message:
        print(f"        {message}")

async def test_health_check():
    """Test 1: Health check endpoint."""
    print("\n🧪 TEST 1: Health Check")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                log_test("Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        log_test("Health Check", False, f"Error: {str(e)}")
        return False

async def test_root_endpoint():
    """Test 2: Root API endpoint."""
    print("\n🧪 TEST 2: Root Endpoint")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/api")
            
            if response.status_code == 200:
                data = response.json()
                log_test("Root Endpoint", True, f"Message: {data.get('message')}")
                return True
            else:
                log_test("Root Endpoint", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        log_test("Root Endpoint", False, f"Error: {str(e)}")
        return False

async def test_upload_resume_text():
    """Test 3: Upload resume as text."""
    print("\n🧪 TEST 3: Upload Resume (Text)")
    
    resume_text = """
John Smith
Email: john.smith@email.com | Phone: (555) 123-4567
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Senior Software Engineer with 8 years of experience in Python and web development.

WORK EXPERIENCE
Senior Software Engineer | Tech Corp | Jan 2020 - Present
- Led development of microservices using Python and FastAPI
- Managed team of 5 developers
- Reduced deployment time by 60%

Software Engineer | StartupXYZ | Jun 2017 - Dec 2019
- Developed REST APIs using Flask
- Worked with PostgreSQL and MongoDB databases

EDUCATION
BS Computer Science | MIT | 2017

SKILLS
Python, JavaScript, FastAPI, Flask, React, Docker, Kubernetes, PostgreSQL, MongoDB
Team Leadership, Agile, Problem Solving
"""
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Create a mock file upload
            files = {
                "file": ("test_resume.txt", resume_text, "text/plain")
            }
            
            response = await client.post(
                f"{BASE_URL}/api/upload-resume",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                resume_id = data.get("data", {}).get("resume_id")
                
                if resume_id:
                    test_data["resume_ids"].append(resume_id)
                    log_test("Upload Resume (Text)", True, f"Resume ID: {resume_id[:8]}...")
                    return True
                else:
                    log_test("Upload Resume (Text)", False, "No resume ID returned")
                    return False
            else:
                log_test("Upload Resume (Text)", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Upload Resume (Text)", False, f"Error: {str(e)}")
        return False

async def test_create_job():
    """Test 4: Create job description."""
    print("\n🧪 TEST 4: Create Job Description")
    
    job_data = {
        "title": "Senior Backend Engineer",
        "description": """
We are looking for a Senior Backend Engineer with strong Python experience.

Requirements:
- 5+ years of Python development experience
- Experience with FastAPI or Flask
- Strong database skills (PostgreSQL, MongoDB)
- Docker and Kubernetes knowledge
- REST API design experience
- Cloud platforms (AWS, Azure, or GCP)

Preferred:
- Microservices architecture experience
- Team leadership experience
- BS in Computer Science

Responsibilities:
- Design and develop scalable backend services
- Mentor junior developers
- Participate in code reviews
- Optimize application performance
        """,
        "requirements": {
            "required_skills": ["Python", "FastAPI", "Flask", "PostgreSQL", "MongoDB", "Docker", "Kubernetes"],
            "preferred_skills": ["AWS", "Microservices", "Team Leadership"],
            "experience_required": "5+ years",
            "education_required": "BS Computer Science (preferred)"
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/upload-job",
                json=job_data
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract job ID from message (format: "Job description created successfully. ID: {id}")
                message = data.get("message", "")
                if "ID:" in message:
                    job_id = message.split("ID:")[1].strip()
                    test_data["job_ids"].append(job_id)
                    log_test("Create Job", True, f"Job ID: {job_id[:8]}...")
                    return True
                else:
                    log_test("Create Job", False, "No job ID in response")
                    return False
            else:
                log_test("Create Job", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Create Job", False, f"Error: {str(e)}")
        return False

async def test_get_all_resumes():
    """Test 5: Get all resumes."""
    print("\n🧪 TEST 5: Get All Resumes")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/api/resumes")
            
            if response.status_code == 200:
                data = response.json()
                resumes = data.get("resumes", [])
                count = len(resumes)
                log_test("Get All Resumes", True, f"Found {count} resume(s)")
                return True
            else:
                log_test("Get All Resumes", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Get All Resumes", False, f"Error: {str(e)}")
        return False

async def test_get_all_jobs():
    """Test 6: Get all jobs."""
    print("\n🧪 TEST 6: Get All Jobs")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/api/jobs")
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("jobs", [])
                count = len(jobs)
                log_test("Get All Jobs", True, f"Found {count} job(s)")
                return True
            else:
                log_test("Get All Jobs", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Get All Jobs", False, f"Error: {str(e)}")
        return False

async def test_match_resume_with_job():
    """Test 7: Match resume with job."""
    print("\n🧪 TEST 7: Match Resume with Job")
    
    if not test_data["resume_ids"] or not test_data["job_ids"]:
        log_test("Match Resume with Job", False, "No resume or job IDs available")
        return False
    
    match_data = {
        "job_id": test_data["job_ids"][0],
        "resume_ids": [test_data["resume_ids"][0]]
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:  # Longer timeout for LLM
            response = await client.post(
                f"{BASE_URL}/api/match",
                json=match_data
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])
                
                if matches:
                    match = matches[0]
                    score = match.get("score", 0)
                    recommendation = match.get("recommendation", "N/A")
                    log_test("Match Resume with Job", True, 
                            f"Score: {score:.1f}/10, Recommendation: {recommendation}")
                    return True
                else:
                    log_test("Match Resume with Job", False, "No matches returned")
                    return False
            else:
                log_test("Match Resume with Job", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Match Resume with Job", False, f"Error: {str(e)}")
        return False

async def test_get_resume_by_id():
    """Test 8: Get specific resume."""
    print("\n🧪 TEST 8: Get Resume by ID")
    
    if not test_data["resume_ids"]:
        log_test("Get Resume by ID", False, "No resume IDs available")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resume_id = test_data["resume_ids"][0]
            response = await client.get(f"{BASE_URL}/api/resumes/{resume_id}")
            
            if response.status_code == 200:
                data = response.json()
                resume = data.get("resume", {})
                name = resume.get("parsed_data", {}).get("name", "Unknown")
                log_test("Get Resume by ID", True, f"Name: {name}")
                return True
            else:
                log_test("Get Resume by ID", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Get Resume by ID", False, f"Error: {str(e)}")
        return False

async def test_get_job_by_id():
    """Test 9: Get specific job."""
    print("\n🧪 TEST 9: Get Job by ID")
    
    if not test_data["job_ids"]:
        log_test("Get Job by ID", False, "No job IDs available")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            job_id = test_data["job_ids"][0]
            response = await client.get(f"{BASE_URL}/api/jobs/{job_id}")
            
            if response.status_code == 200:
                data = response.json()
                job = data.get("job", {})
                title = job.get("title", "Unknown")
                log_test("Get Job by ID", True, f"Title: {title}")
                return True
            else:
                log_test("Get Job by ID", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Get Job by ID", False, f"Error: {str(e)}")
        return False

async def test_delete_resume():
    """Test 10: Delete resume."""
    print("\n🧪 TEST 10: Delete Resume")
    
    if not test_data["resume_ids"]:
        log_test("Delete Resume", False, "No resume IDs available")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resume_id = test_data["resume_ids"][0]
            response = await client.delete(f"{BASE_URL}/api/resumes/{resume_id}")
            
            if response.status_code == 200:
                log_test("Delete Resume", True, f"Deleted resume {resume_id[:8]}...")
                return True
            else:
                log_test("Delete Resume", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Delete Resume", False, f"Error: {str(e)}")
        return False

async def test_delete_job():
    """Test 11: Delete job."""
    print("\n🧪 TEST 11: Delete Job")
    
    if not test_data["job_ids"]:
        log_test("Delete Job", False, "No job IDs available")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            job_id = test_data["job_ids"][0]
            response = await client.delete(f"{BASE_URL}/api/jobs/{job_id}")
            
            if response.status_code == 200:
                log_test("Delete Job", True, f"Deleted job {job_id[:8]}...")
                return True
            else:
                log_test("Delete Job", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Delete Job", False, f"Error: {str(e)}")
        return False

def print_summary():
    """Print test summary."""
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    print(f"\nTotal Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    
    if results['total'] > 0:
        percentage = (results['passed'] / results['total']) * 100
        print(f"Success Rate: {percentage:.1f}%")
    
    if results['failed'] > 0:
        print("\n❌ Failed Tests:")
        for test in results['tests']:
            if not test['passed']:
                print(f"  • {test['name']}: {test['message']}")
    
    print("\n" + "="*70)
    
    if results['failed'] == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Phase 5.1 (API Testing) - COMPLETE")
        print("🚀 Ready for Phase 5.2 (Integration Testing)")
    else:
        print(f"⚠️ {results['failed']} test(s) failed - review and fix")
    
    print("="*70)

async def main():
    """Run all API tests."""
    print("\n" + "="*70)
    print("🧪 PHASE 5: API TESTING SUITE")
    print("="*70)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests in sequence
    await test_health_check()
    await test_root_endpoint()
    await test_upload_resume_text()
    await test_create_job()
    await test_get_all_resumes()
    await test_get_all_jobs()
    await test_match_resume_with_job()
    await test_get_resume_by_id()
    await test_get_job_by_id()
    await test_delete_resume()
    await test_delete_job()
    
    # Print summary
    print_summary()
    
    # Save results to file
    with open("phase5_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: phase5_test_results.json")

if __name__ == "__main__":
    print("\n⚠️ Make sure the server is running at http://127.0.0.1:8000")
    print("   Run: python -m uvicorn app.main:app --reload")
    input("\nPress Enter to start testing...")
    
    asyncio.run(main())
