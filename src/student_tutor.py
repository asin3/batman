
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.runtime_error_boundary import (
    install_runtime_error_boundary
)

install_runtime_error_boundary()

from src.config.paths import (
    DOCS_DIR,
)

from dotenv import load_dotenv
from openai import OpenAI

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

from src.conversation.pending_action_manager import (
    build_pending_action_prompt,
    clear_pending_action,
    extract_pending_action_from_response,
    load_pending_action,
    resolve_pending_action_response,
    save_pending_action
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

from src.understanding.engine import (
    understand
)

from src.understanding.topic_context_resolver import (
    resolve_topic_context
)

from src.orchestration.tutor_router import (

    build_history_text,

    route_request

)

from src.orchestration.quiz_router import (
    display_mcq,
    parse_mcq
)

from src.retrieval.retrieval_engine import (
    retrieve as retrieve_knowledge
)

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

# RETRIEVAL CONTEXT

# ---------------------------------

def build_retrieval_context(
    question,
    top_k=5
):

    results = retrieve_knowledge(
        question,
        top_k=top_k
    )

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    return context, results


def remember_pending_action(
    student_id,
    response_text,
    topic=None
):

    pending_action = extract_pending_action_from_response(
        response_text,
        topic=topic
    )

    if pending_action:

        save_pending_action(
            student_id,
            pending_action
        )

    return pending_action

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
    # PENDING ACTION
    # -----------------------------

    if not is_quiz_active():

        pending_action = load_pending_action(
            student_id
        )

        pending_decision = resolve_pending_action_response(
            question,
            pending_action
        )

        decision_name = pending_decision["decision"]

        if decision_name == "REJECT_PENDING_ACTION":

            clear_pending_action(
                student_id
            )

            history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            response = (
                "Okay. I will leave that for now. "
                "Ask me anything else when you are ready."
            )

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

            continue

        if decision_name in [
            "ACCEPT_PENDING_ACTION",
            "REFINE_PENDING_ACTION",
            "SIMPLIFY_CONTEXT",
            "SUMMARIZE_CONTEXT"
        ]:

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

            history_text = build_history_text(
                history
            )

            prompt = build_pending_action_prompt(
                question,
                pending_action,
                history_text,
                rules,
                pending_decision
            )

            clear_pending_action(
                student_id
            )

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

            remember_pending_action(
                student_id,
                response,
                topic=pending_action.get("topic")
            )

            continue

        if decision_name == "ASK_CLARIFICATION":

            offer_text = pending_action.get(
                "offer_text",
                "the previous offer"
            )

            print(
                "\nDo you want me to continue with this, "
                "skip it, or ask something else?"
            )

            print()
            print(offer_text)

            continue

        if decision_name in [
            "REPLACE_WITH_NEW_REQUEST",
            "START_QUIZ_FROM_CONTEXT"
        ]:

            clear_pending_action(
                student_id
            )

    # -----------------------------
    # UNDERSTANDING ENGINE
    # -----------------------------

    if question.lower() not in ["a", "b", "c", "d"]:

        understanding = understand(

            question,

            student_id

        )

    # -----------------------------
    # CONTINUATION
    # -----------------------------

    if (

        not is_quiz_active()

        and

        understanding

        and

        understanding["intent"]

        and

        understanding["intent"]["name"] == "CONTINUATION"

    ):

        history.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = (
            "I do not have a specific follow-up waiting. "
            "Tell me which part you want me to continue or explain."
        )

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

        remember_pending_action(
            student_id,
            response
        )

        continue

    # -----------------------------
    # START QUIZ
    # -----------------------------

    response_topic = None

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

        topic_decision = resolve_topic_context(
            understanding,
            student_id=student_id
        )

        topics = []

        if topic_decision["resolved_topic"]:

            topics.append(

                topic_decision["resolved_topic"]

            )

        difficulty = understanding["entities"]["difficulty"]

        count = understanding["entities"]["count"] or 0
        
        if topic_decision["needs_clarification"] or not topics:
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

        context, retrieval_results = build_retrieval_context(
            topic,
            top_k=2
        )

        print("\nDEBUG QUIZ CONTEXT")
        print(f"Parsed Topics       : {topics}")
        print(f"Selected Quiz Topic : {topic}")
        print(f"Topic Source        : {topic_decision['source']}")
        print(
            "Retrieval Chunks    : "
            f"{[result['chunk_id'] for result in retrieval_results]}"
        )
        print(
            "Retrieval Headings  : "
            f"{[result['heading'] for result in retrieval_results]}"
        )
        print(
            "Top Heading         : "
            f"{retrieval_results[0]['heading'] if retrieval_results else None}"
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

        context, retrieval_results = build_retrieval_context(
            topic,
            top_k=2
        )

        print("\nDEBUG QUIZ CONTEXT")
        print(f"Parsed Topics       : {topics}")
        print(f"Selected Quiz Topic : {topic}")
        print(
            "Retrieval Chunks    : "
            f"{[result['chunk_id'] for result in retrieval_results]}"
        )
        print(
            "Retrieval Headings  : "
            f"{[result['heading'] for result in retrieval_results]}"
        )
        print(
            "Top Heading         : "
            f"{retrieval_results[0]['heading'] if retrieval_results else None}"
        )

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

    if (

        understanding

        and

        understanding["intent"]

        and

        understanding["intent"]["name"]
        in ["CONCEPT", "HOMEWORK", "REVISION"]

    ):

        tutor_topic_decision = resolve_topic_context(
            understanding,
            learning_state={},
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        if tutor_topic_decision["source"] == "explicit":

            update_learning_state(
                student_id,
                subject="Physics",
                chapter=tutor_topic_decision["resolved_topic"],
                topic=tutor_topic_decision["resolved_topic"],
                last_question=question
            )

            print(
                "\nCurrent Topic Updated : "
                f"{tutor_topic_decision['resolved_topic']}"
            )

            response_topic = tutor_topic_decision["resolved_topic"]
    
    print("\nUNDERSTANDING")

    print(understanding)

    route = route_request(
        understanding
    )

    if route == "QUIZ":

        print("\nRouter -> Quiz")

    else:

        print("\nRouter -> Tutor")

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

        context, retrieval_results = build_retrieval_context(
            question
        )

        print("\nDEBUG RETRIEVAL")

        print(
            f"Chunks Retrieved: "
            f"{len(retrieval_results)}"
        )

        if retrieval_results:

            print(
                f"Top Chunk: "
                f"{retrieval_results[0]['chunk_id']}"
            )

            print(
                f"Top Heading: "
                f"{retrieval_results[0]['heading']}"
            )

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

    remember_pending_action(
        student_id,
        response,
        topic=response_topic
    )
