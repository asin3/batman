"""
===========================================================
Batman Student

Module:
vector_retriever.py

Purpose:
Reusable semantic retrieval service.

Responsibilities:
- Connect to ChromaDB
- Query semantic chunks
- Return context + metadata

Owner:
Batman Core

===========================================================
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import chromadb

from sentence_transformers import SentenceTransformer

from src.config.paths import VECTOR_DB_DIR


# ---------------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# CHROMADB
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)

collection = client.get_collection(
    "icse_class10"
)

# ---------------------------------------------------------
# DEBUG
# ---------------------------------------------------------

DEBUG_RETRIEVAL = True

# ---------------------------------------------------------
# RETRIEVE CONTEXT
# ---------------------------------------------------------

def retrieve_context(
    question,
    top_k=3
):

    try:

        results = collection.query(

            query_texts=[
                question
            ],

            n_results=top_k

        )

    except Exception as e:

        print()

        print("[ERROR] Retrieval failed")

        print(e)

        return {

            "context": "",

            "metadata": [],

            "statistics": {}

        }

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadata = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:

        return {

            "context": "",

            "metadata": [],

            "statistics": {}

        }

    context = "\n\n".join(
        documents
    )

    statistics = {

        "chunks": len(documents),

        "documents": len(

            set(

                m.get(
                    "document_id",
                    ""
                )

                for m in metadata

            )

        )

    }

    if DEBUG_RETRIEVAL:

        print()

        print("=" * 60)

        print("RETRIEVAL")

        print("=" * 60)

        print(f"Question : {question}")

        print(f"Chunks   : {statistics['chunks']}")

        print(f"Documents: {statistics['documents']}")

        print()

        for item in metadata:

            print(

                item.get(
                    "document_id",
                    ""
                ),

                "|",

                item.get(
                    "heading",
                    ""
                )

            )

    return {

        "context": context,

        "metadata": metadata,

        "statistics": statistics

    }

# ---------------------------------------------------------
# STANDALONE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("VECTOR RETRIEVER TEST")
    print("=" * 60)

    question = input(
        "\nQuestion: "
    )

    result = retrieve_context(
        question
    )

    print()

    print("=" * 60)
    print("CONTEXT")
    print("=" * 60)

    print(
        result["context"]
    )

    print()

    print("=" * 60)
    print("METADATA")
    print("=" * 60)

    for item in result["metadata"]:

        print(item)

    print()

    print("=" * 60)
    print("STATISTICS")
    print("=" * 60)

    print(
        result["statistics"]
    )