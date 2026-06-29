"""
===========================================================
Batman Student

Module:
learning_state.py

Purpose:
Manage the student's current learning state.

Owner:
Learning Domain

Reads:
- data/students/<student_id>/learning_state.json

Writes:
- data/students/<student_id>/learning_state.json

Dependencies:
- json
- pathlib

Governed By:
ADR-004 Data Governance

Single Source of Truth:
data/students/<student_id>/learning_state.json

Last Updated:
2026-06-25

===========================================================
"""
from datetime import datetime

import json

from src.config.paths import STUDENTS_DIR


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

STUDENTS = STUDENTS_DIR


# ---------------------------------------------------------
# INTERNAL
# ---------------------------------------------------------

def _state_file(student_id):

    folder = STUDENTS / student_id

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder / "learning_state.json"


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

def load_learning_state(student_id):

    file = _state_file(student_id)

    if not file.exists():

        return {

            "board": "ICSE",

            "grade": "10",

            "subject": "Physics",

            "chapter": None,

            "topic": None,

            "last_question": None,

            "last_updated": None

        }

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

def save_learning_state(
    student_id,
    state
):

    file = _state_file(student_id)

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

def update_learning_state(
    student_id,
    **kwargs
):

    state = load_learning_state(
        student_id
    )

    for key, value in kwargs.items():

        state[key] = value

    state["last_updated"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    save_learning_state(
        student_id,
        state
    )


# ---------------------------------------------------------
# GETTERS
# ---------------------------------------------------------

def get_current_subject(student_id):

    return load_learning_state(
        student_id
    )["subject"]


def get_current_chapter(student_id):

    return load_learning_state(
        student_id
    )["chapter"]


def get_current_topic(student_id):

    return load_learning_state(
        student_id
    )["topic"]


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    student = "STD001"

    update_learning_state(

        student,

        chapter="Force",

        topic="Moment of Force",

        last_question="What is Force?"

    )

    print()

    print(
        load_learning_state(student)
    )