from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from behavior.intent_classifier import classify_intent
from behavior.concept_teacher import get_prompt as concept_prompt
from behavior.homework_guide import get_prompt as homework_prompt
from behavior.study_coach import get_prompt as study_prompt

from retrieval.retrieval_router import should_retrieve

from conversation_manager import load_history
from conversation_manager import save_history

import chromadb
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

rules = Path(
    "docs/student_tutor_rules.md"
).read_text(
    encoding="utf-8"
)

db = chromadb.PersistentClient(
    path="./vector_db"
)

collection = db.get_collection(
    "class10_physics"
)


def ask_batman(
    student_id,
    question
):

    history = load_history(
        student_id
    )

    history.append(
        {
            "role": "user",
            "content": question
        }
    )

    intent = classify_intent(
        question
    )

    retrieve = should_retrieve(
        intent
    )

    if intent == "CONCEPT":

        behavior_prompt = concept_prompt()

    elif intent == "HOMEWORK":

        behavior_prompt = homework_prompt()

    elif intent == "STUDY_PLAN":

        behavior_prompt = study_prompt()

    else:

        behavior_prompt = concept_prompt()

    if retrieve:

        results = collection.query(
            query_texts=[question],
            n_results=2
        )

        context = "\n".join(
            results["documents"][0]
        )

    else:

        context = (
            "No textbook context needed."
        )

    history_text = ""

    for msg in history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""

BATMAN BEHAVIOR:

{behavior_prompt}

GLOBAL RULES:

{rules}

CONVERSATION HISTORY:

{history_text}

TEXTBOOK CONTEXT:

{context}

CURRENT STUDENT QUESTION:

{question}

"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    answer = response.output_text

    history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    save_history(
        student_id,
        history
    )

    return answer