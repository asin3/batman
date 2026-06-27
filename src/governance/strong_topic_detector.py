"""
===========================================================
Batman Student

Module:
strong_topic_detector.py

Purpose:
Identify topics where the student consistently performs
well.

A topic is considered STRONG when:

• Multiple quiz attempts
• Average score above threshold
• Consistent performance

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
from collections import defaultdict

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
# BUILD TOPIC STATISTICS
# ---------------------------------------------------------

def build_topic_statistics(quizzes):

    topics = defaultdict(list)

    for quiz in quizzes:

        topic = normalize_topic_name(

            quiz.get("chapter", "")

        )

        if not topic:

            continue

        topics[topic].append(

            quiz.get("percentage", 0)

        )

    return topics


# ---------------------------------------------------------
# DETECT STRONG TOPICS
# ---------------------------------------------------------

def detect_strong_topics(topic_stats):

    strong_topics = []

    for topic, scores in topic_stats.items():

        attempts = len(scores)

        average = round(

            sum(scores) / attempts,

            2

        )

        if (

            attempts >= 2

            and

            average >= 80

        ):

            strong_topics.append({

                "topic": topic,

                "attempts": attempts,

                "average_percentage": average

            })

    strong_topics.sort(

        key=lambda x: (

            -x["average_percentage"],

            -x["attempts"]

        )

    )

    return strong_topics

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

def display_results(strong_topics):

    print("\n" + "=" * 60)
    print("STRONG TOPIC DETECTOR")
    print("=" * 60)

    if not strong_topics:

        print("\nNo strong topics detected.")

        print("=" * 60)

        return

    for topic in strong_topics:

        print()

        print(f"Topic      : {topic['topic']}")

        print(f"Attempts   : {topic['attempts']}")

        print(
            f"Average %  : {topic['average_percentage']}"
        )

        print("-" * 40)

    print("=" * 60)


# ---------------------------------------------------------
# RUN DETECTOR
# ---------------------------------------------------------

def run_detector():

    history = load_history()

    quizzes = get_quizzes(history)

    topic_stats = build_topic_statistics(quizzes)

    strong_topics = detect_strong_topics(topic_stats)

    display_results(strong_topics)

    return strong_topics

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    run_detector()


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")

        print("-" * 40)

        print(e)

        print("-" * 40)