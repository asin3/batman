from behavior.intent_classifier import classify_intent


def choose_skill(question):

    intent = classify_intent(
        question
    )

    mapping = {

        "LEARN":
        "CONCEPT_TEACHER",

        "SUPER_CHAT":
        "GENERAL_BATMAN",

        "HOMEWORK":
        "HOMEWORK_GUIDE",

        "SOLVED_EXAMPLE":
        "SOLVED_EXAMPLE",

        "STUDY_PLAN":
        "STUDY_COACH",

        "QUIZ":
        "QUIZ_MASTER"
    }

    return mapping.get(
        intent,
        "GENERAL_BATMAN"
    )