"""
============================================================
Batman Student

Module:
engine.py

Purpose:
Central orchestrator for Batman's Understanding Engine.

This module coordinates all understanding components:

Intent
Entities
Confidence
Clarification
Learning

It contains NO business logic.

============================================================
"""

from src.understanding.intent_engine import detect_intent
from src.understanding.entity_extractor import extract_entities
from src.understanding.confidence_engine import calculate_confidence
from src.understanding.clarification_engine import needs_clarification
from src.understanding.learning_engine import learn_interpretation

from src.understanding.conversation_state import (
    update_state,
    build_understanding,
    reset_state
)

# ---------------------------------------------------------
# UNDERSTAND
# ---------------------------------------------------------

def understand(
    student_text,
    student_id=None
):

    # -----------------------------------------------------
    # STEP 1
    # Intent
    # -----------------------------------------------------

    intent = detect_intent(
        student_text
    )

    # -----------------------------------------------------
    # STEP 2
    # Entity Extraction
    # -----------------------------------------------------

    entities = extract_entities(
        student_text,
        intent
    )

    # -----------------------------------------------------
    # STEP 2A
    # Conversation State
    # -----------------------------------------------------

    update_state(
        intent,
        entities
    )

    state = build_understanding()

    intent = state["intent"]

    entities = state["entities"]

    # -----------------------------------------------------
    # STEP 3
    # Confidence
    # -----------------------------------------------------

    confidence = calculate_confidence(
        intent,
        entities
    )

    # -----------------------------------------------------
    # STEP 4
    # Clarification
    # -----------------------------------------------------

    clarification = needs_clarification(
        intent,
        entities,
        confidence
    )

    # -----------------------------------------------------
    # STEP 5
    # Learning
    # -----------------------------------------------------

    if clarification is None:
     
        learn_interpretation(
            student_text,
            intent,
            entities
        )

        reset_state()

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {

        "intent": intent,

        "entities": entities,

        "confidence": confidence,

        "clarification": clarification

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    tests = [

        "Quiz me",

        "Force",

        "Easy",

        "5"

    ]

    for test in tests:

        print("\nStudent:", test)

        print(

            understand(

                test

            )

        )