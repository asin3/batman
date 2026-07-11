"""
============================================================

Batman Student

CPS-003C.1

Semantic Chunk Builder

Purpose

Read document.md from staged artifacts and
produce Batman semantic chunks.

Current Stage

• Read metadata
• Read markdown
• Detect headings
• Create semantic chunks
• Save chunks.json

============================================================
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "biology"
    / "textbook"
    / "staging"
    / "DOC000013"
)

MARKDOWN_FILE = STAGING_FOLDER / "document.md"

OUTPUT_FILE = STAGING_FOLDER / "chunks.json"

print()
print("=" * 60)
print("SEMANTIC CHUNK BUILDER")
print("=" * 60)

markdown = MARKDOWN_FILE.read_text(
    encoding="utf-8"
)

lines = markdown.splitlines()

chunks = []

current_heading = "Document"

buffer = []

for line in lines:

    line = line.strip()

    if not line:
        continue

    if line.startswith("#"):

        if buffer:

            chunks.append({

                "heading": current_heading,

                "content": "\n".join(buffer)

            })

            buffer = []

        current_heading = line.lstrip("#").strip()

    else:

        buffer.append(line)

if buffer:

    chunks.append({

        "heading": current_heading,

        "content": "\n".join(buffer)

    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        indent=4,
        ensure_ascii=False
    )

print()

print(f"Chunks Created : {len(chunks)}")

print()

print(f"Saved : {OUTPUT_FILE}")

print()

print("=" * 60)
print("COMPLETE")
print("=" * 60)