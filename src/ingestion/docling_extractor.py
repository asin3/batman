"""
============================================================

Batman Student

CPS-003B.1

Docling Extractor

Purpose

Select documents for processing.

(Current Stage)

• Load document registry
• Apply Pilot Mode
• Display selected documents

No extraction yet.

============================================================
"""

import json
from pathlib import Path

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.pilot_documents import (
    PILOT_MODE,
    PILOT_DOCUMENTS,
)

from datetime import datetime

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REGISTRY_FILE = (
    PROJECT_ROOT
    / "data"
    / "document_registry.json"
)

# ----------------------------------------------------------
# LOAD REGISTRY
# ----------------------------------------------------------

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:

    registry = json.load(f)

# ----------------------------------------------------------
# FILTER DOCUMENTS
# ----------------------------------------------------------

selected_documents = []

for document in registry:

    if PILOT_MODE:

        if document["document_id"] not in PILOT_DOCUMENTS:

            continue

    selected_documents.append(document)

# ----------------------------------------------------------
# DOCLING EXTRACTION
# ----------------------------------------------------------

from docling.document_converter import DocumentConverter

converter = DocumentConverter()

for document in selected_documents:

    source_pdf = PROJECT_ROOT / "data" / document["path"]

    output_folder = (
        source_pdf.parent.parent
        / "staging"
        / document["document_id"]
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    markdown_file = output_folder / "document.md"

    json_file = output_folder / "document.json"

    # ----------------------------------------------
    # Resume Support
    # ----------------------------------------------

    if markdown_file.exists() and json_file.exists():

        print(f"[SKIPPED] {document['document_id']}")

        continue

    print(f"[PROCESSING] {document['document_id']}")

    result = converter.convert(str(source_pdf))

    doc = result.document

    markdown_file.write_text(
        doc.export_to_markdown(),
        encoding="utf-8"
    )

    json_file.write_text(
        doc.model_dump_json(indent=2),
        encoding="utf-8"
    )

    print(f"[DONE] {document['document_id']}")

    # ----------------------------------------------
    # UPDATE DOCUMENT REGISTRY
    # ----------------------------------------------

    for item in registry:

        if item["document_id"] == document["document_id"]:

            item["status"] = "EXTRACTED"

            break

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:

        json.dump(
            registry,
            f,
            indent=4,
            ensure_ascii=False
        )

    # ----------------------------------------------
    # UPDATE SOURCE METADATA
    # ----------------------------------------------

    metadata_file = source_pdf.parent / "metadata.json"

    if metadata_file.exists():

        with open(metadata_file, "r", encoding="utf-8") as f:

            metadata = json.load(f)

        for item in metadata:

            if item["file"] == document["file"]:

                item["status"] = "EXTRACTED"
                
                item["processing"] = {

                    "engine": "docling",

                    "status": "completed",

                    "processed_at": datetime.now().isoformat(timespec="seconds"),

                    "artifact_folder": f"../staging/{document['document_id']}"

                }

                break

        with open(metadata_file, "w", encoding="utf-8") as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

    print("[UPDATED] metadata")
# ----------------------------------------------------------
# REPORT
# ----------------------------------------------------------

print()

print("=" * 60)
print("DOCLING EXTRACTOR")
print("=" * 60)

print()

print(
    f"Mode                 : "
    f"{'PILOT' if PILOT_MODE else 'FULL'}"
)

print(
    f"Documents Selected   : "
    f"{len(selected_documents)}"
)

print()

print("-" * 60)

for document in selected_documents:

    print()

    print(document["document_id"])

    print(document["subject"])

    print(document["source_type"])

    print(document["file"])

print()

print("=" * 60)
print("READY")
print("=" * 60)