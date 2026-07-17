from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from src.behavior.intent_classifier import classify_intent
from src.behavior.batman_router import choose_skill

from src.behavior.concept_teacher import get_prompt as concept_prompt
from src.behavior.homework_guide import get_prompt as homework_prompt
from src.behavior.study_coach import get_prompt as study_prompt
from src.behavior.solved_example import get_prompt as solved_example_prompt

from src.retrieval.retrieval_router import should_retrieve

from src.conversation.conversation_manager import load_history
from src.conversation.conversation_manager import save_history

from src.conversation.pending_action_manager import (
    build_pending_action_prompt,
    clear_pending_action,
    extract_pending_action_from_response,
    load_pending_action,
    resolve_pending_action_response,
    save_pending_action
)

from src.quiz.quiz_parser import parse_quiz_request
from src.quiz.quiz_generator import generate_mcq

from src.quiz.quiz_manager import (
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

from src.retrieval.knowledge_provider import get_collection

#import chromadb
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent

rules = (
    PROJECT_ROOT
    / "docs"
    / "standards"
    / "student_tutor_rules.md"
).read_text(
    encoding="utf-8"
)


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


def build_safe_history_text(history):

    history_text = ""

    for msg in history:

        role = msg.get(
            "role"
        )

        content = msg.get(
            "content"
        )

        if not role or content is None:

            continue

        msg_mode = msg.get(
            "mode",
            "SUPER_CHAT"
        )

        msg_subject = msg.get(
            "subject",
            ""
        )

        history_text += (
            f"[{msg_mode}] "
            f"[{msg_subject}] "
            f"{role}: "
            f"{content}\n"
        )

    return history_text


def build_subject_followup_instruction(subject):

    if subject != "Biology":

        return ""

    return (
        "For Biology learning responses, end with one short follow-up "
        "offer beginning with 'Would you like'. Example: "
        "'Would you like me to explain this with an example?'"
    )

# ---------------------------------
# KNOWLEDGE ACCESS
# ---------------------------------

collection = get_collection()
# ---------------------------------
# QUIZ HELPERS
# ---------------------------------

def build_quiz_question(
    topic,
    difficulty
):

    if collection is not None:

        results = collection.query(
            query_texts=[topic],
            n_results=2
        )

        context = "\n".join(
            results["documents"][0]
        )

    else:

        context = (
            "Knowledge Base is currently unavailable."
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

    if isinstance(
        question,
        dict
    ):

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

            answer = (
                "Okay. I will leave that for now. "
                "Ask me anything else when you are ready."
            )

            history.append(
                {
                    "mode": "LEARN",
                    "subject": question.get(
                        "subject",
                        ""
                    ),
                    "role": "assistant",
                    "content": answer
                }
            )

            save_history(
                student_id,
                history
            )

            return answer

        if decision_name in [
            "ACCEPT_PENDING_ACTION",
            "REFINE_PENDING_ACTION",
            "SIMPLIFY_CONTEXT",
            "SUMMARIZE_CONTEXT"
        ]:

            student_text = question.get(
                "text",
                question.get(
                    "response",
                    ""
                )
            )

            history.append(
                {
                    "mode": "LEARN",
                    "subject": question.get(
                        "subject",
                        ""
                    ),
                    "role": "user",
                    "content": student_text
                }
            )

            history_text = build_safe_history_text(
                history
            )

            prompt = build_pending_action_prompt(
                student_text,
                pending_action,
                history_text,
                rules,
                pending_decision
            )

            clear_pending_action(
                student_id
            )

            response = client.responses.create(
                model="gpt-5.5",
                input=prompt
            )

            answer = response.output_text

            history.append(
                {
                    "mode": "LEARN",
                    "subject": question.get(
                        "subject",
                        ""
                    ),
                    "role": "assistant",
                    "content": answer
                }
            )

            save_history(
                student_id,
                history
            )

            remember_pending_action(
                student_id,
                answer,
                topic=pending_action.get("topic")
            )

            return answer

        return (
            "I do not have a specific follow-up waiting. "
            "Please type your question in the chat box."
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

    mode = "SUPER_CHAT"
    subject = ""

    if ":" in question:

        possible_subject = (
            question.split(":")[0]
            .strip()
            .upper()
        )

        if possible_subject in [
            "PHYSICS",
            "CHEMISTRY",
            "MATHS",
            "BIOLOGY"
        ]:

            mode = "LEARN"

            subject = (
                possible_subject
                .title()
            )

    history.append(
        {
            "mode": mode,
            "subject": subject,
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

    if retrieve and collection is not None:

        results = collection.query(
            query_texts=[question],
            n_results=2
        )

        context = "\n".join(
            results["documents"][0]
        )

    elif retrieve:

        context = (
            "Knowledge Base is currently unavailable."
        )

    else:

        context = (
            "No textbook context needed."
        )

    # ---------------------------------
    # HISTORY CONTEXT
    # ---------------------------------

    history_text = build_safe_history_text(
        history
    )

    followup_instruction = build_subject_followup_instruction(
        subject
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

FOLLOW-UP RULE:

{followup_instruction}

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
            "mode": mode,
            "subject": subject,
            "role": "assistant",
            "content": answer
        }
    )

    save_history(
        student_id,
        history
    )

    remember_pending_action(
        student_id,
        answer,
        topic=question
    )

    return answer
