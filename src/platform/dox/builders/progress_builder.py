"""
============================================================

Batman Progress Builder

Document
    ↓
progress.json

============================================================
"""

import json
from pathlib import Path


class ProgressBuilder:

    def build(self, document):

        progress = {
            "subjects": []
        }

        for subject in document.subjects:

            subject_data = {
                "title": subject.title,
                "groups": [],
                "chapters": []
            }

            ####################################################
            # Flat Curriculum
            ####################################################

            if not subject.groups:

                for chapter in subject.chapters:

                    chapter_data = {

                        "number": chapter.number,
                        "title": chapter.title,

                        "status": "not_started",
                        "completion": 0,

                        "topics": []

                    }

                    for topic in chapter.topics:

                        chapter_data["topics"].append({

                            "title": topic.title,

                            "status": "not_started"

                        })

                    subject_data["chapters"].append(
                        chapter_data
                    )

            ####################################################
            # Grouped Curriculum
            ####################################################

            else:

                for group in subject.groups:

                    group_data = {

                        "title": group.title,

                        "chapters": []

                    }

                    for chapter in group.chapters:

                        chapter_data = {

                            "number": chapter.number,
                            "title": chapter.title,

                            "status": "not_started",
                            "completion": 0,

                            "topics": []

                        }

                        for topic in chapter.topics:

                            chapter_data["topics"].append({

                                "title": topic.title,

                                "status": "not_started"

                            })

                        group_data["chapters"].append(
                            chapter_data
                        )

                    subject_data["groups"].append(
                        group_data
                    )

            progress["subjects"].append(
                subject_data
            )

        return progress

    ########################################################

    def export(self, progress):

        output = (
            Path("data")
            / "Board"
            / "icse"
            / "class10"
            / "curriculum"
            / "output"
            / "progress.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                progress,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output