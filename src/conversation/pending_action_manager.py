"""
============================================================
Batman Student

Module:
pending_action_manager.py

Purpose:
Store and resolve Batman's pending conversational offers.

Owner:
Conversation Intelligence

Reads:
- Student pending action state
- Student response text or structured UI event

Writes:
- data/students/<student_id>/pending_action.json

Governed By:
ADR-004 Data Governance
ADR-006 Batman Understanding Engine
ADR-012 Hybrid Educational Intelligence Architecture
============================================================
"""

from datetime import datetime
import json
import re
from uuid import uuid4

from src.config.paths import DATA_DIR


PENDING_ACTION_STATUS = "PENDING"

TERMINAL_DECISIONS = {
    "ACCEPT_PENDING_ACTION",
    "REJECT_PENDING_ACTION",
    "REFINE_PENDING_ACTION",
    "SIMPLIFY_CONTEXT",
    "SUMMARIZE_CONTEXT",
}


def _student_folder(student_id, data_dir=DATA_DIR):

    folder = (
        data_dir
        / "students"
        / student_id
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def get_pending_action_path(
    student_id,
    data_dir=DATA_DIR
):

    return (
        _student_folder(
            student_id,
            data_dir=data_dir
        )
        / "pending_action.json"
    )


def load_pending_action(
    student_id,
    data_dir=DATA_DIR
):

    path = get_pending_action_path(
        student_id,
        data_dir=data_dir
    )

    if not path.exists():

        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        action = json.load(file)

    if action.get("status") != PENDING_ACTION_STATUS:

        return None

    return action


def save_pending_action(
    student_id,
    pending_action,
    data_dir=DATA_DIR
):

    path = get_pending_action_path(
        student_id,
        data_dir=data_dir
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            pending_action,
            file,
            indent=2
        )

    return pending_action


def clear_pending_action(
    student_id,
    data_dir=DATA_DIR
):

    path = get_pending_action_path(
        student_id,
        data_dir=data_dir
    )

    if path.exists():

        path.unlink()


def build_pending_action(
    offer_text,
    topic=None,
    action_type="EXPLAIN_MORE",
    source="assistant_offer"
):

    return {
        "action_id": str(
            uuid4()
        ),
        "action_type": action_type,
        "topic": topic,
        "offer_text": offer_text,
        "source": source,
        "status": PENDING_ACTION_STATUS,
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }


def _infer_action_type(offer_text):

    lowered = offer_text.lower()

    if "quiz" in lowered or "test your understanding" in lowered:

        return "START_QUIZ"

    if "summar" in lowered:

        return "SUMMARIZE"

    if "example" in lowered:

        return "SHOW_EXAMPLE"

    return "EXPLAIN_MORE"


def extract_pending_action_from_response(
    response_text,
    topic=None
):

    if not response_text:

        return None

    lowered = response_text.lower()

    offer_markers = [
        "would you like",
        "do you want",
        "shall i",
        "should i",
        "want me to",
        "would you want",
        "would it help"
    ]

    if not any(marker in lowered for marker in offer_markers):

        return None

    return build_pending_action(
        offer_text=response_text,
        topic=topic,
        action_type=_infer_action_type(
            response_text
        )
    )


def _normalize_text(text):

    return re.sub(
        r"\s+",
        " ",
        text.strip().lower()
    )


def _has_token_overlap(
    text,
    pending_action
):

    haystack = " ".join(
        str(value or "")
        for value in [
            pending_action.get("topic"),
            pending_action.get("offer_text")
        ]
    ).lower()

    words = {
        word
        for word in re.findall(
            r"[a-zA-Z]{4,}",
            text.lower()
        )
    }

    ignored = {
        "what",
        "explain",
        "difference",
        "between",
        "please",
        "about",
        "again",
        "that",
        "this"
    }

    words = words - ignored

    return any(
        word in haystack
        for word in words
    )


def _resolve_structured_event(
    event,
    pending_action
):

    if event.get("type") != "PENDING_ACTION_RESPONSE":

        return None

    if event.get("action_id") != pending_action.get("action_id"):

        return {
            "decision": "ASK_CLARIFICATION",
            "reason": "Action id does not match pending action."
        }

    response = (
        event.get("response", "")
        .strip()
        .upper()
    )

    if response == "ACCEPT":

        return {
            "decision": "ACCEPT_PENDING_ACTION",
            "reason": "Structured UI accept."
        }

    if response == "REJECT":

        return {
            "decision": "REJECT_PENDING_ACTION",
            "reason": "Structured UI reject."
        }

    if response == "OTHER":

        return {
            "decision": "REFINE_PENDING_ACTION",
            "reason": "Structured UI custom response.",
            "text": event.get("text", "")
        }

    return {
        "decision": "ASK_CLARIFICATION",
        "reason": "Unknown structured response."
    }


def resolve_pending_action_response(
    student_input,
    pending_action
):

    if not pending_action:

        return {
            "decision": "NO_PENDING_ACTION",
            "reason": "No pending action exists."
        }

    if isinstance(
        student_input,
        dict
    ):

        structured_decision = _resolve_structured_event(
            student_input,
            pending_action
        )

        if structured_decision:

            return structured_decision

    text = str(
        student_input
    )

    normalized = _normalize_text(
        text
    )

    if not normalized:

        return {
            "decision": "ASK_CLARIFICATION",
            "reason": "Empty response."
        }

    if re.fullmatch(
        r"(no|nope|not now|later|skip|cancel|stop|leave it)",
        normalized
    ):

        return {
            "decision": "REJECT_PENDING_ACTION",
            "reason": "Student rejected pending action."
        }

    if re.fullmatch(
        r"(yes|yes please|yeah|yep|sure|ok|okay|go ahead|continue|please do|do it|proceed|explain it|explain that)",
        normalized
    ):

        return {
            "decision": "ACCEPT_PENDING_ACTION",
            "reason": "Student accepted pending action."
        }

    if re.search(
        r"(did not understand|didn't understand|not clear|confused|make it simpler|simpler|re-?explain|again)",
        normalized
    ):

        return {
            "decision": "SIMPLIFY_CONTEXT",
            "reason": "Student asked for simpler explanation."
        }

    if re.search(
        r"(summarize|summary|short version|in short)",
        normalized
    ):

        return {
            "decision": "SUMMARIZE_CONTEXT",
            "reason": "Student asked for summary."
        }

    if re.search(
        r"\b(quiz|test me|mcq|question me)\b",
        normalized
    ):

        return {
            "decision": "START_QUIZ_FROM_CONTEXT",
            "reason": "Student wants quiz instead."
        }

    if (
        _has_token_overlap(
            normalized,
            pending_action
        )
        or
        re.search(
            r"^(explain|tell me about|what about|difference between|compare)\b",
            normalized
        )
    ):

        return {
            "decision": "REFINE_PENDING_ACTION",
            "reason": "Student refined the pending action."
        }

    if re.search(
        r"^(what is|define|homework|solve|study plan|revise|revision)\b",
        normalized
    ):

        return {
            "decision": "REPLACE_WITH_NEW_REQUEST",
            "reason": "Student started a new request."
        }

    return {
        "decision": "ASK_CLARIFICATION",
        "reason": "Pending action response is ambiguous."
    }


def build_pending_action_prompt(
    student_text,
    pending_action,
    history_text,
    rules,
    decision
):

    return f"""
BATMAN PENDING ACTION MODE:

Batman previously offered this action:

Action Type:
{pending_action.get("action_type")}

Topic:
{pending_action.get("topic")}

Offer:
{pending_action.get("offer_text")}

Student response decision:
{decision.get("decision")}

Student response:
{student_text}

Rules:
- Continue from the stored pending action.
- Do not treat the student's response as a new textbook topic.
- If the decision is SIMPLIFY_CONTEXT, re-explain more simply.
- If the decision is SUMMARIZE_CONTEXT, give a concise summary.
- If the decision is REFINE_PENDING_ACTION, focus on the student's requested part.
- Keep the answer grounded in the previous conversation and Batman teaching rules.

GLOBAL RULES:

{rules}

CONVERSATION HISTORY:

{history_text}
"""
