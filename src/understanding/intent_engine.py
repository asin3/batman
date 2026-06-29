"""
============================================================
Batman Student

Module:
intent_engine.py

Purpose:
Determine the student's primary intent using
Python-first rules.

LLM is NOT used in this module.

============================================================
"""

import re


# ---------------------------------------------------------
# INTENT KEYWORDS
# ---------------------------------------------------------

INTENT_PATTERNS = {

    "QUIZ": [

        r"\bquiz\b",
        r"\btest me\b",
        r"\bmcq\b",
        r"\bquestion me\b"

    ],

    "HOMEWORK": [

        r"\bhomework\b",
        r"\bassignment\b",
        r"\bsolve\b"

    ],

    "CONCEPT": [

        r"\bwhat is\b",
        r"\bdefine\b",
        r"\bexplain\b",
        r"\bmeaning\b"

    ],

    "REVISION": [

        r"\brevise\b",
        r"\brevision\b"

    ],

    "STUDY_PLAN": [

        r"\bstudy plan\b",
        r"\bschedule\b",
        r"\btimetable\b"

    ]

}


# ---------------------------------------------------------
# DETECT INTENT
# ---------------------------------------------------------

def detect_intent(

    student_text

):

    text = student_text.lower().strip()

    for intent, patterns in INTENT_PATTERNS.items():

        for pattern in patterns:

            if re.search(

                pattern,
                text

            ):

                return {

                    "name": intent,

                    "confidence": 1.0,

                    "source": "python"

                }

    return {

        "name": "UNKNOWN",

        "confidence": 0.0,

        "source": "python"

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    tests = [

        "Quiz me on Force",

        "Explain Light",

        "Homework on Electricity",

        "Prepare a study plan",

        "Revise Machines",

        "Hello Batman"

    ]

    for test in tests:

        print()

        print(test)

        print(

            detect_intent(

                test

            )

        )