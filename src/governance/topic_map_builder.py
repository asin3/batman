"""
===========================================================
Batman Student

Module:
topic_map_builder.py

Purpose:
Automatically build topic_map.json from the cleaned
textbook.

Owner:
Batman Student Core

Reads:
data/class10/physics/textbook/physics-textbook.txt

Writes:
data/governance/ICSE/class10/physics/topic_map.json

Governed By:
ADR-004 Data Governance

Single Source of Truth:
topic_map.json
===========================================================
"""

import json
import re

from src.config.paths import (
    STAGING_DIR,
    GOVERNANCE_DIR,
)


TEXTBOOK = (
    STAGING_DIR /
    "physics-textbook.txt"
)

OUTPUT = (
    GOVERNANCE_DIR /
    "topic_map.json"
)


def build_topic_map():

    with open(
        TEXTBOOK,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    chapter_pattern = re.compile(
        r"CHAPTER\s+\d+\s*[:-]?\s*(.+)",
        re.IGNORECASE
    )

    topic_pattern = re.compile(
        r"^\d+\.\d+\s+(.+)$",
        re.MULTILINE
    )

    chapters = chapter_pattern.findall(text)

    topics = topic_pattern.findall(text)

    topic_map = {

        "board": "ICSE",

        "grade": "10",

        "subject": "Physics",

        "version": "2.0",

        "topics": []

    }

    for index, chapter in enumerate(chapters):

        topic_map["topics"].append(

            {

                "chapter_id":
                    f"PHY-{index+1:02}",

                "chapter":
                    chapter.strip(),

                "topics": []

            }

        )

    current = 0

    for topic in topics:

        if current >= len(topic_map["topics"]):

            break

        topic_map["topics"][current]["topics"].append(

            {

                "name": topic.strip()

            }

        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            topic_map,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nTopic Map Created")

    print(
        f"Chapters : {len(chapters)}"
    )

    print(
        f"Topics   : {len(topics)}"
    )

    print(
        f"Saved To : {OUTPUT}"
    )


if __name__ == "__main__":

    build_topic_map()