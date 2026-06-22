import json
from pathlib import Path
from datetime import datetime


QUESTION_BANK_FILE = Path(
    "data/class10/physics/question_bank/generated/generated_questions.json"
)

QUESTION_BANK_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

def load_questions():

    if not QUESTION_BANK_FILE.exists():

        return []

    try:

        return json.loads(
            QUESTION_BANK_FILE.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        return []


def save_question(
    difficulty,
    question,
    options,
    correct_answer,
    explanation,
    provider
):

    questions = load_questions()

    record = {
        "grade": "10",
        "subject": "Physics",
        "chapter": "",
        "topic": "",
        "question_type": "INSTA_QUIZ",
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "source": "generated",
        "created_by": provider,
        "timestamp": datetime.now().isoformat()
    }

    questions.append(record)

    QUESTION_BANK_FILE.write_text(
        json.dumps(
            questions,
            indent=4
        ),
        encoding="utf-8"
    )


def question_exists(question_text):

    questions = load_questions()

    for item in questions:

        if (
            item["question"].strip().lower()
            ==
            question_text.strip().lower()
        ):
            return True

    return False