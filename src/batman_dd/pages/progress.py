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

from batman_dd.core.services.student_progress_service import (

    initialize_student_progress,

    get_topic_status,

    get_topic_date,

    get_completed_count,

    get_progress_percentage,

    update_topic_progress

)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

CURRICULUM_DIR = (
    BASE_DIR
    / "data"
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

    st.subheader("📈 Progress")

    tabs = st.tabs(SUBJECTS)

    for index, tab in enumerate(tabs):

        subject_name = SUBJECTS[index]

        with tab:

            curriculum = load_curriculum(subject_name)

            if curriculum is None:

                st.info(

                    f"{subject_name} curriculum not available."

                )

                continue

            student_id = "STD001"

            initialize_student_progress(

                student_id,

                curriculum

            )
            #
            # Subject not yet added
            #
            
            chapters = curriculum.get(
                "chapters",
                []
            )

            if not chapters:

                st.warning(
                    "No chapters found."
                )

                continue

            #
            # Render every chapter
            #

            for chapter in chapters:

                render_chapter(
                    chapter
                )

# ==========================================================
# CHAPTER
# ==========================================================

def render_chapter(chapter):

    chapter_name = chapter["chapter_name"]

    topics = chapter["topics"]

    total_topics = len(topics)

    student_id = "STD001"

    completed_topics = get_completed_count(

        student_id,

        topics

    )

    progress = get_progress_percentage(

        student_id,

        topics

    )

    header = (
        f"📘 {chapter_name}"
        f"      |      "
        f"Topics : {total_topics}"
        f"      |      "
        f"Done : {completed_topics}"
        f"      |      "
        f"{progress}%"
    )

    with st.expander(
        header,
        expanded=False
    ):

        h1, h2, h3 = st.columns(
            [7.5, 1.6, 1.4], gap="small"
        )

        with h1:
            st.caption("Topic")

        with h2:
            st.caption("Status")

        with h3:
            st.caption("Completed On")

        st.markdown(
            "<hr style='margin:2px 0 4px 0;border:0;border-top:1px solid #333;'>",
            unsafe_allow_html=True
        )

        for topic in topics:

            render_topic_row(
                chapter["chapter_id"],
                topic
            )

# ==========================================================
# TOPIC ROW
# ==========================================================

def render_topic_row(

    chapter_id,

    topic

):

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

        student_id = "STD001"

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