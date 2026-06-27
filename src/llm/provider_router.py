#LLM_PROVIDER = "openai"
LLM_PROVIDER = "gemini"

from src.llm.gemini_provider import (
    generate_response as gemini_response
)

from src.llm.openai_provider import (
    generate_response as openai_response
)

def ask_llm(prompt):

    if LLM_PROVIDER == "gemini":
        return gemini_response(prompt)

    return openai_response(prompt)

def get_current_provider():

    return LLM_PROVIDER