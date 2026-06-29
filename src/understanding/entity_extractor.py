"""
============================================================
Batman Student

Module:
entity_extractor.py

Purpose:
Extract structured entities from student input.

This module performs generic extraction only.

It does NOT validate whether extracted entities
exist in the textbook.

LLM is NOT used.

============================================================
"""

import re


# ---------------------------------------------------------
# DIFFICULTIES
# ---------------------------------------------------------

DIFFICULTIES = [

    "easy",
    "medium",
    "hard"

]


# ---------------------------------------------------------
# COMMAND PHRASES
# ---------------------------------------------------------

COMMAND_PATTERNS = [

    r"\bquiz me on\b",
    r"\bquiz me\b",
    r"\btest me on\b",
    r"\btest me\b",
    r"\bask me\b",
    r"\bgive me an\b",
    r"\bgive me a\b",
    r"\bgive me\b",
    r"\bquestions on\b",
    r"\bquiz on\b",
    r"\bquiz\b"

]


# ---------------------------------------------------------
# EXTRACT ENTITIES
# ---------------------------------------------------------

def extract_entities(

    student_text,
    intent

):

    text = student_text.strip()

    text_lower = text.lower()

    entities = {

        "topic": None,

        "difficulty": None,

        "count": None,

        "subject": None

    }

    # -----------------------------------------------------
    # Difficulty
    # -----------------------------------------------------

    for difficulty in DIFFICULTIES:

        if difficulty in text_lower:

            entities["difficulty"] = (

                difficulty.capitalize()

            )

            break

    # -----------------------------------------------------
    # Question Count
    # -----------------------------------------------------

    match = re.search(

        r"\b(\d+)\b",

        text

    )

    if match:

        entities["count"] = int(

            match.group(1)

        )

    # -----------------------------------------------------
    # Topic Extraction
    # -----------------------------------------------------

    cleaned = text

    # Remove command phrases

    for pattern in COMMAND_PATTERNS:

        cleaned = re.sub(

            pattern,

            "",

            cleaned,

            flags=re.IGNORECASE

        )

    # Remove difficulty

    cleaned = re.sub(

        r"\beasy\b|\bmedium\b|\bhard\b",

        "",

        cleaned,

        flags=re.IGNORECASE

    )

    # Remove numbers

    cleaned = re.sub(

        r"\b\d+\b",

        "",

        cleaned

    )

    # Normalize spaces

    cleaned = " ".join(

        cleaned.split()

    )

    cleaned = cleaned.strip()

    # Ignore empty/filler values

    if cleaned.lower() in [

        "",

        "me"

    ]:

        cleaned = ""

    if cleaned:

        entities["topic"] = cleaned.title()

    return entities


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    tests = [

        "Quiz me",

        "Quiz me on Force",

        "Test me",

        "Test me on Light",

        "Ask me 5 questions on Force",

        "Give me an easy quiz on Current Electricity"

    ]

    for test in tests:

        print()

        print(test)

        print(

            extract_entities(

                test,

                {

                    "name": "QUIZ"

                }

            )

        )