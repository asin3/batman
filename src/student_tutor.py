from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from behavior.intent_classifier import classify_intent
from behavior.concept_teacher import get_prompt as concept_prompt
from behavior.homework_guide import get_prompt as homework_prompt
from behavior.study_coach import get_prompt as study_prompt

from retrieval.retrieval_router import should_retrieve

from conversation_manager import load_history
from conversation_manager import save_history

from quiz_parser import parse_quiz_request

from quiz_generator import (
    generate_mcq,
    extract_concept
)

from question_bank import (
    save_question
)

from llm.provider_router import ask_llm

from quiz_manager import (
    start_quiz,
    is_quiz_active,
    set_setup_stage,
    get_setup_stage,
    set_difficulty,
    set_question_count,
    get_quiz_state,
    set_current_answer,
    check_answer,
    is_quiz_complete,
    set_current_explanation,
    get_current_explanation,
    add_asked_question,
    get_asked_questions,
    add_asked_concept,
    get_asked_concepts
)

import chromadb
import os

load_dotenv()

# ---------------------------------

# OPENAI

# ---------------------------------

client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------

# LOAD RULES

# ---------------------------------

rules = Path(
"docs/student_tutor_rules.md"
).read_text(encoding="utf-8")

# ---------------------------------

# EMBEDDING MODEL

# ---------------------------------

embedding_model = SentenceTransformer(
"all-MiniLM-L6-v2"
)

# ---------------------------------

# CHROMADB

# ---------------------------------

db = chromadb.PersistentClient(
path="./vector_db"
)

collection = db.get_collection(
"class10_physics"
)

# ---------------------------------

# STUDENT

# ---------------------------------

student_id = input(
"Enter Student ID: "
)

history = load_history(
student_id
)

print(
f"\nLoaded {len(history)} previous messages."
)

# ---------------------------------

# MAIN LOOP

# ---------------------------------

while True:

    question = input(
    "\nAsk Batman-Student: "
    )

    if question.lower() == "exit":

        print(
            "\nSession Ended"
        )

        break

    stage = get_setup_stage()

    # -----------------------------
    # QUIZ SETUP
    # -----------------------------

    if stage == "DIFFICULTY":

        set_difficulty(question)

        set_setup_stage(
            "QUESTION_COUNT"
        )

        print(
            "\nHow many questions?"
        )

        continue

    if stage == "QUESTION_COUNT":

        try:

            set_question_count(
                int(question)
            )

        except ValueError:

            print(
                "\nPlease enter a number."
            )

            continue

        set_setup_stage("")

        print(
            "\nQuiz Setup Complete"
        )

        print(
            get_quiz_state()
        )

        continue

    # -----------------------------
    # START QUIZ
    # -----------------------------

    if question.lower().startswith("quiz"):

        parsed = parse_quiz_request(question)

        topics = parsed["topics"]
        difficulty = parsed["difficulty"]
        count = parsed["count"]

        if not topics:
            print("\nWhich topic?")
            continue

        if not difficulty:
            print("\nDifficulty? Easy / Medium / Hard")
            continue

        if count == 0:
            print("\nHow many questions?")
            continue

        start_quiz(topics)
        set_difficulty(difficulty)
        set_question_count(count)

        print("\nStarting Quiz...")

        topic = topics[0]

        results = collection.query(
            query_texts=[topic],
            n_results=2
        )

        context = "\n".join(results["documents"][0])

        mcq = generate_mcq(
            context,
            difficulty,
            get_asked_questions(),
            get_asked_concepts()
        )

        import re

        question_match = re.search(
            r"QUESTION:\s*(.*?)\s*A\)",
            mcq,
            re.DOTALL
        )

        correct_match = re.search(
            r"CORRECT:\s*([ABCD])",
            mcq
        )

        explanation_match = re.search(
            r"EXPLANATION:\s*(.*)",
            mcq,
            re.DOTALL
        )

        if question_match:

            question_text = (
                question_match.group(1)
                .strip()
            )

            add_asked_question(
                question_text
            )

            concept = extract_concept(
                question_text
            )

            add_asked_concept(
                concept
            )

        else:

            question_text = ""

        if correct_match:

            set_current_answer(
                correct_match.group(1)
            )

        if explanation_match:

            set_current_explanation(
                explanation_match.group(1).strip()
            )

        save_question(
            difficulty=difficulty,
            question=question_text,
            options={},
            correct_answer=correct_match.group(1)
            if correct_match
            else "",
            explanation=
            explanation_match.group(1).strip()
            if explanation_match
            else "",
            provider="current_provider"
        )

        question_only = re.split(
            r"CORRECT:",
            mcq
        )[0]

        print("\n")
        print(question_only)

        continue

    history.append(
        {
            "role": "user",
            "content": question
        }
    )

    if is_quiz_active():

        answer = question.strip()

        correct = check_answer(answer)

        if correct:

            print("\n✅ Correct")

        else:

            print("\n❌ Wrong")

        print(
            "\nExplanation:\n"
        )

        print(
            get_current_explanation()
        )

        if is_quiz_complete():

            state = get_quiz_state()

            print(
                f"\nQuiz Complete!"
            )

            print(
                f"Score: {state['score']}/{state['total_questions']}"
            )

            from quiz_manager import end_quiz

            end_quiz()

            continue

        print("\nGenerating Next Question...")

        state = get_quiz_state()
        topic = state["topics"][0]

        results = collection.query(
            query_texts=[topic],
            n_results=2
        )

        context = "\n".join(results["documents"][0])

        mcq = generate_mcq(
            context,
            state["difficulty"],
            get_asked_questions(),
            get_asked_concepts()
        )

        import re

        question_match = re.search(
            r"QUESTION:\s*(.*?)\s*A\)",
            mcq,
            re.DOTALL
        )

        correct_match = re.search(
            r"CORRECT:\s*([ABCD])",
            mcq
        )

        explanation_match = re.search(
            r"EXPLANATION:\s*(.*)",
            mcq,
            re.DOTALL
        )

        if question_match:

            question_text = (
                question_match.group(1)
                .strip()
            )

            add_asked_question(
                question_text
            )

            concept = extract_concept(
                question_text
            )

            add_asked_concept(
                concept
            )

        else:

            question_text = ""

        if correct_match:

            set_current_answer(
                correct_match.group(1)
            )

        if explanation_match:

            set_current_explanation(
                explanation_match.group(1).strip()
            )

        save_question(
            difficulty=difficulty,
            question=question_text,
            options={},
            correct_answer=correct_match.group(1)
            if correct_match
            else "",
            explanation=
            explanation_match.group(1).strip()
            if explanation_match
            else "",
            provider="current_provider"
        )

        question_only = re.split(
            r"CORRECT:",
            mcq
        )[0]

        print("\n")
        print(question_only)

        continue

    # -----------------------------
    # INTENT

    if is_quiz_active():

        intent = "QUIZ_ANSWER"

    else:

        intent = classify_intent(
            question
        )

    print(
        f"\nDetected Intent: {intent}"
    )

    retrieve = should_retrieve(
        intent
    )

    print(
        f"\nRetrieve Context: {retrieve}"
    )

    # -----------------------------
    # BEHAVIOR
    # -----------------------------

    if intent == "CONCEPT":

        behavior_prompt = concept_prompt()

    elif intent == "HOMEWORK":

        behavior_prompt = homework_prompt()

    elif intent == "STUDY_PLAN":

        behavior_prompt = study_prompt()

    else:

        behavior_prompt = concept_prompt()

    # -----------------------------
    # RETRIEVAL
    # -----------------------------

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

    # -----------------------------
    # HISTORY CONTEXT
    # -----------------------------

    history_text = ""

    for msg in history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # -----------------------------
    # PROMPT
    # -----------------------------

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


    # -----------------------------
    # GPT
    # -----------------------------

    response = ask_llm(prompt)

    print("\n")
    print("=" * 70)
    print("BATMAN-STUDENT")
    print("=" * 70)
    print("\n")

    print(response)

    history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    save_history(
        student_id,
        history
    )
