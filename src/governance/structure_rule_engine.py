"""
===========================================================
Batman Student

Module:
structure_rule_engine.py

Purpose:
Automatically discover the textbook structure rules.

This module analyzes the NORMALIZED textbook and
produces parser rules that later modules use.

No parser should hardcode assumptions.

Owner:
Knowledge Engine

Reads:
normalized_textbook.txt

Writes:
structure_rules.json

Governed By:
ADR-004 Data Governance

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
    "structure_rules.json"
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
# EXTRACT CONTENTS BLOCK
# ---------------------------------------------------------

def extract_contents(text):

    start = re.search(
        r"\bContents\b",
        text,
        re.IGNORECASE
    )

    if not start:

        raise RuntimeError(
            "Contents section not found."
        )

    end = re.search(
        r"\bCHAPTER\b",
        text[start.end():],
        re.IGNORECASE
    )

    if end:

        return text[
            start.start():
            start.end() + end.start()
        ]

    return text[start.start():]


# ---------------------------------------------------------
# CLEAN
# ---------------------------------------------------------

def clean_lines(contents):

    cleaned = []

    for line in contents.splitlines():

        line = line.strip()

        if not line:
            continue

        line = re.sub(
            r"\s+",
            " ",
            line
        )

        cleaned.append(line)

    return cleaned

# ---------------------------------------------------------
# DETECT UNIT RULE
# ---------------------------------------------------------

def detect_unit_rule(lines):

    pattern = re.compile(
        r"^\([A-Z]\)\s+"
    )

    matches = []

    for line in lines:

        if pattern.match(line):

            matches.append(line)

    return {

        "enabled": len(matches) > 0,

        "regex": pattern.pattern,

        "matches": len(matches),

        "confidence":
            round(
                len(matches) /
                max(len(lines), 1),
                3
            )

    }


# ---------------------------------------------------------
# DETECT CHAPTER RULE
# ---------------------------------------------------------

def detect_chapter_rule(lines):

    candidates = [

        r"^\d+\s+[A-Za-z].+",

        r"^\d+[.:]\s+.+",

        r"^Chapter\s+\d+",

        r"^CHAPTER\s+\d+"

    ]

    best = None

    best_score = -1

    for regex in candidates:

        pattern = re.compile(
            regex,
            re.IGNORECASE
        )

        score = sum(

            1

            for line in lines

            if pattern.match(line)

        )

        if score > best_score:

            best_score = score

            best = regex

    return {

        "regex": best,

        "matches": best_score

    }


# ---------------------------------------------------------
# DETECT TOPIC RULE
# ---------------------------------------------------------

def detect_topic_rule(lines):

    candidates = [

        r"^\d+\.\d+\s+.+",

        r"^\d+\.\d+\.\d+\s+.+",

        r"^[A-Z]\.\s+.+"

    ]

    best = None

    best_score = -1

    for regex in candidates:

        pattern = re.compile(regex)

        score = sum(

            1

            for line in lines

            if pattern.match(line)

        )

        if score > best_score:

            best = regex

            best_score = score

    return {

        "regex": best,

        "matches": best_score

    }


# ---------------------------------------------------------
# DETECT PAGE RANGE RULE
# ---------------------------------------------------------

def detect_page_rule(lines):

    pattern = re.compile(

        r"\d+\s*[-–]\s*\d+$"

    )

    matches = sum(

        1

        for line in lines

        if pattern.search(line)

    )

    return {

        "regex": pattern.pattern,

        "matches": matches

    }


# ---------------------------------------------------------
# BUILD RULES
# ---------------------------------------------------------

def build_rules(lines):

    return {

        "unit_rule":
            detect_unit_rule(lines),

        "chapter_rule":
            detect_chapter_rule(lines),

        "topic_rule":
            detect_topic_rule(lines),

        "page_rule":
            detect_page_rule(lines)

    }

# ---------------------------------------------------------
# SAVE RULES
# ---------------------------------------------------------

def save_rules(rules):

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            rules,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nRules saved.")

    print(OUTPUT_FILE)


# ---------------------------------------------------------
# PRINT SUMMARY
# ---------------------------------------------------------

def print_summary(rules):

    print("\nRule Detection Summary")

    print("-" * 50)

    for name, rule in rules.items():

        print(f"\n{name}")

        print(f"Regex      : {rule['regex']}")

        print(f"Matches    : {rule['matches']}")

        if "confidence" in rule:

            print(
                f"Confidence : {rule['confidence']}"
            )


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

def analyze_textbook():

    print("\nLoading normalized textbook...")

    text = load_text()

    print("Extracting Contents section...")

    contents = extract_contents(text)

    print("Cleaning lines...")

    lines = clean_lines(contents)

    print(
        f"Lines analyzed : {len(lines)}"
    )

    print("Detecting structure rules...")

    rules = build_rules(lines)

    save_rules(rules)

    print_summary(rules)

    return rules

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN STRUCTURE RULE ENGINE")
    print("=" * 60)

    analyze_textbook()

    print()

    print("=" * 60)
    print("STRUCTURE RULE DISCOVERY COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")
        print("-" * 40)
        print(e)
        print("-" * 40)