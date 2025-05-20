import fitz  # PyMuPDF
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Predefined skills list
SKILLS_DB = [
    'python', 'machine learning', 'data analysis', 'deep learning',
    'java', 'c++', 'communication', 'teamwork', 'sql', 'javascript',
    'html', 'css', 'pandas', 'numpy', 'tensorflow', 'project management',
    'problem solving', 'data visualization', 'excel', 'leadership'
]

EDUCATION_LEVELS = [
    'High School', 'Diploma', 'Bachelor', 'Masters', 'PhD'
]

def extract_text_from_pdf(file_obj):
    """
    Extracts text from a PDF file-like object (e.g., from Streamlit).
    """
    text = ""
    file_obj.seek(0)  # Important: reset file pointer to the beginning
    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_name(text):
    """
    Uses spaCy's NER to extract the first PERSON entity as name.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"

def extract_education(text):
    """
    Detects education level mentioned in text.
    """
    for level in EDUCATION_LEVELS:
        if re.search(level, text, re.IGNORECASE):
            return level
    return "Bachelor"  # default fallback

def extract_skills(text):
    """
    Matches skills from the predefined list in the extracted text.
    """
    text = text.lower()
    found_skills = set()
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.add(skill.lower())
    return list(found_skills)

def extract_skills_from_pdf(uploaded_file):
    """
    Main function called from Streamlit.
    Accepts a file-like object and returns parsed resume data.
    """
    text = extract_text_from_pdf(uploaded_file)
    name = extract_name(text)
    education = extract_education(text)
    skills = extract_skills(text)
    return {
        "name": name,
        "education": education,
        "skills": skills
    }
