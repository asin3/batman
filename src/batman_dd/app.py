import streamlit as st
from pathlib import Path
import sys

# ==========================================================
# PATH
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# ==========================================================
# COMPONENTS
# ==========================================================

from batman_dd.components import (
    render_header,
    render_footer
)

# ==========================================================
# PAGES
# ==========================================================

from batman_dd.pages.progress import render_progress_page
from batman_dd.pages.scheduling import render_scheduling_page
from batman_dd.pages.debrief import render_debrief_page
from batman_dd.pages.notes import render_notes_page

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Batman-DD",
    page_icon="🦇",
    layout="wide"
)

st.set_option("client.showSidebarNavigation", False)

# ==========================================================
# LOAD CSS
# ==========================================================

css_path = (
    Path(__file__).parent /
    "styles.css"
)

if css_path.exists():

    with open(
        css_path,
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================================================
# SESSION STATE
# ==========================================================

if "current_page" not in st.session_state:

    st.session_state.current_page = "Progress"

if "selected_subject" not in st.session_state:

    st.session_state.selected_subject = "Physics"

if "student_id" not in st.session_state:

    st.session_state.student_id = "STD001"

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="margin-bottom:0;">
            🦇 BATMAN-DD
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Daily Discipline"
    )

    st.divider()

    if st.button(
        "📈 Progress",
        use_container_width=True
    ):

        st.session_state.current_page = "Progress"

        st.rerun()

    if st.button(
        "📅 Scheduling",
        use_container_width=True
    ):

        st.session_state.current_page = "Scheduling"

        st.rerun()

    if st.button(
        "📝 Daily Debrief",
        use_container_width=True
    ):

        st.session_state.current_page = "Daily Debrief"

        st.rerun()

    if st.button(
        "📒 Quick Notes",
        use_container_width=True
    ):

        st.session_state.current_page = "Quick Notes"

        st.rerun()

    st.divider()

    st.markdown(
        "**Student**"
    )

    st.info(
        st.session_state.student_id
    )

# ==========================================================
# HEADER
# ==========================================================

render_header()

# ==========================================================
# PAGE ROUTER
# ==========================================================

page = st.session_state.current_page

# ----------------------------------------------------------
# PROGRESS
# ----------------------------------------------------------

if page == "Progress":

    render_progress_page()

# ----------------------------------------------------------
# SCHEDULING
# ----------------------------------------------------------

elif page == "Scheduling":

    render_scheduling_page()

# ----------------------------------------------------------
# DAILY DEBRIEF
# ----------------------------------------------------------

elif page == "Daily Debrief":

    render_debrief_page()

# ----------------------------------------------------------
# QUICK NOTES
# ----------------------------------------------------------

elif page == "Quick Notes":

    render_notes_page()

# ----------------------------------------------------------
# UNKNOWN
# ----------------------------------------------------------

else:

    st.warning(
        "Unknown page selected."
    )

# ==========================================================
# RESERVED AREA
# ==========================================================

#
# Future Features
#
# • Notifications
# • Today's Tasks
# • AI Suggestions
# • Revision Reminder
# • Weak Topics
# • Study Streak
#
# These widgets will be rendered
# below the selected page in
# later phases.
#

# ==========================================================
# FOOTER
# ==========================================================

render_footer()

# ==========================================================
# DEBUG (MVP)
# ==========================================================

# Keep disabled.
# Useful while integrating with Batman Core.

DEBUG = False

if DEBUG:

    with st.expander(
        "Debug Information"
    ):

        st.write(
            "Student ID:",
            st.session_state.student_id
        )

        st.write(
            "Current Page:",
            st.session_state.current_page
        )

        st.write(
            "Selected Subject:",
            st.session_state.selected_subject
        )

        st.write(
            st.session_state
        )


# ==========================================================
# FUTURE INTEGRATION NOTES
# ==========================================================

#
# Phase 1
# --------
# Progress
# Scheduling
# Daily Debrief
# Quick Notes
#
# Phase 2
# --------
# JSON Storage
# Batman Core Integration
#
# Phase 3
# --------
# Google Authentication
# Multi Student Support
# AI Planner
# Revision Engine
#
# ==========================================================
# END OF FILE
# ==========================================================