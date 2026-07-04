# =========================================================
# BATMAN PLATFORM
# Google Authentication Test
# =========================================================

import streamlit as st

from src.platform.auth.google_auth import login

st.title("Batman Google Login Test")

result = login()

st.write("RESULT TYPE")
st.write(type(result))

st.write("RESULT")
st.write(result)

st.write("SESSION STATE")
st.write(dict(st.session_state))