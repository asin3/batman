from pypdf import PdfReader

pdf_path = r"data\class10\physics\textbook\chapter-1-force.pdf"

reader = PdfReader(pdf_path)

print(f"Pages: {len(reader.pages)}")

for i in range(3):
    print(f"\n===== PAGE {i+1} =====")

    text = reader.pages[i].extract_text()

    print(text[:1000] if text else "No text found")