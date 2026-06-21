from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_mcq(context, difficulty):

    prompt = f"""
Create ONE MCQ.

Rules:

- Use ONLY supplied context
- Difficulty: {difficulty}

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

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text