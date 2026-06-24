import streamlit as st
import sys
import json
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from batman_engine import ask_batman

from ui.components import (
    render_header,
    render_home_card,
    render_topic_strip,
    render_chat_history
)

# ---------------------------------
# PAGE
# ---------------------------------

st.set_page_config(
    page_title="DRONA",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------
# STATE
# ---------------------------------

if "page" not in st.session_state:
    st.session_state.page = "HOME"

if "subject" not in st.session_state:
    st.session_state.subject = "Physics"

if "learn_messages" not in st.session_state:

    st.session_state.learn_messages = [
        {
            "role": "assistant",
            "content": "Hello. I am Drona. What would you like to learn today?"
        }
    ]

if "superchat_messages" not in st.session_state:

    st.session_state.superchat_messages = [
        {
            "role": "assistant",
            "content": "Hello. I am Drona. How can I help you today?"
        }
    ]

# ---------------------------------
# HISTORY
# ---------------------------------

def load_history():

    try:

        history_path = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "students"
            / "STD001"
            / "history.json"
        )

        with open(
            history_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


def get_last_learning():

    history = load_history()

    subject = "Unknown"
    topic = "Not Started"

    for item in reversed(history):

        if item.get("mode") == "LEARN":

            subject = item.get(
                "subject",
                "Unknown"
            )

            topic = item.get(
                "content",
                "Not Started"
            )

            break

    return (
        f"{subject} → "
        f"{topic}"
    )


def get_last_chat():

    history = load_history()

    for item in reversed(history):

        if item.get("mode") == "SUPER_CHAT":

            return item.get(
                "content",
                ""
            )

    return "No discussion yet"

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.markdown("## 🎓 DRONA")

    st.caption(
        "Learn. Think. Understand."
    )

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.session_state.page = "HOME"
        st.rerun()

    st.markdown("### 📚 Learn")

    if st.button(
        "   Physics",
        use_container_width=True
    ):
        st.session_state.subject = "Physics"
        st.session_state.page = "WORKSPACE"
        st.rerun()

    if st.button(
        "   Chemistry",
        use_container_width=True
    ):
        st.session_state.subject = "Chemistry"
        st.session_state.page = "WORKSPACE"
        st.rerun()

    if st.button(
        "   Maths",
        use_container_width=True
    ):
        st.session_state.subject = "Maths"
        st.session_state.page = "WORKSPACE"
        st.rerun()

    if st.button(
        "   Biology",
        use_container_width=True
    ):
        st.session_state.subject = "Biology"
        st.session_state.page = "WORKSPACE"
        st.rerun()

    st.divider()

    if st.button(
        "💬 Super Chat",
        use_container_width=True
    ):
        st.session_state.page = "SUPER_CHAT"
        st.rerun()

    st.button(
        "📝 Quiz (Coming Soon)",
        disabled=True,
        use_container_width=True
    )

    st.button(
        "📈 Progress (Coming Soon)",
        disabled=True,
        use_container_width=True
    )

# ---------------------------------
# HEADER
# ---------------------------------

render_header()

# ---------------------------------
# HOME
# ---------------------------------

if st.session_state.page == "HOME":

    st.subheader("Welcome Back")

    col1, col2 = st.columns(2)

    with col1:

        render_home_card(
            "📚 Continue Learning",
            get_last_learning()
        )

        render_home_card(
            "📢 Announcements",
            "Coming Soon"
        )

    with col2:

        render_home_card(
            "💬 Latest Discussion",
            get_last_chat()
        )

        render_home_card(
            "📅 Schedule",
            "Coming Soon"
        )

# ---------------------------------
# WORKSPACE
# ---------------------------------

elif st.session_state.page == "WORKSPACE":

    st.subheader(
        f"📚 {st.session_state.subject}"
    )

    render_topic_strip(
        subject=st.session_state.subject,
        topic="Last Topic",
        chapter="Current Chapter",
        grade="10"
    )

    st.divider()

    render_chat_history(
        st.session_state.learn_messages
    )

    question = st.chat_input(
        f"Ask Drona about {st.session_state.subject}"
    )

    if question:

        st.session_state.learn_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        full_question = (
            f"{st.session_state.subject}: "
            f"{question}"
        )

        answer = ask_batman(
            "STD001",
            full_question
        )

        st.session_state.learn_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

# ---------------------------------
# SUPER CHAT
# ---------------------------------

elif st.session_state.page == "SUPER_CHAT":

    st.subheader(
        "💬 Super Chat"
    )

    render_chat_history(
        st.session_state.superchat_messages
    )

    question = st.chat_input(
        "Ask Drona anything..."
    )

    if question:

        st.session_state.superchat_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        answer = ask_batman(
            "STD001",
            question
        )

        st.session_state.superchat_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()