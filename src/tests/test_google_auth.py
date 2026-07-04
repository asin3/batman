# =========================================================
# BATMAN PLATFORM
# Google Authentication Test
# =========================================================

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import streamlit as st

from src.platform.auth.google_auth import login
from src.platform.services.user_service import (
    login_or_register,
    authorize,
)

# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------

st.title("Batman Platform - Google Authentication")

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

google_user = login()

if google_user:

    user = login_or_register(

        email=google_user["email"],
        name=google_user["name"],
        provider="google",

    )

    allowed, message = authorize(user)

    if allowed:

        st.success(f"Welcome, {user.name}.")

    else:

        st.warning(message)