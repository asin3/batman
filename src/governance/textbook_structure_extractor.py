"""
===========================================================
Batman Student

Module:
textbook_structure_extractor.py

Purpose:
Build textbook_structure.json using the selected
Knowledge Parsing Strategy.

This module DOES NOT decide how to parse.

It simply executes the strategy chosen by:

1. OCR Normalizer
2. Structure Rule Engine
3. Knowledge Parsing Strategy

Owner:
Knowledge Engine

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

NORMALIZED_TEXT = (
    GENERATED_DIR /
    "normalized_textbook.txt"
)

RULE_FILE = (
    GOVERNANCE_DIR /
    "structure_rules.json"
)

STRATEGY_FILE = (
    GOVERNANCE_DIR /
    "parsing_strategy.json"
)

OUTPUT_FILE = (
    GOVERNANCE_DIR /
    "textbook_structure.json"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# LOADERS
# ---------------------------------------------------------

def load_text():

    return NORMALIZED_TEXT.read_text(

        encoding="utf-8",

        errors="ignore"

    )


def load_rules():

    with open(

        RULE_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


def load_strategy():

    with open(

        STRATEGY_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


# ---------------------------------------------------------
# CONTENTS
# ---------------------------------------------------------

def extract_contents(text):

    start = re.search(

        r"\bContents\b",

        text,

        re.IGNORECASE

    )

    if not start:

        raise RuntimeError(

            "Contents not found."

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
# PARSER
# ---------------------------------------------------------

class ContentsBasedParser:

    def __init__(

        self,

        text,

        rules,

        strategy

    ):

        self.text = text

        self.rules = rules

        self.strategy = strategy

        self.contents = extract_contents(text)

        self.lines = [

            line.strip()

            for line in self.contents.splitlines()

            if line.strip()

        ]

    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    def build(self):

        structure = {

            "board": "ICSE",

            "grade": "10",

            "subject": "Physics",

            "source":
                "normalized_textbook.txt",

            "strategy":
                self.strategy["layout"],

            "units": [],

            "chapters": []

        }

        self.extract_units(structure)

        self.extract_chapters(structure)

        return structure

    # -----------------------------------------------------
    # PLACEHOLDERS
    # (Implemented in Part 3)
    # -----------------------------------------------------

    def extract_units(

        self,

        structure

    ):

        pass


    def extract_chapters(

        self,

        structure

    ):

        pass


# ---------------------------------------------------------
# STRATEGY EXECUTOR
# ---------------------------------------------------------

def execute_strategy(

    text,

    rules,

    strategy

):

    parser = strategy["parser"]

    if parser == "CONTENTS_BASED":

        engine = ContentsBasedParser(

            text,

            rules,

            strategy

        )

        return engine.build()

    raise RuntimeError(

        f"Unsupported parser: {parser}"

    )

# ---------------------------------------------------------
# CONTENTS BASED PARSER
# ---------------------------------------------------------

    def extract_units(
        self,
        structure
    ):

        unit_regex = re.compile(
            self.rules["unit_rule"]["regex"],
            re.IGNORECASE
        )

        current_unit = None

        for line in self.lines:

            if unit_regex.match(line):

                match = re.match(

                    r"\(([A-Z])\)\s+(.+)",

                    line,

                    re.IGNORECASE

                )

                if not match:
                    continue

                current_unit = {

                    "unit_id": match.group(1),

                    "unit_name": match.group(2).strip(),

                    "chapters": []

                }

                structure["units"].append(
                    current_unit
                )


# ---------------------------------------------------------

    def extract_chapters(
        self,
        structure
    ):

        chapter_regex = re.compile(

            self.rules["chapter_rule"]["regex"],

            re.IGNORECASE

        )

        current_unit = None

        unit_index = 0

        for line in self.lines:

            if re.match(

                self.rules["unit_rule"]["regex"],

                line,

                re.IGNORECASE

            ):

                if unit_index < len(structure["units"]):

                    current_unit = structure["units"][unit_index]

                    unit_index += 1

                continue

            if not chapter_regex.match(line):

                continue

            page_match = re.search(

                r"(\d+)\s*[-–]\s*(\d+)$",

                line

            )

            start_page = None
            end_page = None

            if page_match:

                start_page = int(page_match.group(1))
                end_page = int(page_match.group(2))

            chapter_line = re.sub(

                r"\d+\s*[-–]\s*\d+$",

                "",

                line

            ).strip()

            chapter_match = re.match(

                r"(\d+)[.:]?\s+(.+)",

                chapter_line

            )

            if not chapter_match:

                continue

            chapter_number = int(

                chapter_match.group(1)

            )

            chapter_name = (

                chapter_match.group(2)

                .strip()

            )

            chapter = {

                "chapter_id":
                    f"PHY-{chapter_number:02}",

                "chapter_number":
                    chapter_number,

                "chapter_name":
                    chapter_name,

                "unit":
                    current_unit["unit_name"]
                    if current_unit else None,

                "start_page":
                    start_page,

                "end_page":
                    end_page,

                "topics": []

            }

            structure["chapters"].append(
                chapter
            )

            if current_unit:

                current_unit["chapters"].append(

                    chapter["chapter_id"]

                )

# ---------------------------------------------------------
# BUILD STRUCTURE
# ---------------------------------------------------------

def build_structure():

    print("\nLoading normalized textbook...")

    text = load_text()

    print("Loading structure rules...")

    rules = load_rules()

    print("Loading parsing strategy...")

    strategy = load_strategy()

    print(
        f"Selected Parser : {strategy['parser']}"
    )

    structure = execute_strategy(

        text,

        rules,

        strategy

    )

    return structure


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

def save_structure(structure):

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            structure,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nSaved")

    print(OUTPUT_FILE)

    print()

    print("Summary")

    print("-" * 40)

    print(

        f"Units     : {len(structure['units'])}"

    )

    print(

        f"Chapters  : {len(structure['chapters'])}"

    )

    print(

        f"Strategy  : {structure['strategy']}"

    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN STRUCTURE EXTRACTOR")
    print("=" * 60)

    structure = build_structure()

    save_structure(structure)

    print("\nExtraction Complete.")

    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")

        print("-" * 40)

        print(e)

        print("-" * 40)