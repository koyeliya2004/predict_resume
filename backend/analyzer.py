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

# Real tech skills database
SKILLS_DB = [
    "Python", "JavaScript", "TypeScript", "React", "Next.js", "Vue.js", "Angular",
    "Node.js", "Express.js", "FastAPI", "Flask", "Django", "Spring Boot",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
    "Keras", "XGBoost", "LightGBM", "CatBoost",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "SQLite",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform", "CI/CD", "Jenkins",
    "Git", "GitHub", "GitLab", "Bitbucket",
    "Linux", "REST API", "GraphQL", "gRPC", "WebSockets",
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "SASS",
    "Java", "C++", "C", "Go", "Rust", "R", "Scala", "Kotlin",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
    "NLP", "Computer Vision", "LLM", "Hugging Face", "OpenCV", "NLTK", "spaCy",
    "Tableau", "Power BI", "Excel", "Spark", "Hadoop", "Kafka",
    "Selenium", "Pytest", "Jest", "JUnit", "Postman",
    "Figma", "Jira", "Agile", "Scrum"
]

# Role prediction based on skill sets
ROLE_RULES = [
    (["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn"], "ML/AI Engineer"),
    (["NLP", "NLTK", "spaCy", "Hugging Face", "LLM"], "NLP Engineer"),
    (["Computer Vision", "OpenCV", "YOLO"], "Computer Vision Engineer"),
    (["React", "Next.js", "Vue.js", "Angular", "HTML", "CSS", "Tailwind CSS"], "Frontend Developer"),
    (["Node.js", "FastAPI", "Flask", "Django", "Express.js", "Spring Boot"], "Backend Developer"),
    (["Docker", "Kubernetes", "CI/CD", "Terraform", "Jenkins", "AWS", "GCP", "Azure"], "DevOps/Cloud Engineer"),
    (["SQL", "PostgreSQL", "MySQL", "MongoDB", "Spark", "Hadoop", "Kafka", "Tableau", "Power BI"], "Data Engineer/Analyst"),
    (["React", "Node.js", "MongoDB", "FastAPI", "Flask", "PostgreSQL"], "Full Stack Developer"),
]

SKILL_CATEGORIES = {
    "Languages": ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust", "R", "Scala", "Kotlin"],
    "Frontend": ["React", "Next.js", "Vue.js", "Angular", "HTML", "CSS", "Tailwind CSS", "Bootstrap", "SASS"],
    "Backend": ["Node.js", "Express.js", "FastAPI", "Flask", "Django", "Spring Boot", "REST API", "GraphQL", "gRPC"],
    "ML/AI": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "NLP", "Computer Vision", "Hugging Face", "LLM", "OpenCV", "NLTK", "spaCy"],
    "Databases": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "SQLite"],
    "DevOps/Cloud": ["Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform", "CI/CD", "Jenkins", "Linux"],
    "Data Tools": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI", "Spark", "Hadoop", "Kafka"],
    "Tools": ["Git", "GitHub", "GitLab", "Jira", "Postman", "Figma", "Selenium", "Pytest", "Jest"],
}

def extract_skills(text):
    found = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return list(set(found))

def categorize_skills(skills):
    categorized = {}
    for cat, cat_skills in SKILL_CATEGORIES.items():
        matched = [s for s in skills if s in cat_skills]
        if matched:
            categorized[cat] = matched
    return categorized

def extract_experience_years(text):
    patterns = [
        r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'experience\s*(?:of)?\s*(\d+)[\+]?\s*(?:years?|yrs?)',
    ]
    matches = []
    for pat in patterns:
        matches += re.findall(pat, text, re.IGNORECASE)
    if matches:
        return max(int(m) for m in matches)
    return 0

def extract_education(text):
    degrees = ["B.Tech", "B.E", "B.Sc", "M.Tech", "M.Sc", "MCA", "BCA", "MBA", "Ph.D", "Bachelor", "Master", "Doctorate"]
    found = []
    for deg in degrees:
        if re.search(r'\b' + re.escape(deg) + r'\b', text, re.IGNORECASE):
            found.append(deg)
    return list(set(found))

def extract_email(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(?:\+91[\s-]?)?[6-9]\d{9}|(?:\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}', text)
    return match.group(0) if match else None

def extract_github(text):
    match = re.search(r'github\.com/([\w-]+)', text, re.IGNORECASE)
    return f"github.com/{match.group(1)}" if match else None

def extract_linkedin(text):
    match = re.search(r'linkedin\.com/in/([\w-]+)', text, re.IGNORECASE)
    return f"linkedin.com/in/{match.group(1)}" if match else None

def predict_role(skills):
    best_role = "Software Developer"
    best_score = 0
    for rule_skills, role in ROLE_RULES:
        score = sum(1 for s in skills if s in rule_skills)
        if score > best_score:
            best_score = score
            best_role = role
    return best_role

def compute_score(skills, experience, education):
    score = 0
    score += min(len(skills) * 3, 40)  # up to 40 pts for skills
    score += min(experience * 5, 30)    # up to 30 pts for experience
    score += 10 if education else 0     # 10 pts for education
    score += 5 if len(skills) > 10 else 0
    score += 5 if experience > 2 else 0
    # Bonus for having diverse skills
    cats = categorize_skills(skills)
    score += min(len(cats) * 2, 10)
    return min(score, 100)

def get_ats_score(text, skills):
    # ATS scoring based on keyword density and formatting
    score = 0
    word_count = len(text.split())
    if word_count > 200:
        score += 20
    if word_count > 400:
        score += 10
    score += min(len(skills) * 2, 30)
    if re.search(r'experience|work|employment', text, re.IGNORECASE):
        score += 10
    if re.search(r'education|degree|university|college', text, re.IGNORECASE):
        score += 10
    if re.search(r'project|portfolio|github', text, re.IGNORECASE):
        score += 10
    if re.search(r'achievement|award|certification', text, re.IGNORECASE):
        score += 10
    return min(score, 100)

def suggest_improvements(skills, experience, education, text):
    suggestions = []
    skill_set = set(s.lower() for s in skills)

    if "docker" not in skill_set:
        suggestions.append({"type": "skill", "msg": "Add Docker for containerization knowledge"})
    if "git" not in skill_set:
        suggestions.append({"type": "skill", "msg": "Mention Git version control experience"})
    if not any(c in skill_set for c in ["aws", "gcp", "azure"]):
        suggestions.append({"type": "skill", "msg": "Add cloud platform experience (AWS/GCP/Azure)"})
    if not any(db in skill_set for db in ["sql", "mysql", "postgresql", "mongodb"]):
        suggestions.append({"type": "skill", "msg": "Include database skills (SQL, MongoDB, etc.)"})
    if len(skills) < 6:
        suggestions.append({"type": "content", "msg": "List more technical skills to improve visibility"})
    if experience == 0:
        suggestions.append({"type": "content", "msg": "Explicitly mention years of experience or internship duration"})
    if not education:
        suggestions.append({"type": "content", "msg": "Add your educational qualifications clearly"})
    if not re.search(r'github\.com', text, re.IGNORECASE):
        suggestions.append({"type": "link", "msg": "Add your GitHub profile link to showcase projects"})
    if not re.search(r'linkedin\.com', text, re.IGNORECASE):
        suggestions.append({"type": "link", "msg": "Add your LinkedIn profile for professional presence"})
    if not re.search(r'project', text, re.IGNORECASE):
        suggestions.append({"type": "content", "msg": "Include a Projects section with descriptions and tech used"})
    return suggestions

def extract_name(text):
    try:
        entities = ner_pipeline(text[:512])
        for ent in entities:
            if ent["entity_group"] == "PER":
                return ent["word"]
    except Exception:
        pass
    first_line = text.strip().split('\n')[0].strip()
    return first_line[:60] if first_line else "Unknown"

def analyze_resume(text: str) -> dict:
    skills = extract_skills(text)
    experience = extract_experience_years(text)
    education = extract_education(text)
    role = predict_role(skills)
    suggestions = suggest_improvements(skills, experience, education, text)
    name = extract_name(text)
    score = compute_score(skills, experience, education)
    ats_score = get_ats_score(text, skills)
    categorized = categorize_skills(skills)

    return {
        "name": name,
        "contact": {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "github": extract_github(text),
            "linkedin": extract_linkedin(text),
        },
        "skills": skills,
        "skills_by_category": categorized,
        "experience_years": experience,
        "education": education,
        "predicted_role": role,
        "resume_score": score,
        "ats_score": ats_score,
        "suggestions": suggestions,
        "word_count": len(text.split()),
    }
