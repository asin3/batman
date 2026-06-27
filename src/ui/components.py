import streamlit as st


# ---------------------------------
# HEADER
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

    preview = str(value)

    preview = preview.replace(
        "\n",
        " "
    )

    if len(preview) > 80:

        preview = (
            preview[:80]
            + "..."
        )

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {title}"
        )

        st.write(
            preview
        )


# ---------------------------------
# TOPIC STRIP
# ---------------------------------

def render_topic_strip(
    subject,
    topic="Force",
    chapter="Motion",
    grade="10"
):

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"### {topic}"
        )

    with c2:

        st.markdown(
            f"### {chapter}"
        )


# ---------------------------------
# CHAT HISTORY
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