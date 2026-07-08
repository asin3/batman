import streamlit as st

from src.batman_dd.core.services.student_notes_service import (
    load_notes,
    save_note,
)


def render_notes_page():

    st.title("📝 Quick Notes")

    student_id = st.session_state.student_id

    if st.query_params.get("clear") == "1":

        st.session_state["note_title"] = ""
        st.session_state["note_text"] = ""

        del st.query_params["clear"]

    title = st.text_input(
        "Title",
        key="note_title"
    )

    note = st.text_area(
        "Note",
        key="note_text"
    )

    if st.button("Save Note"):

        if note.strip():

            save_note(
                student_id,
                title,
                note
            )

            st.query_params["clear"] = "1"

            st.rerun()

    st.divider()

    notes = load_notes(student_id)

    if not notes:

        st.info("No notes yet.")

        return

    for item in notes:

        with st.expander(
            item["title"] or "Untitled"
        ):

            st.write(item["note"])