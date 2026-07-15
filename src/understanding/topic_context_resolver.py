"""
============================================================
Batman Student

Module:
topic_context_resolver.py

Purpose:
Resolve the academic topic for a student request without
letting command words become textbook topics.

Owner:
Batman Understanding Engine

Reads:
- Understanding result
- Conversation state
- Student learning state

Writes:
-

Governed By:
ADR-006 Batman Understanding Engine
ADR-012 Hybrid Educational Intelligence Architecture
============================================================
"""

import re

from src.governance.learning_state import load_learning_state
from src.governance.topic_normalizer import normalize_topic_name
from src.understanding.conversation_state import get_state


NON_TOPIC_COMMAND_WORDS = {
    "fast",
    "instant",
    "insta",
    "mini",
    "quick",
    "rapid",
    "short",
    "small",
}

CONTEXT_REFERENCE_WORDS = {
    "current",
    "current topic",
    "it",
    "previous",
    "previous topic",
    "same",
    "same topic",
    "that",
    "that topic",
    "this",
    "this topic",
}

LEADING_TOPIC_REQUEST_PATTERNS = [
    r"^define\s+",
    r"^explain\s+",
    r"^homework\s+on\s+",
    r"^meaning\s+of\s+",
    r"^meaning\s+",
    r"^revise\s+",
    r"^revision\s+on\s+",
    r"^solve\s+",
    r"^teach\s+me\s+",
    r"^tell\s+me\s+about\s+",
    r"^what\s+are\s+",
    r"^what\s+is\s+",
]


def _remove_leading_topic_request_words(topic):

    cleaned = topic

    for pattern in LEADING_TOPIC_REQUEST_PATTERNS:

        cleaned = re.sub(
            pattern,
            "",
            cleaned,
            flags=re.IGNORECASE
        )

    return cleaned


def _remove_leading_non_topic_words(topic):

    words = topic.split()

    while words and words[0].lower() in NON_TOPIC_COMMAND_WORDS:

        words.pop(0)

    while words and words[0].lower() == "on":

        words.pop(0)

    return " ".join(words)


def _candidate_topic(value):

    topic = normalize_topic_name(value)

    if not topic:

        return None

    topic = _remove_leading_topic_request_words(
        topic
    )

    topic = _remove_leading_non_topic_words(
        topic
    )

    topic = normalize_topic_name(
        topic
    )

    topic = re.sub(
        r"[?!.]+$",
        "",
        topic
    ).strip()

    if not topic:

        return None

    lowered = topic.lower()

    if lowered in NON_TOPIC_COMMAND_WORDS:

        return None

    if lowered in CONTEXT_REFERENCE_WORDS:

        return None

    return topic


def _learning_state_topic(student_id, learning_state):

    state = learning_state

    if state is None and student_id:

        state = load_learning_state(
            student_id
        )

    if not state:

        return None

    return (
        _candidate_topic(
            state.get("topic")
        )
        or
        _candidate_topic(
            state.get("chapter")
        )
    )


def _conversation_state_topic(conversation_state):

    state = conversation_state

    if state is None:

        state = get_state()

    if not state:

        return None

    topic = _candidate_topic(
        state.get("current_topic")
    )

    if topic:

        return topic

    entities = state.get(
        "entities",
        {}
    )

    return _candidate_topic(
        entities.get("topic")
    )


def resolve_topic_context(
    understanding,
    student_id=None,
    learning_state=None,
    conversation_state=None
):
    """
    Return Batman's topic decision for the current request.

    The decision is intentionally plain dict data so callers can
    route, clarify, log, or test it without importing UI/runtime code.
    """

    entities = {}

    if understanding:

        entities = understanding.get(
            "entities",
            {}
        )

    raw_topic = entities.get("topic")

    explicit_topic = _candidate_topic(
        raw_topic
    )

    if explicit_topic:

        return {
            "explicit_topic": explicit_topic,
            "resolved_topic": explicit_topic,
            "source": "explicit",
            "confidence": 1.0,
            "needs_clarification": False
        }

    learning_topic = _learning_state_topic(
        student_id,
        learning_state
    )

    if learning_topic:

        return {
            "explicit_topic": None,
            "resolved_topic": learning_topic,
            "source": "learning_state",
            "confidence": 0.75,
            "needs_clarification": False
        }

    conversation_topic = _conversation_state_topic(
        conversation_state
    )

    if conversation_topic:

        return {
            "explicit_topic": None,
            "resolved_topic": conversation_topic,
            "source": "conversation_state",
            "confidence": 0.65,
            "needs_clarification": False
        }

    return {
        "explicit_topic": None,
        "resolved_topic": None,
        "source": None,
        "confidence": 0.0,
        "needs_clarification": True
    }
