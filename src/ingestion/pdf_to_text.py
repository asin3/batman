from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler location
POPPLER_PATH = (
    r"F:\batman_student\tools\poppler\poppler-26.02.0\Library\bin"
)

# Input PDF
PDF_FILE = (
    r"F:\batman_student\data\class10\physics\textbook\chapter-1-force.pdf"
)

print("Converting PDF pages to images...")

pages = convert_from_path(
    PDF_FILE,
    first_page=1,
    last_page=2,      # Only first 2 pages for testing
    poppler_path=POPPLER_PATH
)

all_text = ""

for i, page in enumerate(pages, start=1):
    print(f"OCR Page {i}...")

    text = pytesseract.image_to_string(page)

    all_text += f"\n\n===== PAGE {i} =====\n\n"
    all_text += text

print("\nOCR COMPLETE\n")

print(all_text[:5000])

# Save output
output_file = Path("output_chapter1.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"\nSaved to: {output_file}")