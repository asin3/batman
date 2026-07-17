"""
==========================================================
BATMAN PLATFORM
Data Migration Tool
----------------------------------------------------------
Purpose:
    One-time migration of Local JSON storage
    to Supabase Storage.

Usage:

python -m src.platform.tools.migrate_to_supabase

==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

from pathlib import Path

from src.platform.storage.local_storage_repository import (
    LocalStorageRepository,
)

from src.platform.storage.supabase_storage_repository import (
    SupabaseStorageRepository,
)

import json
import pprint

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = Path("data")

# ==========================================================
# FILE DISCOVERY
# ==========================================================

def discover_json_files():

    files = []

    for file in DATA_PATH.rglob("*.json"):

        files.append(file)

    return sorted(files)

# ==========================================================
# Upload
# ==========================================================

def upload_file(file: Path):

    relative = file.relative_to(DATA_PATH)

    parts = relative.parts

    top_folder = parts[0]

    if top_folder in ["users", "students", "notes", "uploads", "exports"]:

        bucket = top_folder
        object_name = "/".join(parts[1:])

    else:

        bucket = "platform"
        object_name = "/".join(parts)

    with open(file, "r", encoding="utf-8") as f:

        data = json.load(f)

    storage_path = f"{bucket}/{object_name}"

    supabase_repo.write_json(
        storage_path,
        data
    )

    print(f"Uploaded: {storage_path}")

# ==========================================================
# VERIFY
# ==========================================================

def verify_file(file: Path):

    relative = file.relative_to(DATA_PATH)

    parts = relative.parts

    top_folder = parts[0]

    if top_folder in [
        "users",
        "students",
        "notes",
        "uploads",
        "exports",
    ]:

        storage_path = str(relative).replace("\\", "/")

    else:

        storage_path = (
            "platform/"
            + str(relative).replace("\\", "/")
        )

    with open(file, "r", encoding="utf-8") as f:

        local_data = json.load(f)

    cloud_data = supabase_repo.read_json(storage_path)

    if local_data == cloud_data:

        print(f"✓ VERIFIED : {storage_path}")

        return True

    print(f"✗ FAILED    : {storage_path}")

    print("\nLOCAL")

    pprint.pp(local_data)

    print("\nSUPABASE")

    pprint.pp(cloud_data)

    return False

# ==========================================================
# REPOSITORIES
# ==========================================================

local_repo = LocalStorageRepository()
supabase_repo = SupabaseStorageRepository()

# ==========================================================
# MAIN
# ==========================================================

def migrate():

    print("=" * 60)
    print("Batman Platform Data Migration")
    print("=" * 60)

    print("\nSource :", DATA_PATH.resolve())
    print("Target : Supabase Storage\n")

    json_files = discover_json_files()

    print(f"Discovered {len(json_files)} JSON file(s).\n")

    uploaded = 0

    for file in json_files:

        upload_file(file)

        uploaded += 1

    print("\n")
    print("=" * 60)
    print("VERIFYING")
    print("=" * 60)

    passed = 0

    for file in json_files:

        if verify_file(file):

            passed += 1

    print("\n")
    print("=" * 60)
    print(f"VERIFIED {passed}/{len(json_files)} FILES")
    print("=" * 60)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    migrate()