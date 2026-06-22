from llm.provider_router import ask_llm


def classify_intent(question):

    prompt = f"""
You are Batman's Intent Classifier.

Classify the student's request.

Return ONLY ONE of these values:

LEARN
SUPER_CHAT
QUIZ
HOMEWORK
SOLVED_EXAMPLE
STUDY_PLAN

Rules:

- Subject learning questions = LEARN
- Textbook concept questions = LEARN
- Physics questions = LEARN
- Chemistry questions = LEARN
- Biology questions = LEARN
- Maths questions = LEARN

- Quiz requests = QUIZ

- Homework help = HOMEWORK

- Step-by-step worked solutions = SOLVED_EXAMPLE

- Timetable, revision plan, study schedule = STUDY_PLAN

- General conversation, motivation,
career advice, exam stress,
life questions, productivity,
non-subject discussion = SUPER_CHAT

Question:

{question}
"""

    response = ask_llm(
        prompt
    )

    return (
        response
        .strip()
        .upper()
    )