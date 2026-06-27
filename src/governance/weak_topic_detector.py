"""
===========================================================
Batman Student

Module:
weak_topic_detector.py

Purpose:
Detect weak topics based on quiz history.

Owner:
Batman Student Core

Reads:
- data/students/<student_id>/history.json

Writes:
-

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Student History

Last Updated:
2026-06-26
===========================================================
"""

from collections import defaultdict

from src.governance.learning_analytics import load_history

from src.governance.topic_normalizer import (
    normalize_topic_name
)

def detect_weak_topics(student_id):

    history = load_history(student_id)

    topic_stats = defaultdict(
        lambda: {
            "attempts": 0,
            "total_percentage": 0
        }
    )

    for item in history:

        if item.get("type") != "QUIZ":
            continue

        topic = normalize_topic_name(

            item.get(
                "chapter",
                "Unknown"
            )

        )

        topic_stats[topic]["attempts"] += 1

        topic_stats[topic]["total_percentage"] += item.get(
            "percentage",
            0
        )

    weak_topics = []

    for topic, stats in topic_stats.items():

        average = round(
            stats["total_percentage"]
            / stats["attempts"],
            2
        )

        if average < 70:

            weak_topics.append(

                {
                    "topic": topic,
                    "attempts": stats["attempts"],
                    "average_percentage": average
                }

            )

    weak_topics.sort(
        key=lambda x: x["average_percentage"]
    )

    return weak_topics


if __name__ == "__main__":

    student_id = input(
        "Enter Student ID: "
    ).strip().upper()

    weak_topics = detect_weak_topics(
        student_id
    )

    print("\n" + "=" * 60)
    print("WEAK TOPIC DETECTOR")
    print("=" * 60)

    if not weak_topics:

        print("\nNo weak topics detected.")

    else:

        print()

        for topic in weak_topics:

            print(
                f"Topic      : {topic['topic']}"
            )

            print(
                f"Attempts   : {topic['attempts']}"
            )

            print(
                f"Average %  : {topic['average_percentage']}"
            )

            print("-" * 40)

    print("=" * 60)