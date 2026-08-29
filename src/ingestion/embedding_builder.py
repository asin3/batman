"""
============================================================

Batman Student

CPS-003D.1

Embedding Builder

Purpose

Read semantic chunks and generate embeddings.

Current Stage

• Read chunks.json
• Generate embeddings
• Save embeddings.json

============================================================
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "Board"
    / "icse"
    / "class10"
    / "biology"
    / "textbook"
    / "staging"
    / "DOC000013"
)

CHUNKS_FILE = STAGING_FOLDER / "chunks.json"

OUTPUT_FILE = STAGING_FOLDER / "embeddings.json"

# ---------------------------------------------------------
# DEBUG SETTINGS
# ---------------------------------------------------------

SAVE_DEBUG_EMBEDDINGS = True
#SAVE_DEBUG_EMBEDDINGS = False


print()
print("=" * 60)
print("EMBEDDING BUILDER")
print("=" * 60)

print()
print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model Ready")

with open(
    CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

embeddings = []

for index, chunk in enumerate(chunks, start=1):

    vector = model.encode(
        chunk["content"]
    ).tolist()

    embeddings.append({

        "chunk_id": index,

        "heading": chunk["heading"],

        "content": chunk["content"],

        "embedding": vector

    })

    print(
        f"Embedded {index}/{len(chunks)}"
    )

if SAVE_DEBUG_EMBEDDINGS:

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            embeddings,
            f,
            ensure_ascii=False,
            indent=4
        )

    print()

    print(f"Saved      : {OUTPUT_FILE}")

else:

    print()

    print("Debug embedding file skipped.")

print()

print(f"Embeddings : {len(embeddings)}")

print()

print("=" * 60)
print("COMPLETE")
print("=" * 60)