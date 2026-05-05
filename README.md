# 🧠 AI Resume Analyzer

> A full-stack AI-powered Resume Analyzer built with **React + Tailwind CSS** (Frontend) and **FastAPI + spaCy/HuggingFace** (Backend). Upload your resume and get instant AI feedback on skills, experience, and job role prediction.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) ![React](https://img.shields.io/badge/React-18-61DAFB?logo=react) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi) ![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 📄 Upload PDF or plain text resume
- 🤖 Extracts **Name, Skills, Experience, Education** using NLP (spaCy NER)
- 🏷️ Predicts **Job Role/Category** using a pretrained classifier (HuggingFace)
- 📊 Skill gap analysis with suggestions
- ⚡ Fast REST API with FastAPI
- 🎨 Clean, responsive UI with React + Tailwind CSS

---

## 🗂️ Project Structure

```
predict_resume/
├── frontend/                 # React + Tailwind CSS
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── UploadForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── SkillBadge.jsx
│   │   └── index.css
│   ├── package.json
│   └── tailwind.config.js
├── backend/                  # FastAPI + Python
│   ├── main.py
│   ├── analyzer.py
│   ├── requirements.txt
│   └── model/
│       └── (pretrained model files)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js >= 18
- Python >= 3.10
- pip

---

### 🔧 Backend Setup (FastAPI)

```bash
# 1. Navigate to backend folder
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Run the server
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

---

### 🎨 Frontend Setup (React)

```bash
# 1. Navigate to frontend folder
cd frontend

# 2. Install dependencies
npm install

# 3. Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

> Make sure the backend is running before using the frontend!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Upload resume text/PDF, returns analysis |
| `GET`  | `/health` | Health check |

### Example Request

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "John Doe, Python Developer, 3 years experience..."}'
```

### Example Response

```json
{
  "name": "John Doe",
  "skills": ["Python", "FastAPI", "Machine Learning"],
  "experience_years": 3,
  "predicted_role": "Backend Developer",
  "education": "B.Tech CSE",
  "suggestions": ["Add Docker skills", "Mention cloud platforms"]
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Tailwind CSS, Vite |
| Backend | FastAPI, Python 3.10+ |
| NLP Model | spaCy (`en_core_web_sm`) |
| ML Model | HuggingFace `dslim/bert-base-NER` |
| PDF Parsing | PyMuPDF (fitz) |
| Deployment | Vercel (frontend) + Render (backend) |

---

## ☁️ Deployment

### Deploy Backend on Render
1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your `predict_resume` repo
4. Set root directory to `backend`
5. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`

### Deploy Frontend on Vercel
1. Go to [vercel.com](https://vercel.com) → New Project
2. Connect your `predict_resume` repo
3. Set root directory to `frontend`
4. Update API URL in `src/App.jsx` to your Render backend URL
5. Deploy!

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 👩‍💻 Author

**Koyeliya Ghosh** — [@koyeliya2004](https://github.com/koyeliya2004)  
CSE Student | MAKAUT | ML & Full-Stack Enthusiast

---

## 📄 License

MIT License — see [LICENSE](LICENSE)
