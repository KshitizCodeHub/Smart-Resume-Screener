"""
Simple Manual Test Helper
Creates sample test files for you to upload through the UI
"""
import os
from pathlib import Path

# Create test_data directory
test_dir = Path("test_data")
test_dir.mkdir(exist_ok=True)

print("📁 Creating test files in 'test_data' folder...")

# Sample Resume 1 - Strong Match for Backend Role
resume1 = """
ALEX JOHNSON
Email: alex.johnson@email.com | Phone: (555) 123-4567 | LinkedIn: linkedin.com/in/alexjohnson
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Senior Backend Engineer with 7 years of experience building scalable web applications using Python, 
FastAPI, and cloud technologies. Proven track record of leading teams and delivering high-performance systems.

WORK EXPERIENCE

Senior Backend Engineer | TechCorp Inc. | San Francisco, CA | Jan 2020 - Present
• Led development of microservices architecture using Python and FastAPI, serving 1M+ users
• Designed and implemented RESTful APIs with 99.9% uptime
• Managed team of 5 engineers, conducted code reviews, and mentored junior developers
• Optimized database queries in PostgreSQL and MongoDB, reducing response time by 60%
• Implemented CI/CD pipelines using Docker, Kubernetes, and Jenkins
• Migrated legacy Flask applications to FastAPI, improving performance by 3x

Software Engineer | StartupXYZ | San Francisco, CA | Jun 2017 - Dec 2019
• Developed backend services using Python, Flask, and Django
• Worked with PostgreSQL, Redis, and MongoDB databases
• Built authentication and authorization systems using JWT
• Collaborated with frontend team to design and implement REST APIs
• Wrote comprehensive unit and integration tests achieving 90%+ coverage

Junior Developer | WebSolutions | Remote | Jan 2016 - May 2017
• Built web applications using Python and JavaScript
• Maintained MySQL databases and wrote SQL queries
• Fixed bugs and added features to existing codebases

EDUCATION
Bachelor of Science in Computer Science | Stanford University | 2016
GPA: 3.8/4.0 | Dean's List 2014-2016

SKILLS
Languages: Python, JavaScript, TypeScript, SQL, Bash
Frameworks: FastAPI, Flask, Django, Express.js, React
Databases: PostgreSQL, MongoDB, Redis, MySQL
DevOps: Docker, Kubernetes, AWS, GCP, Jenkins, GitLab CI/CD
Other: REST APIs, Microservices, Agile/Scrum, Git, Linux

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Docker Certified Associate (2021)
"""

# Sample Resume 2 - Moderate Match for Backend Role
resume2 = """
MARIA GARCIA
maria.garcia@email.com | (555) 987-6543 | GitHub: github.com/mariagarcia
Boston, MA

ABOUT ME
Full Stack Developer with 4 years of experience building web applications. 
Passionate about learning new technologies and solving complex problems.

PROFESSIONAL EXPERIENCE

Full Stack Developer | Digital Agency | Boston, MA | Mar 2021 - Present
• Develop full-stack web applications using React, Node.js, and Express
• Work with MongoDB and PostgreSQL databases
• Create responsive UIs with React, Redux, and Material-UI
• Implement REST APIs for mobile and web applications
• Use Git for version control and collaborate with team of 8 developers

Junior Developer | Local Startup | Boston, MA | Jun 2020 - Feb 2021
• Built features for e-commerce platform using JavaScript and Python
• Worked with Django and Flask frameworks
• Maintained MySQL database and wrote queries
• Fixed bugs and improved code quality

EDUCATION
BS in Information Technology | Boston University | 2020
Relevant Courses: Data Structures, Algorithms, Web Development, Databases

TECHNICAL SKILLS
Frontend: React, JavaScript, HTML, CSS, Redux, Bootstrap
Backend: Node.js, Express, Python, Flask, Django
Databases: MongoDB, PostgreSQL, MySQL
Tools: Git, Docker, VS Code, Postman, npm

PROJECTS
• E-commerce Platform: Built full-stack app with React and Node.js
• Blog CMS: Created content management system using Django
• Weather App: Developed API integration using Python and FastAPI
"""

# Sample Resume 3 - Weak Match for Backend Role (Frontend focused)
resume3 = """
CHRIS ANDERSON
chris.anderson@email.com | (555) 456-7890
Los Angeles, CA

PROFILE
Creative Frontend Developer with strong design skills and 3 years of experience 
building beautiful, user-friendly web interfaces.

WORK HISTORY

Frontend Developer | Creative Studio | Los Angeles, CA | Jan 2022 - Present
• Design and develop responsive websites using HTML, CSS, and JavaScript
• Create interactive UIs with React and Vue.js
• Work closely with designers to implement pixel-perfect designs
• Use Figma and Adobe XD for prototyping
• Optimize websites for performance and SEO

Web Designer | Marketing Agency | Los Angeles, CA | Jun 2021 - Dec 2021
• Designed websites and landing pages
• Built WordPress sites for clients
• Created graphics using Photoshop and Illustrator
• Basic JavaScript for interactive elements

EDUCATION
Associate Degree in Web Design | Community College | 2021

SKILLS
Design: Figma, Adobe XD, Photoshop, Illustrator
Frontend: HTML, CSS, JavaScript, React, Vue.js, Sass
CMS: WordPress, Webflow
Other: Git, npm, Responsive Design, SEO
"""

# Sample Job Description - Backend Engineer
job_desc = """
SENIOR BACKEND ENGINEER

ABOUT THE ROLE
We are seeking an experienced Senior Backend Engineer to join our growing engineering team. 
You will be responsible for designing, developing, and maintaining scalable backend services 
that power our platform used by millions of users.

REQUIREMENTS
• 5+ years of professional software development experience
• Strong proficiency in Python (FastAPI, Flask, or Django)
• Experience with REST API design and development
• Solid understanding of databases (PostgreSQL, MongoDB, or similar)
• Experience with Docker and containerization
• Knowledge of cloud platforms (AWS, GCP, or Azure)
• Experience with microservices architecture
• Strong problem-solving and debugging skills
• Excellent communication and teamwork abilities

PREFERRED QUALIFICATIONS
• Experience with Kubernetes and orchestration
• Knowledge of CI/CD pipelines (Jenkins, GitLab CI, or similar)
• Experience leading or mentoring other engineers
• Bachelor's degree in Computer Science or related field
• Familiarity with message queues (RabbitMQ, Kafka, etc.)
• Experience with Redis or other caching solutions

RESPONSIBILITIES
• Design and develop high-quality, scalable backend services
• Build and maintain RESTful APIs
• Optimize application performance and database queries
• Write clean, maintainable, and well-tested code
• Participate in code reviews and technical discussions
• Mentor junior engineers and share knowledge
• Collaborate with frontend developers and product managers
• Monitor and troubleshoot production issues

WHAT WE OFFER
• Competitive salary and equity
• Health, dental, and vision insurance
• 401(k) with company match
• Flexible work arrangements (hybrid/remote options)
• Professional development budget
• Great team culture and modern tech stack
"""

# Write files
files_created = []

with open(test_dir / "resume_strong_match.txt", "w", encoding="utf-8") as f:
    f.write(resume1)
    files_created.append("resume_strong_match.txt")

with open(test_dir / "resume_moderate_match.txt", "w", encoding="utf-8") as f:
    f.write(resume2)
    files_created.append("resume_moderate_match.txt")

with open(test_dir / "resume_weak_match.txt", "w", encoding="utf-8") as f:
    f.write(resume3)
    files_created.append("resume_weak_match.txt")

with open(test_dir / "job_backend_engineer.txt", "w", encoding="utf-8") as f:
    f.write(job_desc)
    files_created.append("job_backend_engineer.txt")

print("\n✅ Successfully created test files:\n")
for file in files_created:
    print(f"   📄 {file}")

print(f"\n📍 Location: {test_dir.absolute()}")

print("\n" + "="*70)
print("🧪 HOW TO USE THESE FILES")
print("="*70)

print("""
1. Open the frontend in your browser (double-click frontend/index.html)

2. UPLOAD RESUMES:
   • Go to Upload tab
   • Upload: resume_strong_match.txt (should score HIGH 8-9/10)
   • Upload: resume_moderate_match.txt (should score MEDIUM 6-7/10)
   • Upload: resume_weak_match.txt (should score LOW 3-4/10)

3. CREATE JOB:
   • Copy content from job_backend_engineer.txt
   • Paste into Job Description field
   • Title: "Senior Backend Engineer"
   • Click Upload

4. MATCH & COMPARE:
   • Go to Match tab
   • Select the job
   • Check all 3 resumes
   • Click "Match Resumes"
   • Wait 20-30 seconds
   • COMPARE THE SCORES!

EXPECTED RESULTS:
✅ Alex Johnson (Resume 1) → Score 8-9/10 → STRONG_FIT
✅ Maria Garcia (Resume 2) → Score 6-7/10 → GOOD_FIT or POTENTIAL_FIT
✅ Chris Anderson (Resume 3) → Score 3-5/10 → WEAK_FIT or NOT_RECOMMENDED

This will validate that the AI is correctly evaluating candidates! 🎯
""")

print("="*70)
print("🚀 Ready to test! Good luck!")
print("="*70)
