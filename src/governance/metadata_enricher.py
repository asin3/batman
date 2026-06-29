"""
===========================================================
Batman Student

Module:
metadata_enricher.py

Purpose:
Enrich chunk metadata using Governance Maps.

Owner:
Governance Domain

Reads:
- data/governance/ICSE/class10/physics/chapter_map.json
- data/governance/ICSE/class10/physics/topic_map.json

Writes:
- None

Dependencies:
- governance_loader.py

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Governance Maps

Last Updated:
2026-06-25

===========================================================
"""

from src.governance.governance_loader import (
    get_chapters,
    get_topics
)


# ---------------------------------------------------------
# ENRICH
# ---------------------------------------------------------

def enrich_metadata(
    metadata,
    text
):

    metadata = metadata.copy()

    chapters = get_chapters()["chapters"]

    topics = get_topics()["topics"]

    metadata["chapter"] = "TBD"

    metadata["topic"] = "TBD"

    text_lower = text.lower()

    # -----------------------------------------------------
    # Chapter Detection
    # -----------------------------------------------------

    for chapter in chapters:

        chapter_name = chapter["name"].lower()

        if chapter_name in text_lower:

            metadata["chapter"] = chapter["name"]

            break

    # -----------------------------------------------------
    # Topic Detection
    # -----------------------------------------------------

    for chapter in topics:

        for topic in chapter["topics"]:

            topic_name = topic["name"]

            if topic_name.lower() in text_lower:

                metadata["topic"] = topic_name

                return metadata

    return metadata


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    sample = {

        "board": "ICSE",

        "grade": "10",

        "subject": "Physics",

        "chapter": "TBD",

        "topic": "TBD"

    }

    text = """

    Force is a push or pull.

    """

    print(

        enrich_metadata(

            sample,

            text

        )

    )