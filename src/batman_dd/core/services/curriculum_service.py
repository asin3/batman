import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[4]

CURRICULUM_FILE = (
    BASE_DIR
    / "data"
    / "Board"
    / "icse"
    / "class10"
    / "curriculum"
    / "output"
    / "curriculum.json"
)


def load_curriculum():
    with open(CURRICULUM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(name: str) -> str:
    return (
        name.lower()
        .replace("mathematics", "maths")
        .strip()
    )


def get_subject(subject_name):
    curriculum = load_curriculum()

    for subject in curriculum["subjects"]:
        if normalize(subject["title"]) == normalize(subject_name):
            return subject

    return None