"""
============================================================

Batman Curriculum Builder

Generic Document
        ↓
Batman curriculum.json

============================================================
"""

import json
from pathlib import Path


class CurriculumBuilder:

    def build(self, document):

        curriculum = {
            "subjects": []
        }

        for subject in document.subjects:

            subject_data = {
                "title": subject.title,
                "groups": [],
                "chapters": []
            }

            ####################################################
            # Grouped curriculum
            ####################################################

            if subject.groups:

                for group in subject.groups:

                    group_data = {
                        "title": group.title,
                        "chapters": []
                    }

                    for chapter in group.chapters:

                        group_data["chapters"].append({

                            "number": chapter.number,
                            "title": chapter.title,
                            "topics": [
                                topic.title
                                for topic in chapter.topics
                            ],

                        })

                    subject_data["groups"].append(group_data)

            ####################################################
            # Flat curriculum
            ####################################################

            else:

                for chapter in subject.chapters:

                    subject_data["chapters"].append({

                        "number": chapter.number,
                        "title": chapter.title,
                        "topics": [
                            topic.title
                            for topic in chapter.topics
                        ],

                    })

            curriculum["subjects"].append(subject_data)

        return curriculum

    ########################################################

    def export(self, curriculum):

        output = (
            Path("data")
            / "class10"
            / "curriculum"
            / "output"
            / "curriculum.json"
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
                curriculum,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output