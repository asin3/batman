"""
============================================================
Batman Student

Module:
clarification_engine.py

Purpose:
Determine the next clarification question required
to complete Batman's understanding.

Batman asks ONE question at a time.

============================================================
"""


# ---------------------------------------------------------
# CLARIFICATION QUESTIONS
# ---------------------------------------------------------

QUESTIONS = {

    "topic":

        "Which topic?",

    "difficulty":

        "Difficulty? Easy / Medium / Hard",

    "count":

        "How many questions?"

}


# ---------------------------------------------------------
# NEEDS CLARIFICATION
# ---------------------------------------------------------

def needs_clarification(

    intent,
    entities,
    confidence

):

    if confidence["complete"]:

        return None

    field = confidence["missing"][0]

    return {

        "field": field,

        "question": QUESTIONS[field]

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    confidence = {

        "complete": False,

        "missing": [

            "difficulty",

            "count"

        ]

    }

    print(

        needs_clarification(

            {},

            {},

            confidence

        )

    )