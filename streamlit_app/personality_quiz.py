from transformers import pipeline

# Load the text generation model once (you can do this outside functions if preferred)
generator = pipeline('text-generation', model='gpt2')

def generate_technical_questions(user_skills, num_questions=5):
    prompt = (
        f"Generate {num_questions} technical personality quiz questions for someone skilled in: "
        f"{', '.join(user_skills)}. "
        "The questions should assess their strengths, preferences, and interests related to these skills in a professional context. "
        "Use clear and concise language."
    )
    response = generator(prompt, max_length=150, num_return_sequences=1, truncation=True)
    generated_text = response[0]['generated_text']

    questions = []
    for line in generated_text.split('\n'):
        line = line.strip()
        if line.endswith('?'):
            questions.append(line)
        if len(questions) >= num_questions:
            break

    # Fallback if GPT-2 output is insufficient
    if len(questions) < num_questions:
        questions = [f"Do you enjoy working with {skill} in a technical environment?" for skill in user_skills[:num_questions]]

    # Return list of dicts with dummy trait 'Technical' for now
    return [{'question': q, 'trait': 'Technical'} for q in questions]

# Your original static personality quiz questions
def get_quiz_questions():
    return [
        {'question': "I enjoy working with numbers and solving analytical problems.", 'trait': 'Analytical'},
        {'question': "I prefer creative tasks like drawing, designing, or writing.", 'trait': 'Creative'},
        {'question': "I like building or fixing things using tools or machines.", 'trait': 'Practical'},
        {'question': "I enjoy helping others solve problems or give advice.", 'trait': 'Supportive'},
        {'question': "I like organizing events or managing projects.", 'trait': 'Leadership'}
    ]

def evaluate_personality(responses, questions=None):
    """
    responses: list of integers (Likert scale 1-5) for each question
    questions: list of question dicts with 'trait' keys. If None, uses static quiz.
    """
    if questions is None:
        questions = get_quiz_questions()

    scores = {
        'Analytical': 0,
        'Creative': 0,
        'Practical': 0,
        'Supportive': 0,
        'Leadership': 0,
        'Technical': 0  # add Technical if you use generated questions
    }

    for i, response in enumerate(responses):
        trait = questions[i]['trait']
        if trait in scores:
            scores[trait] += response
        else:
            scores[trait] = response  # In case new trait appears

    top_trait = max(scores, key=scores.get)
    return trait_to_career(top_trait)

def trait_to_career(trait):
    mapping = {
        'Analytical': ['Data Scientist', 'AI Engineer', 'Data Analyst'],
        'Creative': ['UI/UX Designer', 'Content Creator', 'Graphic Designer'],
        'Practical': ['Software Engineer', 'DevOps Engineer', 'Hardware Engineer'],
        'Supportive': ['Career Counselor', 'HR Specialist', 'Teacher'],
        'Leadership': ['Product Manager', 'Team Lead', 'Project Manager'],
        'Technical': ['Software Developer', 'Machine Learning Engineer', 'Data Engineer']  # new mapping
    }
    return mapping.get(trait, [])

# Example usage (for testing)
if __name__ == "__main__":
    skills = ['python', 'machine learning', 'data analysis']
    tech_questions = generate_technical_questions(skills)
    print("Technical Questions Generated:")
    for q in tech_questions:
        print(q['question'])
    
    # Use static quiz for evaluation example
    responses = [4, 3, 5, 2, 1]  # sample Likert responses
    careers = evaluate_personality(responses)
    print(f"Recommended careers for personality: {careers}")
