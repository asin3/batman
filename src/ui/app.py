import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from batman_engine import ask_batman
from learn_manager import (
    get_subjects,
    get_workspace_sections
)

# -----------------------------------
# PAGE
# -----------------------------------

st.set_page_config(
    page_title="Batman Student",
    page_icon="🦇",
    layout="wide"
)

# -----------------------------------
# STYLE
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #020617;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.pillar-card {
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #1E293B;
    background: #0F172A;
    margin-bottom: 15px;
}

.subject-card {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1E293B;
    background: #111827;
}

.workspace-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
    background: #0F172A;
    text-align: center;
}

.user-card {
    background: #111827;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}

.assistant-card {
    background: #0F172A;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #1E293B;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION
# -----------------------------------

if "page" not in st.session_state:
    st.session_state.page = "HOME"

if "subject" not in st.session_state:
    st.session_state.subject = None

if "section" not in st.session_state:
    st.session_state.section = "Learn"

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

col1, col2 = st.columns([5,1])

with col1:

    st.title(
        "🦇 Batman Student"
    )

with col2:

    st.info(
        "STD001"
    )

st.divider()

# ===================================
# HOME
# ===================================

if st.session_state.page == "HOME":

    st.subheader(
        "What would you like help with today?"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "📚 Learn",
            use_container_width=True
        ):
            st.session_state.page = "LEARN"
            st.rerun()

        st.button(
            "🎯 Study Planner",
            use_container_width=True,
            disabled=True
        )

        st.button(
            "📈 Progress",
            use_container_width=True,
            disabled=True
        )

    with c2:

        st.button(
            "📝 Quiz",
            use_container_width=True,
            disabled=True
        )

        if st.button(
            "💬 Super Chat",
            use_container_width=True
        ):
            st.session_state.page = "SUPER_CHAT"
            st.rerun()

# ===================================
# LEARN
# ===================================

elif st.session_state.page == "LEARN":

    st.subheader(
        "Choose Subject"
    )

    cols = st.columns(4)

    subjects = get_subjects()

    for i, subject in enumerate(subjects):

        with cols[i]:

            if st.button(
                subject,
                use_container_width=True
            ):

                st.session_state.subject = subject
                st.session_state.page = "WORKSPACE"

                st.rerun()

    if st.button("⬅ Back"):

        st.session_state.page = "HOME"
        st.rerun()

# ===================================
# WORKSPACE
# ===================================

elif st.session_state.page == "WORKSPACE":

    st.subheader(
        f"📚 {st.session_state.subject}"
    )

    cols = st.columns(4)

    sections = get_workspace_sections()

    for i, section in enumerate(sections):

        with cols[i]:

            if st.button(
                section,
                use_container_width=True
            ):

                st.session_state.section = section

    st.divider()

    if st.session_state.section != "Learn":

        st.info(
            f"{st.session_state.section} Module Coming Soon"
        )

    else:

        for msg in st.session_state.messages:

            if msg["role"] == "user":

                st.markdown(
                    f"""
                    <div class="user-card">
                    {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="assistant-card">
                    {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        question = st.chat_input(
            f"Ask Batman about {st.session_state.subject}"
        )

        if question:

            full_question = (
                f"{st.session_state.subject}: "
                f"{question}"
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            try:

                answer = ask_batman(
                    "STD001",
                    full_question
                )

            except Exception as e:

                answer = str(e)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

    if st.button("⬅ Back to Subjects"):

        st.session_state.page = "LEARN"
        st.rerun()

# ===================================
# SUPER CHAT
# ===================================

elif st.session_state.page == "SUPER_CHAT":

    st.subheader(
        "💬 Super Chat"
    )

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f"""
                <div class="user-card">
                {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="assistant-card">
                {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

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

            answer = str(e)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    if st.button("⬅ Back Home"):

        st.session_state.page = "HOME"
        st.rerun()