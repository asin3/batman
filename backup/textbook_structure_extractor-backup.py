"""
===========================================================
Batman Student

Module:
textbook_structure_extractor.py

Purpose:
Extract textbook hierarchy from the NORMALIZED textbook.

Owner:
Knowledge Engine

Reads:
normalized_textbook.txt

Writes:
textbook_structure.json

===========================================================
"""

from pathlib import Path
import json
import re


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "physics"
    / "textbook"
    / "normalized_textbook.txt"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "governance"
    / "ICSE"
    / "class10"
    / "physics"
    / "textbook_structure.json"
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
# FIND CONTENTS
# ---------------------------------------------------------

def extract_contents(text):

    start = re.search(
        r"\bContents\b",
        text,
        re.IGNORECASE
    )

    if not start:

        raise RuntimeError(
            "Contents page not found."
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

def clean_line(line):

    line = line.strip()

    if not line:

        return ""

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line

# ---------------------------------------------------------
# EXTRACT UNITS
# ---------------------------------------------------------

def extract_units(contents):

    units = []

    current_unit = None

    for raw in contents.splitlines():

        line = clean_line(raw)

        if not line:
            continue

        match = re.match(

            r"\(([A-F])\)\s+(.+)",

            line,

            re.IGNORECASE

        )

        if not match:
            continue

        current_unit = {

            "unit_id": match.group(1).upper(),

            "unit_name": match.group(2).strip(),

            "chapters": []

        }

        units.append(current_unit)

    return units


# ---------------------------------------------------------
# EXTRACT CHAPTERS
# ---------------------------------------------------------

def extract_chapters(contents, units):

    chapters = []

    current_unit = None

    unit_index = -1

    chapter_pattern = re.compile(

        r"^\s*(\d{1,2})\s*[.:;-]?\s*(.+?)\s+(\d+)\s*[-–]\s*(\d+)\s*$"

    )

    for raw in contents.splitlines():

        line = clean_line(raw)

        if not line:
            continue

        unit_match = re.match(

            r"\(([A-F])\)",

            line,

            re.IGNORECASE

        )

        if unit_match:

            unit_index += 1

            if unit_index < len(units):

                current_unit = units[unit_index]

            continue

        match = chapter_pattern.match(line)

        if not match:
            continue

        chapter = {

            "chapter_id":
                f"PHY-{int(match.group(1)):02}",

            "chapter_number":
                int(match.group(1)),

            "chapter_name":
                match.group(2).strip(),

            "unit":
                current_unit["unit_name"]
                if current_unit else None,

            "start_page":
                int(match.group(3)),

            "end_page":
                int(match.group(4)),

            "topics": []

        }

        chapters.append(chapter)

        if current_unit:

            current_unit["chapters"].append(

                chapter["chapter_id"]

            )

    return chapters

# ---------------------------------------------------------
# BUILD STRUCTURE
# ---------------------------------------------------------

def build_structure():

    print("\nLoading normalized textbook...")

    text = load_text()

    print("Locating Contents section...")

    contents = extract_contents(text)

    print("Extracting Units...")

    units = extract_units(contents)

    print(f"Units found : {len(units)}")

    print("Extracting Chapters...")

    chapters = extract_chapters(
        contents,
        units
    )

    print(f"Chapters found : {len(chapters)}")

    structure = {

        "board": "ICSE",

        "grade": "10",

        "subject": "Physics",

        "source": "normalized_textbook.txt",

        "units": units,

        "chapters": chapters

    }

    return structure


# ---------------------------------------------------------
# SAVE JSON
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

    print("\nSaved:")

    print(OUTPUT_FILE)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def print_summary(structure):

    print("\nSummary")

    print("-" * 40)

    print(

        f"Units          : {len(structure['units'])}"

    )

    print(

        f"Chapters       : {len(structure['chapters'])}"

    )

    total_pages = 0

    for chapter in structure["chapters"]:

        if (

            chapter["start_page"] is not None

            and

            chapter["end_page"] is not None

        ):

            total_pages += (

                chapter["end_page"]

                -

                chapter["start_page"]

                +

                1

            )

    print(

        f"Pages Covered  : {total_pages}"

    )

    print(

        "Output         : textbook_structure.json"

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

    print_summary(structure)

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