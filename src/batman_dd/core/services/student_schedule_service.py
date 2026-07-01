"""
Batman-DD
Student Schedule Service

Owns all student scheduling.

UI never reads/writes JSON directly.
"""

from pathlib import Path
from datetime import datetime

import json


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

def get_schedule_file(

    student_id: str

) -> Path:

    student_folder = STUDENT_DIR / student_id

    student_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    return student_folder / "schedule.json"


# ==========================================================
# LOAD
# ==========================================================

def load_schedule(

    student_id: str

):

    schedule_file = get_schedule_file(

        student_id

    )

    if not schedule_file.exists():

        return {}

    with open(

        schedule_file,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)
    
# ==========================================================
# SAVE
# ==========================================================

def save_schedule(

    student_id: str,

    schedule_data: dict

):

    schedule_file = get_schedule_file(

        student_id

    )

    with open(

        schedule_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            schedule_data,

            f,

            indent=4,

            ensure_ascii=False

        )


# ==========================================================
# UPDATE A SINGLE DAY
# ==========================================================

def update_day_schedule(

    student_id: str,

    schedule_date: str,

    subjects: list

):

    #
    # Business Rule
    # Maximum 4 subjects per day.
    #

    if len(subjects) > 4:

        raise ValueError(

            "Maximum 4 subjects allowed per day."

        )

    #
    # Remove blank subjects.
    #

    clean_subjects = []

    slot = 1

    for item in subjects:

        subject = item.get(

            "subject",

            ""

        ).strip()

        if subject:

            clean_subjects.append(

                {

                    "slot": slot,

                    "subject": subject

                }

            )

            slot += 1

    subjects = clean_subjects

    schedule = load_schedule(

        student_id

    )

    schedule[schedule_date] = {

        "subjects": subjects,

        "last_updated": datetime.now().isoformat(

            timespec="seconds"

        )

    }

    save_schedule(

        student_id,

        schedule

    )

    return schedule

# ==========================================================
# GET SCHEDULE FOR A DAY
# ==========================================================

def get_day_schedule(

    student_id: str,

    schedule_date: str

) -> list:

    schedule = load_schedule(

        student_id

    )

    day = schedule.get(

        schedule_date,

        {}

    )

    return day.get(

        "subjects",

        []

    )


# ==========================================================
# GET SUBJECT COUNT
# ==========================================================

def get_subject_count(

    student_id: str,

    schedule_date: str

) -> int:

    subjects = get_day_schedule(

        student_id,

        schedule_date

    )

    return len(

        subjects

    )


# ==========================================================
# CHECK IF DAY HAS A SCHEDULE
# ==========================================================

def day_has_schedule(

    student_id: str,

    schedule_date: str

) -> bool:

    return get_subject_count(

        student_id,

        schedule_date

    ) > 0


# ==========================================================
# GET LAST UPDATED
# ==========================================================

def get_last_updated(

    student_id: str,

    schedule_date: str

):

    schedule = load_schedule(

        student_id

    )

    day = schedule.get(

        schedule_date,

        {}

    )

    return day.get(

        "last_updated",

        None

    )

# ==========================================================
# GET MONTH SCHEDULE
# ==========================================================

def get_month_schedule(

    student_id: str,

    year: int,

    month: int

) -> dict:

    """
    Returns all scheduled days
    for the requested month.

    Example:

    {
        "2026-07-02": {...},
        "2026-07-05": {...}
    }
    """

    schedule = load_schedule(

        student_id

    )

    month_prefix = (

        f"{year:04d}"

        f"-"

        f"{month:02d}"

    )

    month_schedule = {}

    for schedule_date, day_data in schedule.items():

        if schedule_date.startswith(

            month_prefix

        ):

            month_schedule[

                schedule_date

            ] = day_data

    return month_schedule


# ==========================================================
# GET ALL SCHEDULED DAYS
# ==========================================================

def get_scheduled_days(

    student_id: str,

    year: int,

    month: int

) -> list:

    """
    Returns a sorted list of dates
    that contain schedule data.
    """

    month_schedule = get_month_schedule(

        student_id,

        year,

        month

    )

    return sorted(

        month_schedule.keys()

    )

# ==========================================================
# INITIALIZE STUDENT SCHEDULE
# ==========================================================

def initialize_student_schedule(

    student_id: str

):

    """
    Creates an empty schedule.json for a
    new student if it does not already exist.
    """

    schedule_file = get_schedule_file(

        student_id

    )

    if schedule_file.exists():

        return load_schedule(

            student_id

        )

    save_schedule(

        student_id,

        {}

    )

    return {}


# ==========================================================
# VALIDATION
# ==========================================================

VALID_SUBJECTS = [

    "Physics",

    "Chemistry",

    "Biology",

    "Maths"

]


def validate_subjects(

    subjects: list

) -> bool:

    """
    Validates the subject list before saving.
    """

    if len(subjects) > 4:

        return False

    for item in subjects:

        subject = item.get(

            "subject",

            ""

        ).strip()

        if subject and subject not in VALID_SUBJECTS:

            return False

    return True


# ==========================================================
# CLEAR A DAY
# ==========================================================

def clear_day_schedule(

    student_id: str,

    schedule_date: str

):

    schedule = load_schedule(

        student_id

    )

    if schedule_date in schedule:

        del schedule[

            schedule_date

        ]

        save_schedule(

            student_id,

            schedule

        )


# ==========================================================
# END OF FILE
# ==========================================================