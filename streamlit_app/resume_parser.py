# import fitz               # PyMuPDF
# import easyocr
# import numpy as np
# import re
# import spacy

# # Load models
# nlp = spacy.load("en_core_web_sm")
# reader = easyocr.Reader(['en'], gpu=False)

# # ----------------------------------------------------------
# # Skills DB (Tech + Non-Tech)
# # ----------------------------------------------------------
# SKILLS_DB = [
#     # technical skills
#     "python","java","c","c++","c#","javascript","typescript","html","css","react","node",
#     "angular","vue","bootstrap","django","flask","sql","mysql","postgresql","mongodb",
#     "excel","power bi","tableau","data analysis","data science","machine learning",
#     "deep learning","ai","ml","nlp","opencv","pandas","numpy","matplotlib","seaborn",
#     "keras","tensorflow","pytorch","scikit-learn","docker","kubernetes","aws","azure",
#     "gcp","git","linux","jenkins","terraform","ci cd","devops",
#     "network security","penetration testing","ethical hacking","cybersecurity",
#     "data structures","algorithms","api development","microservices","system design",

#     # soft skills
#     "communication","teamwork","leadership","time management","problem solving",
#     "analytical thinking","creativity","adaptability","critical thinking",
#     "decision making","attention to detail","public speaking",

#     # professional
#     "project management","business analysis","customer service","sales","marketing",
#     "presentation skills","management","negotiation","research","documentation",

#     # tools
#     "figma","adobe xd","photoshop","illustrator","jira","notion","microsoft office",
#     "word","powerpoint","slack",

#     # misc
#     "content writing","blogging","seo","social media management",
#     "ui design","ux design","wireframing","prototyping","user research"
# ]

# SKILLS_DB = [s.lower() for s in SKILLS_DB]   # normalize

# # ----------------------------------------------------------
# # Degree / Branch Patterns
# # ----------------------------------------------------------
# DEGREE_PATTERNS = [
#     r"\b(b\.?\s*tech|btech|b\.e|be|bachelor|bsc|b\.sc|ba|bca)\b",
#     r"\b(mtech|m\.tech|mca|msc|m\.sc|master|mba)\b",
#     r"\b(phd|ph\.d)\b",
#     r"\b(diploma|higher secondary|intermediate)\b"
# ]

# BRANCH_PATTERNS = [
#     r"computer science|cse|information technology|it",
#     r"electronics and communication|ece",
#     r"mechanical|civil|electrical",
#     r"data science|machine learning|ai|deep learning"
# ]

# # ----------------------------------------------------------
# # 1) Extract TEXT using OCR + PyMuPDF
# # ----------------------------------------------------------
# def extract_text_from_pdf(file_obj):
#     text_list = []
#     file_obj.seek(0)

#     with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
#         for page in doc:
#             pix = page.get_pixmap()
#             arr = np.frombuffer(pix.samples, dtype=np.uint8)

#             try:
#                 img = arr.reshape(pix.h, pix.w, pix.n)
#             except:
#                 from PIL import Image
#                 img = Image.frombytes("RGB", (pix.w, pix.h), pix.samples)
#                 img = np.array(img)

#             if img.ndim == 3 and img.shape[2] == 4:
#                 img = img[:, :, :3]

#             ocr_lines = reader.readtext(img, detail=0, paragraph=True)

#             if isinstance(ocr_lines, list):
#                 text_list.extend([x.strip() for x in ocr_lines if x and x.strip()])

#     return "\n".join(text_list)

# # ----------------------------------------------------------
# # 2) Clean BEFORE name extraction
# # ----------------------------------------------------------
# def clean_text_before_name_extraction(text):
#     cleaned = []
#     for line in text.split("\n"):
#         low = line.lower().strip()

#         if any(x in low for x in ["http", "www", ".com", "linkedin", "github", "drive.google"]):
#             continue
#         if "@" in low:
#             continue
#         if re.search(r"\+?\d[\d\-\(\)\s]{6,}\d", low):
#             continue
#         if len(line.split()) > 5:
#             continue

#         cleaned.append(line.strip())

#     return "\n".join(cleaned)

# # ----------------------------------------------------------
# # 3) ROBUST NAME EXTRACTOR (fixed all errors)
# # ----------------------------------------------------------
# def extract_name(text):
#     doc = nlp(text)

#     INVALID = {
#         "resume","cv","profile","contact","details","email","phone",
#         "linkedin","github","summary","projects"
#     }

#     candidates = set()

#     # spaCy PERSON detection
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             nm = ent.text.strip()
#             if nm.replace(" ", "").isalpha() and not any(w in INVALID for w in nm.lower().split()):
#                 candidates.add(nm)

#     # regex fallback
#     regex_matches = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3}\b", text)
#     for m in regex_matches:
#         if not any(w in INVALID for w in m.lower().split()):
#             candidates.add(m)

#     # choose best candidate
#     def score(name):
#         score = 0
#         if name in text.split("\n")[:5]:
#             score += 10
#         if 1 <= len(name.split()) <= 3:
#             score += 10
#         if not name.isupper():
#             score += 5
#         return score

#     if not candidates:
#         return "Unknown"

#     return max(candidates, key=score)

# # ----------------------------------------------------------
# # 4) EDUCATION EXTRACTION
# # ----------------------------------------------------------
# def extract_education(text):
#     low = text.lower()
#     degree = None

#     for patt in DEGREE_PATTERNS:
#         m = re.search(patt, low)
#         if m:
#             tok = m.group().upper()
#             if "BTECH" in tok or "B.TECH" in tok: degree = "B.Tech"
#             elif tok in ["BE","B.E"]: degree = "B.E"
#             elif "BCA" in tok: degree = "BCA"
#             elif "BSC" in tok: degree = "B.Sc"
#             elif "MTECH" in tok or "M.TECH" in tok: degree = "M.Tech"
#             elif "MCA" in tok: degree = "MCA"
#             elif "MSC" in tok or "M.SC" in tok: degree = "M.Sc"
#             elif "MBA" in tok: degree = "MBA"
#             elif "PHD" in tok: degree = "PhD"
#             else: degree = tok.title()
#             break

#     branch = None
#     for patt in BRANCH_PATTERNS:
#         m = re.search(patt, low)
#         if m:
#             branch = m.group().title()
#             break

#     if degree and branch:
#         return f"{degree} in {branch}"
#     if degree:
#         return degree
#     return "Unknown"

# # ----------------------------------------------------------
# # 5) SKILLS EXTRACTION
# # ----------------------------------------------------------
# def extract_skills(text):
#     text_norm = re.sub(r"[^\w\s]", " ", text.lower())
#     tokens = text_norm.split()

#     found = set()

#     # single-token
#     for t in tokens:
#         if t in SKILLS_DB:
#             found.add(t)

#     # multi-word
#     joined = " " + " ".join(tokens) + " "
#     for skill in SKILLS_DB:
#         if " " in skill and f" {skill} " in joined:
#             found.add(skill)

#     return sorted(found)

# # ----------------------------------------------------------
# # 6) MAIN WRAPPER
# # ----------------------------------------------------------
# def extract_skills_from_pdf(uploaded_file):
#     text = extract_text_from_pdf(uploaded_file)
#     clean_name_text = clean_text_before_name_extraction(text)

#     return {
#         "name": extract_name(clean_name_text),
#         "education": extract_education(text),
#         "skills": extract_skills(text)
#     }
# resume_parser.py
import fitz               # PyMuPDF
import io
import re
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import spacy
import logging

# ------------------------------------------------------------
# 🚫 Disable Tesseract completely (Streamlit Cloud CANNOT run it)
# ------------------------------------------------------------
pytesseract = None
TESSERACT_AVAILABLE = False

# EasyOCR (lazy-load)
_easyocr_reader = None

# OpenCV support
try:
    import cv2
    OPENCV_AVAILABLE = True
except:
    cv2 = None
    OPENCV_AVAILABLE = False

nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------- SKILLS DB ----------------
SKILLS_DB = [
    "python","java","c","c++","c#","javascript","typescript","html","css","react","node",
    "angular","vue","bootstrap","django","flask","sql","mysql","postgresql","mongodb",
    "excel","power bi","tableau","data analysis","data science","machine learning",
    "deep learning","ai","ml","nlp","opencv","pandas","numpy","matplotlib","seaborn",
    "keras","tensorflow","pytorch","scikit-learn","docker","kubernetes","aws","azure",
    "gcp","git","linux","jenkins","terraform","ci cd","devops",
    "network security","penetration testing","ethical hacking","cybersecurity",
    "data structures","algorithms","api development","microservices","system design",
    "communication","teamwork","leadership","time management","problem solving",
    "analytical thinking","creativity","adaptability","critical thinking",
    "decision making","attention to detail","public speaking",
    "project management","business analysis","customer service","sales","marketing",
    "presentation skills","management","negotiation","research","documentation",
    "figma","adobe xd","photoshop","illustrator","jira","notion","microsoft office",
    "word","powerpoint","slack","content writing","blogging","seo","social media management",
    "ui design","ux design","wireframing","prototyping","user research"
]
SKILLS_DB = [s.lower() for s in SKILLS_DB]

# ---------------- OCR HELPERS ----------------

def _init_easyocr():
    """Load EasyOCR only once."""
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(['en'], gpu=False)
        except Exception as e:
            logger.error("EasyOCR init failed: %s", e)
            _easyocr_reader = None
    return _easyocr_reader


def deskew_cv2_image(img):
    """Deskew using OpenCV."""
    if not OPENCV_AVAILABLE:
        return img
    try:
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        if coords.size == 0:
            return img
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(np.array(img), M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return Image.fromarray(rotated)
    except:
        return img


def enhance_for_ocr(img):
    """Light enhancement."""
    img = img.convert("RGB")
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageOps.autocontrast(img)

    # Upscale (helps small text)
    w, h = img.size
    if max(w, h) < 2000:
        img = img.resize((w * 2, h * 2), Image.LANCZOS)

    return img


def ocr_image_with_easyocr(img):
    """Run EasyOCR only."""
    reader = _init_easyocr()
    if reader is None:
        return ""
    arr = np.array(img)
    try:
        text_lines = reader.readtext(arr, detail=0, paragraph=True)
        return "\n".join(text_lines)
    except:
        text_lines = reader.readtext(arr, detail=0)
        return "\n".join(text_lines)


def ocr_image_multi_scale(img):
    """Main OCR Engine (EasyOCR ONLY)."""
    try:
        img = deskew_cv2_image(img)
    except:
        pass

    img = enhance_for_ocr(img)

    try:
        txt = ocr_image_with_easyocr(img)
        return txt.strip()
    except:
        return ""

# ---------------- TEXT EXTRACT FROM PDF ----------------

def extract_text_from_pdf(file_obj):
    text_list = []
    file_obj.seek(0)
    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
        for page_num in range(len(doc)):
            pix = doc.load_page(page_num).get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            text = ocr_image_multi_scale(img)
            if text:
                text_list.append(text)
    return "\n\n".join(text_list)


# ---------------- CLEAN NAME EXTRACTION ----------------

def clean_text_before_name_extraction(text):
    cleaned = []
    if not text:
        return ""
    for line in text.split("\n"):
        low = line.lower().strip()
        if any(x in low for x in ["http", "www", ".com", "linkedin", "github"]):
            continue
        if "@" in low:
            continue
        if re.search(r"\+?\d[\d\-\(\)\s]{6,}\d", low):
            continue
        if len(line.split()) > 6:
            continue
        if low in {"summary","education","experience","skills","projects","achievements","contact","objective"}:
            continue
        if line.strip():
            cleaned.append(line.strip())
    return "\n".join(cleaned)


# ---------------- NAME, EDUCATION, SKILLS ----------------

def extract_name(text):
    if not text:
        return "Unknown"
    doc = nlp(text)
    candidates = {
        ent.text.strip() for ent in doc.ents
        if ent.label_ == "PERSON"
    }
    if not candidates:
        return "Unknown"
    return next(iter(candidates))


def extract_education(text):
    low = text.lower()
    if "btech" in low or "b.tech" in low:
        return "B.Tech"
    if "bsc" in low:
        return "B.Sc"
    if "be" in low:
        return "B.E"
    if "mtech" in low:
        return "M.Tech"
    if "mca" in low:
        return "MCA"
    if "msc" in low:
        return "M.Sc"
    if "mba" in low:
        return "MBA"
    return "Unknown"


def extract_skills(text):
    if not text:
        return []
    tokens = re.sub(r"[^\w\s]", " ", text.lower()).split()
    found = {t for t in tokens if t in SKILLS_DB}

    joined = " " + " ".join(tokens) + " "
    for skill in SKILLS_DB:
        if " " in skill and f" {skill} " in joined:
            found.add(skill)

    return sorted(found)

# ---------------- MAIN WRAPPER ----------------

def extract_skills_from_pdf(uploaded_file):
    text = extract_text_from_pdf(uploaded_file)
    cleaned = clean_text_before_name_extraction(text)

    name = extract_name(cleaned)
    education = extract_education(text)
    skills = extract_skills(text)

    return {
        "name": name,
        "education": education,
        "skills": skills
    }

