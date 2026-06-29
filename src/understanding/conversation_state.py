"""
============================================================
Batman Student

Module:
conversation_state.py

Purpose:
Maintain Batman's short-term understanding state.

This module stores partial understanding across
multiple conversation turns.

It is Batman's working memory.

Long-term learning belongs to learning_engine.py.

============================================================
"""


# ---------------------------------------------------------
# CONVERSATION STATE
# ---------------------------------------------------------

_state = {

    "intent": None,

    "entities": {

        "topic": None,

        "difficulty": None,

        "count": None,

        "subject": None

    }

}


# ---------------------------------------------------------
# GET
# ---------------------------------------------------------

def get_state():

    return _state


# ---------------------------------------------------------
# RESET
# ---------------------------------------------------------

def reset_state():

    global _state

    _state = {

        "intent": None,

        "entities": {

            "topic": None,

            "difficulty": None,

            "count": None,

            "subject": None

        }

    }


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

def update_state(

    intent,

    entities

):

    global _state

    if intent["name"] != "UNKNOWN":

        _state["intent"] = intent

    for key, value in entities.items():

        if value is not None:

            _state["entities"][key] = value


# ---------------------------------------------------------
# BUILD
# ---------------------------------------------------------

def build_understanding():

    return {

        "intent": _state["intent"],

        "entities": _state["entities"]

    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    update_state(

        {

            "name": "QUIZ"

        },

        {

            "topic": "Force",

            "difficulty": None,

            "count": None,

            "subject": None

        }

    )

    print(build_understanding())

    update_state(

        {

            "name": "UNKNOWN"

        },

        {

            "topic": None,

            "difficulty": "Easy",

            "count": None,

            "subject": None

        }

    )

    print(build_understanding())

    reset_state()

    print(build_understanding())