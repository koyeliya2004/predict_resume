from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import docx
import io
import os
from analyzer import analyze_resume

app = FastAPI(
    title="Resume Analyzer API",
    description="Analyze resumes using NLP and pretrained models",
    version="2.0.0"
)

# Allow requests from Vercel frontend and localhost
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://*.vercel.app",
    "https://predict-resume.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ALLOWED_ORIGINS after getting your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


@app.get("/")
def root():
    return {"message": "Resume Analyzer API is running", "version": "2.0.0"}


@app.post("/analyze/text")
def analyze_text(request: TextRequest):
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume text too short. Please provide full resume content.")
    return analyze_resume(request.text)


@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(content)
    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF, DOCX, or TXT.")

    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Could not extract meaningful text from file.")

    return analyze_resume(text)
