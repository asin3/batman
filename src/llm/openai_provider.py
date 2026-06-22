from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

def generate_response(prompt):

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text