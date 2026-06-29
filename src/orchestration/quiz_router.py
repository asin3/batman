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

    display_mcq(sample)