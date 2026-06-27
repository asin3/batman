"""
===========================================================
Batman Student

Module:
student_dashboard.py

Purpose:
Unified Student Dashboard API.

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
Student Memory Layer
===========================================================
"""

from src.governance.learning_state import (
    load_learning_state,
)

from src.governance.learning_analytics import (
    get_learning_analytics,
)

from src.governance.weak_topic_detector import (
    detect_weak_topics,
)

from src.governance.adaptive_revision import (
    get_revision_plan,
)


def get_student_dashboard(student_id):

    dashboard = {

        "student_id":
            student_id,

        "learning_state":
            load_learning_state(
                student_id
            ),

        "analytics":
            get_learning_analytics(
                student_id
            ),

        "weak_topics":
            detect_weak_topics(
                student_id
            ),

        "revision_plan":
            get_revision_plan(
                student_id
            )

    }

    return dashboard


if __name__ == "__main__":

    student_id = input(
        "Enter Student ID: "
    ).strip().upper()

    dashboard = get_student_dashboard(
        student_id
    )

    print("\n" + "=" * 60)
    print("BATMAN STUDENT DASHBOARD")
    print("=" * 60)

    print()

    print("Learning State")
    print("-" * 60)
    print(
        dashboard["learning_state"]
    )

    print()

    print("Analytics")
    print("-" * 60)
    print(
        dashboard["analytics"]
    )

    print()

    print("Weak Topics")
    print("-" * 60)
    print(
        dashboard["weak_topics"]
    )

    print()

    print("Revision Plan")
    print("-" * 60)
    print(
        dashboard["revision_plan"]
    )

    print()

    print("=" * 60)