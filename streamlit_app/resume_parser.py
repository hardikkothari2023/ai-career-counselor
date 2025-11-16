import fitz               # pymupdf
import easyocr
import numpy as np
import re
import spacy

# init models
nlp = spacy.load("en_core_web_sm")
reader = easyocr.Reader(['en'], gpu=False)

# ------------------ Skill DB (tech + non-tech) ------------------
SKILLS_DB = [
    # technical
    "python","java","c","c++","c#","javascript","typescript","html","css","react","node",
    "angular","vue","bootstrap","django","flask","sql","mysql","postgresql","mongodb",
    "excel","power bi","tableau","data analysis","data science","machine learning",
    "deep learning","ai","ml","dl","nlp","opencv","pandas","numpy","matplotlib",
    "seaborn","keras","tensorflow","pytorch","scikit-learn","docker","kubernetes",
    "aws","azure","gcp","git","linux","jenkins","terraform","ci cd","devops",
    "network security","penetration testing","ethical hacking","cybersecurity",
    "data structures","algorithms","api development","microservices","system design",
    # soft / professional / tools
    "communication","teamwork","leadership","time management","problem solving",
    "analytical thinking","creativity","adaptability","critical thinking","decision making",
    "attention to detail","public speaking","project management","business analysis",
    "customer service","sales","marketing","presentation skills","management",
    "negotiation","research","documentation","figma","adobe xd","photoshop","illustrator",
    "jira","notion","microsoft office","word","powerpoint","slack","content writing",
    "blogging","seo","social media management","ui design","ux design","wireframing",
    "prototyping","user research"
]
# normalize SKILLS_DB to lowercase for safe matching
SKILLS_DB = [s.lower() for s in SKILLS_DB]

# ------------------ Degree + branch patterns ------------------
DEGREE_PATTERNS = [
    r"\b(b\.?\s*tech|btech|b\.?\s*e\b|be\b|bachelor|bsc\b|b\.sc\b|ba\b|bca\b)\b",
    r"\b(mtech|m\.?\s*tech|mca\b|msc\b|m\.?sc\b|master|mba)\b",
    r"\b(phd|ph\.?d)\b",
    r"\b(diploma|higher secondary|intermediate)\b"
]
BRANCH_PATTERNS = [
    r"computer science|cse|information technology|it|software engineering",
    r"electronics and communication|ece",
    r"mechanical|civil|electrical",
    r"data science|machine learning|artificial intelligence|ai|nlp|deep learning"
]

# ============================
# 1) OCR + text extraction (keeps paragraph lines)
# ============================
def extract_text_from_pdf(file_obj):
    """
    Uses PyMuPDF to render each page, EasyOCR to extract text lines.
    Returns a newline-joined string preserving line structure.
    """
    text_output = []
    file_obj.seek(0)

    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
        for page in doc:
            pix = page.get_pixmap()
            arr = np.frombuffer(pix.samples, dtype=np.uint8)
            channels = pix.n  # 3 or 4
            try:
                img = arr.reshape(pix.h, pix.w, channels)
            except Exception:
                # fallback: use PIL conversion if reshape fails
                from PIL import Image
                img = Image.frombytes("RGB", (pix.w, pix.h), pix.samples)
                img = np.array(img)

            # if 4 channels, drop alpha
            if img.ndim == 3 and img.shape[2] == 4:
                img = img[:, :, :3]

            # EasyOCR paragraph mode gives more natural grouping
            try:
                ocr_lines = reader.readtext(img, detail=0, paragraph=True)
            except Exception:
                # final fallback to line-mode
                ocr_lines = reader.readtext(img, detail=0)
            # keep lines
            if isinstance(ocr_lines, list):
                text_output.extend([ln.strip() for ln in ocr_lines if ln and ln.strip()])
            else:
                text_output.append(str(ocr_lines).strip())

    return "\n".join(text_output)


# ============================
# 2) Clean text before name extraction (remove links, emails, phones, long lines)
# ============================
def clean_text_before_name_extraction(text):
    cleaned = []
    for line in text.split("\n"):
        low = line.lower().strip()

        # remove obvious urls / handles
        if any(x in low for x in ["http", "www", ".com", "linkedin", "github", "drive.google"]):
            continue

        # remove email lines
        if "@" in low:
            continue

        # remove phone-like lines (heuristic)
        if re.search(r"\+?\d[\d\-\(\)\s]{6,}\d", low):
            continue

        # skip lines that are too long (not likely a name)
        if len(line.split()) > 6:
            continue

        # skip lines that look like section headers
        if low.strip() in {"summary", "education", "experience", "skills", "projects", "achievements", "contact"}:
            continue

        if line.strip():
            cleaned.append(line.strip())

    return "\n".join(cleaned)


# ============================
# 3) Robust name extraction
# ============================
def extract_name(text):
    """
    Robust name extractor:
    - run spaCy NER on text (prefer PERSON entities),
    - use regex fallback,
    - score candidates by position and length.
    """
    if not text or not text.strip():
        return "Unknown"

    doc = nlp(text)
    name_candidates = set()
    INVALID = {
        "resume","cv","profile","details","contact","email","phone","linkedin","github","about","summary"
    }

    # spaCy PERSON entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            nm = ent.text.strip()
            # skip noisy ones
            words = [w.lower() for w in nm.split()]
            if any(w in INVALID for w in words):
                continue
            # must be alphabetic when spaces removed
            if nm.replace(" ", "").isalpha():
                name_candidates.add(nm)

    # regex fallback (1-4 capitalized words)
    regex_matches = re.findall(r"\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+){0,3}\b", text)
    for r in regex_matches:
        lw = [w.lower() for w in r.split()]
        if any(w in INVALID for w in lw):
            continue
        # skip single-word generic headers
        if len(r.split()) >= 1 and len(r) <= 60:
            name_candidates.add(r)

    # Scoring function: position (top lines), length, not ALL CAPS
    def score(name):
        s = 0
        words = name.split()
        # prefer short names (1-3 words)
        if 1 <= len(words) <= 3:
            s += 10
        # penalty if all uppercase (likely header)
        if not name.isupper():
            s += 5
        # position bonus if appears in first 6 lines of original text
        lines = text.split("\n")[:8]
        if any(name in ln for ln in lines):
            s += 15
        # prefer names with proper capitalization
        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+){0,2}$", name):
            s += 5
        return s

    if not name_candidates:
        return "Unknown"

    return max(name_candidates, key=score)


# ============================
# 4) Education extraction
# ============================
def extract_education(text):
    text_lower = text.lower()
    degree = None
    for patt in DEGREE_PATTERNS:
        m = re.search(patt, text_lower)
        if m:
            degree_found = m.group().upper()
            # map to readable label
            if "BTECH" in degree_found or "B.TECH" in degree_found or "BTECH" in degree_found.lower():
                degree = "B.Tech"
            elif degree_found.strip() in {"BE", "B.E", "B E"}:
                degree = "B.E"
            elif "BCA" in degree_found:
                degree = "BCA"
            elif "BSC" in degree_found or "B.SC" in degree_found:
                degree = "B.Sc"
            elif "MTECH" in degree_found or "M.TECH" in degree_found:
                degree = "M.Tech"
            elif "MCA" in degree_found:
                degree = "MCA"
            elif "MSC" in degree_found or "M.SC" in degree_found:
                degree = "M.Sc"
            elif "MASTER" in degree_found or "MBA" in degree_found:
                degree = "Masters"
            elif "PHD" in degree_found or "PH.D" in degree_found:
                degree = "PhD"
            elif "DIPLOMA" in degree_found:
                degree = "Diploma"
            else:
                degree = degree_found.title()
            break

    # branch detection
    branch = None
    for patt in BRANCH_PATTERNS:
        m = re.search(patt, text_lower)
        if m:
            branch = m.group().title()
            break

    if degree and branch:
        return f"{degree} in {branch}"
    if degree:
        return degree
    # fallback: look for words like "Bachelor of Technology in Computer Science"
    m = re.search(r"(bachelor|master|associate)[\w\s\,\-]{0,60}in\s+([A-Za-z &]+)", text_lower)
    if m:
        deg = m.group(1).title()
        br = m.group(2).strip().title()
        return f"{deg} in {br}"

    return "Unknown"


# ============================
# 5) Skills extraction
# ============================
def extract_skills(text):
    """
    Match skill tokens and short n-grams against SKILLS_DB.
    Return sorted list of found skills (de-duplicated).
    """
    text_norm = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = text_norm.split()

    found = set()

    # match single token skills
    for t in tokens:
        if t in SKILLS_DB:
            found.add(t)

    # match multi-word skills from SKILLS_DB (bigram/phrase matching)
    text_join = " " + " ".join(tokens) + " "
    for skill in SKILLS_DB:
        if " " in skill and f" {skill} " in text_join:
            found.add(skill)

    # heuristic: check for acronyms commonly used
    acronyms = {"ml": "machine learning", "dl": "deep learning", "ai": "ai"}
    for a, full in acronyms.items():
        if re.search(rf"\b{a}\b", text_norm) and full in SKILLS_DB:
            found.add(full)

    return sorted(found)


# ============================
# 6) MAIN wrapper
# ============================
def extract_skills_from_pdf(uploaded_file):
    """
    Main entrypoint used by the Streamlit app.
    Returns: {"name": ..., "education": ..., "skills": [...]}.
    """
    text = extract_text_from_pdf(uploaded_file)
    cleaned_for_name = clean_text_before_name_extraction(text)

    return {
        "name": extract_name(cleaned_for_name),
        "education": extract_education(text),
        "skills": extract_skills(text)
    }
