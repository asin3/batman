"""
Batman-DD
Student Progress Service

Owns all student progress.

UI never reads/writes JSON directly.
"""

from pathlib import Path
import json

from datetime import datetime

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]

STUDENT_DIR = (
    PROJECT_ROOT
    / "data"
    / "students"
)


# ==========================================================
# HELPERS
# ==========================================================

def get_progress_file(

    student_id: str

) -> Path:

    student_folder = STUDENT_DIR / student_id

    student_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    return student_folder / "progress.json"


# ==========================================================
# LOAD
# ==========================================================

def load_progress(

    student_id: str

):

    progress_file = get_progress_file(

        student_id

    )

    if not progress_file.exists():

        return {}

    with open(

        progress_file,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)
    
# ==========================================================
# SAVE
# ==========================================================

def save_progress(

    student_id: str,

    progress_data: dict

):

    progress_file = get_progress_file(

        student_id

    )

    with open(

        progress_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            progress_data,

            f,

            indent=4,

            ensure_ascii=False

        )


# ==========================================================
# UPDATE A SINGLE TOPIC
# ==========================================================

def update_topic_progress(

    student_id: str,

    topic_id: str,

    status: str,

    completed_on=None

):

    progress = load_progress(

        student_id

    )

    # ------------------------------------------------------
# Business Rule
# Only completed topics can have a completion date.
# ------------------------------------------------------

    if status != "Completed":

        completed_on = None

    progress[topic_id] = {

        "status": status,

        "completed_on": (
            completed_on.isoformat()
            if completed_on
            else None
        ),

        "last_updated": datetime.now().isoformat(

            timespec="seconds"

        )

    }

    save_progress(

        student_id,

        progress

    )

    return progress

# ==========================================================
# GET TOPIC STATUS
# ==========================================================

def get_topic_status(

    student_id: str,

    topic_id: str

) -> str:

    progress = load_progress(

        student_id

    )

    return progress.get(

        topic_id,

        {}

    ).get(

        "status",

        "Not Started"

    )


# ==========================================================
# GET COMPLETION DATE
# ==========================================================

def get_topic_date(

    student_id: str,

    topic_id: str

):

    progress = load_progress(

        student_id

    )

    return progress.get(

        topic_id,

        {}

    ).get(

        "completed_on",

        None

    )


# ==========================================================
# CHECK IF TOPIC EXISTS
# ==========================================================

def topic_exists(

    student_id: str,

    topic_id: str

) -> bool:

    progress = load_progress(

        student_id

    )

    return topic_id in progress

# ==========================================================
# CHAPTER PROGRESS
# ==========================================================

def get_completed_count(

    student_id: str,

    topics: list

) -> int:

    completed = 0

    progress = load_progress(

        student_id

    )

    for topic in topics:

        topic_id = topic["topic_id"]

        topic_data = progress.get(

            topic_id,

            {}

        )

        if topic_data.get(

            "status"

        ) == "Completed":

            completed += 1

    return completed


# ==========================================================
# CHAPTER PERCENTAGE
# ==========================================================

def get_progress_percentage(

    student_id: str,

    topics: list

) -> int:

    total_topics = len(

        topics

    )

    if total_topics == 0:

        return 0

    completed = get_completed_count(

        student_id,

        topics

    )

    return round(

        (completed / total_topics) * 100

    )

# ==========================================================
# INITIALIZE STUDENT PROGRESS
# ==========================================================

def initialize_student_progress(

    student_id: str,

    curriculum: dict

):

    progress = load_progress(

        student_id

    )

    modified = False

    chapters = curriculum.get(

        "chapters",

        []

    )

    for chapter in chapters:

        topics = chapter.get(

            "topics",

            []

        )

        for topic in topics:

            topic_id = topic["topic_id"]

            if topic_id not in progress:

                progress[topic_id] = {

                    "status": "Not Started",

                    "completed_on": None

                }

                modified = True

    if modified:

        save_progress(

            student_id,

            progress

        )

    return progress


# ==========================================================
# END OF FILE
# ==========================================================