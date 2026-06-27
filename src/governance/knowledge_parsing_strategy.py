"""
===========================================================
Batman Student

Module:
knowledge_parsing_strategy.py

Purpose:
Determine HOW a textbook should be parsed.

This module does NOT parse the textbook.

It analyzes textbook characteristics and selects
the most appropriate parsing strategy.

Owner:
Knowledge Engine

Reads:
normalized_textbook.txt
structure_rules.json

Writes:
parsing_strategy.json

===========================================================
"""

from pathlib import Path
import json


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RULE_FILE = (
    PROJECT_ROOT
    / "data"
    / "governance"
    / "ICSE"
    / "class10"
    / "physics"
    / "structure_rules.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "governance"
    / "ICSE"
    / "class10"
    / "physics"
    / "parsing_strategy.json"
)


# ---------------------------------------------------------
# LOAD RULES
# ---------------------------------------------------------

def load_rules():

    with open(

        RULE_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)
    
# ---------------------------------------------------------
# DETECT PARSING STRATEGY
# ---------------------------------------------------------

def determine_strategy(rules):

    strategy = {

        "layout": "UNKNOWN",

        "parser": "GENERIC",

        "chapter_style": "UNKNOWN",

        "topic_style": "UNKNOWN",

        "unit_style": "UNKNOWN",

        "page_style": "UNKNOWN"

    }

    # -------------------------------------
    # UNIT STYLE
    # -------------------------------------

    if rules["unit_rule"]["enabled"]:

        strategy["unit_style"] = "LETTER_SECTION"

    # -------------------------------------
    # CHAPTER STYLE
    # -------------------------------------

    chapter_regex = rules["chapter_rule"]["regex"]

    if chapter_regex == r"^\d+[.:]\s+.+":

        strategy["chapter_style"] = "NUMBER_TITLE"

    elif chapter_regex == r"^CHAPTER\s+\d+":

        strategy["chapter_style"] = "CHAPTER_HEADING"

    else:

        strategy["chapter_style"] = "CUSTOM"

    # -------------------------------------
    # TOPIC STYLE
    # -------------------------------------

    topic_regex = rules["topic_rule"]["regex"]

    if topic_regex == r"^\d+\.\d+\s+.+":

        strategy["topic_style"] = "DECIMAL"

    elif topic_regex == r"^\d+\.\d+\.\d+\s+.+":

        strategy["topic_style"] = "MULTI_DECIMAL"

    else:

        strategy["topic_style"] = "CUSTOM"

    # -------------------------------------
    # PAGE STYLE
    # -------------------------------------

    if rules["page_rule"]["matches"] > 0:

        strategy["page_style"] = "PAGE_RANGE"

    else:

        strategy["page_style"] = "UNKNOWN"

    # -------------------------------------
    # PARSER SELECTION
    # -------------------------------------

    if (

        strategy["unit_style"] == "LETTER_SECTION"

        and

        strategy["chapter_style"] == "NUMBER_TITLE"

        and

        strategy["page_style"] == "PAGE_RANGE"

    ):

        strategy["layout"] = "ICSE_SELINA"

        strategy["parser"] = "CONTENTS_BASED"

    else:

        strategy["layout"] = "GENERIC"

        strategy["parser"] = "HEURISTIC"

    return strategy

# ---------------------------------------------------------
# SAVE STRATEGY
# ---------------------------------------------------------

def save_strategy(strategy):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            strategy,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nStrategy saved.")

    print(OUTPUT_FILE)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def print_summary(strategy):

    print("\nSelected Parsing Strategy")

    print("-" * 50)

    print(
        f"Layout          : {strategy['layout']}"
    )

    print(
        f"Parser          : {strategy['parser']}"
    )

    print(
        f"Unit Style      : {strategy['unit_style']}"
    )

    print(
        f"Chapter Style   : {strategy['chapter_style']}"
    )

    print(
        f"Topic Style     : {strategy['topic_style']}"
    )

    print(
        f"Page Style      : {strategy['page_style']}"
    )


# ---------------------------------------------------------
# BUILD STRATEGY
# ---------------------------------------------------------

def build_strategy():

    print("\nLoading structure rules...")

    rules = load_rules()

    print("Selecting parsing strategy...")

    strategy = determine_strategy(rules)

    save_strategy(strategy)

    print_summary(strategy)

    return strategy

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN KNOWLEDGE PARSING STRATEGY")
    print("=" * 60)

    build_strategy()

    print()

    print("=" * 60)
    print("PARSING STRATEGY SELECTED")
    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")

        print("-" * 40)

        print(e)

        print("-" * 40)