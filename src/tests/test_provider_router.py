import sys

sys.path.append("src")

from llm.provider_router import ask_llm

response = ask_llm(
    "What is force?"
)

print(response)