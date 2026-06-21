import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import chromadb

from quiz_generator import generate_mcq

db = chromadb.PersistentClient(
    path="./vector_db"
)

collection = db.get_collection(
    "class10_physics"
)

results = collection.query(
    query_texts=["force"],
    n_results=2
)

context = "\n".join(
    results["documents"][0]
)

print(
    generate_mcq(
        context,
        "easy"
    )
)