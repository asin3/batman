"""
============================================================
Batman Student

Module:
deepseek_provider.py

Purpose:
DeepSeek LLM Provider

============================================================
"""

import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()


client = OpenAI(

    api_key=os.getenv("DEEPSEEK_API_KEY"),

    base_url="https://api.deepseek.com"

)


# ---------------------------------------------------------
# GENERATE RESPONSE
# ---------------------------------------------------------

def generate_response(prompt):

    response = client.chat.completions.create(

        model="deepseek-v4-flash",

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print(

        generate_response(

            "Reply with exactly: Batman Ready"

        )

    )