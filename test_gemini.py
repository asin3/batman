import sys

sys.path.append("src")

from llm.gemini_provider import generate_response

print(
    generate_response(
        "What is force?"
    )
)