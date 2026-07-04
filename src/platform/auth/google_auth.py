# =========================================================
# BATMAN PLATFORM
# Google Authentication
# =========================================================

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
import streamlit as st
from streamlit_oauth import OAuth2Component
import json
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

def load_google_config():

    config_path = (
        Path(__file__).resolve().parents[3]
        / "secrets"
        / "google_oauth.json"
    )

    with open(config_path, "r") as f:
        config = json.load(f)

    return config["web"]

def create_google_oauth():

    google = load_google_config()

    return OAuth2Component(

        client_id=google["client_id"],

        client_secret=google["client_secret"],

        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",

        token_endpoint="https://oauth2.googleapis.com/token",
    )


# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

from src.platform.providers.google_oauth import get_user_info


def login():

    # Already authenticated
    if "user" in st.session_state:
        return {
            "email": st.session_state.user.email,
            "name": st.session_state.user.name,
        }
    
    if "user" not in st.session_state:
        
        oauth = create_google_oauth()

        result = oauth.authorize_button(

            name="Continue with Google",

            redirect_uri="http://localhost:8501",

            scope="openid email profile",

            key="google_login",

        )

        if result is None:

            return None

        user_info = get_user_info(

            result["token"]["id_token"]

        )

        return {

            "email": user_info["email"],

            "name": user_info["name"],

            "picture": user_info.get("picture", ""),

        }