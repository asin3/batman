"""
===========================================================
Batman Student

Module:
document_scanner.py

Purpose:
Discover academic PDF documents and register them.

Owner:
Content Domain

Reads:
- data/

Writes:
- data/document_registry.json
- metadata.json (inside each source folder)

Dependencies:
- pathlib
- json

Governed By:
ADR-007 Knowledge Ingestion Lifecycle

Single Source of Truth:
Academic Content

===========================================================
"""

from pathlib import Path
import json

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

DATA_FOLDER = Path("data")

REGISTRY_FILE = DATA_FOLDER / "document_registry.json"

SOURCE_FOLDER_NAME = "source"

IGNORE_FOLDERS = {
    "archive",
    "generated",
    "staging",
    "__pycache__",
}

VALID_SUBJECTS = {
    "physics",
    "chemistry",
    "biology",
    "maths",
}

VALID_SOURCE_TYPES = {
    "textbook",
    "notes",
    "pyq",
    "question_bank",
    "references",
    "samplesolvedpapers",
}

# ---------------------------------------------------------
# LOAD MASTER REGISTRY
# ---------------------------------------------------------

if REGISTRY_FILE.exists():

    registry = json.loads(
        REGISTRY_FILE.read_text(
            encoding="utf-8"
        )
    )

else:

    registry = []

# ---------------------------------------------------------
# INDEX EXISTING DOCUMENTS
# ---------------------------------------------------------

registry_by_path = {}

highest_id = 0

for record in registry:

    registry_by_path[record["path"]] = record

    try:

        highest_id = max(
            highest_id,
            int(
                record["document_id"].replace(
                    "DOC",
                    ""
                )
            )
        )

    except Exception:
        pass

next_id = highest_id + 1

# ---------------------------------------------------------
# SCAN SOURCE FOLDERS
# ---------------------------------------------------------

for source_folder in sorted(
    DATA_FOLDER.rglob(SOURCE_FOLDER_NAME)
):

    if any(
        part.lower() in IGNORE_FOLDERS
        for part in source_folder.parts
    ):
        continue

    folder_metadata = []

    for pdf_file in sorted(
        source_folder.glob("*.pdf")
    ):

        relative_path = str(
            pdf_file.relative_to(DATA_FOLDER)
        ).replace("\\", "/")

        parts = [
            p.lower()
            for p in pdf_file.parts
        ]

        # -----------------------------
        # BOARD
        # -----------------------------

        board = "ICSE"

        for part in parts:

            if part.upper() in {
                "ICSE",
                "CBSE",
                "STATE",
            }:

                board = part.upper()

        # -----------------------------
        # CLASS
        # -----------------------------

        grade = ""

        for part in parts:

            if part.startswith("class"):

                grade = part.replace(
                    "class",
                    ""
                )

        # -----------------------------
        # SUBJECT
        # -----------------------------

        subject = ""

        for part in parts:

            if part in VALID_SUBJECTS:

                subject = part.title()

        # -----------------------------
        # SOURCE TYPE
        # -----------------------------

        source_type = ""

        for part in parts:

            if part in VALID_SOURCE_TYPES:

                source_type = part

        # -----------------------------
        # EXISTING DOCUMENT
        # -----------------------------

        if relative_path in registry_by_path:

            record = registry_by_path[
                relative_path
            ]

            record["board"] = board
            record["grade"] = grade
            record["subject"] = subject
            record["source_type"] = source_type

        else:

            record = {

                "document_id":
                    f"DOC{next_id:06d}",

                "file":
                    pdf_file.name,

                "path":
                    relative_path,

                "board":
                    board,

                "grade":
                    grade,

                "subject":
                    subject,

                "source_type":
                    source_type,

                "status":
                    "RAW"

            }

            registry.append(record)

            registry_by_path[
                relative_path
            ] = record

            next_id += 1

        folder_metadata.append(record)

    # -----------------------------------------------------
    # WRITE FOLDER METADATA
    # -----------------------------------------------------

    metadata_file = (
        source_folder /
        "metadata.json"
    )

    metadata_file.write_text(

        json.dumps(
            folder_metadata,
            indent=4
        ),

        encoding="utf-8"

    )

# ---------------------------------------------------------
# SAVE MASTER REGISTRY
# ---------------------------------------------------------

registry.sort(
    key=lambda x: x["document_id"]
)

REGISTRY_FILE.write_text(

    json.dumps(
        registry,
        indent=4
    ),

    encoding="utf-8"

)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()

print("=" * 60)

print("DOCUMENT SCAN COMPLETE")

print("=" * 60)

print(f"Registered Documents : {len(registry)}")

print(f"Registry File        : {REGISTRY_FILE}")

print("=" * 60)