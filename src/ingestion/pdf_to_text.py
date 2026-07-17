"""
===========================================================
Batman Student

Module:
pdf_to_text.py

Purpose:
OCR all RAW documents registered in document_registry.json

Owner:
Content Domain

Reads:
- data/document_registry.json
- PDF files

Writes:
- *.txt
- document_registry.json

Dependencies:
- pdf2image
- pytesseract

Governed By:
ADR-007 Knowledge Ingestion Lifecycle

===========================================================
"""

from pathlib import Path
import json

from pdf2image import convert_from_path
import pytesseract

# ---------------------------------------------------------
# TESSERACT
# ---------------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ---------------------------------------------------------
# POPPLER
# ---------------------------------------------------------

POPPLER_PATH = (
    r"F:\batman_student\tools\poppler\poppler-26.02.0\Library\bin"
)

# ---------------------------------------------------------
# PROJECT PATHS
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

# ---------------------------------------------------------
# OCR
# ---------------------------------------------------------

processed = 0

skipped = 0

for document in registry:

    if document["status"] != "RAW":

        skipped += 1

        continue

    pdf_path = DATA_FOLDER / document["path"]

    if not pdf_path.exists():

        print()

        print(

            f"Missing : {pdf_path}"

        )

        continue

    print()

    print(

        f"Processing : {pdf_path.name}"

    )

    pages = convert_from_path(

        str(pdf_path),

        poppler_path=POPPLER_PATH

    )

    text = ""

    for page_no, page in enumerate(

        pages,

        start=1

    ):

        print(

            f"  OCR Page {page_no}"

        )

        page_text = pytesseract.image_to_string(

            page

        )

        text += (

            f"\n\n===== PAGE {page_no} =====\n\n"

        )

        text += page_text

    output_file = (

        pdf_path.with_suffix(".txt")

    )

    output_file.write_text(

        text,

        encoding="utf-8"

    )

    document["status"] = "OCR_DONE"

    REGISTRY_FILE.write_text(

        json.dumps(

            registry,

            indent=4

        ),

        encoding="utf-8"

    )

    processed += 1

# ---------------------------------------------------------
# SAVE REGISTRY
# ---------------------------------------------------------

#REGISTRY_FILE.write_text(

    #registry,

        #indent=4

    #),

    #encoding="utf-8"

#)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()

print("=" * 60)

print("OCR COMPLETE")

print("=" * 60)

print(

    f"Processed : {processed}"

)

print(

    f"Skipped   : {skipped}"

)

print("=" * 60)