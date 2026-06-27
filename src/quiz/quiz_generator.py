from src.llm.provider_router import ask_llm


def extract_concept(question_text):

    prompt = f"""
Identify the SINGLE physics concept
being tested.

Return ONLY the concept name.

Question:

{question_text}
"""

    response = ask_llm(
        prompt
    )

    return response.strip()


def generate_mcq(
    context,
    difficulty,
    asked_questions=None,
    asked_concepts=None
):

    if asked_questions is None:

        asked_questions = []

    if asked_concepts is None:

        asked_concepts = []

    blocked_questions = "\n".join(
        asked_questions
    )

    blocked_concepts = "\n".join(
        asked_concepts
    )

    prompt = f"""
Create ONE MCQ.

Rules:

- Use ONLY supplied context
- Difficulty: {difficulty}

DO NOT repeat any of these questions:

{blocked_questions}

DO NOT generate questions from
these concepts:

{blocked_concepts}

Return EXACTLY in this format:

QUESTION:
...

A)
...

B)
...

C)
...

D)
...

CORRECT:
A

EXPLANATION:
...

CONTEXT:

{context}
"""

    response = ask_llm(
        prompt
    )

    return response