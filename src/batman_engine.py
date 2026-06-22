from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from behavior.intent_classifier import classify_intent
from behavior.batman_router import choose_skill

from behavior.concept_teacher import get_prompt as concept_prompt
from behavior.homework_guide import get_prompt as homework_prompt
from behavior.study_coach import get_prompt as study_prompt
from behavior.solved_example import get_prompt as solved_example_prompt

from retrieval.retrieval_router import should_retrieve

from conversation_manager import load_history
from conversation_manager import save_history

from quiz_parser import parse_quiz_request
from quiz_generator import generate_mcq

from quiz_manager import (
    start_quiz,
    is_quiz_active,
    set_difficulty,
    set_question_count,
    get_quiz_state,
    set_current_answer,
    check_answer,
    is_quiz_complete,
    end_quiz,
    set_current_explanation,
    get_current_explanation
)

import chromadb
import os
import re

load_dotenv()

# ---------------------------------
# OPENAI
# ---------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------
# RULES
# ---------------------------------

rules = Path(
    "docs/student_tutor_rules.md"
).read_text(
    encoding="utf-8"
)

# ---------------------------------
# CHROMA
# ---------------------------------

db = chromadb.PersistentClient(
    path="./vector_db"
)

collection = db.get_collection(
    "class10_physics"
)

# ---------------------------------
# QUIZ HELPERS
# ---------------------------------

def build_quiz_question(
    topic,
    difficulty
):

    results = collection.query(
        query_texts=[topic],
        n_results=2
    )

    context = "\n".join(
        results["documents"][0]
    )

    mcq = generate_mcq(
        context,
        difficulty
    )

    match = re.search(
        r"CORRECT:\s*([ABCD])",
        mcq
    )

    if match:

        set_current_answer(
            match.group(1)
        )

    explanation_match = re.search(
        r"EXPLANATION:\s*(.*)",
        mcq,
        re.DOTALL
    )

    if explanation_match:

        set_current_explanation(
            explanation_match.group(1).strip()
        )

    question_only = re.split(
        r"CORRECT:",
        mcq
    )[0]

    return question_only.strip()

# ---------------------------------
# MAIN
# ---------------------------------

def ask_batman(
    student_id,
    question
):

    history = load_history(
        student_id
    )

    # ---------------------------------
    # QUIZ ANSWER FLOW
    # ---------------------------------

    if is_quiz_active():

        answer = question.strip()

        correct = check_answer(
            answer
        )

        explanation = (
            get_current_explanation()
        )

        response_text = ""

        if correct:

            response_text += (
                "✅ Correct\n\n"
            )

        else:

            response_text += (
                "❌ Wrong\n\n"
            )

        if explanation:

            response_text += (
                "📘 Explanation:\n\n"
                + explanation +
                "\n\n"
            )

        if is_quiz_complete():

            state = get_quiz_state()

            final_score = (
                f"🏁 Quiz Complete!\n\n"
                f"Score: "
                f"{state['score']}/"
                f"{state['total_questions']}"
            )

            end_quiz()

            return (
                response_text +
                final_score
            )

        state = get_quiz_state()

        next_question = build_quiz_question(
            state["topics"][0],
            state["difficulty"]
        )

        return (
            response_text +
            "\n\nNext Question:\n\n" +
            next_question
        )

    # ---------------------------------
    # QUIZ START
    # ---------------------------------

    if question.lower().startswith(
        "quiz"
    ):

        parsed = parse_quiz_request(
            question
        )

        topics = parsed["topics"]
        difficulty = parsed["difficulty"]
        count = parsed["count"]

        if not topics:
            return "Which topic?"

        if not difficulty:
            return "Difficulty? Easy / Medium / Hard"

        if count == 0:
            return "How many questions?"

        start_quiz(topics)

        set_difficulty(
            difficulty
        )

        set_question_count(
            count
        )

        first_question = (
            build_quiz_question(
                topics[0],
                difficulty
            )
        )

        return (
            f"🎯 Quiz Started\n\n"
            f"Topic: {topics[0]}\n"
            f"Difficulty: {difficulty}\n"
            f"Questions: {count}\n\n"
            f"{first_question}"
        )

    # ---------------------------------
    # HISTORY
    # ---------------------------------

    history.append(
        {
            "role": "user",
            "content": question
        }
    )

    # ---------------------------------
    # BATMAN BRAIN
    # ---------------------------------

    intent = classify_intent(
        question
    )

    skill = choose_skill(
        question
    )

    retrieve = should_retrieve(
        intent
    )

    # ---------------------------------
    # SKILL SELECTION
    # ---------------------------------

    if skill == "CONCEPT_TEACHER":

        behavior_prompt = (
            concept_prompt()
        )

    elif skill == "HOMEWORK_GUIDE":

        behavior_prompt = (
            homework_prompt()
        )

    elif skill == "STUDY_COACH":

        behavior_prompt = (
            study_prompt()
        )

    elif skill == "SOLVED_EXAMPLE":

        behavior_prompt = (
            solved_example_prompt()
        )

    else:

        behavior_prompt = (
            concept_prompt()
        )

    # ---------------------------------
    # RETRIEVAL
    # ---------------------------------

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

    # ---------------------------------
    # HISTORY CONTEXT
    # ---------------------------------

    history_text = ""

    for msg in history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # ---------------------------------
    # PROMPT
    # ---------------------------------

    prompt = f"""

BATMAN SKILL:

{skill}

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