"""
===========================================================
Batman Student

Module:
adaptive_revision.py

Purpose:
Recommend revision topics based on learning analytics,
weak topics and current learning state.

Owner:
Batman Student Core

Reads:
- learning_state.json
- history.json

Writes:
-

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Student History
===========================================================
"""

from src.governance.learning_state import load_learning_state
from src.governance.weak_topic_detector import detect_weak_topics

from src.governance.topic_normalizer import (
    normalize_topic_name
)

def get_revision_plan(student_id):

    state = load_learning_state(student_id)

    weak_topics = detect_weak_topics(student_id)

    recommendations = []

    if weak_topics:

        recommendations.append(
            {
                "reason": "Weak Quiz Performance",
                "topic": weak_topics[0]["topic"]
            }
        )

    if state.get("topic"):

        recommendations.append(
            {
                "reason": "Continue Current Topic",
                "topic": normalize_topic_name(

                    state["topic"]

                )
            }
        )

    return {
        "student": student_id,
        "recommendations": recommendations
    }


if __name__ == "__main__":

    student_id = input(
        "Enter Student ID: "
    ).strip().upper()

    plan = get_revision_plan(student_id)

    print("\n" + "=" * 60)
    print("ADAPTIVE REVISION")
    print("=" * 60)

    if not plan["recommendations"]:

        print("\nNo revision required.")

    else:

        for item in plan["recommendations"]:

            print(
                f"\nReason : {item['reason']}"
            )

            print(
                f"Topic  : {item['topic']}"
            )

    print("=" * 60)