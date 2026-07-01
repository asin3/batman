"""
Batman-DD
Scheduling Page

Monthly study planner.

UI only.

Business logic lives in
student_schedule_service.py
"""

from datetime import date
import calendar

import streamlit as st

from batman_dd.core.services.student_schedule_service import (

    initialize_student_schedule,

    get_month_schedule,

    get_day_schedule,

    update_day_schedule

)


# ==========================================================
# CONSTANTS
# ==========================================================

STUDENT_ID = "STD001"

WEEKDAYS = [

    "Mon",

    "Tue",

    "Wed",

    "Thu",

    "Fri",

    "Sat",

    "Sun"

]


# ==========================================================
# PAGE
# ==========================================================

def render_scheduling_page():

    initialize_student_schedule(

        STUDENT_ID

    )

    #
    # Month State
    #

    if "schedule_year" not in st.session_state:

        st.session_state.schedule_year = date.today().year

    if "schedule_month" not in st.session_state:

        st.session_state.schedule_month = date.today().month

    render_month()

# ==========================================================
# MONTH RENDERER
# ==========================================================

def render_month():

    year = st.session_state.schedule_year

    month = st.session_state.schedule_month

    month_data = get_month_schedule(

        STUDENT_ID,

        year,

        month

    )

    # ------------------------------------------------------
    # Month Navigation
    # ------------------------------------------------------

    left, center, right = st.columns(

        [1, 6, 1]

    )

    with left:

        if st.button(

            "◀",

            use_container_width=True,

            key="prev_month"

        ):

            if month == 1:

                st.session_state.schedule_month = 12

                st.session_state.schedule_year -= 1

            else:

                st.session_state.schedule_month -= 1

            st.rerun()

    with center:

        st.markdown(

            f"<h3 style='text-align:center;'>"

            f"{calendar.month_name[month]} {year}"

            f"</h3>",

            unsafe_allow_html=True

        )

    with right:

        if st.button(

            "▶",

            use_container_width=True,

            key="next_month"

        ):

            if month == 12:

                st.session_state.schedule_month = 1

                st.session_state.schedule_year += 1

            else:

                st.session_state.schedule_month += 1

            st.rerun()

    # ------------------------------------------------------
    # Weekday Header
    # ------------------------------------------------------

    weekday_columns = st.columns(7)

    for index, weekday in enumerate(WEEKDAYS):

        with weekday_columns[index]:

            st.markdown(

                f"<div style='text-align:center;"

                f"font-weight:600;'>"

                f"{weekday}"

                f"</div>",

                unsafe_allow_html=True

            )

    # ------------------------------------------------------
    # Calendar Grid
    # ------------------------------------------------------

    cal = calendar.Calendar(firstweekday=0)

    month_days = cal.monthdayscalendar(

        year,

        month

    )

    today = date.today()

    for week in month_days:

        day_columns = st.columns(

            7,

            gap="small"

        )

        for col_index, day in enumerate(week):

            with day_columns[col_index]:

                #
                # Empty cell
                #

                if day == 0:

                    st.markdown(

                        "<div style='height:120px;'></div>",

                        unsafe_allow_html=True

                    )

                    continue

                #
                # Date String
                #

                schedule_date = (

                    f"{year:04d}"

                    f"-"

                    f"{month:02d}"

                    f"-"

                    f"{day:02d}"

                )

                #
                # Today Highlight
                #

                is_today = (

                    today.year == year

                    and

                    today.month == month

                    and

                    today.day == day

                )

                border = (

                    "#2E86FF"

                    if is_today

                    else "#444444"

                )

                                #
                # Subjects planned for this day
                #

                day_schedule = month_data.get(

                    schedule_date,

                    {}

                )

                subjects = day_schedule.get(

                    "subjects",

                    []

                )

                                #
                # Edit Schedule
                #

                st.markdown(

                    '<div class="schedule-day-wrapper">',

                    unsafe_allow_html=True

                )

                with st.popover(

                    "✏️"

                ):

                    st.caption(

                        schedule_date

                    )

                    subject_options = [

                        "",

                        "Physics",

                        "Chemistry",

                        "Biology",

                        "Maths"

                    ]

                    selected_subjects = []

                    #
                    # Four slots
                    #

                    for slot in range(4):

                        default_subject = ""

                        if slot < len(subjects):

                            default_subject = subjects[slot][

                                "subject"

                            ]

                        value = st.selectbox(

                            f"Subject {slot+1}",

                            subject_options,

                            index=subject_options.index(

                                default_subject

                            ),

                            key=f"{schedule_date}_{slot}"

                        )

                        if value:

                            selected_subjects.append(

                                {

                                    "slot": slot + 1,

                                    "subject": value

                                }

                            )

                    #
                    # Save Only When Changed
                    #

                    saved_subjects = get_day_schedule(

                        STUDENT_ID,

                        schedule_date

                    )

                    if selected_subjects != saved_subjects:

                        update_day_schedule(

                            STUDENT_ID,

                            schedule_date,

                            selected_subjects

                        )

                        st.success(

                            "Saved",

                            icon="✅"

                        )

                        st.rerun()

                #
                # Day Card
                #

                card_html = f"""
<div style="
border:2px solid {border};
border-radius:8px;
padding:8px;
min-height:130px;
">

<div style="
font-weight:700;
font-size:16px;
margin-bottom:8px;
">
{day}
</div>
"""

                #
                # Planned subjects
                #

                for item in subjects:

                    card_html += f"""
<div style="
font-size:13px;
padding-left:6px;
margin-bottom:4px;
">
• {item['subject']}
</div>
"""

                card_html += "</div>"

                st.markdown(

                    card_html,

                    unsafe_allow_html=True

                )

                st.markdown(

                    '</div>',

                    unsafe_allow_html=True

                )
