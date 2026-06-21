from dotenv import load_dotenv
import os
from openai import OpenAI

tests/test_intent.py
tests/test_history.py

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-5.5",
    input="Explain force in one sentence for a Class 10 student."
)

print(response.output_text)