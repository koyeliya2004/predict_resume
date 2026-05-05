from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_resume

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    resume_text: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Resume Analyzer is running!"}

@app.post("/analyze")
def analyze(request: ResumeRequest):
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    result = analyze_resume(request.resume_text)
    return result
