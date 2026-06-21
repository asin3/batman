import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def get_history_path(student_id):

    student_folder = os.path.join(
        BASE_DIR,
        "data",
        "students",
        student_id
    )

    os.makedirs(student_folder, exist_ok=True)

    return os.path.join(
        student_folder,
        "history.json"
    )


def load_history(student_id):

    file_path = get_history_path(student_id)

    if not os.path.exists(file_path):

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(student_id, history):

    file_path = get_history_path(student_id)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)