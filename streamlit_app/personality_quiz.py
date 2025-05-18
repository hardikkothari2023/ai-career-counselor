from transformers import pipeline

# Load a text generation model (GPT-2)
generator = pipeline('text-generation', model='gpt2')

def generate_quiz_questions(user_skills, num_questions=5):
    prompt = (
        f"Generate {num_questions} personalized personality quiz questions "
        f"for a person with skills in: {', '.join(user_skills)}. "
        "The questions should assess their interests and strengths related to careers."
    )
    
    response = generator(prompt, max_length=150, num_return_sequences=1)
    generated_text = response[0]['generated_text']

    # Extract questions from generated text
    questions = []
    for line in generated_text.split('\n'):
        line = line.strip()
        if line.endswith('?'):
            questions.append(line)
        if len(questions) >= num_questions:
            break

    # Fallback in case not enough questions
    if len(questions) < num_questions:
        questions = [f"Do you enjoy working with {skill}?" for skill in user_skills[:num_questions]]

    return questions

if __name__ == "__main__":
    skills = ['python', 'machine learning', 'data analysis']
    questions = generate_quiz_questions(skills)
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q}")
