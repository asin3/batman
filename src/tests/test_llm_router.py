"""
============================================================
Batman Student

LLM Router Test

============================================================
"""

from src.llm.provider_router import (

    ask_llm,

    get_current_provider

)


print(

    "Provider:",

    get_current_provider()

)

print()

response = ask_llm(

    "Reply with exactly: Batman Ready"

)

print(response)