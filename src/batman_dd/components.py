import streamlit as st
from datetime import date


# ==========================================================
# APP HEADER
# ==========================================================

def render_header():

   pass 

# ==========================================================
# PAGE TITLE
# ==========================================================

def render_page_title(
    title: str,
    subtitle: str = ""
):

    st.markdown(
        f"""
        <div class="page-title">

            <h2>{title}</h2>

            <p>{subtitle}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SECTION TITLE
# ==========================================================

def render_section_title(
    title: str
):

    st.markdown(
        f"""
        <div class="section-title">

            {title}

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# STATUS LEGEND
# ==========================================================

def render_progress_legend():

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            "☐ Not Started"
        )

    with c2:

        st.warning(
            "◐ In Progress"
        )

    with c3:

        st.success(
            "☑ Completed"
        )


# ==========================================================
# SUBJECT TABS
# ==========================================================

def render_subject_tabs():

    tabs = st.tabs(
        [
            "Physics",
            "Chemistry",
            "Biology",
            "Maths"
        ]
    )

    return tabs
# ==========================================================
# SUBJECT CHIP
# ==========================================================

def render_subject_chip(
    subject: str
):

    st.markdown(
        f"""
        <div class="subject-chip">
            {subject}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# CHAPTER HEADER
# ==========================================================

def render_chapter_header(
    chapter_name: str
):

    st.markdown(
        f"""
        <div class="chapter-header">

            📘 {chapter_name}

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# TOPIC ROW
# ==========================================================

def render_topic_row(
    topic_name: str,
    status: str = "not_started",
    completed_on=None
):

    col1, col2, col3 = st.columns(
        [6, 2, 2]
    )

    with col1:

        st.markdown(
            topic_name
        )

    with col2:

        option = st.selectbox(

            "",

            [
                "☐",
                "◐",
                "☑"
            ],

            index={
                "not_started": 0,
                "in_progress": 1,
                "completed": 2
            }.get(
                status,
                0
            ),

            key=f"{topic_name}_status",

            label_visibility="collapsed"
        )

    with col3:

        selected_date = None

        if option == "☑":

            selected_date = st.date_input(

                "",

                value=completed_on
                if completed_on
                else date.today(),

                key=f"{topic_name}_date",

                label_visibility="collapsed"
            )

    return option, selected_date


# ==========================================================
# HORIZONTAL DIVIDER
# ==========================================================

def render_divider():

    st.divider()

# ==========================================================
# INFO CARD
# ==========================================================

def render_info_card(
    title: str,
    value: str = "",
    icon: str = "📌"
):

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-card-icon">
                {icon}
            </div>

            <div class="info-card-title">
                {title}
            </div>

            <div class="info-card-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# EMPTY STATE
# ==========================================================

def render_empty_state(
    message: str
):

    st.markdown(
        f"""
        <div class="empty-state">

            {message}

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SAVE BUTTON
# ==========================================================

def render_save_button():

    return st.button(

        "💾 Save",

        use_container_width=True,

        type="primary"
    )


# ==========================================================
# CANCEL BUTTON
# ==========================================================

def render_cancel_button():

    return st.button(

        "Cancel",

        use_container_width=True
    )


# ==========================================================
# NOTE EDITOR
# ==========================================================

def render_note_editor(

    label: str,

    height: int = 220,

    key: str = "note"

):

    return st.text_area(

        label,

        height=height,

        key=key
    )

# ==========================================================
# CALENDAR DAY CARD
# ==========================================================

def render_calendar_day(
    day: int,
    subjects=None,
    selected=False
):

    if subjects is None:
        subjects = []

    css = "calendar-day"

    if selected:
        css += " selected"

    html = f"""
    <div class="{css}">

        <div class="calendar-date">
            {day}
        </div>

        <div class="calendar-subjects">
    """

    for subject in subjects:

        html += f"""
            <div class="calendar-subject">
                {subject}
            </div>
        """

    html += """
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ==========================================================
# DEBRIEF FIELD
# ==========================================================

def render_debrief_field(
    title,
    key,
    height=120
):

    st.markdown(
        f"#### {title}"
    )

    return st.text_area(
        "",
        key=key,
        height=height,
        label_visibility="collapsed"
    )


# ==========================================================
# SUCCESS BANNER
# ==========================================================

def render_success_banner(
    message
):

    st.success(message)


# ==========================================================
# WARNING BANNER
# ==========================================================

def render_warning_banner(
    message
):

    st.warning(message)


# ==========================================================
# ERROR BANNER
# ==========================================================

def render_error_banner(
    message
):

    st.error(message)

# ==========================================================
# LOADING SPINNER
# ==========================================================

from contextlib import contextmanager


@contextmanager
def render_loading(
    message="Loading..."
):

    with st.spinner(message):
        yield


# ==========================================================
# PAGE FOOTER
# ==========================================================

def render_footer():

    st.divider()

    st.caption(
        "Batman-DD MVP • Selten Technologies"
    )


# ==========================================================
# PAGE SPACER
# ==========================================================

def render_spacer(
    lines=1
):

    for _ in range(lines):

        st.write("")


# ==========================================================
# BADGE
# ==========================================================

def render_badge(
    text,
    color="blue"
):

    st.markdown(
        f"""
        <span class="badge badge-{color}">
            {text}
        </span>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# DATE PICKER
# ==========================================================

def render_date_picker(
    label="Select Date",
    key=None
):

    return st.date_input(
        label,
        value=date.today(),
        key=key
    )


# ==========================================================
# COMING SOON CARD
# ==========================================================

def render_coming_soon(
    title,
    description=""
):

    st.markdown(
        f"""
        <div class="coming-soon-card">

            <h3>{title}</h3>

            <p>{description}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# APP MESSAGE
# ==========================================================

def render_app_message(
    message
):

    st.info(message)


# ==========================================================
# END OF FILE
# ==========================================================