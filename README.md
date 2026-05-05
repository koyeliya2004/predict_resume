# 🧠 Resume Analyzer — AI Powered

A full-stack resume analysis tool using **BERT NER** (HuggingFace `dslim/bert-base-NER`) + **spaCy** for NLP-based resume parsing and evaluation.

## ✨ Features

- 📄 **Upload PDF / DOCX / TXT** or paste resume text directly
- 🎯 **Role Prediction** — predicts your best-fit job role (ML Engineer, Full Stack, DevOps, etc.)
- 🛠️ **Skills Detection** — categorized by Languages, Frontend, Backend, ML/AI, Databases, DevOps, Data Tools
- 📊 **Resume Score** — evaluated on skills diversity, experience, education, and content richness
- 🤖 **ATS Score** — Applicant Tracking System compatibility score
- 💡 **Improvement Suggestions** — actionable feedback for skill gaps, missing sections, and links
- 👤 **Contact Extraction** — detects email, phone, GitHub, LinkedIn using regex + NER
- 🎓 **Education Detection** — recognizes B.Tech, M.Tech, BCA, MCA, MBA, Ph.D, etc.

## 🏗️ Project Structure

```
predict_resume/
├── backend/
│   ├── main.py            # FastAPI server
│   ├── analyzer.py        # Core NLP analysis engine
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── index.html         # Main UI
    ├── style.css          # Dark theme design
    └── app.js             # API calls + result rendering
```

## 🚀 Setup & Run

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
```

### Frontend

Open `frontend/index.html` directly in your browser, or serve it with:

```bash
cd frontend
python -m http.server 3000
```

Then go to `http://localhost:3000`

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze/text` | Analyze raw text (JSON body: `{"text": "..."}`) |
| POST | `/analyze/file` | Analyze uploaded file (PDF/DOCX/TXT) |

## 🧩 Models Used

- **`dslim/bert-base-NER`** — HuggingFace pretrained BERT for Named Entity Recognition (extracts person names)
- **`en_core_web_sm`** — spaCy English model for text processing
- Custom rule-based extractors for skills, experience, education, contact details

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + Python |
| NLP | HuggingFace Transformers, spaCy |
| File Parsing | pdfplumber, python-docx |
| Frontend | Vanilla HTML/CSS/JS (dark theme) |

---
Made by [koyeliya2004](https://github.com/koyeliya2004)
