"""
===========================================================
Batman Student

Module:
ocr_normalizer.py

Purpose:
Normalize OCR-generated textbook text before any
knowledge extraction.

This module converts noisy OCR into deterministic,
parser-friendly academic text.

Owner:
Knowledge Engine

Reads:
data/class10/physics/textbook/physics-textbook.txt

Writes:
data/class10/physics/textbook/normalized_textbook.txt

Governed By:
ADR-004 Data Governance

Single Source of Truth:
physics-textbook.txt

===========================================================
"""

from pathlib import Path
import re


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_TEXT = (
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
    / "class10"
    / "physics"
    / "textbook"
    / "normalized_textbook.txt"
)


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

def load_text():

    if not RAW_TEXT.exists():

        raise FileNotFoundError(
            f"Missing:\n{RAW_TEXT}"
        )

    return RAW_TEXT.read_text(
        encoding="utf-8",
        errors="ignore"
    )


# ---------------------------------------------------------
# BASIC NORMALIZATION
# ---------------------------------------------------------

def normalize_text(text):

    # Normalize line endings
    text = text.replace(
        "\r\n",
        "\n"
    )

    # Tabs → spaces
    text = text.replace(
        "\t",
        " "
    )

    # Multiple spaces
    text = re.sub(
        r"[ ]{2,}",
        " ",
        text
    )

    # Multiple blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text

# ---------------------------------------------------------
# REMOVE OCR NOISE
# ---------------------------------------------------------

def remove_ocr_noise(text):

    # Remove page markers
    text = re.sub(

        r"===== PAGE\s+\d+\s+=====",

        "",

        text,

        flags=re.IGNORECASE

    )

    # Remove isolated page numbers

    text = re.sub(

        r"^\s*-?\d+\s*$",

        "",

        text,

        flags=re.MULTILINE

    )

    # Remove isolated ~

    text = re.sub(

        r"^\s*~\s*$",

        "",

        text,

        flags=re.MULTILINE

    )

    # Remove form-feed characters

    text = text.replace(

        "\f",

        ""

    )

    return text


# ---------------------------------------------------------
# NORMALIZE PUNCTUATION
# ---------------------------------------------------------

def normalize_punctuation(text):

    replacements = {

        "—": "-",

        "–": "-",

        "“": "\"",

        "”": "\"",

        "‘": "'",

        "’": "'",

        "…": "...",

        "•": "-"

    }

    for old, new in replacements.items():

        text = text.replace(

            old,

            new

        )

    return text


# ---------------------------------------------------------
# NORMALIZE COMMON OCR ERRORS
# ---------------------------------------------------------

def normalize_common_words(text):

    corrections = {

        "Retraction through": "Refraction through",

        "Carcwits": "Circuits",

        "Hlectro": "Electro",

        "atid": "and",

        "Ble ctr Chl": "Electricity",

        "Calortinety": "Calorimetry"

    }

    for wrong, correct in corrections.items():

        text = re.sub(

            wrong,

            correct,

            text,

            flags=re.IGNORECASE

        )

    return text

# ---------------------------------------------------------
# CONTENTS CLEANUP
# ---------------------------------------------------------

def normalize_contents(text):

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            lines.append("")
            continue

        # Compress long dotted leaders
        line = re.sub(

            r"\.{3,}",

            " ... ",

            line

        )

        # Normalize page ranges
        line = re.sub(

            r"\s*[-—–]+\s*",

            " - ",

            line

        )

        # Collapse repeated whitespace
        line = re.sub(

            r"\s{2,}",

            " ",

            line

        )

        lines.append(line)

    return "\n".join(lines)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

def save_text(text):

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(

        text,

        encoding="utf-8"

    )

    print("\nNormalized textbook saved.")

    print(f"Output : {OUTPUT}")


# ---------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------

def build_normalized_text():

    print("\nLoading textbook...")

    text = load_text()

    print("Basic normalization...")

    text = normalize_text(text)

    print("Removing OCR noise...")

    text = remove_ocr_noise(text)

    print("Normalizing punctuation...")

    text = normalize_punctuation(text)

    print("Correcting common OCR words...")

    text = normalize_common_words(text)

    print("Cleaning contents formatting...")

    text = normalize_contents(text)

    save_text(text)

    return text

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("BATMAN OCR NORMALIZER")
    print("=" * 60)

    normalized_text = build_normalized_text()

    print()

    print("=" * 60)
    print("NORMALIZATION COMPLETE")
    print("=" * 60)

    print(
        f"Characters : {len(normalized_text)}"
    )

    print(
        f"Lines      : {len(normalized_text.splitlines())}"
    )

    print(
        f"Output     : {OUTPUT}"
    )

    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")
        print("-" * 40)
        print(e)
        print("-" * 40)