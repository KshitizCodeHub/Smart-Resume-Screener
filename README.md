<div align="center">

# 🎯 Smart Resume Screener

**AI-Powered Resume Screening and Intelligent Candidate Matching**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Google AI](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/KshitizCodeHub/Smart-Resume-Screener?style=social)](https://github.com/KshitizCodeHub/Smart-Resume-Screener/stargazers)

[Installation](#installation) • [Features](#key-features) • [API Documentation](#api-endpoints) • [Contributing](#contributing)

</div>

---

## 📹 Demo

<div align="center">

[**Watch Demo Video** ⏯️](./assets/demo-video.mp4)

</div>

---

## Overview

Smart Resume Screener is an AI-powered recruitment platform that automates resume screening and candidate evaluation. Built with Google's Gemini AI, it provides intelligent analysis and matching capabilities for modern hiring workflows.

### Key Features

- **AI-Powered Matching** - Semantic analysis using Google Gemini AI
- **Automated Processing** - PDF and DOCX resume parsing
- **Comprehensive Analytics** - Interactive dashboards and scoring metrics  
- **RESTful API** - Complete API with Swagger documentation
- **Modern Interface** - Responsive UI with dark/light themes
- **Enterprise Ready** - Secure, scalable architecture

---

## Tech Stack

**Backend:** Python 3.12+ • FastAPI • MongoDB • Google Gemini AI • Pydantic • Motor

**Frontend:** HTML5 • CSS3 • JavaScript • Chart.js

**Tools:** PyPDF2 • pdfplumber • python-docx • pytest • uvicorn

---

## Installation

### Prerequisites

- Python 3.12+
- MongoDB 8.0+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Setup

```bash
# Clone repository
git clone https://github.com/KshitizCodeHub/Smart-Resume-Screener.git
cd Smart-Resume-Screener

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env file)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=resume_screener_db
GEMINI_API_KEY=your_gemini_api_key_here

# Run application
uvicorn app.main:app --reload
```

**Access the application:**
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Usage

1. **Upload Resumes** - Upload PDF/DOCX resume files
2. **Create Jobs** - Define job descriptions and requirements
3. **Match Candidates** - Run AI-powered matching analysis
4. **Review Results** - View scores, justifications, and analytics

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/resumes` | Get all resumes |
| `POST` | `/api/resumes` | Upload resume |
| `GET` | `/api/jobs` | Get all jobs |
| `POST` | `/api/jobs` | Create job |
| `POST` | `/api/match` | Match resume with job |
| `GET` | `/api/analytics/*` | Analytics data |

**Full API Documentation:** http://localhost:8000/docs

---

## Testing

```bash
pytest                    # Run all tests
pytest --cov=app         # With coverage
pytest -v                # Verbose output
```

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open a Pull Request

**Code Standards:** Follow PEP 8, ensure tests pass, update documentation.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Google Gemini AI** - Language understanding
- **FastAPI Community** - Framework support
- **MongoDB** - Data storage
- **Chart.js** - Data visualization

---

<div align="center">

⭐ **Star this repository if you find it helpful**

---

**Smart Resume Screener** • Built with Google Gemini AI

</div>
