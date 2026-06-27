from datetime import datetime

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"


def get_history_path(student_id):

    student_folder = (
        DATA_FOLDER
        / "students"
        / student_id
    )

    student_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return student_folder / "history.json"


def load_history(student_id):

    file_path = get_history_path(
        student_id
    )

    if not file_path.exists():

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump([], f)

        return []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        history = json.load(f)

    # -------------------------
    # Backward Compatibility
    # -------------------------

    for msg in history:

        if "mode" not in msg:

            msg["mode"] = (
                "SUPER_CHAT"
            )

        if "subject" not in msg:

            msg["subject"] = ""

    return history


def save_history(
    student_id,
    history
):

    file_path = get_history_path(
        student_id
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=2
        )

def save_quiz_history(
    student_id,
    subject,
    chapter,
    difficulty,
    score,
    total
):

    history = load_history(student_id)

    history.append(
        {
            "type": "QUIZ",
            "mode": "QUIZ",
            "subject": subject,
            "chapter": chapter,
            "difficulty": difficulty,
            "score": score,
            "total": total,
            "percentage": round((score / total) * 100),
            "timestamp": datetime.now().isoformat()
        }
    )

    save_history(
        student_id,
        history
    )