"""
Batman-DD
Student Progress Service

Owns all student progress.

UI never reads/writes JSON directly.
"""

from src.platform.storage.storage_router import StorageRouter

from datetime import datetime
import streamlit as st


# ==========================================================
# PATHS
# ==========================================================




# ==========================================================
# HELPERS
# ==========================================================

# ==========================================================
# STORAGE
# ==========================================================

repository = StorageRouter.get_repository()

# ==========================================================
# CACHE
# ==========================================================

def get_progress_cache(student_id: str):

    cache_key = f"progress_{student_id}"

    if cache_key not in st.session_state:

        path = f"students/{student_id}/progress.json"

        if repository.exists(path):

            st.session_state[cache_key] = repository.read_json(path)

        else:

            st.session_state[cache_key] = {}

    return st.session_state[cache_key]


# ==========================================================
# LOAD
# ==========================================================

def load_progress(student_id: str):

    return get_progress_cache(student_id)
    
# ==========================================================
# SAVE
# ==========================================================

def save_progress(student_id: str, progress_data: dict):

    path = f"students/{student_id}/progress.json"

    repository.write_json(
        path,
        progress_data
    )

    cache_key = f"progress_{student_id}"

    st.session_state[cache_key] = progress_data

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