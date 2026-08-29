"""
============================================================

Batman Schedule Builder

Document
    ↓
schedule.json

============================================================
"""

import json
from pathlib import Path


class ScheduleBuilder:

    def build(self, document):

        schedule = {
            "subjects": []
        }

        for subject in document.subjects:

            subject_data = {
                "title": subject.title,
                "enabled": True,
                "target_date": None,
                "groups": [],
                "chapters": []
            }

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
                            "planned_date": None,
                            "completed": False
                        })

                    subject_data["groups"].append(group_data)

            else:

                for chapter in subject.chapters:

                    subject_data["chapters"].append({
                        "number": chapter.number,
                        "title": chapter.title,
                        "planned_date": None,
                        "completed": False
                    })

            schedule["subjects"].append(subject_data)

        return schedule

    def export(self, schedule):

        output = (
            Path("data")
            / "Board"
            / "icse"
            / "class10"
            / "curriculum"
            / "output"
            / "schedule.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output, "w", encoding="utf-8") as file:

            json.dump(
                schedule,
                file,
                indent=4,
                ensure_ascii=False
            )

        return output