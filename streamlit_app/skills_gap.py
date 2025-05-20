# skills_gap.py

# Predefined required skills for each career
REQUIRED_SKILLS = {
    'Data Scientist': {'python', 'sql', 'machine learning', 'pandas', 'numpy', 'matplotlib'},
    'Web Developer': {'html', 'css', 'javascript', 'react', 'node.js', 'git'},
    'Software Engineer': {'python', 'java', 'c++', 'git', 'linux', 'data structures'},
    'AI Engineer': {'python', 'tensorflow', 'keras', 'deep learning', 'machine learning'},
    'DevOps Engineer': {'docker', 'aws', 'linux', 'git', 'ci/cd', 'kubernetes'},
    'UI/UX Designer': {'figma', 'adobe xd', 'wireframing', 'user research', 'creativity'},
    'Database Admin': {'sql', 'mysql', 'postgresql', 'performance tuning', 'data backup'},
    'Cybersecurity Analyst': {'network security', 'firewalls', 'linux', 'python', 'encryption'},
    'Cloud Engineer': {'aws', 'azure', 'gcp', 'terraform', 'docker', 'linux'},
    'Data Analyst': {'python', 'sql', 'excel', 'tableau', 'pandas', 'data visualization'},
}

def get_missing_skills(user_skills, predicted_career):
    required = REQUIRED_SKILLS.get(predicted_career, set())
    missing = required - set(user_skills)
    return list(missing)
# user_skills = ['python', 'sql']
# career = 'Data Scientist'

# missing = analyze_skill_gap(user_skills, career)
# print("Missing Skills:", missing)