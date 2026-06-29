from src.config.settings import (
    LLM_PROVIDER
)

from src.llm.gemini_provider import (
    generate_response as gemini_response
)

from src.llm.openai_provider import (
    generate_response as openai_response
)

from src.llm.deepseek_provider import (
    generate_response as deepseek_response
)

def ask_llm(prompt):

    if LLM_PROVIDER == "gemini":

        response = gemini_response(prompt)

    elif LLM_PROVIDER == "deepseek":

        response = deepseek_response(prompt)

    else:

        response = openai_response(prompt)

    if response is None:

        return (
            "Batman could not reach the AI service "
            "at the moment. Please try again shortly."
        )

    return response

def get_current_provider():

    return LLM_PROVIDER