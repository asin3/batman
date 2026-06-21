from pathlib import Path

input_file = Path("clean_chapter1.txt")

text = input_file.read_text(encoding="utf-8")

CHUNK_SIZE = 1000

chunks = []

for i in range(0, len(text), CHUNK_SIZE):
    chunk = text[i:i + CHUNK_SIZE]
    chunks.append(chunk)

print(f"Total Chunks: {len(chunks)}")

for idx, chunk in enumerate(chunks[:3], start=1):
    print("\n" + "=" * 50)
    print(f"CHUNK {idx}")
    print("=" * 50)
    print(chunk[:500])