"""
===========================================================
Batman Student

Utility:
move_ocr_output_to_staging.py

Purpose:
Move generated OCR text files from source/ to staging/.

Reads:
- data/document_registry.json

Writes:
- staging/*.txt

===========================================================
"""

import json
import shutil
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

DATA_FOLDER = Path("data")

REGISTRY_FILE = DATA_FOLDER / "document_registry.json"

# ---------------------------------------------------------
# LOAD REGISTRY
# ---------------------------------------------------------

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:

    registry = json.load(f)

# ---------------------------------------------------------
# COUNTERS
# ---------------------------------------------------------

moved = 0
skipped = 0
missing = 0

# ---------------------------------------------------------
# PROCESS
# ---------------------------------------------------------

for document in registry:

    pdf_path = DATA_FOLDER / document["path"]

    source_folder = pdf_path.parent

    staging_folder = source_folder.parent / "staging"

    staging_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    source_txt = source_folder / (
        pdf_path.stem + ".txt"
    )

    target_txt = staging_folder / (
        pdf_path.stem + ".txt"
    )

    if not source_txt.exists():

        missing += 1

        print(
            f"[MISSING] {source_txt.name}"
        )

        continue

    if target_txt.exists():

        skipped += 1

        print(
            f"[SKIPPED] {target_txt.name}"
        )

        continue

    shutil.move(

        str(source_txt),

        str(target_txt)

    )

    moved += 1

    print(

        f"[MOVED] {source_txt.name}"

    )

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()

print("=" * 60)
print("OCR MIGRATION COMPLETE")
print("=" * 60)
print(f"Moved   : {moved}")
print(f"Skipped : {skipped}")
print(f"Missing : {missing}")
print("=" * 60)