# =========================================================
# BATMAN PLATFORM
# Student Repository
# =========================================================

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from src.platform.storage.storage_router import StorageRouter
from src.platform.services.user_repository import get_user

# ---------------------------------------------------------
# REPOSITORY
# ---------------------------------------------------------

repository = StorageRouter.get_repository()

# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def generate_student_id() -> str:

    folders = repository.list("students")

    ids = []

    for folder in folders:

        if folder.startswith("STD"):

            ids.append(int(folder.replace("STD", "")))

    if not ids:

        return "STD000001"

    return f"STD{max(ids)+1:06d}"


# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def assign_student_id(user_id: str) -> str:

    user = get_user(user_id)

    if user is None:

        raise ValueError(f"User not found: {user_id}")

    if user.student_id:

        return user.student_id

    student_id = generate_student_id()

    user.student_id = student_id

    repository.write_json(

        f"users/{user.user_id}/profile.json",

        {

            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "provider": user.provider,
            "status": user.status,
            "student_id": user.student_id,

        }

    )

    return student_id


# ---------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------

def create_student_workspace(student_id: str):

    empty = {}

    files = [

        "history.json",
        "learning_state.json",
        "progress.json",
        "schedule.json",

    ]

    for filename in files:

        path = f"students/{student_id}/{filename}"

        if not repository.exists(path):

            repository.write_json(

                path,

                empty

            )


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    create_student_workspace("STD000003")

    print("Student Repository Ready")