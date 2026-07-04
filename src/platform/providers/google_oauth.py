# =========================================================
# BATMAN PLATFORM
# Google OAuth Provider
# =========================================================

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from google.oauth2 import id_token
from google.auth.transport import requests

# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def get_user_info(id_token_string):

    return id_token.verify_oauth2_token(

        id_token_string,

        requests.Request(),

        clock_skew_in_seconds=10

    )