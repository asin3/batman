from sentence_transformers import SentenceTransformer
import chromadb

QUESTION = "What is translational motion?"

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_collection(
    name="class10_physics"
)

# Convert question into embedding
question_embedding = model.encode(
    QUESTION
).tolist()

# Search
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)

print("\nQUESTION:")
print(QUESTION)

print("\nTOP MATCHES:\n")

for idx, doc in enumerate(results["documents"][0], start=1):
    print("=" * 60)
    print(f"MATCH {idx}")
    print("=" * 60)
    print(doc[:1000])