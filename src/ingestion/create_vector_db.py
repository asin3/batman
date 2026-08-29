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
- data/Board/icse/class10/physics/textbook/
- data/Board/icse/class10/physics/notes/

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
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.paths import (
    STAGING_DIR,
    VECTOR_DB_DIR,
)

import chromadb
import json

from sentence_transformers import (
    SentenceTransformer
)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

VECTOR_DB = VECTOR_DB_DIR

REGISTRY_FILE = (
    PROJECT_ROOT
    / "data"
    / "document_registry.json"
)

# ---------------------------------------------------------
# INDEX MODE
# ---------------------------------------------------------

REBUILD_INDEX = False

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
    name="icse_class10"
)


# ---------------------------------------------------------
# COUNTERS
# ---------------------------------------------------------

documents_added = 0

chunks_added = 0

# ---------------------------------------------------------
# INGESTION
# ---------------------------------------------------------

# ---------------------------------------------------------
# PROCESS STAGED CHUNKS
# ---------------------------------------------------------

with open(
    REGISTRY_FILE,
    "r",
    encoding="utf-8"
) as f:

    registry = json.load(f)

for document in registry:

    # ---------------------------------------------------------
    # INDEX FILTER
    # ---------------------------------------------------------

    if REBUILD_INDEX:

        if document["status"] not in [

            "EXTRACTED",

            "INDEXED"

        ]:

            continue

    else:

        if document["status"] != "EXTRACTED":

            continue
    
    print(
        f"[{document['status']}] "
        f"{document['document_id']}"
    )


    source_pdf = (
        PROJECT_ROOT
        / "data"
        / document["path"]
    )

    chunk_file = (
        source_pdf.parent.parent
        / "staging"
        / document["document_id"]
        / "chunks.json"
    )

    if not chunk_file.exists():

        print(
            f"[MISSING] {document['document_id']}"
        )

        continue

    print()

    print(
        f"Reading {document['document_id']}"
    )

    with open(
        chunk_file,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    for index, chunk in enumerate(chunks):

        embedding = model.encode(
            chunk["content"]
        ).tolist()

        collection.add(

            ids=[
                f"{document['document_id']}_{index}"
            ],

            embeddings=[
                embedding
            ],

            documents=[
                chunk["content"]
            ],

            metadatas=[{

                "document_id": document["document_id"],
                "subject": document["subject"],
                "board": document["board"],
                "grade": document["grade"],
                "source_type": document["source_type"],
                "heading": chunk["heading"]

            }]

        )

        chunks_added += 1

    documents_added += 1
# ---------------------------------------------------------
# UPDATE REGISTRY STATUS
# ---------------------------------------------------------

    document["status"] = "INDEXED"

# ---------------------------------------------------------
# SAVE UPDATED REGISTRY
# ---------------------------------------------------------

with open(
    REGISTRY_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        registry,
        f,
        indent=4,
        ensure_ascii=False
    )

print()

print("[UPDATED] document_registry.json")


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
    "Collection: icse_class10"
)

print(

    f"Vector DB : {VECTOR_DB}"

)

print("=" * 60)        