# =========================================================
# BATMAN PLATFORM
# Student Repository
# =========================================================

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from pathlib import Path
import json


# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------

STUDENTS_PATH = Path("data/students")


# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def generate_student_id() -> str:

    STUDENTS_PATH.mkdir(parents=True, exist_ok=True)

    folders = [

        folder.name

        for folder in STUDENTS_PATH.iterdir()

        if folder.is_dir()

    ]

    if not folders:

        return "STD000001"

    numbers = [

        int(folder.replace("STD", ""))

        for folder in folders

    ]

    return f"STD{max(numbers)+1:06d}"

# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def assign_student_id(user_id: str) -> str:

    profile_path = Path("data/users") / user_id / "profile.json"

    with open(profile_path, "r") as file:

        profile = json.load(file)

    if profile["student_id"]:

        return profile["student_id"]

    student_id = generate_student_id()

    profile["student_id"] = student_id

    with open(profile_path, "w") as file:

        json.dump(profile, file, indent=4)

    return student_id

# ---------------------------------------------------------
# PUBLIC FUNCTIONS 2
# ---------------------------------------------------------

def create_student_workspace(student_id: str) -> None:

    student_path = STUDENTS_PATH / student_id

    student_path.mkdir(parents=True, exist_ok=True)

    files = [

        "history.json",
        "learning_state.json",
        "progress.json",
        "schedule.json",

    ]

    for filename in files:

        file_path = student_path / filename

        if not file_path.exists():

            file_path.write_text("{}")


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    create_student_workspace("STD000003")

    print("STD000003")