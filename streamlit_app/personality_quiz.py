# import random

# def generate_technical_questions(user_skills, num_questions=5):
#     """
#     Generate simple, personalized questions based on the user's resume skills.
#     The questions focus on skill familiarity and career direction.
#     """
#     # Basic templates for skill-based questions
#     skill_templates = [
#         "How confident are you in your knowledge of {skill}?",
#         "Have you ever worked on a project using {skill}?",
#         "Do you want to improve your skills in {skill} further?",
#         "Would you like to build a career involving {skill}?",
#         "How often do you use {skill} in your studies or projects?"
#     ]
    
#     # Career-oriented general questions
#     career_templates = [
#         "Which of your skills do you enjoy using the most?",
#         "Would you prefer a job that focuses on coding or data analysis?",
#         "Do you enjoy teamwork or independent technical work more?",
#         "Are you more interested in software development or AI-related roles?",
#         "Would you like to take on leadership roles in technical projects?"
#     ]
    
#     # Generate skill-based questions
#     questions = []
#     for skill in user_skills[:num_questions]:
#         template = random.choice(skill_templates)
#         questions.append({'question': template.format(skill=skill), 'trait': 'Technical'})
    
#     # Add a few general questions to suggest roles
#     extra_qs = random.sample(career_templates, min(3, len(career_templates)))
#     for q in extra_qs:
#         questions.append({'question': q, 'trait': 'Career'})
    
#     return questions[:num_questions + len(extra_qs)]


# def get_quiz_questions():
#     """Static fallback quiz (non-technical)."""
#     return [
#         {'question': "I enjoy working with numbers and solving analytical problems.", 'trait': 'Analytical'},
#         {'question': "I prefer creative tasks like designing or writing.", 'trait': 'Creative'},
#         {'question': "I like organizing events or managing projects.", 'trait': 'Leadership'},
#     ]


# def evaluate_personality(responses, questions=None):
#     if questions is None:
#         questions = get_quiz_questions()

#     scores = {'Technical': 0, 'Career': 0, 'Analytical': 0, 'Creative': 0, 'Leadership': 0}

#     for i, response in enumerate(responses):
#         trait = questions[i]['trait']
#         scores[trait] += response

#     top_trait = max(scores, key=scores.get)
#     return trait_to_career(top_trait)


# def trait_to_career(trait):
#     mapping = {
#         'Technical': ['Software Developer', 'Data Scientist', 'AI Engineer'],
#         'Career': ['Project Manager', 'Tech Consultant', 'Research Analyst'],
#         'Analytical': ['Data Analyst', 'Statistician'],
#         'Creative': ['UI/UX Designer', 'Content Creator'],
#         'Leadership': ['Team Lead', 'Product Manager']
#     }
#     return mapping.get(trait, [])


# # Example usage
# if __name__ == "__main__":
#     resume_skills = ['Python', 'Machine Learning', 'Data Analysis']
#     questions = generate_technical_questions(resume_skills)
    
#     print("\nGenerated Personalized Questions:\n")
#     for q in questions:
#         print("•", q['question'])
# personality_quiz.py
"""
Stable personality quiz module for AI Career Counselor.

Exports:
- get_quiz_questions() -> list[dict]: 12 core fixed questions (no randomness).
- generate_technical_questions(user_skills, num_questions=5) -> list[dict]: deterministic
  personalized technical questions (based on top skills).
- evaluate_personality(responses, questions, top_n=3) -> dict:
    {
      "trait_scores": {trait: raw_score, ...},
      "normalized_scores": {trait: 0.0-1.0, ...},
      "ranked_careers": [ ("Career Title", score), ... ]  # top_n by default
    }

Design goals:
- Deterministic behavior (no random.sample / random.choice).
- Weighted scoring: personalized technical questions carry slightly more weight.
- Safe to plug into your Streamlit app (returns structured data).
"""

from typing import List, Dict, Tuple

# -------------------------
# 1) Fixed core questions
# -------------------------
def get_quiz_questions() -> List[Dict]:
    """
    Return a stable, fixed set of personality questions.
    Each question is a dict: {'question': str, 'trait': str, 'weight': float}
    Weight defaults to 1.0 for core questions.
    """
    base = [
        # Analytical (2)
        {'question': "I enjoy solving analytical problems and working with data.", 'trait': 'Analytical', 'weight': 1.0},
        {'question': "I am comfortable identifying patterns or insights from complex information.", 'trait': 'Analytical', 'weight': 1.0},

        # Creative (2)
        {'question': "I enjoy designing, writing, or creating visually appealing content.", 'trait': 'Creative', 'weight': 1.0},
        {'question': "I prefer tasks that involve imagination and out-of-the-box thinking.", 'trait': 'Creative', 'weight': 1.0},

        # Leadership (2)
        {'question': "I like coordinating tasks and managing people in group projects.", 'trait': 'Leadership', 'weight': 1.0},
        {'question': "I am comfortable making decisions and taking responsibility for outcomes.", 'trait': 'Leadership', 'weight': 1.0},

        # Technical Interest (2)
        {'question': "I enjoy working with technology, coding, or engineering tasks.", 'trait': 'Technical', 'weight': 1.0},
        {'question': "I like understanding how systems, algorithms, or machines work.", 'trait': 'Technical', 'weight': 1.0},

        # Work Preference / Career Direction (4)
        {'question': "I prefer structured environments with clear instructions.", 'trait': 'Career', 'weight': 1.0},
        {'question': "I enjoy independent work as much as collaborative teamwork.", 'trait': 'Career', 'weight': 1.0},
        {'question': "I want a career that involves continuous learning and building new skills.", 'trait': 'Career', 'weight': 1.0},
        {'question': "I would prefer a role that mixes communication with technical thinking.", 'trait': 'Career', 'weight': 1.0},
    ]
    return base


# -------------------------------------------------
# 2) Deterministic personalized technical questions
# -------------------------------------------------
def generate_technical_questions(user_skills: List[str], num_questions: int = 5) -> List[Dict]:
    """
    Generate deterministic, resume-based 'Technical' questions from user_skills.

    - Uses a fixed template order so responses don't shift.
    - Truncates/pads to `num_questions` deterministically.
    - These questions are flagged with a slightly higher weight to increase technical signal.

    Params:
      user_skills: list of skill strings (preferably normalized)
      num_questions: how many personalized questions to generate

    Returns:
      list of question dicts: {'question': str, 'trait': 'Technical', 'weight': float}
    """
    # stable templates in fixed order
    templates = [
        "How confident are you in using {skill} in real projects?",
        "Have you completed a project or coursework using {skill}?",
        "How often do you practice or apply {skill} (daily/weekly/monthly)?",
        "Do you want to master {skill} at an advanced level?",
        "Would you feel comfortable explaining {skill} to others?"
    ]

    # ensure deterministic skill selection: keep order provided, trimmed to num_questions
    selected_skills = user_skills[:num_questions]

    questions = []
    for i, skill in enumerate(selected_skills):
        tmpl = templates[i % len(templates)]
        qtext = tmpl.format(skill=skill)
        # personalized technical questions get weight 1.25 (more influence than core questions)
        questions.append({'question': qtext, 'trait': 'Technical', 'weight': 1.25})

    # if fewer skills than num_questions, pad with general stable technical prompts
    pad_index = 0
    while len(questions) < num_questions:
        skill = "technical concepts"
        tmpl = templates[pad_index % len(templates)]
        questions.append({'question': tmpl.format(skill=skill), 'trait': 'Technical', 'weight': 1.25})
        pad_index += 1

    return questions


# -------------------------
# 3) Career mapping table
# -------------------------
def trait_to_career_mapping() -> Dict[str, List[Tuple[str, float]]]:
    """
    Returns mapping trait -> list of (career_title, base_score_weight)
    base_score_weight is used to slightly bias mapping (not required).
    """
    return {
        'Technical': [
            ('Software Developer', 1.0),
            ('Data Scientist', 0.95),
            ('AI Engineer', 0.9),
            ('Cloud Engineer', 0.85),
            ('Cybersecurity Analyst', 0.8),
        ],
        'Analytical': [
            ('Data Analyst', 1.0),
            ('Business Analyst', 0.95),
            ('ML Engineer', 0.9)
        ],
        'Creative': [
            ('UI/UX Designer', 1.0),
            ('Graphic Designer', 0.95),
            ('Content Creator', 0.9)
        ],
        'Leadership': [
            ('Project Manager', 1.0),
            ('Team Lead', 0.95),
            ('Product Manager', 0.9)
        ],
        'Career': [
            ('Tech Consultant', 1.0),
            ('Research Analyst', 0.95),
            ('Operations Manager', 0.9)
        ]
    }


# ------------------------------------
# 4) Evaluation function (scoring)
# ------------------------------------
def evaluate_personality(responses: List[int], questions: List[Dict] = None, top_n: int = 3) -> Dict:
    """
    Evaluate personality and return ranked career recommendations.

    Params:
      responses: list of integer responses (scale 1..5) aligned to `questions`
      questions: list of question dicts (if None, uses get_quiz_questions())
      top_n: how many career recommendations to return

    Returns:
      {
        "trait_scores": {trait: raw_weighted_score, ...},
        "normalized_scores": {trait: 0.0-1.0, ...},
        "ranked_careers": [ (career_title, score_float), ... ]  # top_n
      }

    Notes:
      - If questions is None, only the fixed core questions are used.
      - The function is deterministic and robust to mismatched lengths
        (extra responses ignored; missing responses treated as neutral=3).
    """
    if questions is None:
        questions = get_quiz_questions()

    # ensure lengths align: if responses shorter, pad with neutral (3); if longer, ignore extra
    expected = len(questions)
    if len(responses) < expected:
        padded = responses + [3] * (expected - len(responses))
    else:
        padded = responses[:expected]

    # initialize trait accumulators
    trait_scores: Dict[str, float] = {}
    trait_weights_sum: Dict[str, float] = {}

    for resp, q in zip(padded, questions):
        trait = q.get('trait', 'Career')
        weight = float(q.get('weight', 1.0))
        # normalize response from 1..5 to 0..1 (0 for 1, 1 for 5)
        resp_norm = (resp - 1) / 4.0
        # accumulate weighted score
        trait_scores[trait] = trait_scores.get(trait, 0.0) + resp_norm * weight
        trait_weights_sum[trait] = trait_weights_sum.get(trait, 0.0) + weight

    # compute average per trait (0..1)
    normalized_scores: Dict[str, float] = {}
    for trait, total in trait_scores.items():
        denom = trait_weights_sum.get(trait, 1.0)
        normalized_scores[trait] = total / denom if denom != 0 else 0.0

    # Now map trait scores -> career scores using trait_to_career_mapping
    mapping = trait_to_career_mapping()

    career_scores: Dict[str, float] = {}
    for trait, score in normalized_scores.items():
        careers = mapping.get(trait, [])
        for career_title, base_weight in careers:
            # career score contribution: trait_score * base_weight
            # We also scale by trait importance (e.g., Technical questions might be slightly more reliable).
            contribution = score * base_weight
            career_scores[career_title] = career_scores.get(career_title, 0.0) + contribution

    # Sort careers by score descending
    ranked = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top_n recommended careers with scores, plus raw/normalized trait scores
    return {
        "trait_scores": trait_scores,
        "normalized_scores": normalized_scores,
        "ranked_careers": ranked[:top_n]  # list of tuples (career, score)
    }


# -------------------------
# Example (self-test)
# -------------------------
if __name__ == "__main__":
    # quick demo: assume 12 core questions answered with 3 (neutral)
    core = get_quiz_questions()
    demo_skills = ["python", "machine learning", "sql"]
    tech_qs = generate_technical_questions(demo_skills, num_questions=5)
    all_questions = core + tech_qs

    # sample responses: neutral for core, slightly positive for personalized tech
    responses = [3]*len(core) + [4]*len(tech_qs)
    result = evaluate_personality(responses, all_questions, top_n=5)
    print("Normalized trait scores:", result["normalized_scores"])
    print("Top careers:", result["ranked_careers"])
