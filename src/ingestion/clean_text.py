from pathlib import Path
import re

input_file = Path("output_chapter1.txt")
output_file = Path("clean_chapter1.txt")

text = input_file.read_text(encoding="utf-8")

# Remove common watermark
text = re.sub(
    r"Downloaded from.*",
    "",
    text,
    flags=re.IGNORECASE
)

# Remove excessive blank lines
text = re.sub(r"\n{3,}", "\n\n", text)

# Remove repeated spaces
text = re.sub(r"[ \t]+", " ", text)

output_file.write_text(text, encoding="utf-8")

print(f"Saved cleaned file: {output_file}")
print("\nPreview:\n")
print(text[:2000])