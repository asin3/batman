"""
===========================================================
Batman Student

Module:
create_vector_db.py

Purpose:
Read knowledge sources, create chunks, enrich metadata,
generate embeddings and store them inside ChromaDB.

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
- src.ingestion.chunk_text
- src.governance.metadata_enricher

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

from sentence_transformers import (
    SentenceTransformer
)

from src.ingestion.chunk_text import (
    chunk_text
)

from src.governance.metadata_enricher import (
    enrich_metadata
)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

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
# EMBEDDING MODEL
# ---------------------------------------------------------

print()

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# CHROMADB
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(
        VECTOR_DB
    )
)

collection = client.get_or_create_collection(

    name="class10_physics"

)


# ---------------------------------------------------------
# KNOWLEDGE SOURCES
# ---------------------------------------------------------

SOURCES = [

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
# COUNTERS
# ---------------------------------------------------------

documents_added = 0

chunks_added = 0

# ---------------------------------------------------------
# INGESTION
# ---------------------------------------------------------

for folder, source in SOURCES:

    if not folder.exists():

        print(
            f"\nSkipping: {folder}"
        )

        continue

    print()

    print(
        f"Scanning: {folder.name}"
    )

    for file_path in sorted(
        folder.glob("*.txt")
    ):

        print(
            f"Reading: {file_path.name}"
        )

        text = file_path.read_text(

            encoding="utf-8",

            errors="ignore"

        )

        base_metadata = {

            "board": "ICSE",

            "grade": "10",

            "subject": "Physics",

            "chapter": "TBD",

            "topic": "TBD",

            "page": "TBD",

            "document": file_path.name,

            "source": source

        }

        chunks = chunk_text(

            text,

            base_metadata

        )

        print(

            f"Chunks: {len(chunks)}"

        )

        for chunk in chunks:

            enriched_metadata = enrich_metadata(

                chunk["metadata"],

                chunk["text"]

            )

            chunk["metadata"] = enriched_metadata

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

                    enriched_metadata

                ]

            )

            chunks_added += 1

        documents_added += 1

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()

print("=" * 60)

print("VECTOR DATABASE CREATED")

print("=" * 60)

print(

    f"Documents : {documents_added}"

)

print(

    f"Chunks    : {chunks_added}"

)

print(

    "Collection: class10_physics"

)

print(

    f"Vector DB : {VECTOR_DB}"

)

print("=" * 60)        