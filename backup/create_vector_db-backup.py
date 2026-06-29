"""
===========================================================
Batman Student

Module:
create_vector_db.py

Purpose:
Read knowledge sources, create chunks, generate embeddings,
and store them in ChromaDB with standard metadata.

Owner:
Content Domain

Reads:
- data/class10/physics/textbook/
- data/class10/physics/notes/

Writes:
- vector_db/

Dependencies:
- chromadb
- sentence_transformers
- chunk_text.py

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Academic Content

Last Updated:
2026-06-25

===========================================================
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunk_text import chunk_text

from src.governance.metadata_enricher import (
    enrich_metadata
)

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

TEXTBOOK_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "physics"
    / "textbook"
)

NOTES_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "class10"
    / "physics"
    / "notes"
)

VECTOR_DB = (
    PROJECT_ROOT
    / "vector_db"
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# CHROMADB
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTOR_DB)
)

collection = client.get_or_create_collection(
    name="class10_physics"
)


# ---------------------------------------------------------
# SOURCES
# ---------------------------------------------------------

sources = [

    (
        TEXTBOOK_FOLDER,
        "textbook"
    ),

    (
        NOTES_FOLDER,
        "notes"
    )

]


# ---------------------------------------------------------
# INGEST
# ---------------------------------------------------------

documents_added = 0
chunks_added = 0

for folder, source in sources:

    if not folder.exists():

        print(
            f"Skipping: {folder}"
        )

        continue

    print(
        f"\nScanning: {folder.name}"
    )

    for file_path in sorted(folder.glob("*.txt")):

        print(
            f"Reading: {file_path.name}"
        )

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        metadata = {

            "board": "ICSE",

            "grade": "10",

            "subject": "Physics",

            "chapter": "TBD",
            
            "topic": "TBD",

            "page": "TBD",

            "document": file_path.name,

            "source": source

        }

        metadata = enrich_metadata(
            metadata,
            chunk
        )

        chunks = chunk_text(
            text,
            metadata
        )

        print(
            f"Chunks: {len(chunks)}"
        )

        for chunk in chunks:

            embedding = model.encode(
                chunk["text"]
            ).tolist()

            collection.add(

                ids=[
                    chunk["chunk_id"]
                ],

                embeddings=[
                    embedding
                ],

                documents=[
                    chunk["text"]
                ],

                metadatas=[
                    chunk["metadata"]
                ]

            )

            chunks_added += 1

        documents_added += 1


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 60)

print("VECTOR DATABASE CREATED")

print("=" * 60)

print(
    f"Documents : {documents_added}"
)

print(
    f"Chunks    : {chunks_added}"
)

print(
    f"Collection: class10_physics"
)

print(
    f"Vector DB : {VECTOR_DB}"
)

print("=" * 60)