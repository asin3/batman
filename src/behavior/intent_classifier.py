from llm.provider_router import ask_llm


def classify_intent(question):

    prompt = f"""
Classify the student's request.

Return ONLY ONE WORD:

CONCEPT
HOMEWORK
SOLVED_EXAMPLE
STUDY_PLAN
QUIZ

Question:
{question}
"""

    response = ask_llm(prompt)

    return response.strip()