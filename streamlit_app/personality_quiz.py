import random

def generate_technical_questions(user_skills, num_questions=5):
    """
    Generate simple, personalized questions based on the user's resume skills.
    The questions focus on skill familiarity and career direction.
    """
    # Basic templates for skill-based questions
    skill_templates = [
        "How confident are you in your knowledge of {skill}?",
        "Have you ever worked on a project using {skill}?",
        "Do you want to improve your skills in {skill} further?",
        "Would you like to build a career involving {skill}?",
        "How often do you use {skill} in your studies or projects?"
    ]
    
    # Career-oriented general questions
    career_templates = [
        "Which of your skills do you enjoy using the most?",
        "Would you prefer a job that focuses on coding or data analysis?",
        "Do you enjoy teamwork or independent technical work more?",
        "Are you more interested in software development or AI-related roles?",
        "Would you like to take on leadership roles in technical projects?"
    ]
    
    # Generate skill-based questions
    questions = []
    for skill in user_skills[:num_questions]:
        template = random.choice(skill_templates)
        questions.append({'question': template.format(skill=skill), 'trait': 'Technical'})
    
    # Add a few general questions to suggest roles
    extra_qs = random.sample(career_templates, min(3, len(career_templates)))
    for q in extra_qs:
        questions.append({'question': q, 'trait': 'Career'})
    
    return questions[:num_questions + len(extra_qs)]


def get_quiz_questions():
    """Static fallback quiz (non-technical)."""
    return [
        {'question': "I enjoy working with numbers and solving analytical problems.", 'trait': 'Analytical'},
        {'question': "I prefer creative tasks like designing or writing.", 'trait': 'Creative'},
        {'question': "I like organizing events or managing projects.", 'trait': 'Leadership'},
    ]


def evaluate_personality(responses, questions=None):
    if questions is None:
        questions = get_quiz_questions()

    scores = {'Technical': 0, 'Career': 0, 'Analytical': 0, 'Creative': 0, 'Leadership': 0}

    for i, response in enumerate(responses):
        trait = questions[i]['trait']
        scores[trait] += response

    top_trait = max(scores, key=scores.get)
    return trait_to_career(top_trait)


def trait_to_career(trait):
    mapping = {
        'Technical': ['Software Developer', 'Data Scientist', 'AI Engineer'],
        'Career': ['Project Manager', 'Tech Consultant', 'Research Analyst'],
        'Analytical': ['Data Analyst', 'Statistician'],
        'Creative': ['UI/UX Designer', 'Content Creator'],
        'Leadership': ['Team Lead', 'Product Manager']
    }
    return mapping.get(trait, [])


# Example usage
if __name__ == "__main__":
    resume_skills = ['Python', 'Machine Learning', 'Data Analysis']
    questions = generate_technical_questions(resume_skills)
    
    print("\nGenerated Personalized Questions:\n")
    for q in questions:
        print("•", q['question'])
