import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

_ner_pipeline = None

def get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline is None:
        try:
            from transformers import pipeline
            _ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
        except Exception:
            _ner_pipeline = False
    return _ner_pipeline if _ner_pipeline else None


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

ROLE_RULES = [
    (["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn"], "ML/AI Engineer"),
    (["NLP", "NLTK", "spaCy", "Hugging Face", "LLM"], "NLP Engineer"),
    (["Computer Vision", "OpenCV"], "Computer Vision Engineer"),
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
    return list({skill for skill in SKILLS_DB if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)})

def categorize_skills(skills):
    return {cat: [s for s in skills if s in cat_skills] for cat, cat_skills in SKILL_CATEGORIES.items() if any(s in cat_skills for s in skills)}

def extract_experience_years(text):
    matches = re.findall(r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)', text, re.IGNORECASE)
    matches += re.findall(r'experience\s*(?:of)?\s*(\d+)[\+]?\s*(?:years?|yrs?)', text, re.IGNORECASE)
    return max(int(m) for m in matches) if matches else 0

def extract_education(text):
    degrees = ["B.Tech", "B.E", "B.Sc", "M.Tech", "M.Sc", "MCA", "BCA", "MBA", "Ph.D", "Bachelor", "Master", "Doctorate"]
    return list({d for d in degrees if re.search(r'\b' + re.escape(d) + r'\b', text, re.IGNORECASE)})

def extract_email(text):
    m = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
    return m.group(0) if m else None

def extract_phone(text):
    m = re.search(r'(?:\+91[\s-]?)?[6-9]\d{9}|(?:\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}', text)
    return m.group(0) if m else None

def extract_github(text):
    m = re.search(r'github\.com/([\w-]+)', text, re.IGNORECASE)
    return f"github.com/{m.group(1)}" if m else None

def extract_linkedin(text):
    m = re.search(r'linkedin\.com/in/([\w-]+)', text, re.IGNORECASE)
    return f"linkedin.com/in/{m.group(1)}" if m else None

def extract_name(text):
    ner = get_ner_pipeline()
    if ner:
        try:
            for ent in ner(text[:512]):
                if ent["entity_group"] == "PER":
                    return ent["word"]
        except Exception:
            pass
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    for line in text.strip().split('\n'):
        line = line.strip()
        if line and 2 < len(line) < 60 and not re.search(r'[@http]|resume|cv|summary|objective', line, re.IGNORECASE):
            return line
    return "Unknown"

def predict_role(skills):
    best_role, best_score = "Software Developer", 0
    for rule_skills, role in ROLE_RULES:
        score = sum(1 for s in skills if s in rule_skills)
        if score > best_score:
            best_score, best_role = score, role
    return best_role

def compute_score(skills, experience, education):
    score = min(len(skills) * 3, 40) + min(experience * 5, 30)
    score += 10 if education else 0
    score += 5 if len(skills) > 10 else 0
    score += 5 if experience > 2 else 0
    score += min(len(categorize_skills(skills)) * 2, 10)
    return min(score, 100)

def get_ats_score(text, skills):
    score = 0
    wc = len(text.split())
    if wc > 200: score += 20
    if wc > 400: score += 10
    score += min(len(skills) * 2, 30)
    for kw in ['experience|work|employment', 'education|degree|university', 'project|portfolio|github', 'achievement|award|certification']:
        if re.search(kw, text, re.IGNORECASE): score += 10
    return min(score, 100)

def match_job_description(resume_skills, jd_text):
    jd_skills = extract_skills(jd_text)
    if not jd_skills:
        return {"match_score": 0, "matched_skills": [], "missing_skills": [], "jd_skills_total": 0}
    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    return {"match_score": int(len(matched)/len(jd_skills)*100), "matched_skills": matched, "missing_skills": missing, "jd_skills_total": len(jd_skills)}

def get_section_checklist(text):
    return {
        "Contact Info": bool(re.search(r'email|phone|linkedin|github|@', text, re.IGNORECASE)),
        "Summary/Objective": bool(re.search(r'summary|objective|profile|about', text, re.IGNORECASE)),
        "Skills": bool(re.search(r'skill|technologies|tech stack|tools', text, re.IGNORECASE)),
        "Experience": bool(re.search(r'experience|work|employment|internship', text, re.IGNORECASE)),
        "Education": bool(re.search(r'education|degree|university|college|b\.tech|m\.tech|bca|mca', text, re.IGNORECASE)),
        "Projects": bool(re.search(r'project|built|developed|created|implemented', text, re.IGNORECASE)),
        "Certifications": bool(re.search(r'certification|certified|certificate|course', text, re.IGNORECASE)),
        "Achievements": bool(re.search(r'achievement|award|honor|winner|rank|prize', text, re.IGNORECASE)),
    }

def suggest_improvements(skills, experience, education, text):
    suggestions = []
    skill_set = set(s.lower() for s in skills)
    if "docker" not in skill_set: suggestions.append({"type": "skill", "msg": "Add Docker for containerization knowledge"})
    if "git" not in skill_set: suggestions.append({"type": "skill", "msg": "Mention Git version control experience"})
    if not any(c in skill_set for c in ["aws", "gcp", "azure"]): suggestions.append({"type": "skill", "msg": "Add cloud platform experience (AWS/GCP/Azure)"})
    if not any(db in skill_set for db in ["sql", "mysql", "postgresql", "mongodb"]): suggestions.append({"type": "skill", "msg": "Include database skills (SQL, MongoDB, etc.)"})
    if len(skills) < 6: suggestions.append({"type": "content", "msg": "List more technical skills to improve ATS visibility"})
    if experience == 0: suggestions.append({"type": "content", "msg": "Explicitly mention years of experience or internship duration"})
    if not education: suggestions.append({"type": "content", "msg": "Add your educational qualifications clearly"})
    if not re.search(r'github\.com', text, re.IGNORECASE): suggestions.append({"type": "link", "msg": "Add your GitHub profile link to showcase projects"})
    if not re.search(r'linkedin\.com', text, re.IGNORECASE): suggestions.append({"type": "link", "msg": "Add your LinkedIn profile for professional presence"})
    if not re.search(r'project', text, re.IGNORECASE): suggestions.append({"type": "content", "msg": "Include a Projects section with tech stack and impact"})
    if not re.search(r'certification|certified', text, re.IGNORECASE): suggestions.append({"type": "content", "msg": "Add certifications (Coursera, Google, AWS, etc.) to stand out"})
    return suggestions

def analyze_resume(text: str, jd_text: str = None) -> dict:
    skills = extract_skills(text)
    experience = extract_experience_years(text)
    education = extract_education(text)
    return {
        "name": extract_name(text),
        "contact": {"email": extract_email(text), "phone": extract_phone(text), "github": extract_github(text), "linkedin": extract_linkedin(text)},
        "skills": skills,
        "skills_by_category": categorize_skills(skills),
        "experience_years": experience,
        "education": education,
        "predicted_role": predict_role(skills),
        "resume_score": compute_score(skills, experience, education),
        "ats_score": get_ats_score(text, skills),
        "suggestions": suggest_improvements(skills, experience, education, text),
        "section_checklist": get_section_checklist(text),
        "jd_match": match_job_description(skills, jd_text) if jd_text else None,
        "word_count": len(text.split()),
    }
