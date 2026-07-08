"""
============================================================
Batman DOX Import Engine (BDIE)

Base Profile

Every document profile derives from this class.

============================================================
"""


class BaseProfile:

    ########################################################
    # MATCH
    ########################################################

    def match(self, headers):

        raise NotImplementedError

    ########################################################
    # PARSE
    ########################################################

    def parse(self, table, headers):

        return {

            "groups": self.get_groups(
                table,
                headers,
            ),

            "chapters": self.get_chapters(
                table,
                headers,
            ),

            "topics": self.get_topics(
                table,
                headers,
            ),
        }

    ########################################################
    # GROUPS
    ########################################################

    def get_groups(self, table, headers):

        return []

    ########################################################
    # CHAPTERS
    ########################################################

    def get_chapters(self, table, headers):

        return []

    ########################################################
    # TOPICS
    ########################################################

    def get_topics(self, table, headers):

        return []

    ########################################################
    # NAME
    ########################################################

    @property
    def name(self):

        return self.__class__.__name__