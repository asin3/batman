"""
Batman-DD
Progress Tracker

Phase 1
--------
Curriculum driven UI

Phase 2
--------
Student Progress

Phase 3
--------
Batman Core Integration
"""

from pathlib import Path
import json

from datetime import date
import streamlit as st

from src.batman_dd.core.services.student_progress_service import (

    initialize_student_progress,

    get_topic_status,

    get_topic_date,

    get_completed_count,

    get_progress_percentage,

    update_topic_progress

)
from src.batman_dd.core.services.curriculum_service import get_subject

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

CURRICULUM_DIR = (
    BASE_DIR
    / "data"
    / "Board"
    / "icse"
    / "class10"
    / "curriculum"
)


# ==========================================================
# SUBJECT ORDER (Frozen)
# ==========================================================

SUBJECTS = [
    "Physics",
    "Chemistry",
    "Biology",
    "Maths"
]


# ==========================================================
# LOAD CURRICULUM
# ==========================================================

def load_curriculum(subject_name: str):

    file_name = subject_name.lower() + ".json"

    file_path = CURRICULUM_DIR / file_name

    if not file_path.exists():

        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================================
# PAGE
# ==========================================================

def render_progress_page():

    student_id = st.session_state.user.student_id
    
    st.subheader("📈 Progress")

    physics = load_curriculum("Physics")

    initialize_student_progress(
        student_id,
        physics
    )

    tabs = st.tabs(SUBJECTS)

    for index, tab in enumerate(tabs):

        subject_name = SUBJECTS[index]

        with tab:

            curriculum = get_subject(subject_name)

            if curriculum is None:

                st.info(

                    f"{subject_name} curriculum not available."

                )

                continue

            # ------------------------------------------
            # Flat subjects (Mathematics)
            # ------------------------------------------

            if curriculum.get("chapters"):

                for chapter in curriculum["chapters"]:

                    render_chapter(
                        subject_name,
                        "",
                        chapter,
                        student_id
                    )

            # ------------------------------------------
            # Grouped subjects (Physics/Chemistry/Biology)
            # ------------------------------------------

            elif curriculum.get("groups"):

                for group in curriculum["groups"]:

                    st.markdown(f"#### 📘 {group['title']}")

                    for chapter in group["chapters"]:

                        render_chapter(
                            subject_name,
                            group["title"],
                            chapter,
                            student_id
                        )

            else:

                st.warning("No chapters found.")

# ==========================================================
# CHAPTER
# ==========================================================

def render_chapter(
    subject_name,
    group_name,
    chapter,
    student_id
):

    chapter_name = chapter.get(
        "chapter_name",
        chapter.get("title")
    )

    chapter_id = chapter.get(
        "chapter_id",
        chapter.get("number")
    )

    widget_prefix = (
        f"{subject_name}_{group_name}_{chapter_id}"
    )

    topics = chapter.get("topics", [])

    # ------------------------------------------------------
    # CHAPTER HAS TOPICS (Maths)
    # ------------------------------------------------------

    if topics:

        total_topics = len(topics)

        completed_topics = sum(
            1
            for topic in topics
            if get_topic_status(
                student_id,
                (
                    f"{chapter_id}_{topic}"
                    if isinstance(topic, str)
                    else topic["topic_id"]
                )
            ) == "Completed"
        )

        total_topics = len(topics)

        progress = (
            int(completed_topics * 100 / total_topics)
            if total_topics
            else 0
        )

        header = (
            f"📘 {chapter_name}"
            f" | Topics : {total_topics}"
            f" | Done : {completed_topics}"
            f" | {progress}%"
        )

        with st.expander(header, expanded=False):

            h1, h2, h3 = st.columns(
                [7.5, 1.6, 1.4],
                gap="small"
            )

            with h1:
                st.caption("Topic")

            with h2:
                st.caption("Status")

            with h3:
                st.caption("Completed On")

            st.divider()

            for topic in topics:

                render_topic_row(
                    student_id,
                    chapter_id,
                    topic
                )

    # ------------------------------------------------------
    # CHAPTER HAS NO TOPICS (Physics/Chemistry/Biology)
    # ------------------------------------------------------

    else:

        saved_status = get_topic_status(
            student_id,
            chapter_id
        )

        saved_date = get_topic_date(
            student_id,
            chapter_id
        )

        progress = (
            100
            if saved_status == "Completed"
            else 0
        )

        header = (
            f"📘 {chapter_name}"
            f" | Status : {saved_status}"
            f" | {progress}%"
        )

        with st.expander(header, expanded=False):

            c1, c2 = st.columns([2, 2])

            with c1:

                status = st.selectbox(

                    "Status",

                    [
                        "Not Started",
                        "In Progress",
                        "Completed"
                    ],

                    index=[
                        "Not Started",
                        "In Progress",
                        "Completed"
                    ].index(saved_status),

                    key=f"{widget_prefix}_chapter_status"
                )

            with c2:

                if saved_date:
                    saved_date = date.fromisoformat(saved_date)

                if status == "Completed":

                    completed_on = st.date_input(

                        "Completed On",

                        value=saved_date
                        if saved_date
                        else date.today(),

                        key=f"{widget_prefix}_chapter_date"
                    )

                else:

                    completed_on = None

            current_date = (
                completed_on.isoformat()
                if completed_on
                else None
            )

            if (
                status != saved_status
                or current_date != get_topic_date(student_id, chapter_id)
            ):

                update_topic_progress(
                    student_id,
                    chapter_id,
                    status,
                    completed_on
                )

                st.rerun()

# ==========================================================
# TOPIC ROW
# ==========================================================

def render_topic_row(
    
    student_id,

    chapter_id,

    topic

):

    if isinstance(topic, str):

        topic_id = f"{chapter_id}_{topic}"

        topic_name = topic

    else:

        topic_id = topic["topic_id"]

        topic_name = topic["topic_name"]

    col_topic, col_status, col_date = st.columns(
            [5.5, 1.2, 1.3], gap="small", vertical_alignment="center")

    # ------------------------------------------------------
    # Topic
    # ------------------------------------------------------

    with col_topic:

        st.write(topic_name)

    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    with col_status:

        saved_status = get_topic_status(

            student_id,

            topic_id

        )

        status_options = [

            "Not Started",

            "In Progress",

            "Completed"

        ]

        status = st.selectbox(

            "Status",

            status_options,

            index=status_options.index(

                saved_status

            ),

            key=f"{topic_id}_status",

            label_visibility="collapsed"

        )

    # ------------------------------------------------------
    # Completed On
    # ------------------------------------------------------

    with col_date:

        saved_date = get_topic_date(

            student_id,

            topic_id

        )

        if saved_date:

            saved_date = date.fromisoformat(

                saved_date

            )

        if status == "Completed":

            completed_on = st.date_input(

                "Completed On",

                value=saved_date
                if saved_date
                else date.today(),

                max_value=date.today(),

                key=f"{topic_id}_completed_on",

                label_visibility="collapsed"

            )

        else:

            completed_on = None

    # ------------------------------------------------------
    # SAVE CHANGES
    # ------------------------------------------------------

    saved_status = get_topic_status(
    student_id,
    topic_id
    )

    saved_date = get_topic_date(
        student_id,
        topic_id
    )

    current_date = (
        completed_on.isoformat()
        if completed_on
        else None
    )

    if (
        status != saved_status
        or
        current_date != saved_date
    ):

            update_topic_progress(
                student_id,
                topic_id,
                status,
                completed_on
            )

            st.rerun()

    #
    # ------------------------------------------------------
    # Phase 2 Hooks
    # ------------------------------------------------------
    #
    # Backend integration (not implemented yet):
    #
    # student_progress_service.get_topic_status(
    #     student_id,
    #     topic_id
    # )
    #
    # student_progress_service.save_topic_status(
    #     student_id,
    #     topic_id,
    #     status,
    #     completed_on
    # )
    #
    # Progress calculation:
    #
    # completed_topics
    # total_topics
    # progress_percentage
    #
    # These values will automatically update the
    # chapter header summary.
    #




# ==========================================================
# END OF FILE
# ==========================================================