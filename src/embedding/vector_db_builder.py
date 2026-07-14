"""
============================================================

Batman Student

Vector Database Builder

Purpose

Create the Vector Database from the frozen
Knowledge Repository and embeddings.

============================================================
"""

import json
import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
import numpy as np

from src.knowledge.knowledge_repository import KnowledgeRepository

DOCUMENT_FOLDER = (

    PROJECT_ROOT
    / "data"
    / "class10"
    / "biology"
    / "textbook"
    / "staging"
    / "DOC000013"

)

repository = KnowledgeRepository(DOCUMENT_FOLDER)

assets = repository.load_all()

chunks = assets["chunks"]

embeddings = np.load(

    DOCUMENT_FOLDER / "embeddings.npy"

)

client = chromadb.PersistentClient(

    path=str(

        DOCUMENT_FOLDER / "vectordb"

    )

)

collection = client.get_or_create_collection(

    name="knowledge"

)

collection.add(

    ids=[

        chunk["id"]

        for chunk in chunks

    ],

    embeddings=embeddings.tolist(),

    documents=[

        chunk["content"]

        for chunk in chunks

    ],

    metadatas=[

        {

            "heading": chunk["heading"],

            "page": chunk["page"],

            "figure_refs": json.dumps(

                chunk["figure_refs"]

            ),

            "table_refs": json.dumps(

                chunk["table_refs"]

            )

        }

        for chunk in chunks

    ]

)

print()

print("=" * 60)

print("VECTOR DATABASE BUILDER")

print("=" * 60)

print()

print(f"Chunks Indexed : {len(chunks)}")

print(f"Embeddings     : {len(embeddings)}")

print(f"Collection     : knowledge")

print()

print("READY")