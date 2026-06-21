from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

# ---------------------------------
# CONFIG
# ---------------------------------

TEXTBOOK_FOLDER = Path(
    "data/class10/physics/textbook"
)

NOTES_FOLDER = Path(
    "data/class10/physics/notes"
)

CHUNK_SIZE = 1000

# ---------------------------------
# LOAD MODEL
# ---------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------------------------------
# CHROMADB
# ---------------------------------

client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_or_create_collection(
    name="class10_physics"
)

# ---------------------------------
# INGEST FILES
# ---------------------------------

chunk_counter = 0

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

for folder, source_type in sources:

    if not folder.exists():
        continue

    for file_path in folder.glob("*.txt"):

        print(
            f"Reading: {file_path.name}"
        )

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = [
            text[i:i + CHUNK_SIZE]
            for i in range(
                0,
                len(text),
                CHUNK_SIZE
            )
        ]

        for chunk in chunks:

            embedding = model.encode(
                chunk
            ).tolist()

            collection.add(
                ids=[
                    f"chunk_{chunk_counter}"
                ],
                embeddings=[
                    embedding
                ],
                documents=[
                    chunk
                ],
                metadatas=[
                    {
                        "source_type": source_type,
                        "subject": "physics",
                        "grade": "10",
                        "file": file_path.name
                    }
                ]
            )

            chunk_counter += 1

print(
    f"\nTotal Chunks Added: {chunk_counter}"
)