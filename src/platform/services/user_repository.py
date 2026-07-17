# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from pathlib import Path
import json

from src.platform.users.user_model import User
from src.platform.storage.storage_router import StorageRouter

# ---------------------------------------------------------
# USER REPOSITORY
# ---------------------------------------------------------

USERS_PATH = Path("data/users")
repository = StorageRouter.get_repository()


def get_users_path():

    return USERS_PATH


def generate_user_id():

    ids = []

    user_folders = repository.list("users")

    for folder in user_folders:

        if folder.startswith("USR"):

            ids.append(int(folder[3:]))

    if not ids:

        return "USR000001"

    next_id = max(ids) + 1

    return f"USR{next_id:06d}"


def create_user_folder(user):

    user_folder = USERS_PATH / user.user_id

    user_folder.mkdir(parents=True, exist_ok=True)

    return user_folder


def create_profile(user):

    profile = {

        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "provider": user.provider,
        "status": user.status,
        "student_id": user.student_id

    }

    repository.write_json(
        f"users/{user.user_id}/profile.json",
        profile
    )

    return profile


def get_user(user_id):

    path = f"users/{user_id}/profile.json"

    if not repository.exists(path):

        return None

    data = repository.read_json(path)

    return User(**data)


def get_user_by_email(email):

    user_folders = repository.list("users")

    for folder in user_folders:

        user = get_user(folder)

        if (
            user
            and user.email.lower() == email.lower()
        ):
            return user

    return None

# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print(generate_user_id())