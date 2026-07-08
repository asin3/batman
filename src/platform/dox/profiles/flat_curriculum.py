from src.platform.dox.profiles.base_profile import BaseProfile


class FlatCurriculumProfile(BaseProfile):

    REQUIRED = {
        "chapter_number",
        "chapter_title",
        "topics",
    }

    def match(self, headers):

        return self.REQUIRED.issubset(set(headers))

    ########################################################
    # CHAPTERS
    ########################################################

    def get_chapters(self, table, headers):

        chapters = []

        no_col = headers.index("chapter_number")
        title_col = headers.index("chapter_title")
        topic_col = headers.index("topics")

        current = None

        for row in table.rows[1:]:

            number = row.cells[no_col].text.strip()
            title = row.cells[title_col].text.strip()
            topic = row.cells[topic_col].text.strip()

            # New chapter
            if number:

                current = {

                    "number": number,
                    "title": title,
                    "topics": []

                }

                if topic:
                    current["topics"].append(topic)

                chapters.append(current)

            # Continuation row
            elif current and topic:

                current["topics"].append(topic)

        return chapters
    
    ########################################################
    # GROUPS
    ########################################################

    def get_groups(self, table, headers):

            return []

    ########################################################
    # TOPICS
    ########################################################

    def get_topics(self, table, headers):

        topics = []

        for chapter in self.get_chapters(table, headers):

            topics.append({

                "chapter": chapter["number"],

                "topics": chapter["topics"]

            })

        return topics