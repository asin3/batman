"""
============================================================
Batman Student

Module:
confidence_engine.py

Purpose:
Evaluate how complete Batman's understanding is.

This module does NOT guess.

It reports:

• Which fields are resolved
• Which fields are missing
• Whether Batman has enough information
  to continue

============================================================
"""


# ---------------------------------------------------------
# REQUIRED FIELDS
# ---------------------------------------------------------

REQUIRED_FIELDS = {

    "QUIZ": [

        "topic",
        "difficulty",
        "count"

    ],

    "CONCEPT": [

        "topic"

    ],

    "HOMEWORK": [

        "topic"

    ],

    "REVISION": [

        "topic"

    ],

    "STUDY_PLAN": []

}


# ---------------------------------------------------------
# CALCULATE
# ---------------------------------------------------------

def calculate_confidence(

    intent,
    entities

):

    intent_name = intent["name"]

    required = REQUIRED_FIELDS.get(

        intent_name,

        []

    )

    missing = []

    resolved = 0

    for field in required:

        if entities.get(field) is None:

            missing.append(

                field

            )

        else:

            resolved += 1

    return {

        "complete": len(missing) == 0,

        "resolved": resolved,

        "required": len(required),

        "missing": missing

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    intent = {

        "name": "QUIZ"

    }

    entities = {

        "topic": "Force",

        "difficulty": None,

        "count": None

    }

    print(

        calculate_confidence(

            intent,

            entities

        )

    )