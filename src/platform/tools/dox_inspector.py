"""
============================================================
Batman DOX Import Engine (BDIE)

DOX Inspector

Purpose:
Loads any DOCX document and displays a structural summary.

============================================================
"""

from pathlib import Path

from src.platform.dox.docx_reader import DocxReader
from src.platform.dox.parser import DocumentParser


############################################################
# INSPECT
############################################################

def inspect_document(file_path: str):

    reader = DocxReader(file_path)

    document = reader.read()

    parser = DocumentParser(document)

    parser.summary()


############################################################
# TEST
############################################################

if __name__ == "__main__":

    docx_file = input("DOCX Path: ").strip()

    inspect_document(docx_file)