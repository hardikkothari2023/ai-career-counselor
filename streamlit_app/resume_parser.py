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
