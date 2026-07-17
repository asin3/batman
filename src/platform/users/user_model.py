# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from dataclasses import dataclass


# ---------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------

@dataclass
class User:

    user_id: str = ""

    email: str = ""

    name: str = ""

    provider: str = ""

    status: str = ""

    student_id: str = ""