"""
============================================================
Batman Student

Module:
settings.py

Purpose:
Central Configuration

All project-wide configurable values
must be stored here.

============================================================
"""

# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

#LLM_PROVIDER = "deepseek"
#LLM_PROVIDER = "openai"
LLM_PROVIDER = "gemini"

# Options:
# openai
# gemini
# deepseek


# ---------------------------------------------------------
# EMBEDDINGS
# ---------------------------------------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------
# CURRICULUM
# ---------------------------------------------------------

BOARD = "ICSE"

GRADE = "10"

SUBJECT = "Physics"

# ---------------------------------------------------------
# GOOGLE AUTH
# ---------------------------------------------------------

GOOGLE_CLIENT_SECRET_FILE = "secrets/google_client_secret.json"

GOOGLE_REDIRECT_URI = "http://localhost:8501"

GOOGLE_SCOPES = [

    "openid",

    "https://www.googleapis.com/auth/userinfo.email",

    "https://www.googleapis.com/auth/userinfo.profile",

]

# ----------------------------------------------------------
# KNOWLEDGE ASSET FOLDERS
# ----------------------------------------------------------

FIGURES_FOLDER = "figures"

TABLES_FOLDER = "tables"

EMBEDDINGS_FOLDER = "embeddings"