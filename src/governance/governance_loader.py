"""
===========================================================
Batman Student

Module:
governance_loader.py

Purpose:
Load Governance Maps used across Batman Student.

Owner:
Governance Domain

Reads:
- data/governance/subject_map.json
- data/governance/chapter_map.json
- data/governance/topic_map.json

Writes:
- None

Dependencies:
- json
- pathlib

Governed By:
ADR-004 Data Governance

Single Source of Truth:
data/governance/

Last Updated:
2026-06-25

===========================================================
"""

import json

from src.config.paths import (
    DATA_DIR,
)


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

from src.config.paths import DATA_DIR

# ---------------------------------------------------------
# GOVERNANCE ROOT
# ---------------------------------------------------------

BOARD = "ICSE"

GRADE = "class10"

SUBJECT = "physics"

GOVERNANCE = (
    DATA_DIR
    / "governance"
    / BOARD
    / GRADE
)


# ---------------------------------------------------------
# INTERNAL
# ---------------------------------------------------------

def _load(filename):

    if filename == "subject_map.json":

        file = (
            GOVERNANCE
            / filename
        )

    else:

        file = (
            GOVERNANCE
            / SUBJECT
            / filename
        )

    if not file.exists():

        raise FileNotFoundError(
            f"{file} not found."
        )

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

# ---------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------

def get_subjects():

    return _load(
        "subject_map.json"
    )


def get_chapters():

    return _load(
        "chapter_map.json"
    )


def get_topics():

    return _load(
        "topic_map.json"
    )


def get_subject(subject_name):

    data = get_subjects()

    for subject in data["subjects"]:

        if (
            subject["name"].lower()
            ==
            subject_name.lower()
        ):

            return subject

    return None


def get_chapter(chapter_number):

    data = get_chapters()

    for chapter in data["chapters"]:

        if (
            chapter["number"]
            ==
            chapter_number
        ):

            return chapter

    return None


def get_topics_for_chapter(chapter_id):

    data = get_topics()

    for chapter in data["topics"]:

        if (
            chapter["chapter_id"]
            ==
            chapter_id
        ):

            return chapter["topics"]

    return []


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nSubjects")
    print("-" * 40)

    for subject in get_subjects()["subjects"]:

        print(f"- {subject['name']}")

    print("\nChapter 1")
    print("-" * 40)

    chapter = get_chapter(1)

    print(f"Board    : {chapter['board']}")
    print(f"Grade    : {chapter['grade']}")
    print(f"Subject  : {chapter['subject']}")
    print(f"Chapter  : {chapter['number']}")
    print(f"Name     : {chapter['name']}")
    print(f"Document : {chapter['document']}")
    print(f"Source   : {chapter['source']}")

    print("\nTopics")
    print("-" * 40)

    print(
        get_topics_for_chapter(
            "PHY-01"
        )
    )