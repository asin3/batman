import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from batman_engine import ask_batman

# -----------------------------------
# PAGE
# -----------------------------------

st.set_page_config(
    page_title="Batman Student",
    page_icon="🦇",
    layout="wide"
)

# -----------------------------------
# STYLING
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #020617;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 2rem !important;
}

p {
    font-size: 1rem;
}

.user-card {
    background: #111827;
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 8px;
    margin-bottom: 8px;
}

.assistant-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 20px;
    margin-top: 10px;
    margin-bottom: 18px;
}

.student-badge {
    background: #1E3A5F;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
}

.hero-subtitle {
    color: #CBD5E1;
    font-size: 1.25rem;
    margin-top: -10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION
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

col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        "# 🦇 Batman Student"
    )

    st.markdown(
        '<div class="hero-subtitle">AI Tutor for Class 10 Physics</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="student-badge">
        👨‍🎓 STD001
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------------
# QUIZ STATUS
# -----------------------------------

try:

    from quiz_manager import (
        is_quiz_active,
        get_quiz_state
    )

    if is_quiz_active():

        state = get_quiz_state()

        current_q = (
            state["current_question"] + 1
        )

        total_q = (
            state["total_questions"]
        )

        score = (
            state["score"]
        )

        topic = (
            state["topics"][0]
            if state["topics"]
            else "Quiz"
        )

        st.info(
            f"🎯 {topic.title()} Quiz | Question {current_q}/{total_q} | Score: {score}"
        )

except:
    pass

# -----------------------------------
# CHAT
# -----------------------------------

st.markdown(
    "## Conversation"
)

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class="user-card">
            🔴 {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-card">
            🦇 {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
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

        answer = (
            f"ERROR:\n\n{str(e)}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()