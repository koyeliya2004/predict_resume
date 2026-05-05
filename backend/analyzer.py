import spacy
import re
from transformers import pipeline

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Pretrained HuggingFace NER pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

# Common tech skills keyword list
SKILLS_DB = [
    "Python", "JavaScript", "React", "Node.js", "FastAPI", "Flask", "Django",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
    "SQL", "MongoDB", "PostgreSQL", "Docker", "Kubernetes", "AWS", "GCP", "Azure",
    "Git", "GitHub", "Linux", "REST API", "HTML", "CSS", "Tailwind", "TypeScript",
    "Java", "C++", "C", "R", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "NLP", "Computer Vision", "LLM", "Hugging Face", "Keras", "OpenCV"
]

# Simple role prediction based on skill keywords
ROLE_MAP = {
    "Machine Learning": "ML Engineer",
    "Deep Learning": "AI/ML Engineer",
    "React": "Frontend Developer",
    "Node.js": "Full Stack Developer",
    "FastAPI": "Backend Developer",
    "Flask": "Backend Developer",
    "Django": "Backend Developer",
    "SQL": "Data Analyst",
    "TensorFlow": "ML Engineer",
    "PyTorch": "ML Engineer",
    "Computer Vision": "Computer Vision Engineer",
    "NLP": "NLP Engineer",
    "Docker": "DevOps Engineer",
    "Kubernetes": "DevOps Engineer",
}

def extract_skills(text):
    found = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return list(set(found))

def extract_experience_years(text):
    matches = re.findall(r'(\d+)[\+]?\s*(?:years?|yrs?)', text, re.IGNORECASE)
    if matches:
        return max(int(m) for m in matches)
    return 0

def predict_role(skills):
    for skill in skills:
        if skill in ROLE_MAP:
            return ROLE_MAP[skill]
    return "Software Developer"

def suggest_skills(skills):
    suggestions = []
    skill_set = set(s.lower() for s in skills)
    if "docker" not in skill_set:
        suggestions.append("Add Docker for containerization")
    if "git" not in skill_set:
        suggestions.append("Mention Git/GitHub experience")
    if "aws" not in skill_set and "gcp" not in skill_set and "azure" not in skill_set:
        suggestions.append("Add cloud platform experience (AWS/GCP/Azure)")
    if "sql" not in skill_set and "mongodb" not in skill_set:
        suggestions.append("Include database skills (SQL or MongoDB)")
    if len(skills) < 5:
        suggestions.append("List more technical skills for better visibility")
    return suggestions

def extract_name(text):
    entities = ner_pipeline(text[:512])  # limit input for speed
    for ent in entities:
        if ent["entity_group"] == "PER":
            return ent["word"]
    # fallback: first line
    first_line = text.strip().split('\n')[0]
    return first_line[:50] if first_line else "Unknown"

def analyze_resume(text: str) -> dict:
    skills = extract_skills(text)
    experience = extract_experience_years(text)
    role = predict_role(skills)
    suggestions = suggest_skills(skills)
    name = extract_name(text)

    return {
        "name": name,
        "skills": skills,
        "experience_years": experience,
        "predicted_role": role,
        "suggestions": suggestions,
    }
