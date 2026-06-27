quiz_state = {
    "active": False,
    "topics": [],
    "difficulty": "",
    "total_questions": 0,
    "current_question": 0,
    "score": 0,
    "setup_stage": "",
    "setup_data": {},
    "current_answer": "",
    "current_explanation": "",
    "asked_questions": [],
    "asked_concepts": []
}


def start_quiz(topics):

    quiz_state["active"] = True
    quiz_state["topics"] = topics
    quiz_state["asked_questions"] = []
    quiz_state["asked_concepts"] = []

    return quiz_state


def set_difficulty(level):

    quiz_state["difficulty"] = level

    return quiz_state


def set_question_count(count):

    quiz_state["total_questions"] = count

    return quiz_state


def is_quiz_active():

    return quiz_state["active"]


def set_setup_stage(stage):

    quiz_state["setup_stage"] = stage

    return quiz_state


def get_setup_stage():

    return quiz_state["setup_stage"]


def get_quiz_state():

    return quiz_state


def set_setup_data(data):

    quiz_state["setup_data"] = data

    return quiz_state


def get_setup_data():

    return quiz_state["setup_data"]


def clear_setup_data():

    quiz_state["setup_data"] = {}

    return quiz_state


def increment_question():

    quiz_state["current_question"] += 1

    return quiz_state


def increment_score():

    quiz_state["score"] += 1

    return quiz_state


def is_quiz_complete():

    return (
        quiz_state["current_question"]
        >=
        quiz_state["total_questions"]
    )


def end_quiz():

    quiz_state["active"] = False
    quiz_state["current_question"] = 0
    quiz_state["score"] = 0
    quiz_state["current_answer"] = ""
    quiz_state["current_explanation"] = ""
    quiz_state["asked_questions"] = []
    quiz_state["asked_concepts"] = []

    return quiz_state


def reset_runtime():

    quiz_state["current_question"] = 0
    quiz_state["score"] = 0

    return quiz_state


def set_current_answer(answer):

    quiz_state["current_answer"] = answer

    return quiz_state


def get_current_answer():

    return quiz_state["current_answer"]


def set_current_explanation(explanation):

    quiz_state["current_explanation"] = explanation

    return quiz_state


def get_current_explanation():

    return quiz_state["current_explanation"]


def add_asked_question(question):

    quiz_state["asked_questions"].append(
        question
    )

    return quiz_state


def get_asked_questions():

    return quiz_state["asked_questions"]

def add_asked_concept(concept):

    quiz_state["asked_concepts"].append(
        concept
    )

    return quiz_state


def get_asked_concepts():

    return quiz_state["asked_concepts"]

def check_answer(student_answer):

    correct = (
        student_answer.upper()
        ==
        quiz_state["current_answer"].upper()
    )

    if correct:

        increment_score()

    increment_question()

    return correct