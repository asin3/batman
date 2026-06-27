"""
===========================================================
Batman Student

Module:
progress_tracker.py

Purpose:
Measure a student's overall learning progress.

Calculates:

• Total quizzes attempted
• Total questions answered
• Correct answers
• Overall percentage
• Chapters covered
• Last activity

Owner:
Student Intelligence

Reads:
history.json

Writes:
None

===========================================================
"""

from pathlib import Path
import json

from src.governance.topic_normalizer import (
    normalize_topic_name
)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STUDENT_ID = input("Enter Student ID: ").strip()

HISTORY_FILE = (
    PROJECT_ROOT
    / "data"
    / "students"
    / STUDENT_ID
    / "history.json"
)


# ---------------------------------------------------------
# LOAD HISTORY
# ---------------------------------------------------------

def load_history():

    if not HISTORY_FILE.exists():

        raise FileNotFoundError(HISTORY_FILE)

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ---------------------------------------------------------
# FILTER QUIZZES
# ---------------------------------------------------------

def get_quizzes(history):

    return [

        item

        for item in history

        if item.get("type") == "QUIZ"

    ]
# ---------------------------------------------------------
# CALCULATE PROGRESS
# ---------------------------------------------------------

def calculate_progress(quizzes):

    total_quizzes = len(quizzes)

    total_questions = 0

    total_correct = 0

    chapters = set()

    last_activity = None

    for quiz in quizzes:

        total_questions += quiz.get(

            "total",

            0

        )

        total_correct += quiz.get(

            "score",

            0

        )

        chapter = normalize_topic_name(

            quiz.get(

                "chapter",

                ""

            )

        )

        if chapter:

            chapters.add(chapter)

        timestamp = quiz.get(

            "timestamp"

        )

        if timestamp:

            if (

                last_activity is None

                or

                timestamp > last_activity

            ):

                last_activity = timestamp

    overall_percentage = 0

    if total_questions > 0:

        overall_percentage = round(

            (

                total_correct

                / total_questions

            ) * 100,

            2

        )

    return {

        "total_quizzes": total_quizzes,

        "total_questions": total_questions,

        "correct_answers": total_correct,

        "overall_percentage": overall_percentage,

        "chapters_covered": sorted(

            list(chapters)

        ),

        "last_activity": last_activity

    }

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

def display_progress(progress):

    print("\n" + "=" * 60)
    print("STUDENT PROGRESS TRACKER")
    print("=" * 60)

    print()

    print(f"Quiz Sessions      : {progress['total_quizzes']}")

    print(f"Questions Attempted: {progress['total_questions']}")

    print(f"Correct Answers    : {progress['correct_answers']}")

    print(f"Overall Percentage : {progress['overall_percentage']}%")

    print(f"Chapters Covered   : {len(progress['chapters_covered'])}")

    print(f"Last Activity      : {progress['last_activity']}")

    print()

    if progress["chapters_covered"]:

        print("Covered Chapters")

        print("-" * 40)

        for chapter in progress["chapters_covered"]:

            print(f"- {chapter}")

    print()

    print("=" * 60)


# ---------------------------------------------------------
# RUN TRACKER
# ---------------------------------------------------------

def run_tracker():

    history = load_history()

    quizzes = get_quizzes(history)

    progress = calculate_progress(

        quizzes

    )

    display_progress(

        progress

    )

    return progress

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    run_tracker()


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")
        print("-" * 40)
        print(e)
        print("-" * 40)