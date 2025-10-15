<div align="center">

# 🎯 Smart Resume Screener

### *AI-Powered Intelligent Resume Matching & Candidate Screening*

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-brightgreen.svg)](https://www.mongodb.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)](https://ai.google.dev/)

**Transform your hiring process with AI-driven resume analysis and intelligent candidate matching!**

---

### 🎥 Demo Video

<video width="100%" autoplay loop muted playsinline controls>
  <source src="./assets/demo-video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

</div>

## ✨ Overview

Smart Resume Screener revolutionizes recruitment by automatically analyzing resumes and intelligently matching candidates with job requirements using Google's Gemini AI.

### 🚀 Key Features

- 🤖 **AI-Powered Matching** - Advanced semantic understanding using Google Gemini
- 📊 **Interactive Analytics** - Beautiful data visualizations with real-time insights
- 🌓 **Modern UI/UX** - Sleek interface with dark/light mode
- ⚡ **Lightning Fast** - Asynchronous processing
- 📁 **Multi-Format Support** - Handles PDF and DOCX formats
- 🎯 **Smart Scoring** - Comprehensive evaluation (0-100 scale)

---

## 🛠️ Tech Stack

**Backend:** Python 3.12+ • FastAPI • MongoDB • Google Gemini AI  
**Frontend:** HTML5 • CSS3 • JavaScript • Chart.js  
**Key Libraries:** PyPDF2, pdfplumber, python-docx, Motor, pytest

---

## ⚡ Quick Start

### Prerequisites
- Python 3.12+
- MongoDB 8.0+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

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
GEMINI_API_KEY=your_api_key_here

# Run application
uvicorn app.main:app --reload
```

**Access:**
- 🌐 Application: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

---

## 🎯 Usage

1. **Upload Resumes** - Click "Upload Resume" and select PDF/DOCX files
2. **Add Jobs** - Create job descriptions with requirements
3. **Match** - Select resume and job, click "Match" for AI analysis
4. **Analyze** - View scores, justifications, and analytics dashboard

---

## � API Endpoints

```
GET/POST   /api/resumes       # Resume management
GET/POST   /api/jobs          # Job management  
POST       /api/match         # Match resume with job
GET        /api/analytics/*   # Analytics data
```

📚 **Full API Docs:** http://localhost:8000/docs

---

## 🧪 Testing

```bash
pytest                          # Run all tests
pytest --cov=app               # With coverage
pytest -v                      # Verbose output
```

---

## 🚧 Roadmap

- [ ] Email notifications
- [ ] Bulk resume processing
- [ ] Multi-language support
- [ ] Mobile app
- [ ] ATS integration
- [ ] Role-based access control

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

##  License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**Kshitiz**
- GitHub: [@KshitizCodeHub](https://github.com/KshitizCodeHub)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and ☕**

**Smart Resume Screener** - *Hire Smarter, Not Harder* 🎯

</div>