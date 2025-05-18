# resume_parser.py

import fitz  # PyMuPDF
import re

# Sample skills set for matching (can be expanded)
SKILL_SET = {
    'python', 'java', 'c++', 'sql', 'html', 'css', 'javascript',
    'react', 'node.js', 'machine learning', 'deep learning',
    'nlp', 'data analysis', 'pandas', 'numpy', 'django', 'flask',
    'git', 'docker', 'linux', 'aws', 'tensorflow', 'keras'
}


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in SKILL_SET:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    return list(found_skills)


def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    return {
        "text": text,
        "skills": skills
    }
# result = parse_resume("HardikKothari-2022PUFCEBADX11350.pdf")
# print("Skills found:", result["skills"])