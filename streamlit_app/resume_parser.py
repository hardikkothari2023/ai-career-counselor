import fitz
import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Expanded Skills Database (add more later)
SKILLS_DB = [

    # ---------------- TECHNICAL SKILLS ----------------
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "html", "css", "react", "node", "angular", "vue", "bootstrap",
    "django", "flask",

    # Data & ML
    "sql", "mysql", "postgresql", "mongodb", "power bi", "excel",
    "tableau", "data analysis", "data science", "machine learning",
    "deep learning", "ai", "ml", "dl", "nlp", "opencv", "pandas",
    "numpy", "matplotlib", "seaborn", "keras", "tensorflow",
    "pytorch", "scikit-learn",

    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "git",
    "linux", "jenkins", "terraform", "ci cd", "devops",

    # Cybersecurity
    "network security", "penetration testing", "ethical hacking",
    "cybersecurity", "firewalls", "vulnerability assessment",

    # Software Engineering
    "data structures", "algorithms", "api development",
    "microservices", "system design",

    # ---------------- SOFT SKILLS (NON-TECH) ----------------
    "communication", "teamwork", "leadership",
    "time management", "problem solving", "analytical thinking",
    "creativity", "adaptability", "critical thinking",
    "decision making", "attention to detail",
    "public speaking", "collaboration",

    # ---------------- PROFESSIONAL SKILLS ----------------
    "project management", "business analysis",
    "customer service", "sales", "marketing",
    "presentation skills", "management", "negotiation",
    "research", "documentation",

    # ---------------- TOOLS ----------------
    "figma", "adobe xd", "photoshop", "illustrator",
    "jira", "notion", "microsoft office", "word",
    "powerpoint", "slack",

    # ---------------- OTHER SKILLS ----------------
    "content writing", "blogging", "seo",
    "social media management", "ui design", "ux design",
    "wireframing", "prototyping", "user research"
]


# Degree Patterns
DEGREE_PATTERNS = [
    r"(b\.?tech|btech|b\.?e|be|bachelor|bsc|b\.sc|ba|bca)",
    r"(mtech|m\.?tech|mca|msc|m\.sc|master|mba)",
    r"(phd|ph\.?d)",
    r"(diploma|higher secondary|intermediate)"
]

# Branch / Field
BRANCH_PATTERNS = [
    r"computer science|cse|it|information technology",
    r"ece|electronics and communication",
    r"mechanical|civil|electrical",
    r"ai|machine learning|data science"
]

# ------------------ PDF TEXT EXTRACTION ------------------
def extract_text_from_pdf(file_obj):
    text = ""
    file_obj.seek(0)
    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text


# ------------------ NAME EXTRACTION ------------------
def extract_name(text):
    doc = nlp(text)

    INVALID_NAME_WORDS = {
        "resume", "curriculum", "vitae", "cv", "profile",
        "details", "contact", "name", "personal", "information"
    }

    # Step 1: NER candidates (PERSON)
    candidates = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            clean = ent.text.strip()
            # Skip if contains invalid words
            words = clean.lower().split()
            if not any(w in INVALID_NAME_WORDS for w in words):
                # skip likely non-name patterns with digits
                if not any(char.isdigit() for char in clean):
                    if 2 <= len(clean.split()) <= 4:
                        candidates.append(clean)

    if candidates:
        # choose shortest or first
        return min(candidates, key=lambda x: len(x.split()))

    # Step 2: Use top few lines heuristic
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, line in enumerate(lines[:5]):  # look first up to 5 lines
        words = line.split()
        if 2 <= len(words) <= 4:
            lw = [w.lower() for w in words]
            if not any(w in INVALID_NAME_WORDS for w in lw):
                if not any(ch.isdigit() for ch in line):
                    return line

    # Step 3: Regex fallback
    name_pattern = r"[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+){1,3}"
    match = re.search(name_pattern, text)
    if match:
        candidate = match.group()
        if all(w.lower() not in INVALID_NAME_WORDS for w in candidate.lower().split()):
            return candidate

    return "Unknown"




# ------------------ DEGREE EXTRACTION ------------------
def extract_education(text):
    text_lower = text.lower()

    # 1. Find degree
    degree = None
    for pattern in DEGREE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            degree = match.group().upper()
            break

    # Standardize
    if degree:
        if "BTECH" in degree or "B.TECH" in degree: degree = "B.Tech"
        elif degree in ["BE","B.E","B E"]: degree = "B.E"
        elif "BCA" in degree: degree = "BCA"
        elif "BSC" in degree or "B.SC" in degree: degree = "B.Sc"
        elif "MTECH" in degree: degree = "M.Tech"
        elif "MSC" in degree: degree = "M.Sc"
        elif "MCA" in degree: degree = "MCA"
        elif "MASTER" in degree: degree = "Masters"
        elif "PHD" in degree: degree = "PhD"
        elif "DIPLOMA" in degree: degree = "Diploma"

    # 2. Detect Branch / Field
    branch = None
    for pattern in BRANCH_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            branch = match.group().title()
            break

    # 3. Combine degree + branch
    if degree and branch:
        return f"{degree} in {branch}"
    elif degree:
        return degree

    # Default fallback
    return "Bachelor"


# ------------------ SKILLS EXTRACTION ------------------
def extract_skills(text):
    words = text.lower().replace("-", " ").replace("/", " ")
    found = set()

    for skill in SKILLS_DB:
        if skill in words:
            found.add(skill)

    return list(found)


# ------------------ MAIN FUNCTION ------------------
def extract_skills_from_pdf(uploaded_file):
    text = extract_text_from_pdf(uploaded_file)

    return {
        "name": extract_name(text),
        "education": extract_education(text),
        "skills": extract_skills(text)
    }
