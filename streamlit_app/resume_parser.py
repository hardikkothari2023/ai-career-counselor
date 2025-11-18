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

# Try to import pytesseract, if not available fallback to EasyOCR at runtime
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except Exception:
    pytesseract = None
    TESSERACT_AVAILABLE = False

# Lazy import EasyOCR only if needed (keeps startup light)
_easyocr_reader = None

# OpenCV for deskew and preprocessing
try:
    import cv2
    OPENCV_AVAILABLE = True
except Exception:
    cv2 = None
    OPENCV_AVAILABLE = False

nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------- SKILLS DB (same as before, normalized)
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

# Degree / Branch Patterns (kept similar)
DEGREE_PATTERNS = [
    r"\b(b\.?\s*tech|btech|b\.?e\b|be\b|bachelor|bsc\b|b\.sc\b|ba\b|bca\b)\b",
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


# ---------------- IMAGE PREPROCESSING HELPERS ----------------
def pil_to_cv2(img: Image.Image):
    arr = np.array(img)
    if arr.ndim == 2:
        return arr
    # RGB -> BGR for cv2
    return arr[:, :, ::-1].copy()


def cv2_to_pil(img_cv):
    if img_cv.ndim == 2:
        return Image.fromarray(img_cv)
    # BGR -> RGB
    return Image.fromarray(img_cv[:, :, ::-1])


def deskew_cv2_image(img: Image.Image):
    """Deskew using OpenCV if available, otherwise return original."""
    if not OPENCV_AVAILABLE:
        return img
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


def enhance_for_ocr(img: Image.Image):
    """Apply contrast, sharpening, denoise and resize to improve OCR."""
    # convert to RGB
    img = img.convert("RGB")

    # small blur removal and sharpen
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.SHARPEN)

    # autocontrast and enhance
    img = ImageOps.autocontrast(img)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    # upscale (helps small text)
    w, h = img.size
    scale = 2 if max(w, h) < 2000 else 1
    if scale > 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    return img


# ---------------- CORE OCR: TESSERACT (with fallback)
def _init_easyocr():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(['en'], gpu=False)
        except Exception as e:
            logger.error("Failed to initialize EasyOCR: %s", e)
            _easyocr_reader = None
    return _easyocr_reader


def ocr_image_with_tesseract(img: Image.Image, config="--psm 3"):
    """Return text from PIL image using pytesseract."""
    if not TESSERACT_AVAILABLE or pytesseract is None:
        raise RuntimeError("Tesseract not available")
    return pytesseract.image_to_string(img, lang='eng', config=config)


def ocr_image_with_easyocr(img: Image.Image):
    reader = _init_easyocr()
    if reader is None:
        raise RuntimeError("EasyOCR not available")
    arr = np.array(img)
    try:
        # paragraph=True groups lines
        text_lines = reader.readtext(arr, detail=0, paragraph=True)
        return "\n".join(text_lines)
    except Exception:
        # fall back to line mode
        text_lines = reader.readtext(arr, detail=0)
        return "\n".join(text_lines)


def ocr_image_multi_scale(img: Image.Image):
    """Run OCR at multiple scales and pick best non-empty output."""
    # try deskew first
    try:
        img = deskew_cv2_image(img)
    except Exception:
        pass

    img = enhance_for_ocr(img)

    # Try Tesseract first
    if TESSERACT_AVAILABLE:
        try:
            # Try two PSM modes to improve layout parsing
            for cfg in ["--psm 3", "--psm 6", "--psm 11"]:
                txt = ocr_image_with_tesseract(img, config=cfg)
                if txt and len(txt.strip()) > 10:
                    return txt
        except Exception as e:
            logger.warning("Tesseract OCR failed: %s", e)

    # Fallback to EasyOCR
    try:
        txt = ocr_image_with_easyocr(img)
        if txt and len(txt.strip()) > 0:
            return txt
    except Exception as e:
        logger.warning("EasyOCR fallback failed: %s", e)

    # Final fallback: return empty string
    return ""


# ---------------- PDF -> IMAGE -> OCR pipeline
def extract_text_from_pdf(file_obj):
    """
    Render PDF pages with PyMuPDF and run OCR on each page.
    Returns full text joined with newlines.
    """
    text_list = []
    file_obj.seek(0)
    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # increase dpi for clearer image
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            page_text = ocr_image_multi_scale(img)
            # ensure we keep some separation between pages
            if page_text:
                text_list.append(page_text.strip())
    return "\n\n".join(text_list)


# ---------------- CLEAN TEXT BEFORE NAME EXTRACTION
def clean_text_before_name_extraction(text):
    cleaned = []
    if not text:
        return ""
    for line in text.split("\n"):
        low = line.lower().strip()

        # remove lines with urls/handles/emails/phone
        if any(x in low for x in ["http", "www", ".com", "linkedin", "github", "drive.google"]):
            continue
        if "@" in low:
            continue
        if re.search(r"\+?\d[\d\-\(\)\s]{6,}\d", low):
            continue
        # skip lines that are long section sentences (not likely name)
        if len(line.split()) > 6:
            continue
        # skip common headings
        if low.strip() in {"summary", "education", "experience", "skills", "projects", "achievements", "contact", "objective"}:
            continue

        if line.strip():
            cleaned.append(line.strip())
    return "\n".join(cleaned)


# ---------------- ROBUST NAME EXTRACTION
def extract_name(text):
    """
    Multi-pass approach:
    1) spaCy PERSON entities
    2) heuristic: top-of-document capitalized lines
    3) regex fallback
    4) scoring to pick best candidate
    """
    if not text or not text.strip():
        return "Unknown"

    doc = nlp(text)
    INVALID = {
        "resume", "cv", "profile", "contact", "details", "email", "phone",
        "linkedin", "github", "summary", "projects", "objective"
    }

    candidates = set()

    # spaCy PERSON entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            nm = ent.text.strip()
            lw = [w.lower() for w in nm.split()]
            if any(w in INVALID for w in lw):
                continue
            # sanity: letters only (allow spaces & dots)
            if re.sub(r"[^A-Za-z\s\.]", "", nm).strip():
                candidates.add(nm)

    # top lines heuristic (first 8 lines after cleaning)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, ln in enumerate(lines[:8]):
        if 1 <= len(ln.split()) <= 4:
            # ignore if contains url/email/phone
            if any(x in ln.lower() for x in ["http", "@", "linkedin", "github", ".com"]):
                continue
            if re.search(r"\d", ln):
                continue
            candidates.add(ln)

    # regex fallback
    regex_matches = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3}\b", text)
    for m in regex_matches:
        if len(m.split()) <= 4:
            candidates.add(m)

    if not candidates:
        return "Unknown"

    # scoring: prefer candidates in top lines, short (1-3 words), not ALL CAPS
    def score(name):
        s = 0
        words = name.split()
        if 1 <= len(words) <= 3:
            s += 10
        if not name.isupper():
            s += 5
        # position bonus
        if any(name in ln for ln in lines[:8]):
            s += 8
        # penalize includes common headings
        if any(w in name.lower() for w in INVALID):
            s -= 10
        return s

    best = max(candidates, key=score)
    return best


# ---------------- EDUCATION EXTRACTION
def extract_education(text):
    low = text.lower()
    degree = None
    for patt in DEGREE_PATTERNS:
        m = re.search(patt, low)
        if m:
            tok = m.group().upper()
            if "BTECH" in tok or "B.TECH" in tok: degree = "B.Tech"
            elif tok in ["BE", "B.E"]: degree = "B.E"
            elif "BCA" in tok: degree = "BCA"
            elif "BSC" in tok or "B.SC" in tok: degree = "B.Sc"
            elif "MTECH" in tok or "M.TECH" in tok: degree = "M.Tech"
            elif "MCA" in tok: degree = "MCA"
            elif "MSC" in tok or "M.SC" in tok: degree = "M.Sc"
            elif "MBA" in tok: degree = "MBA"
            elif "PHD" in tok or "PH.D" in tok: degree = "PhD"
            else:
                degree = tok.title()
            break

    branch = None
    for patt in BRANCH_PATTERNS:
        m = re.search(patt, low)
        if m:
            branch = m.group().title()
            break

    if degree and branch:
        return f"{degree} in {branch}"
    if degree:
        return degree
    # final fallback: look for "Bachelor of ... in Computer Science"
    m = re.search(r"(bachelor|master|associate)[\w\s\,\-]{0,80}in\s+([A-Za-z &]+)", low)
    if m:
        deg = m.group(1).title()
        br = m.group(2).strip().title()
        return f"{deg} in {br}"
    return "Unknown"


# ---------------- SKILLS EXTRACTION
def extract_skills(text):
    if not text:
        return []
    text_norm = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = text_norm.split()
    found = set()

    # single-token
    for t in tokens:
        if t in SKILLS_DB:
            found.add(t)

    # multi-word
    joined = " " + " ".join(tokens) + " "
    for skill in SKILLS_DB:
        if " " in skill and f" {skill} " in joined:
            found.add(skill)

    # acronym heuristics
    acronyms = {"ml": "machine learning", "dl": "deep learning", "ai": "ai"}
    for a, full in acronyms.items():
        if re.search(rf"\b{a}\b", text_norm) and full in SKILLS_DB:
            found.add(full)

    return sorted(found)


# ---------------- MAIN WRAPPER
def extract_skills_from_pdf(uploaded_file):
    """
    Returns: {"name": ..., "education": ..., "skills": [...]}
    This is the main function your Streamlit app should call.
    """
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
