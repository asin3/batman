"""
============================================================
Batman DOX Import Engine (BDIE)

Document Builder

Purpose:
Builds the universal Document object from
normalized document data.

============================================================
"""

from importlib.resources import path

from src.platform.dox.document_model import (
    Document,
    Subject,
    Group,
    Chapter,
    Topic,
)


class ModelBuilder:

    def __init__(self):

        self.document = Document(
            document_type="curriculum"
        )

    ########################################################
    # ADD SUBJECT
    ########################################################

    def add_subject(self, title: str):

        self.document.subjects.append(
            Subject(title=title)
        )

    ########################################################
    # ADD GROUP
    ########################################################

    def add_group(self, subject_title: str, group_title: str):

        for subject in self.document.subjects:

            if subject.title == subject_title:

                # Avoid duplicates
                for group in subject.groups:

                    if group.title == group_title:
                        return

                subject.groups.append(
                    Group(title=group_title)
                )

                return

    ########################################################
    # ADD CHAPTER
    ########################################################

    def add_chapter(
        self,
        subject_title,
        group_title,
        number,
        title,
        topics,
    ):

        chapter = Chapter(
            number=number,
            title=title,
            full_title=title,
            topics=[
                Topic(title=t)
                for t in topics
            ],
        )

        for subject in self.document.subjects:

            if subject.title != subject_title:
                continue

            ####################################################
            # Flat Curriculum (Mathematics)
            ####################################################

            if group_title is None:

                subject.chapters.append(chapter)
                return

            ####################################################
            # Grouped Curriculum
            ####################################################

            subject.chapters.append(chapter)

            for group in subject.groups:

                if group.title == group_title:

                    group.chapters.append(chapter)
                    return
            
    ########################################################
    # ADD TOPIC
    ########################################################

    def add_topic(
        self,
        subject_title: str,
        group_title: str,
        chapter_number: str,
        topic_title: str,
    ):

        for subject in self.document.subjects:

            if subject.title != subject_title:
                continue

            for group in subject.groups:

                if group.title != group_title:
                    continue

                for chapter in group.chapters:

                    if chapter.number != chapter_number:
                        continue

                    chapter.topics.append(
                        Topic(title=topic_title)
                    )

                    return
    ########################################################
    # BUILD
    ########################################################

    def build(self):

        return self.document


############################################################
# TEST
############################################################

if __name__ == "__main__":

    from src.platform.dox.docx_reader import DocxReader
    from src.platform.dox.parser import DocumentParser

    file_path = input("DOCX Path: ").strip()

    reader = DocxReader(file_path)

    document = reader.read()

    parser = DocumentParser(document)

    context = parser.get_context()

    builder = ModelBuilder()

    for item in context:
        builder.add_subject(item["subject"])

    groups = parser.get_groups()

    for subject, group_list in groups.items():

        for group in group_list:

            builder.add_group(subject, group)

    chapters = parser.get_chapters()

    for subject, chapter_list in chapters.items():

        for chapter in chapter_list:

            group = chapter.get("group")

            # Grouped curriculum (Physics/Chemistry/Biology)
            if group:

                builder.add_chapter(
                    subject,
                    group,
                    chapter["number"],
                    chapter["title"],
                    chapter.get("topics", []),
                )

            # Flat curriculum (Mathematics)
            else:

                builder.add_chapter(
                    subject,
                    None,
                    chapter["number"],
                    chapter["title"],
                    chapter.get("topics", []),
                )

    model = builder.build()

    for subject in model.subjects:

        print()
        print(subject.title)

        # Flat curriculum
        if not subject.groups:

            for chapter in subject.chapters:

                print(
                    f"    {chapter.number}  {chapter.title}"
                )

            continue

        # Grouped curriculum
        for group in subject.groups:

            print(f"  {group.title}")

            for chapter in group.chapters:

                print(
                    f"      {chapter.number}  {chapter.title}"
                )
    print()

    from src.platform.dox.document_exporter import DocumentExporter
    exporter = DocumentExporter()
    document_path = exporter.export(model)

    from src.platform.dox.builders.curriculum_builder import CurriculumBuilder
    builder = CurriculumBuilder()
    curriculum = builder.build(model)
    curriculum_path = builder.export(curriculum)

    from src.platform.dox.builders.progress_builder import ProgressBuilder
    progress_builder = ProgressBuilder()
    progress = progress_builder.build(model)
    progress_path = progress_builder.export(progress)

    from src.platform.dox.builders.schedule_builder import ScheduleBuilder
    schedule_builder = ScheduleBuilder()
    schedule = schedule_builder.build(model)
    schedule_path = schedule_builder.export(schedule)

    print()
    print("Schedule exported:")
    print(schedule_path)

    print()
    print("Progress exported:")
    print(progress_path)

    print()
    print("Curriculum exported:")
    print(curriculum_path)

    print()
    print("Document exported:")
    print(document_path)