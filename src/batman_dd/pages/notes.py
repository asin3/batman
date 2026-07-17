import streamlit as st

from src.batman_dd.core.services.student_notes_service import (
    load_notes,
    save_note,
    delete_notes,
)


##########################################
# Notes Page
##########################################

def render_notes_page():

    st.title("📝 Quick Notes")

    student_id = st.session_state.student_id

    ##########################################
    # Clear Form After Save
    ##########################################

    if st.query_params.get("clear") == "1":

        st.session_state["note_title"] = ""
        st.session_state["note_text"] = ""

        del st.query_params["clear"]

    ##########################################
    # New Note
    ##########################################

    title = st.text_input(
        "Title",
        key="note_title"
    )

    note = st.text_area(
        "Note",
        key="note_text"
    )

    if st.button(
        "Save Note",
        use_container_width=True
    ):

        if note.strip():

            save_note(
                student_id,
                title,
                note
            )

            st.query_params["clear"] = "1"
            st.rerun()

    st.divider()

    ##########################################
    # Load Notes
    ##########################################

    notes = load_notes(student_id)

    if not notes:

        st.info("No notes yet.")
        return

    ##########################################
    # Bulk Delete Toolbar
    ##########################################

    col1, col2 = st.columns([1, 2])

    with col1:

        select_all = st.checkbox(
            "Select All",
            key="select_all_notes"
        )

    with col2:

        delete_clicked = st.button(
            "🗑 Delete Selected",
            use_container_width=True
        )

    ##########################################
    # Notes List
    ##########################################

    selected_ids = []

    for item in notes:

        col_check, col_note = st.columns([1, 12])

        with col_check:

            checked = st.checkbox(
                "Select",
                value=select_all,
                key=f"note_{item['id']}",
                label_visibility="collapsed"
            )

        if checked:
            selected_ids.append(item["id"])

        with col_note:

            with st.expander(
                item["title"] or "Untitled"
            ):

                st.write(item["note"])

    ##########################################
    # Delete Confirmation
    ##########################################

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if delete_clicked:

        if not selected_ids:

            st.warning("Please select at least one note.")

        else:

            st.session_state.confirm_delete = True
            st.session_state.selected_note_ids = selected_ids
            st.rerun()

    if st.session_state.confirm_delete:

        @st.dialog("⚠ Delete Notes")
        def confirm_delete_dialog():

            st.warning(
                "The selected notes will be permanently deleted.\n\n"
                "This action cannot be undone."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🗑 Delete Permanently",
                    type="primary",
                    use_container_width=True,
                ):

                    delete_notes(
                        student_id,
                        st.session_state.selected_note_ids
                    )

                    st.session_state.confirm_delete = False
                    st.session_state.selected_note_ids = []

                    st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                ):

                    st.session_state.confirm_delete = False
                    st.session_state.selected_note_ids = []

                    st.rerun()

        confirm_delete_dialog()