"""
===========================================================
Batman Student

Module:
textbook_structure_extractor.py

Purpose:
Extract the academic structure from the master textbook.

This module builds the first structured representation
of the textbook before metadata enrichment and vectorization.

Owner:
Knowledge Engine

Reads:
data/class10/physics/textbook/physics-textbook.txt

Writes:
data/governance/ICSE/class10/physics/
textbook_structure.json

Governed By:
ADR-004 Data Governance

Single Source of Truth:
physics-textbook.txt

===========================================================
"""

from pathlib import Path
import json
import re


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEXTBOOK = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "physics"
    / "textbook"
    / "physics-textbook.txt"
)

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "governance"
    / "ICSE"
    / "class10"
    / "physics"
    / "textbook_structure.json"
)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# LOAD TEXTBOOK
# ---------------------------------------------------------

def load_textbook():

    if not TEXTBOOK.exists():

        raise FileNotFoundError(
            f"Missing textbook:\n{TEXTBOOK}"
        )

    return TEXTBOOK.read_text(
        encoding="utf-8",
        errors="ignore"
    )


# ---------------------------------------------------------
# CLEAN LINE
# ---------------------------------------------------------

def clean_line(line):

    line = line.strip()

    if not line:
        return ""

    if line.startswith("====="):
        return ""

    if line == "~":
        return ""

    if re.fullmatch(
        r"-?\d+",
        line
    ):
        return ""

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line


# ---------------------------------------------------------
# EXTRACT CONTENTS PAGE
# ---------------------------------------------------------

def extract_contents(text):

    match = re.search(

        r"Contents(.*?)===== PAGE 2 =====",

        text,

        re.DOTALL | re.IGNORECASE

    )

    if not match:

        return None

    return match.group(1)
    
# ---------------------------------------------------------
# EXTRACT UNITS
# ---------------------------------------------------------

def extract_units(contents):

    units = []

    pattern = re.compile(

        r"\(([A-F])\)\s+([A-Z ,&]+)",

        re.IGNORECASE

    )

    for match in pattern.finditer(contents):

        units.append(

            {

                "unit_id": match.group(1),

                "unit_name": (
                    match.group(2)
                    .strip()
                    .title()
                ),

                "chapters": []

            }

        )

    return units


# ---------------------------------------------------------
# EXTRACT CHAPTERS
# ---------------------------------------------------------

def extract_chapters(contents, units):

    chapter_pattern = re.compile(

        r"^\s*(\d{1,2})[.;,:]?\s+(.+?)\s+\d+\s*[-—]\s*\d+\s*$",

        re.MULTILINE

    )

    chapters = []

    current_unit = 0

    current_letter = None

    lines = contents.splitlines()

    for line in lines:

        line = clean_line(line)

        if not line:
            continue

        unit_match = re.match(

            r"\(([A-F])\)",

            line,

            re.IGNORECASE

        )

        if unit_match:

            current_letter = (
                unit_match.group(1)
                .upper()
            )

            for i, unit in enumerate(units):

                if unit["unit_id"] == current_letter:

                    current_unit = i

                    break

            continue

        chapter_match = chapter_pattern.match(line)

        if not chapter_match:

            continue

        chapter_number = int(

            chapter_match.group(1)

        )

        chapter_name = (

            chapter_match.group(2)

            .replace("atid", "and")
            .replace("Retraction", "Refraction")
            .replace("Carcwits", "Circuits")
            .replace("Hlectro", "Electro")

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
                units[current_unit]["unit_name"],

            "topics": []

        }

        chapters.append(chapter)

        units[current_unit][
            "chapters"
        ].append(

            chapter["chapter_id"]

        )

    return chapters
    
# ---------------------------------------------------------
# BUILD STRUCTURE
# ---------------------------------------------------------

def build_structure():

    print("\nLoading textbook...")

    text = load_textbook()

    print("Extracting contents page...")

    contents = extract_contents(text)

    if contents is None:

        raise RuntimeError(
            "Contents page not found."
        )

    print("Extracting units...")

    units = extract_units(contents)

    print(
        f"Units found : {len(units)}"
    )

    print("Extracting chapters...")

    chapters = extract_chapters(
        contents,
        units
    )

    print(
        f"Chapters found : {len(chapters)}"
    )

    structure = {

        "board": "ICSE",

        "grade": "10",

        "subject": "Physics",

        "units": units,

        "chapters": chapters

    }

    return structure


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

def save_structure(structure):

    with open(

        OUTPUT,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            structure,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nSaved:")

    print(OUTPUT)

    print()

    print("Summary")

    print("-" * 40)

    print(

        f"Units    : {len(structure['units'])}"

    )

    print(

        f"Chapters : {len(structure['chapters'])}"

    )

    print(

        f"Output   : textbook_structure.json"

    )
    
# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN KNOWLEDGE STRUCTURE EXTRACTOR")
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