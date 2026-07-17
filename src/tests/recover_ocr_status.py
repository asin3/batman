"""
===========================================================
Batman Student

Utility:
recover_ocr_status.py

Purpose:
Recover OCR status after an interrupted OCR run.

Reads:
- data/document_registry.json
- OCR text files

Writes:
- data/document_registry.json

===========================================================
"""

import json
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

DATA_FOLDER = Path("data")

REGISTRY_FILE = (
    DATA_FOLDER /
    "document_registry.json"
)

# ---------------------------------------------------------
# LOAD REGISTRY
# ---------------------------------------------------------

registry = json.loads(

    REGISTRY_FILE.read_text(

        encoding="utf-8"

    )

)

updated = 0

# ---------------------------------------------------------
# RECOVERY
# ---------------------------------------------------------

for document in registry:

    if document["status"] != "RAW":

        continue

    pdf_path = DATA_FOLDER / document["path"]

    txt_path = pdf_path.with_suffix(".txt")

    if txt_path.exists():

        document["status"] = "OCR_DONE"

        updated += 1

        print(

            f"Recovered : {document['document_id']}"

        )

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

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

print("OCR RECOVERY COMPLETE")

print("=" * 60)

print(

    f"Recovered : {updated}"

)

print("=" * 60)