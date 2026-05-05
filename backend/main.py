from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pdfplumber
import docx
import io
from analyzer import analyze_resume

app = FastAPI(title="Resume Analyzer API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    jd_text: Optional[str] = None

def read_pdf(b):
    t=""
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        for p in pdf.pages:
            x=p.extract_text()
            if x: t+=x+"\n"
    return t.strip()

def read_docx(b):
    doc=docx.Document(io.BytesIO(b))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

@app.get("/")
def root():
    return {"message":"Resume Analyzer API v3.0 is running ✅","version":"3.0.0"}

@app.post("/analyze/text")
def analyze_text(req: TextRequest):
    if not req.text or len(req.text.strip())<50:
        raise HTTPException(400,"Resume text too short.")
    return analyze_resume(req.text, req.jd_text)

@app.post("/analyze/file")
async def analyze_file(file: UploadFile=File(...), jd_text: Optional[str]=Form(None)):
    content=await file.read()
    name=file.filename.lower()
    if name.endswith(".pdf"): text=read_pdf(content)
    elif name.endswith(".docx"): text=read_docx(content)
    elif name.endswith(".txt"): text=content.decode("utf-8",errors="ignore")
    else: raise HTTPException(400,"Upload PDF, DOCX or TXT only.")
    if not text or len(text.strip())<50:
        raise HTTPException(400,"Could not extract text from file.")
    return analyze_resume(text, jd_text)
