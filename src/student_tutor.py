from src.config.paths import (
    DOCS_DIR,
    VECTOR_DB_DIR,
)

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from src.behavior.intent_classifier import classify_intent
from src.behavior.concept_teacher import get_prompt as concept_prompt
from src.behavior.homework_guide import get_prompt as homework_prompt
from src.behavior.study_coach import get_prompt as study_prompt
from src.retrieval.retrieval_router import should_retrieve

from src.conversation.conversation_manager import (
    load_history,
    save_history,
    save_quiz_history
)

from src.quiz.quiz_parser import parse_quiz_request

from src.quiz.quiz_generator import (
    generate_mcq,
    extract_concept
)

from src.question_bank import (
    save_question
)

from src.llm.provider_router import (
    ask_llm,
    get_current_provider
)

from src.quiz.quiz_manager import (
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

from src.governance.learning_state import (
    update_learning_state
)

from src.governance.topic_normalizer import (
    normalize_topic_name
)

from src.understanding.engine import (
    understand
)

from src.orchestration.tutor_router import (
    build_history_text
)

from src.orchestration.quiz_router import (
    display_mcq,
    parse_mcq
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

rules = (
    DOCS_DIR
    / "standards"
    / "student_tutor_rules.md"
).read_text(
    encoding="utf-8"
)

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
    path=str(VECTOR_DB_DIR)
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

    understanding = None

    # -----------------------------
    # EXIT
    # -----------------------------

    if question.lower() == "exit":

        print(
            "\nSession Ended"
        )

        break

    # -----------------------------   
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

        print("\nStarting Quiz...")

        start_quiz()

        continue

    # -----------------------------
    # START QUIZ
    # -----------------------------

    if (

        understanding

        and

        understanding["intent"]

        and

        understanding["intent"]["name"] == "QUIZ"

    ):
    
        history.append(
            {
                "role": "user",
                "content": question
            }
        )

        save_history(
            student_id,
            history
        )
        # -----------------------------
        # UNDERSTANDING RESULT
        # -----------------------------

        topics = []

        if understanding["entities"]["topic"]:

            topics.append(

                understanding["entities"]["topic"]

            )

        difficulty = understanding["entities"]["difficulty"]

        count = understanding["entities"]["count"] or 0

        topics = [

            normalize_topic_name(topic)

            for topic in topics

        ]
        
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

        update_learning_state(
            student_id,
            subject="Physics",
            chapter=topic,
            topic=topic,
            last_question=question
        )

        results = collection.query(
            query_texts=[topic],
            n_results=2
        )

        context = "\n".join(results["documents"][0])

        metadata = results["metadatas"][0][0]

        update_learning_state(
            student_id,
            board=metadata.get("board"),
            grade=metadata.get("grade"),
            subject=metadata.get("subject"),
            chapter=metadata.get("chapter"),
            topic=metadata.get("topic"),
            last_question=question
        )

        mcq = generate_mcq(
            context,
            difficulty,
            get_asked_questions(),
            get_asked_concepts()
        )

        import re

        question_match, correct_match, explanation_match = parse_mcq(
            mcq
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
            provider=get_current_provider()
        )

        question_only = display_mcq(
            mcq
        )

        history.append(
            {
                "role": "assistant",
                "content": question_only
            }
        )

        save_history(
            student_id,
            history
        )

        continue

    if not is_quiz_active():

        history.append(
            {
                "role": "user",
                "content": question
            }
        )

    if is_quiz_active():

        answer = question.strip()

        history.append(
        {
            "role": "user",
            "content": answer
        }
        )

        save_history(
            student_id,
            history
        )

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

        history.append(
            {
                "role": "assistant",
                "content":
                    get_current_explanation()
            }
        )

        save_history(
            student_id,
            history
        )

        if is_quiz_complete():

            state = get_quiz_state()

            print(
                f"\nQuiz Complete!"
            )

            print(
                f"Score: {state['score']}/{state['total_questions']}"
            )

            save_quiz_history(
                student_id=student_id,
                subject="Physics",
                chapter=state["topics"][0],
                difficulty=state["difficulty"],
                score=state["score"],
                total=state["total_questions"]
            )

            from src.quiz.quiz_manager import end_quiz

            end_quiz()

            continue

        print("\nGenerating Next Question...")

        state = get_quiz_state()
        topic = state["topics"][0]

        update_learning_state(
            student_id,
            subject="Physics",
            chapter=topic,
            topic=topic
        )

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

        question_match, correct_match, explanation_match = parse_mcq(
            mcq
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
            difficulty=state["difficulty"],
            question=question_text,
            options={},
            correct_answer=correct_match.group(1)
            if correct_match
            else "",
            explanation=
            explanation_match.group(1).strip()
            if explanation_match
            else "",
            provider=get_current_provider()
        )

        question_only = display_mcq(
            mcq
        )

        history.append(
            {
                "role": "assistant",
                "content": question_only
            }
        )

        save_history(
            student_id,
            history
        )

        continue
    
    # -----------------------------
    # UNDERSTANDING ENGINE
    # -----------------------------

    if question.lower() not in ["a", "b", "c", "d"]:

        understanding = understand(

            question,

            student_id

        )

    print("\nUNDERSTANDING")

    print(understanding)

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

        metadata = results["metadatas"][0][0]

        print("\nDEBUG METADATA")
        print(metadata)

        update_learning_state(
            student_id,
            board=metadata.get("board"),
            grade=metadata.get("grade"),
            subject=metadata.get("subject"),
            chapter=metadata.get("chapter"),
            topic=metadata.get("topic"),
            last_question=question
        )

        print("\nLearning State Updated")

    else:

        context = (
            "No textbook context needed."
        )

    # -----------------------------
    # HISTORY CONTEXT
    # -----------------------------

    history_text = build_history_text(
        history
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
