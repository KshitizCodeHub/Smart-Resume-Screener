<div align="center">

# 🎯 Smart Resume Screener

### *AI-Powered Intelligent Resume Matching & Candidate Screening*

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-brightgreen.svg)](https://www.mongodb.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Transform your hiring process with AI-driven resume analysis and intelligent candidate matching!**

[🚀 Features](#-features) • [📸 Screenshots](#-screenshots) • [🛠️ Tech Stack](#️-tech-stack) • [⚡ Quick Start](#-quick-start) • [📖 Documentation](#-documentation)

---

</div>

## ✨ Overview

**Smart Resume Screener** is a cutting-edge AI-powered application that revolutionizes the recruitment process by automatically analyzing resumes, extracting key information, and intelligently matching candidates with job requirements. Powered by Google's Gemini AI, it provides comprehensive scoring, detailed justifications, and actionable insights to help you find the perfect candidate faster.

### 🎥 Demo Video

<div align="center">

<video width="100%" controls>
  <source src="./assets/demo-video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

**📹 [Download Demo Video](./assets/demo-video.mp4)** *(Click if video doesn't play)*

</div>

### 🎥 What Makes It Special?

- 🤖 **AI-Powered Matching**: Advanced LLM integration using Google Gemini for semantic understanding
- 📊 **Interactive Analytics**: Beautiful data visualizations with real-time insights
- 🌓 **Modern UI/UX**: Sleek interface with dark/light mode support
- ⚡ **Lightning Fast**: Asynchronous processing for optimal performance
- 📁 **Multi-Format Support**: Handles PDF and DOCX resume formats seamlessly
- 🎯 **Smart Scoring**: Comprehensive evaluation with detailed breakdowns

---

## 🚀 Features

### 📄 **Resume Processing**
- ✅ Upload multiple resumes (PDF/DOCX formats)
- ✅ Automatic text extraction and parsing
- ✅ Intelligent skill detection and categorization
- ✅ Experience and education extraction
- ✅ Contact information parsing (email, phone)

### 💼 **Job Description Management**
- ✅ Create and manage job postings
- ✅ Define required skills and qualifications
- ✅ Specify experience requirements
- ✅ Set educational criteria

### 🎯 **Intelligent Matching**
- ✅ AI-powered semantic matching using Google Gemini
- ✅ Comprehensive scoring (0-100 scale)
- ✅ Detailed match justification
- ✅ Skills gap analysis
- ✅ Confidence level indicators
- ✅ Personalized recommendations

### 📊 **Advanced Analytics Dashboard**
- ✅ **Skills Match Overview**: Visual breakdown of candidate skills alignment
- ✅ **Score Distribution**: Histogram showing candidate score ranges
- ✅ **Top Candidates**: Quick view of highest-scoring applicants
- ✅ **Match Quality Metrics**: Comprehensive performance indicators
- ✅ **Real-time Updates**: Live data synchronization

### 🎨 **User Experience**
- ✅ Modern, responsive design
- ✅ Dark/light theme toggle
- ✅ Intuitive navigation
- ✅ Loading states and animations
- ✅ Error handling with user-friendly messages
- ✅ Mobile-responsive layout

---

## 📸 Screenshots

<div align="center">

### 🏠 Dashboard Overview
*Main interface showing uploaded resumes and job descriptions*

### 📊 Match Analytics
*Interactive charts displaying candidate scores and skill matches*

### 🎯 Detailed Match Results
*Comprehensive scoring with AI-generated justifications*

### 🌓 Dark Mode
*Sleek dark theme for comfortable viewing*

</div>

---

## 🛠️ Tech Stack

### **Backend**
| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core Language | 3.12+ |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | Web Framework | 0.115+ |
| ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white) | Database | 8.0+ |
| ![Google AI](https://img.shields.io/badge/Google_AI-4285F4?style=flat&logo=google&logoColor=white) | LLM Integration | Gemini 1.5 |

### **Frontend**
| Technology | Purpose |
|------------|---------|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | Structure |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | Styling |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Interactivity |
| ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white) | Data Visualization |

### **Key Libraries**
- **Document Processing**: PyPDF2, pdfplumber, python-docx
- **Async Operations**: Motor (async MongoDB driver)
- **AI/ML**: Google Generative AI SDK
- **Testing**: pytest, pytest-asyncio, httpx
- **Validation**: Pydantic

---

## ⚡ Quick Start

### 📋 Prerequisites

Before you begin, ensure you have the following installed:
- 🐍 Python 3.12 or higher
- 🍃 MongoDB 8.0 or higher (running locally or MongoDB Atlas)
- 🔑 Google Gemini API key ([Get one here](https://ai.google.dev/))

### 🔧 Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/smart-resume-screener.git
cd smart-resume-screener
```

2️⃣ **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
```

**Required environment variables:**
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=resume_screener_db

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

5️⃣ **Start MongoDB**
```bash
# If running locally
mongod

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in .env with your Atlas connection string
```

6️⃣ **Run the application**
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

7️⃣ **Open your browser**
```
🌐 Application: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
📖 ReDoc: http://localhost:8000/redoc
```

---

## 🎯 Usage Guide

### 1️⃣ Upload Resumes
- Click **"Upload Resume"** button
- Select PDF or DOCX files
- System automatically extracts text, skills, and contact info
- View uploaded resumes in the dashboard

### 2️⃣ Add Job Descriptions
- Click **"Add Job Description"** button
- Fill in job title, description, and requirements
- Specify required skills and qualifications
- Save the job posting

### 3️⃣ Match Resumes with Jobs
- Select a resume from the uploaded list
- Choose a job description to match against
- Click **"Match"** button
- View detailed matching results with:
  - Overall match score (0-100)
  - AI-generated justification
  - Skills alignment breakdown
  - Missing qualifications
  - Confidence level
  - Personalized recommendations

### 4️⃣ Analyze Results
- Navigate to **"Match Analytics"** tab
- View interactive charts:
  - Skills Match Overview
  - Score Distribution
  - Top Candidates
- Export results for further analysis

---

## 📖 Documentation

### 📁 Project Structure
```
smart-resume-screener/
├── 📂 app/
│   ├── 📂 api/              # API endpoints
│   │   └── routes.py        # REST API routes
│   ├── 📂 database/         # Database configuration
│   │   └── mongodb.py       # MongoDB connection
│   ├── 📂 models/           # Data models
│   │   ├── resume.py        # Resume schema
│   │   ├── job.py           # Job description schema
│   │   └── match.py         # Match result schema
│   ├── 📂 services/         # Business logic
│   │   ├── pdf_parser.py    # Document parsing
│   │   ├── text_extractor.py # Text extraction
│   │   ├── matcher.py       # Matching logic
│   │   └── llm_service_enhanced.py # AI integration
│   ├── 📂 static/           # Static files
│   │   ├── css/
│   │   │   └── styles.css   # Application styles
│   │   └── js/
│   │       └── app.js       # Frontend logic
│   ├── 📂 templates/        # HTML templates
│   │   └── index.html       # Main UI
│   └── main.py              # Application entry point
├── 📂 tests/                # Test suite
│   ├── conftest.py          # Test configuration
│   ├── test_api.py          # API tests
│   ├── test_parser.py       # Parser tests
│   └── test_llm.py          # LLM tests
├── 📄 requirements.txt      # Python dependencies
├── 📄 .env.example          # Environment template
├── 📄 pytest.ini            # Test configuration
└── 📄 README.md             # This file
```

### 🔌 API Endpoints

#### **Resume Endpoints**
```http
GET    /api/resumes          # Get all resumes
POST   /api/resumes          # Upload new resume
GET    /api/resumes/{id}     # Get resume by ID
DELETE /api/resumes/{id}     # Delete resume
```

#### **Job Endpoints**
```http
GET    /api/jobs             # Get all jobs
POST   /api/jobs             # Create new job
GET    /api/jobs/{id}        # Get job by ID
PUT    /api/jobs/{id}        # Update job
DELETE /api/jobs/{id}        # Delete job
```

#### **Match Endpoints**
```http
POST   /api/match            # Match resume with job
GET    /api/matches          # Get all matches
GET    /api/matches/{id}     # Get match by ID
```

#### **Analytics Endpoints**
```http
GET    /api/analytics/overview    # Get analytics overview
GET    /api/analytics/skills      # Get skills statistics
GET    /api/analytics/scores      # Get score distribution
```

**📚 For detailed API documentation, visit**: `http://localhost:8000/docs`

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

**Test Coverage:**
- ✅ API endpoint testing
- ✅ Document parsing tests
- ✅ LLM service mocking
- ✅ Database operations
- ✅ Score calculation logic

---

## 🎨 Features in Detail

### 🤖 AI-Powered Matching Algorithm

The matching system uses Google's Gemini 1.5 Pro model with advanced prompting techniques:

1. **Context Building**: Combines resume data and job requirements
2. **Semantic Analysis**: LLM understands context beyond keyword matching
3. **Comprehensive Scoring**: Multi-dimensional evaluation including:
   - Technical skills match
   - Experience relevance
   - Educational background
   - Soft skills alignment
4. **Detailed Justification**: Human-readable explanations
5. **Actionable Insights**: Recommendations for both candidates and recruiters

### 📊 Analytics Dashboard

**Skills Match Overview:**
- Doughnut chart showing skills alignment percentage
- Color-coded segments (matched vs. missing skills)
- Interactive tooltips

**Score Distribution:**
- Bar chart displaying candidate score ranges
- Categories: Excellent (80-100), Good (60-79), Average (40-59), Below Average (0-39)
- Real-time updates

**Top Candidates:**
- Ranked list of highest-scoring matches
- Quick-view cards with key metrics
- One-click access to detailed results

### 🌓 Theme Support

- **Light Mode**: Clean, professional appearance for daytime use
- **Dark Mode**: Eye-friendly dark theme for extended sessions
- **Persistent Preference**: Theme selection saved in browser
- **Smooth Transitions**: Animated theme switching

---

## 🔒 Security & Privacy

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Input validation and sanitization
- ✅ MongoDB injection prevention
- ✅ CORS configuration for API security
- ✅ File upload restrictions (size and type)
- ✅ Secure document parsing

---

## 🚧 Roadmap

### 🎯 Upcoming Features
- [ ] 📧 Email integration for candidate notifications
- [ ] 📊 Advanced analytics with ML-based insights
- [ ] 🔄 Bulk resume processing
- [ ] 🌍 Multi-language support
- [ ] 📱 Mobile app development
- [ ] 🔗 ATS (Applicant Tracking System) integration
- [ ] 📈 Historical trend analysis
- [ ] 🤝 Collaborative hiring workflows
- [ ] 🔐 Role-based access control
- [ ] ☁️ Cloud deployment guides (AWS, Azure, GCP)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✍️ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

### 📝 Contribution Guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Follow PEP 8 style guide for Python code
- Ensure all tests pass before submitting PR

---

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature suggestion? Please open an issue on GitHub with:

- 🐞 **Bug Reports**: Detailed description, steps to reproduce, expected vs actual behavior
- 💡 **Feature Requests**: Clear description of the feature and its benefits
- 📸 **Screenshots**: If applicable, include screenshots or recordings

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- 🎨 UI/UX inspiration from modern design systems
- 🤖 Google Gemini AI for powerful language understanding
- 📊 Chart.js for beautiful data visualizations
- 🚀 FastAPI community for excellent documentation
- 🍃 MongoDB for flexible data storage
- 💡 Open-source community for inspiration and support

---

## 📞 Support

Need help? Have questions?

- 📖 **Documentation**: Check the `/docs` folder
- 💬 **Discussions**: Join GitHub Discussions
- 🐛 **Issues**: Report bugs on GitHub Issues
- 📧 **Email**: your.email@example.com

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and ☕**

![GitHub stars](https://img.shields.io/github/stars/yourusername/smart-resume-screener?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/smart-resume-screener?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/smart-resume-screener?style=social)

---

**Smart Resume Screener** - *Hire Smarter, Not Harder* 🎯

</div>
