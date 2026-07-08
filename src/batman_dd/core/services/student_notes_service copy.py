import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[4]

NOTES_DIR = (
    BASE_DIR
    / "data"
    / "students"
)


def _notes_file(student_id: str) -> Path:
    student_dir = NOTES_DIR / student_id
    student_dir.mkdir(parents=True, exist_ok=True)
    return student_dir / "notes.json"


def load_notes(student_id: str):
    file = _notes_file(student_id)

    if not file.exists():
        return []

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_note(student_id: str, title: str, note: str):

    notes = load_notes(student_id)

    notes.insert(
        0,
        {
            "title": title,
            "note": note
        }
    )

    with open(
        _notes_file(student_id),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(notes, f, indent=4)