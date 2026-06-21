from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# ---------------------------------
# TESSERACT
# ---------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ---------------------------------
# POPPLER
# ---------------------------------

POPPLER_PATH = (
    r"F:\batman_student\tools\poppler\poppler-26.02.0\Library\bin"
)

# ---------------------------------
# PDF FOLDER
# ---------------------------------

PDF_FOLDER = Path(
    "data/class10/physics/textbook"
)

# ---------------------------------
# PROCESS ALL PDFS
# ---------------------------------

for pdf_file in PDF_FOLDER.glob("*.pdf"):

    print(f"\nProcessing: {pdf_file.name}")

    pages = convert_from_path(
        str(pdf_file),
        poppler_path=POPPLER_PATH
    )

    all_text = ""

    for i, page in enumerate(pages, start=1):

        print(f"  OCR Page {i}")

        text = pytesseract.image_to_string(
            page
        )

        all_text += (
            f"\n\n===== PAGE {i} =====\n\n"
        )

        all_text += text

    output_file = (
        pdf_file.parent /
        f"{pdf_file.stem}.txt"
    )

    output_file.write_text(
        all_text,
        encoding="utf-8"
    )

    print(
        f"Saved: {output_file.name}"
    )

print("\nALL PDFS PROCESSED")