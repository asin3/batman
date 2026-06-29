"""
============================================================
Batman Student

Module:
tutor_router.py

Purpose:
Future home for tutor orchestration.

============================================================
"""
# ---------------------------------------------------------
# BUILD HISTORY
# ---------------------------------------------------------

def build_history_text(history):

    history_text = ""

    for msg in history:

        if "role" not in msg:
            continue

        history_text += (

            f"{msg['role']}: "

            f"{msg['content']}\n"

        )

    return history_text

def handle_tutor():
    pass

# ---------------------------------------------------------
# SAMPLE TEST
# ---------------------------------------------------------
