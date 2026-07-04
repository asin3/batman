# =========================================================
# BATMAN PLATFORM
# Authentication Gate
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
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def authenticate():

    # ---------------------------------------------
    # Already authenticated
    # ---------------------------------------------

    if "user" in st.session_state:

        return st.session_state.user

    # ---------------------------------------------
    # Google Login
    # ---------------------------------------------
    
    google_user = login()

    if not google_user:

        st.stop()

    # ---------------------------------------------
    # Batman User
    # ---------------------------------------------

    user = login_or_register(

        email=google_user["email"],

        name=google_user["name"],

        provider="google",

    )

    # ---------------------------------------------
    # Authorization
    # ---------------------------------------------

    allowed, message = authorize(user)

    if not allowed:

        st.warning(message)

        st.stop()

    # ---------------------------------------------
    # Persist Session
    # ---------------------------------------------

    st.session_state.user = user

    return user


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------

def logout():

    if "user" in st.session_state:

        del st.session_state.user

    st.rerun()


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Authentication Gate Ready")