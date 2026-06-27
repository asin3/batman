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

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    max-width: 1400px;
    padding-top: 2rem;
}

h1{
    font-size: 3rem !important;
    font-weight: 800 !important;
}

h2{
    font-size: 2rem !important;
}

h3{
    font-size: 1.5rem !important;
}

p, li{
    font-size: 1.05rem !important;
}

.main-title{
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0;
}

.sub-title{
    font-size: 22px;
    color: #9aa6b2;
    margin-top: 0;
}

.student-chip{
    background:#1e3a5f;
    color:white;
    padding:12px 18px;
    border-radius:12px;
    text-align:center;
    font-weight:600;
    margin-top:25px;
}

.chat-shell{
    background:#0d1117;
    border:1px solid #2b313c;
    border-radius:18px;
    padding:25px;
}

.feature-card{
    background:#1b3552;
    border-radius:16px;
    padding:22px;
    margin-bottom:15px;
    border:1px solid rgba(255,255,255,0.08);
}

.feature-title{
    font-size:20px;
    font-weight:700;
    margin-bottom:10px;
}

.feature-text{
    font-size:16px;
    color:#d8e3f0;
}

section[data-testid="stChatMessage"]{
    padding-top:10px;
    padding-bottom:10px;
}

section[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"]{
    font-size:18px;
    line-height:1.7;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello. I am Batman. What would you like to learn today?"
        }
    ]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

col1, col2 = st.columns([8, 2])

with col1:

    st.markdown("""
    <div class="main-title">
        🦇 Batman Student
    </div>

    <div class="sub-title">
        Learn. Think. Understand.
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(
        """
        <div class="student-chip">
            STD001
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("## Conversation")

with st.container():

    st.markdown(
        '<div class="chat-shell">',
        unsafe_allow_html=True
    )

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# INPUT
# --------------------------------------------------

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
            "ERROR\n\n"
            f"{str(e)}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

st.markdown("## What can Batman do?")

c1, c2 = st.columns(2)

with c1:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            📘 Concept Teacher
        </div>
        <div class="feature-text">
            Explain textbook concepts in simple language with examples and memory tricks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            🎯 Insta Quiz
        </div>
        <div class="feature-text">
            Generate interactive quizzes directly from textbook content and score responses.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            📝 Homework Guide
        </div>
        <div class="feature-text">
            Help students solve problems step-by-step without immediately revealing answers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            📚 Study Coach
        </div>
        <div class="feature-text">
            Create revision plans, practice schedules and exam preparation roadmaps.
        </div>
    </div>
    """, unsafe_allow_html=True)