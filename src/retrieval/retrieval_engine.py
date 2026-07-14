"""
============================================================

Batman Student

Retrieval Engine

Purpose

Perform semantic retrieval from Batman's
Knowledge Repository.

============================================================
"""

import sys

from pathlib import Path

import chromadb

from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))


MODEL_NAME = "all-MiniLM-L6-v2"


DOCUMENT_FOLDER = (

    PROJECT_ROOT

    / "data"

    / "class10"

    / "biology"

    / "textbook"

    / "staging"

    / "DOC000013"

)


model = SentenceTransformer(

    MODEL_NAME

)


client = chromadb.PersistentClient(

    path=str(

        DOCUMENT_FOLDER / "vectordb"

    )

)


collection = client.get_collection(

    "knowledge"

)


def retrieve(question, top_k=5):

    query_embedding = model.encode(

        question,

        convert_to_numpy=True

    )


    raw_results = collection.query(

        query_embeddings=[

            query_embedding.tolist()

        ],

        n_results=top_k

    )


    results = []


    for index in range(

        len(raw_results["ids"][0])

    ):

        results.append(

            {

                "chunk_id": (

                    raw_results["ids"][0][index]

                ),

                "score": (

                    raw_results["distances"][0][index]

                ),

                "heading": (

                    raw_results["metadatas"][0][index]

                    .get("heading")

                ),

                "figure_refs": (

                    raw_results["metadatas"][0][index]

                    .get("figure_refs")

                ),

                "table_refs": (

                    raw_results["metadatas"][0][index]

                    .get("table_refs")

                ),

                "content": (

                    raw_results["documents"][0][index]

                )

            }

        )


    return results


def print_results(results):

    print()

    print("=" * 60)

    print("RETRIEVAL RESULTS")

    print("=" * 60)

    print()


    for index, result in enumerate(

        results,

        start=1

    ):

        print(

            f"Rank : {index}"

        )

        print(

            f"Chunk : {result['chunk_id']}"

        )

        print(

            f"Score : {result['score']:.4f}"

        )

        print(

            f"Heading : {result['heading']}"

        )

        print(

            f"Figures : {result['figure_refs']}"

        )

        print(

            f"Tables : {result['table_refs']}"

        )

        print()

        print(

            result["content"]

        )

        print()

        print("-" * 60)


if __name__ == "__main__":

    question = input(

        "\nQuestion : "

    )


    results = retrieve(

        question

    )


    print_results(

        results

    )