import json

from src.platform.storage.storage_router import StorageRouter


repository = StorageRouter.get_repository()


def _notes_path(student_id: str) -> str:
    return f"students/{student_id}/notes.json"


def load_notes(student_id: str):

    path = _notes_path(student_id)

    if not repository.exists(path):
        return []

    return repository.read_json(path)


def save_note(student_id: str, title: str, note: str):

    path = _notes_path(student_id)

    notes = []

    if repository.exists(path):
        notes = repository.read_json(path)

    notes.insert(
        0,
        {
            "title": title,
            "note": note
        }
    )

    repository.write_json(
        path,
        notes
    )