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

LLM_PROVIDER = "deepseek"
#LLM_PROVIDER = "openai"
#LLM_PROVIDER = "gemini"

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