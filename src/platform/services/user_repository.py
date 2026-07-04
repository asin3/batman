# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from pathlib import Path
import json

from src.platform.users.user_model import User


# ---------------------------------------------------------
# USER REPOSITORY
# ---------------------------------------------------------

USERS_PATH = Path("data/users")


def get_users_path():

    return USERS_PATH


def generate_user_id():

    ids = []

    for folder in USERS_PATH.iterdir():

        if folder.is_dir() and folder.name.startswith("USR"):

            ids.append(int(folder.name[3:]))

    if not ids:

        return "USR000001"

    next_id = max(ids) + 1

    return f"USR{next_id:06d}"


def create_user_folder(user):

    user_folder = USERS_PATH / user.user_id

    user_folder.mkdir(parents=True, exist_ok=True)

    return user_folder


def create_profile(user):

    user_folder = create_user_folder(user)

    profile = {

        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "provider": user.provider,
        "status": user.status,
        "student_id": user.student_id

    }

    profile_path = user_folder / "profile.json"

    with open(profile_path, "w", encoding="utf-8") as file:

        json.dump(profile, file, indent=4)

    return profile_path


def get_user(user_id):

    profile_path = USERS_PATH / user_id / "profile.json"

    if not profile_path.exists():

        return None

    with open(profile_path, "r", encoding="utf-8") as file:

        data = json.load(file)

    return User(**data)


def get_user_by_email(email):

    for user_folder in USERS_PATH.iterdir():

        if not user_folder.is_dir():

            continue

        user = get_user(user_folder.name)

        if user and user.email.lower() == email.lower():

            return user

    return None


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print(generate_user_id())