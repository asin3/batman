"""
===========================================================
Batman Student
Module: knowledge_validation.py

Purpose:
Validate the master textbook before indexing.

Owner:
Content Domain

Reads:
data/class10/physics/textbook/physics-textbook.txt
vector_db/

Writes:
data/class10/physics/reports/

Governed By:
ADR-004 Data Governance

Single Source of Truth:
physics-textbook.txt
===========================================================
"""

from src.config.paths import (
    STAGING_DIR,
    REPORTS_DIR,
    VECTOR_DB_DIR,
)

import json
from datetime import datetime


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

TEXTBOOK = (
    STAGING_DIR /
    "physics-textbook.txt"
)

REPORTS = REPORTS_DIR

VECTOR_DB = VECTOR_DB_DIR

REPORTS.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# LOAD TEXTBOOK
# ---------------------------------------------------------

if not TEXTBOOK.exists():

    print("\nERROR")
    print(f"Missing:\n{TEXTBOOK}")
    exit()


text = TEXTBOOK.read_text(
    encoding="utf-8",
    errors="ignore"
)


# ---------------------------------------------------------
# BASIC STATS
# ---------------------------------------------------------

characters = len(text)

words = len(text.split())

lines = len(text.splitlines())


# ---------------------------------------------------------
# STRUCTURE
# ---------------------------------------------------------

import re

# ---------------------------------------------------------
# CHAPTER DETECTION (FROM CONTENTS PAGE)
# ---------------------------------------------------------

chapter_count = 0

contents_match = re.search(
    r"Contents(.*?)===== PAGE 2 =====",
    text,
    re.DOTALL | re.IGNORECASE
)

if contents_match:

    contents = contents_match.group(1)

    chapter_matches = re.findall(
        r'^\s*(1[0-2])[,.;:]?\s+[A-Za-z]',
        contents,
        re.MULTILINE
    )

    chapter_count = len(chapter_matches)

page_count = text.count("===== PAGE")

mcq_count = text.upper().count(
    "MULTIPLE CHOICE"
)

exercise_count = text.upper().count(
    "EXERCISE"
)

numerical_count = text.upper().count(
    "NUMERICAL"
)

example_count = (
    text.upper().count("EXAMPLE")
    + text.upper().count("SOLVED EXAMPLE")
)

figure_count = (
    text.upper().count("FIG.")
    + text.upper().count("FIGURE")
)


# ---------------------------------------------------------
# VECTOR DB
# ---------------------------------------------------------

vector_exists = VECTOR_DB.exists()


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

warnings = []

if words < 1000:
    warnings.append(
        "Very low word count."
    )

if chapter_count == 0:

    warnings.append(
        "Unable to identify chapter headings. OCR format may require a custom parser."
    )

if page_count == 0:
    warnings.append(
        "No page markers detected."
    )

if not vector_exists:
    warnings.append(
        "Vector DB folder missing."
    )

status = "PASS"

if warnings:
    status = "WARNING"


# ---------------------------------------------------------
# JSON REPORT
# ---------------------------------------------------------

report = {

    "generated_at":
        datetime.now().isoformat(),

    "board":
        "ICSE",

    "grade":
        "10",

    "subject":
        "Physics",

    "master_source":
        str(TEXTBOOK),

    "statistics": {

        "characters":
            characters,

        "words":
            words,

        "lines":
            lines,

        "estimated_chapters":
            chapter_count,

        "estimated_pages":
            page_count,

        "mcq_sections":
            mcq_count,

        "exercise_sections":
            exercise_count,

        "numerical_sections":
            numerical_count,

        "worked_examples":
            example_count,

        "figure_mentions":
            figure_count,

        "vector_db_exists":
            vector_exists

    },

    "warnings":
        warnings,

    "status":
        status
}


json_file = (
    REPORTS
    / "knowledge_validation.json"
)

with open(
    json_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )


# ---------------------------------------------------------
# TEXT REPORT
# ---------------------------------------------------------

txt_file = (
    REPORTS
    / "knowledge_validation.txt"
)

with open(
    txt_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 60 + "\n")
    f.write("BATMAN KNOWLEDGE VALIDATION REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write("Board          : ICSE\n")
    f.write("Grade          : 10\n")
    f.write("Subject        : Physics\n\n")

    f.write(
        f"Master Source  : {TEXTBOOK.name}\n\n"
    )

    f.write("TEXTBOOK\n")
    f.write("-" * 60 + "\n")

    f.write(
        f"Characters      : {characters}\n"
    )

    f.write(
        f"Words           : {words}\n"
    )

    f.write(
        f"Lines           : {lines}\n"
    )

    f.write(
        f"Chapters        : {chapter_count}\n"
    )

    f.write(
        f"Pages           : {page_count}\n"
    )

    f.write(
        f"MCQ Sections    : {mcq_count}\n"
    )

    f.write(
        f"Exercise        : {exercise_count}\n"
    )

    f.write(
        f"Numericals      : {numerical_count}\n"
    )

    f.write(
        f"Examples        : {example_count}\n"
    )

    f.write(
        f"Figure Mentions : {figure_count}\n\n"
    )

    f.write("VECTOR DATABASE\n")
    f.write("-" * 60 + "\n")

    f.write(
        f"Exists : {vector_exists}\n\n"
    )

    if warnings:

        f.write("WARNINGS\n")
        f.write("-" * 60 + "\n")

        for warning in warnings:

            f.write(
                f"- {warning}\n"
            )

        f.write("\n")

    f.write(
        f"STATUS : {status}\n"
    )


# ---------------------------------------------------------
# CONSOLE
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("BATMAN KNOWLEDGE VALIDATION")
print("=" * 60)

print(f"Master Source : {TEXTBOOK.name}")
print(f"Words         : {words}")
print(f"Lines         : {lines}")
print(f"Pages         : {page_count}")
print(f"Chapters      : {chapter_count}")
print(f"MCQ Sections  : {mcq_count}")
print(f"Exercises     : {exercise_count}")
print(f"Numericals    : {numerical_count}")
print(f"Examples      : {example_count}")
print(f"Figures       : {figure_count}")
print(f"Vector DB     : {vector_exists}")

print("\nStatus :", status)

if warnings:

    print("\nWarnings:")

    for warning in warnings:

        print("-", warning)

print("\nReports Generated:")
print(json_file)
print(txt_file)
print("=" * 60)