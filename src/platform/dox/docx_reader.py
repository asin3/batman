"""
============================================================
Batman DOX Import Engine (BDIE)

DOCX Reader

Purpose:
Reads a DOCX document and returns the raw python-docx
Document object.

No parsing happens here.

============================================================
"""

from pathlib import Path

from docx import Document


############################################################
# DOCX READER
############################################################

class DocxReader:

    def __init__(self, file_path: str):

        self.file_path = Path(file_path)

    ########################################################
    # READ
    ########################################################

    def read(self):

        if not self.file_path.exists():
            raise FileNotFoundError(self.file_path)

        return Document(self.file_path)


############################################################
# TEST
############################################################

if __name__ == "__main__":

    print("Batman DOX Reader Ready")