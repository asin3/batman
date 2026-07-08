"""
============================================================
Batman DOX Import Engine (BDIE)

Profile Detector

Detects the document profile based on normalized headers.

============================================================
"""

from src.platform.dox.profiles.grouped_curriculum import (
    GroupedCurriculumProfile,
)

from src.platform.dox.profiles.flat_curriculum import (
    FlatCurriculumProfile,
)


class ProfileDetector:

    def __init__(self):

        self.profiles = [

            GroupedCurriculumProfile(),

            FlatCurriculumProfile(),

        ]

    ########################################################
    # DETECT
    ########################################################

    def detect(self, headers):

        for profile in self.profiles:

            if profile.match(headers):

                return profile

        return None


############################################################
# TEST
############################################################

if __name__ == "__main__":

    detector = ProfileDetector()

    print(detector.detect([
        "group",
        "chapter_number",
        "chapter_title",
    ]))