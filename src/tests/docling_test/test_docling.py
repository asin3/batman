"""
============================================================

Batman Student

CPS-003.1

Docling Evaluation

Purpose

Evaluate Docling extraction capability.

No Batman integration.

============================================================
"""

from pathlib import Path

from docling.document_converter import DocumentConverter


# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

PDF_FILE = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "physics"
    / "textbook"
    / "source"
    / "physics_textbook1.pdf"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "src"
    / "tests"
    / "docling_test"
    / "output"
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------------------------------
# DOCLING
# ----------------------------------------------------------

print()

print("=" * 60)
print("DOCLING EVALUATION")
print("=" * 60)

print()

print("Loading PDF...")

converter = DocumentConverter()

result = converter.convert(str(PDF_FILE))

document = result.document

print("Completed")

print()

# ----------------------------------------------------------
# EXPORT MARKDOWN
# ----------------------------------------------------------

markdown_file = OUTPUT_FOLDER / "text.md"

markdown_file.write_text(

    document.export_to_markdown(),

    encoding="utf-8"

)

print("Markdown exported")

# ----------------------------------------------------------
# EXPORT JSON
# ----------------------------------------------------------

json_file = OUTPUT_FOLDER / "document.json"

json_file.write_text(

    document.model_dump_json(

        indent=2

    ),

    encoding="utf-8"

)

print("JSON exported")

print()

print("=" * 60)
print("DOCLING TEST COMPLETE")
print("=" * 60)

print()

print("Output Folder")

print(OUTPUT_FOLDER)