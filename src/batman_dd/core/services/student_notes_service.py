import json

from src.platform.storage.storage_router import StorageRouter


repository = StorageRouter.get_repository()


##########################################
# Notes Path
##########################################

def _notes_path(student_id: str) -> str:
    return f"students/{student_id}/notes.json"


##########################################
# Generate Note ID
##########################################

def _generate_note_id(notes):

    highest = 0

    for note in notes:

        note_id = note.get("id", "")

        if note_id.startswith("NOTE"):

            try:
                highest = max(
                    highest,
                    int(note_id.replace("NOTE", ""))
                )
            except ValueError:
                pass

    return f"NOTE{highest + 1:06d}"


##########################################
# Load Notes
##########################################

def load_notes(student_id: str):

    path = _notes_path(student_id)

    if not repository.exists(path):
        return []

    notes = repository.read_json(path)

    upgraded = False

    for note in notes:

        if "id" not in note:

            note["id"] = _generate_note_id(notes)
            upgraded = True

    if upgraded:
        repository.write_json(path, notes)

    return notes


##########################################
# Save Note
##########################################

def save_note(student_id: str, title: str, note: str):

    path = _notes_path(student_id)

    notes = load_notes(student_id)

    notes.insert(
        0,
        {
            "id": _generate_note_id(notes),
            "title": title,
            "note": note
        }
    )

    repository.write_json(
        path,
        notes
    )


##########################################
# Delete Single Note
##########################################

def delete_note(student_id: str, note_id: str):

    notes = load_notes(student_id)

    notes = [
        note
        for note in notes
        if note["id"] != note_id
    ]

    repository.write_json(
        _notes_path(student_id),
        notes
    )


##########################################
# Delete Multiple Notes
##########################################

def delete_notes(student_id: str, note_ids: list[str]):

    notes = load_notes(student_id)

    print("DELETE IDS:", note_ids)
    
    notes = [
        note
        for note in notes
        if note["id"] not in note_ids
    ]

    print("REMAINING:", len(notes))

    repository.write_json(
        _notes_path(student_id),
        notes
    )