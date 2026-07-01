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

# ---------------------------------------------------------
# ROUTE REQUEST
# ---------------------------------------------------------

def route_request(understanding):

    if understanding is None:

        return "TUTOR"

    intent = understanding["intent"]["name"]

    if intent == "QUIZ":

        return "QUIZ"

    return "TUTOR"



def handle_tutor():

    print("Tutor Router")

# ---------------------------------------------------------
# SAMPLE TEST
# ---------------------------------------------------------
if __name__ == "__main__":

    quiz = {

        "intent": {

            "name": "QUIZ"

        }

    }

    concept = {

        "intent": {

            "name": "CONCEPT"

        }

    }

    print(route_request(quiz))

    print(route_request(concept))

    print(route_request(None))