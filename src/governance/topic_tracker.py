"""
===========================================================
Batman Student

Module:
topic_tracker.py

Purpose:
Resolve and track the student's current chapter/topic
using Governance Maps.

Owner:
Batman Student Core

Reads:
- topic_map.json

Writes:
-

Governed By:
ADR-004 Data Governance

Single Source of Truth:
topic_map.json
===========================================================
"""

from src.governance.governance_loader import (
    get_topics,
)


# ---------------------------------------------------------
# FIND TOPIC
# ---------------------------------------------------------

def find_topic(query):

    query = query.lower()

    data = get_topics()

    for chapter in data["topics"]:

        for topic in chapter["topics"]:

            if topic["name"].lower() in query:

                return {

                    "chapter": chapter["name"],

                    "topic": topic["name"]

                }

    return {

        "chapter": None,

        "topic": None

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk: "
        )

        if query.lower() == "exit":

            break

        result = find_topic(query)

        print("\nResult")

        print("-" * 40)

        print(
            f"Chapter : {result['chapter']}"
        )

        print(
            f"Topic   : {result['topic']}"
        )