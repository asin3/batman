"""
============================================================
Batman Student

Module:
quiz_router.py

Purpose:
Quiz orchestration.

This module will gradually receive all quiz
execution logic from student_tutor.py.

============================================================
"""


# ---------------------------------------------------------
# DISPLAY MCQ
# ---------------------------------------------------------

import re


def display_mcq(mcq):

    question_only = re.split(

        r"CORRECT:",

        mcq

    )[0]

    print("\n")

    print(question_only)

    return question_only

# ---------------------------------------------------------
# PARSE MCQ
# ---------------------------------------------------------

def parse_mcq(mcq):

    question_match = re.search(

        r"QUESTION:\s*(.*?)\s*A\)",

        mcq,

        re.DOTALL

    )

    correct_match = re.search(

        r"CORRECT:\s*([ABCD])",

        mcq

    )

    explanation_match = re.search(

        r"EXPLANATION:\s*(.*)",

        mcq,

        re.DOTALL

    )

    return (

        question_match,

        correct_match,

        explanation_match

    )


# ---------------------------------------------------------
# HANDLE QUIZ
# ---------------------------------------------------------

def handle_quiz():

    pass


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    sample = """

QUESTION:
What is Force?

A) Push

B) Pull

C) Both

D) None

CORRECT: C

EXPLANATION:
Force is a push or pull.

"""

    question_match, correct_match, explanation_match = parse_mcq(sample)

    print(question_match.group(1).strip())

    print(correct_match.group(1))

    print(explanation_match.group(1).strip())