"""
============================================================
Batman DOX Import Engine (BDIE)

Document Exporter

Exports the generic Document model to JSON.

============================================================
"""

import json
from pathlib import Path
from dataclasses import asdict


class DocumentExporter:

    def export(self, document):

        output_path = (
            Path("data")
            / "Board"
            / "icse"
            / "class10"
            / "curriculum"
            / "output"
            / "document.json"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(document),
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_path