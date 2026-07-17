from src.platform.dox.profiles.base_profile import BaseProfile


class GroupedCurriculumProfile(BaseProfile):

    REQUIRED = {
        "group",
        "chapter_number",
        "chapter_title",
    }

    def match(self, headers):

        return self.REQUIRED.issubset(set(headers))

    ########################################################
    # GROUPS
    ########################################################

    def get_groups(self, table, headers):

        groups = []

        unit_col = headers.index("group")

        previous = None

        for row in table.rows[1:]:

            value = row.cells[unit_col].text.strip()

            if value:
                previous = value

            if previous and previous not in groups:
                groups.append(previous)

        return groups
    
    ########################################################
    # CHAPTERS
    ########################################################

    def get_chapters(self, table, headers):

        chapters = []

        unit_col = headers.index("group")
        no_col = headers.index("chapter_number")
        title_col = headers.index("chapter_title")

        current_group = None

        for row in table.rows[1:]:

            unit = row.cells[unit_col].text.strip()

            if unit:
                current_group = unit

            chapters.append({

                "group": current_group,
                "number": row.cells[no_col].text.strip(),
                "title": row.cells[title_col].text.strip(),

            })

        return chapters

        ########################################################
        # TOPICS
        ########################################################

        def get_topics(self, table, headers):

            return []