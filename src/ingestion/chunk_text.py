"""
===========================================================
Batman Student

Module:
chunk_text.py

Purpose:
Create reusable text chunks with source metadata for
vector indexing.

Owner:
Content Domain

Reads:
- Raw textbook / notes text

Writes:
- None (returns chunks to caller)

Dependencies:
- hashlib

Governed By:
ADR-004 Data Governance

Single Source of Truth:
Input text supplied by ingestion pipeline

Last Updated:
2026-06-25

===========================================================
"""

import hashlib


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
):
    """
    Returns:

    [
        {
            "chunk_id": "...",
            "text": "...",
            "metadata": {...}
        }
    ]
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    chunk_number = 1

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text)
        )

        chunk = text[start:end].strip()

        if chunk:

            chunk_id = hashlib.md5(
                chunk.encode("utf-8")
            ).hexdigest()

            chunk_metadata = metadata.copy()

            chunk_metadata.update({

                "chunk_number": chunk_number,

                "chunk_size": len(chunk)

            })

            chunks.append({

                "chunk_id": chunk_id,

                "text": chunk,

                "metadata": chunk_metadata

            })

            chunk_number += 1

        if end >= len(text):
            break

        start = end - overlap

    return chunks


if __name__ == "__main__":

    sample = """
    Force is a push or pull acting on a body.
    It changes the state of rest or motion.
    """ * 50

    metadata = {

        "board": "ICSE",

        "grade": "10",

        "subject": "Physics",

        "chapter": "TBD",

        "topic": "TBD",

        "page": "TBD",

        "document": "sample.txt",

        "source": "textbook"

    }

    chunks = chunk_text(
        sample,
        metadata
    )

    print(
        f"Chunks Created: {len(chunks)}"
    )

    print()

    print(chunks[0]["metadata"])

    print()

    print(chunks[0]["text"][:300])