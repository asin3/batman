"""
============================================================

Batman Student

Knowledge Repository

Purpose

Single access layer for all Batman Knowledge Assets.

Downstream components must never open JSON files directly.

============================================================
"""

import json

from pathlib import Path


class KnowledgeRepository:

    def __init__(self, document_folder: Path):

        self.document_folder = document_folder

    def load_document(self):

        with open(

            self.document_folder / "document.json",

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    def load_chunks(self):

        with open(

            self.document_folder / "chunks.json",

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    def load_figures(self):

        with open(

            self.document_folder / "figure_manifest.json",

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    def load_manifest(self):

        with open(

            self.document_folder / "manifest.json",

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    def load_all(self):

        return {

            "document": self.load_document(),

            "chunks": self.load_chunks(),

            "figures": self.load_figures(),

            "manifest": self.load_manifest()

        }


if __name__ == "__main__":

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DOCUMENT_FOLDER = (

        PROJECT_ROOT

        / "data"

        / "class10"

        / "biology"

        / "textbook"

        / "staging"

        / "DOC000013"

    )

    repo = KnowledgeRepository(

        DOCUMENT_FOLDER

    )

    assets = repo.load_all()

    print()

    print("=" * 60)

    print("KNOWLEDGE REPOSITORY")

    print("=" * 60)

    print()

    print(f"Document : {'OK' if assets['document'] else 'FAIL'}")

    print(f"Chunks   : {len(assets['chunks'])}")

    print(f"Figures  : {len(assets['figures'])}")

    print(f"Manifest : {'OK' if assets['manifest'] else 'FAIL'}")

    print()

    print("READY")