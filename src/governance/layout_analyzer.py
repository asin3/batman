"""
===========================================================
Batman Student

Module:
layout_analyzer.py

Purpose:
Analyze the normalized textbook and describe its
actual layout.

This module DOES NOT parse the textbook.

It only discovers:

• Contents boundaries
• Unit format
• Chapter format
• Topic format
• Page numbering
• OCR quality

Owner:
Knowledge Engine

Reads:
normalized_textbook.txt

Writes:
layout_analysis.json

===========================================================
"""

import json
import re

from src.config.paths import (
    GENERATED_DIR,
    GOVERNANCE_DIR,
)


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

INPUT_FILE = (
    GENERATED_DIR /
    "normalized_textbook.txt"
)

OUTPUT_FILE = (
    GOVERNANCE_DIR /
    "layout_analysis.json"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

def load_text():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(INPUT_FILE)

    return INPUT_FILE.read_text(

        encoding="utf-8",

        errors="ignore"

    )


# ---------------------------------------------------------
# SPLIT INTO LINES
# ---------------------------------------------------------

def get_lines():

    text = load_text()

    return [

        line.rstrip()

        for line in text.splitlines()

    ]


# ---------------------------------------------------------
# FIND CONTENTS
# ---------------------------------------------------------

def locate_contents(lines):

    start = None
    end = None

    for i, line in enumerate(lines):

        if re.search(

            r"\bContents\b",

            line,

            re.IGNORECASE

        ):

            start = i
            break

    if start is None:

        raise RuntimeError(

            "Contents section not found."

        )

    for i in range(

        start + 1,

        len(lines)

    ):

        if re.search(

            r"\bCHAPTER\b",

            lines[i],

            re.IGNORECASE

        ):

            end = i

            break

    if end is None:

        end = min(

            start + 250,

            len(lines)

        )

    return start, end

# ---------------------------------------------------------
# ANALYZE LAYOUT
# ---------------------------------------------------------

def analyze_layout(lines, start, end):

    contents = lines[start:end]

    analysis = {

        "contents_start_line": start,

        "contents_end_line": end,

        "unit_candidates": [],

        "chapter_candidates": [],

        "topic_candidates": [],

        "page_candidates": []

    }

    unit_pattern = re.compile(

        r"^\([A-Z]\)\s+"

    )

    chapter_pattern = re.compile(

        r"^\d+\s+[A-Za-z]"

    )

    topic_pattern = re.compile(

        r"^\d+\.\d+\s+"

    )

    page_pattern = re.compile(

        r"\d+\s*[-–]\s*\d+$"

    )

    for line in contents:

        line = line.strip()

        if not line:

            continue

        if unit_pattern.match(line):

            analysis["unit_candidates"].append(line)

            continue

        if chapter_pattern.match(line):

            analysis["chapter_candidates"].append(line)

            continue

        if topic_pattern.match(line):

            analysis["topic_candidates"].append(line)

            continue

        if page_pattern.search(line):

            analysis["page_candidates"].append(line)

    return analysis


# ---------------------------------------------------------
# BUILD REPORT
# ---------------------------------------------------------

def build_report():

    print("\nLoading normalized textbook...")

    lines = get_lines()

    print("Locating Contents...")

    start, end = locate_contents(lines)

    print(

        f"Contents : {start} → {end}"

    )

    report = analyze_layout(

        lines,

        start,

        end

    )

    return report

# ---------------------------------------------------------
# BUILD SUMMARY
# ---------------------------------------------------------

def summarize(report):

    summary = {

        "contents_start_line":
            report["contents_start_line"],

        "contents_end_line":
            report["contents_end_line"],

        "unit_count":
            len(report["unit_candidates"]),

        "chapter_count":
            len(report["chapter_candidates"]),

        "topic_count":
            len(report["topic_candidates"]),

        "page_count":
            len(report["page_candidates"]),

        "unit_examples":
            report["unit_candidates"][:5],

        "chapter_examples":
            report["chapter_candidates"][:10],

        "topic_examples":
            report["topic_candidates"][:10],

        "page_examples":
            report["page_candidates"][:10]

    }

    return summary


# ---------------------------------------------------------
# SAVE REPORT
# ---------------------------------------------------------

def save_report(summary):

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            summary,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nLayout analysis saved.")

    print(OUTPUT_FILE)


# ---------------------------------------------------------
# PRINT SUMMARY
# ---------------------------------------------------------

def print_summary(summary):

    print("\nLayout Summary")

    print("-" * 50)

    print(

        f"Contents Lines : {summary['contents_start_line']} → {summary['contents_end_line']}"

    )

    print(

        f"Units          : {summary['unit_count']}"

    )

    print(

        f"Chapters       : {summary['chapter_count']}"

    )

    print(

        f"Topics         : {summary['topic_count']}"

    )

    print(

        f"Page Patterns  : {summary['page_count']}"

    )

    print("\nSample Chapters")

    print("-" * 50)

    for item in summary["chapter_examples"]:

        print(item)

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN LAYOUT ANALYZER")
    print("=" * 60)

    report = build_report()

    summary = summarize(report)

    save_report(summary)

    print_summary(summary)

    print()

    print("=" * 60)
    print("LAYOUT ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")

        print("-" * 40)

        print(e)

        print("-" * 40)