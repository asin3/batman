"""
===========================================================
Batman Student

Module:
learning_analytics.py

Purpose:
Generate learning analytics from a student's learning
history and quiz history.

Owner:
Batman Student Core

Reads:
- data/students/<student_id>/history.json
- data/students/<student_id>/learning_state.json

Writes:
-

Dependencies:
- json
- collections
- pathlib

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Student History

Last Updated:
2026-06-25
===========================================================
"""

import json

from collections import Counter

from pathlib import Path


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

STUDENTS_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "students"
)


# ---------------------------------------------------------
# LOAD HISTORY
# ---------------------------------------------------------

def load_history(student_id):

    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]

    history_file = (
        ROOT
        / "data"
        / "students"
        / student_id
        / "history.json"
    )

    if not history_file.exists():

        return []

    print(f"Loading: {history_file}")

    with open(
        history_file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ---------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------

def get_learning_analytics(student_id):

    history = load_history(student_id)
    print(f"Records: {len(history)}")
    print(history[-1] if history else "EMPTY")

    quizzes = []

    for item in history:

        if item.get("type") == "QUIZ":
            quizzes.append(item)

    #print(f"Quiz records found: {len(quizzes)}")

    if not quizzes:

        return {

            "total_quizzes": 0,

            "average_score": 0,

            "average_percentage": 0,

            "best_subject": None,

            "weak_subject": None,

            "best_chapter": None,

            "weak_chapter": None,

            "recent_quizzes": []

        }

    total_score = sum(

        q["score"]

        for q in quizzes

    )

    total_questions = sum(

        q["total"]

        for q in quizzes

    )

    average_percentage = round(

        (

            total_score
            /
            total_questions

        ) * 100,

        2

    )

    subject_scores = {}

    chapter_scores = {}

    for quiz in quizzes:

        subject = quiz.get(
            "subject",
            "Unknown"
        )

        chapter = quiz.get(
            "chapter",
            "Unknown"
        )

        percentage = quiz.get(
            "percentage",
            0
        )

        subject_scores.setdefault(
            subject,
            []
        ).append(
            percentage
        )

        chapter_scores.setdefault(
            chapter,
            []
        ).append(
            percentage
        )

    subject_average = {

        k: sum(v) / len(v)

        for k, v

        in subject_scores.items()

    }

    chapter_average = {

        k: sum(v) / len(v)

        for k, v

        in chapter_scores.items()

    }

    recent = sorted(

        quizzes,

        key=lambda x: x.get(
            "timestamp",
            ""
        ),

        reverse=True

    )[:5]

    return {

        "total_quizzes":

            len(quizzes),

        "average_score":

            round(

                total_score
                /
                total_questions,

                2

            ),

        "average_percentage":

            average_percentage,

        "best_subject":

            max(

                subject_average,

                key=subject_average.get

            ),

        "weak_subject":

            min(

                subject_average,

                key=subject_average.get

            ),

        "best_chapter":

            max(

                chapter_average,

                key=chapter_average.get

            ),

        "weak_chapter":

            min(

                chapter_average,

                key=chapter_average.get

            ),

        "recent_quizzes":

            recent

    }

# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    student_id = input("Enter Student ID: ").strip().upper()

    analytics = get_learning_analytics(student_id)

    print("\n" + "=" * 60)
    print("LEARNING ANALYTICS")
    print("=" * 60)

    for key, value in analytics.items():
        print(f"{key:<20}: {value}")

    print("=" * 60)