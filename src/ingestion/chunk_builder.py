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

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge.document_adapter import (
    load_document,
    get_content_texts,
)

STAGING_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "biology"
    / "textbook"
    / "staging"
    / "DOC000013"
)

DOCUMENT_JSON = STAGING_FOLDER / "document.json"

OUTPUT_FILE = STAGING_FOLDER / "chunks.json"

print()
print("=" * 60)
print("SEMANTIC CHUNK BUILDER")
print("=" * 60)

#markdown = MARKDOWN_FILE.read_text(
#    encoding="utf-8"
#)

#lines = markdown.splitlines()

document = load_document(
    DOCUMENT_JSON
)

lines = get_content_texts(
    document
)

# ---------------------------------------------------------
# BATMAN CHUNK
# ---------------------------------------------------------

def create_chunk(

    chunk_id,

    heading,

    content,

    page,

    label,

    parent,

    children,

    source_objects
):

    return {

        "id": chunk_id,

        "heading": heading,

        "content": content,

        "page": page,

        "label": label,

        "parent": parent,

        "children": children,

        "source_objects": source_objects,

        "figure_refs": [],

        "table_refs": []

    }

chunks = []

#current_heading = "Document"

#buffer = []

#for line in lines:

#    text = line["text"].strip()

#    if not text:
#        continue

#    if text.startswith("#"):

#        if buffer:

#            chunks.append({

#                "heading": current_heading,

#                "content": "\n".join(buffer)

#            })

#           buffer = []

#        current_heading = text.lstrip("#").strip()

#    else:

#        buffer.append(text)

#if buffer:

#    chunks.append({

#        "heading": current_heading,

#        "content": "\n".join(buffer)

#    })

current_heading = "Document"

current_page = None

buffer = []

source_buffer = []

for item in lines:

    if item["label"] == "section_header":

        content = "\n".join(buffer).strip()

        if len(content) >= 30:

            chunk_id = f"CHUNK{len(chunks)+1:06d}"

            source_objects = source_buffer.copy()

            chunks.append(

                create_chunk(

                    chunk_id=chunk_id,

                    heading=current_heading,

                    content=content,

                    page=current_page,

                    label=item["label"],

                    parent=None,

                    source_objects=source_objects,

                    children=[]

                )

            )

        buffer = []

        source_buffer = []

        current_heading = item["text"]

        current_page = item["page"]

        continue

    buffer.append(

        item["text"]

    )

    source_buffer.append(

        item["id"]

    )

content = "\n".join(buffer).strip()

if len(content) >= 30:

    chunk_id = f"CHUNK{len(chunks)+1:06d}"
    
    chunks.append(

        create_chunk(

            chunk_id=chunk_id,

            heading=current_heading,

            content=content,

            page=current_page,

            label="section_header",

            parent=None,

            source_objects=source_buffer,

            children=[]

        )

    )

buffer = []


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