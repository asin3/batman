# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from src.platform.users.user_model import User

from src.platform.services.user_repository import (
    create_profile,
    generate_user_id,
    get_user,
    get_user_by_email,
)

from src.platform.services.student_repository import (
    assign_student_id,
    create_student_workspace,
)

import json
from pathlib import Path

# ---------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------




# ---------------------------------------------------------
# USER SERVICE
# ---------------------------------------------------------

def create_user(email, name, provider):

    return User(

        user_id=generate_user_id(),

        email=email,

        name=name,

        provider=provider,

        status="PENDING",

        student_id=""

    )


def login_or_register(email, name, provider):

    user = get_user_by_email(email)

    if user:

        return user

    user = create_user(

        email=email,

        name=name,

        provider=provider

    )

    create_profile(user)

    return user

# ---------------------------------------------------------
# AUTHORIZATION
# ---------------------------------------------------------

def authorize(user: User) -> tuple[bool, str]:

    if user.status == "ACTIVE":
        return True, "Welcome to Batman."

    if user.status == "PENDING":
        return False, "Your account is awaiting admin approval."

    if user.status == "REJECTED":
        return False, "Your registration has been rejected."

    if user.status == "SUSPENDED":
        return False, "Your account has been suspended."

    return False, "Unknown account status."

# ---------------------------------------------------------
# ADMIN
# ---------------------------------------------------------

def approve_user(user_id: str) -> User:

    profile_path = Path("data/users") / user_id / "profile.json"

    with open(profile_path, "r") as file:

        profile = json.load(file)

    profile["status"] = "ACTIVE"

    with open(profile_path, "w") as file:

        json.dump(profile, file, indent=4)

    student_id = assign_student_id(user_id)

    create_student_workspace(student_id)

    return get_user(user_id)


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    user = approve_user("USR000001")

    print(user)