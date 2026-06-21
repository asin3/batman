from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text.strip()