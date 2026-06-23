import streamlit as st


# ---------------------------------
# APP HEADER
# ---------------------------------

def render_header():

    st.title("🎓 DRONA")

    st.caption(
        "Learn. Think. Understand."
    )


# ---------------------------------
# HOME CARD
# ---------------------------------

def render_home_card(
    title,
    value
):

    with st.container(
        border=True
    ):

        st.subheader(
            title
        )

        st.write(
            value
        )


# ---------------------------------
# TOPIC STRIP
# ---------------------------------

def render_topic_strip(
    subject,
    topic="Not Started",
    chapter="Not Available",
    grade="10"
):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Subject",
            subject
        )

    with col2:
        st.metric(
            "Topic",
            topic
        )

    with col3:
        st.metric(
            "Chapter",
            chapter
        )

    with col4:
        st.metric(
            "Grade",
            grade
        )


# ---------------------------------
# LEARN CHAT
# ---------------------------------

def render_chat_history(
    messages
):

    for msg in messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )