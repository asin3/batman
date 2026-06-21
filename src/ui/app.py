import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from batman_engine import ask_batman

st.set_page_config(
    page_title="Batman Student",
    page_icon="🦇",
    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello. I am Batman. What would you like to learn today?"
        }
    ]

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
# 🦇 Batman Student
### Learn. Think. Understand.
""")

col1, col2 = st.columns([5, 1])

with col2:
    st.info("STD001")

st.divider()

# -----------------------------------
# CHAT
# -----------------------------------

st.subheader("Conversation")

chat_container = st.container()

with chat_container:

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

# -----------------------------------
# INPUT
# -----------------------------------

question = st.chat_input(
    "Ask Batman anything..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    try:

        answer = ask_batman(
            "STD001",
            question
        )

    except Exception as e:

        answer = f"ERROR:\n\n{str(e)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()

# -----------------------------------
# FEATURES
# -----------------------------------

st.divider()

st.subheader(
    "What can Batman do?"
)

c1, c2 = st.columns(2)

with c1:

    st.info(
        "📘 Concept Teacher\n\nExplain textbook concepts in simple language."
    )

    st.info(
        "🎯 Insta Quiz\n\nGenerate quizzes directly from textbook content."
    )

with c2:

    st.info(
        "📝 Homework Guide\n\nGuide students without revealing answers immediately."
    )

    st.info(
        "📚 Study Coach\n\nCreate revision plans and exam preparation schedules."
    )