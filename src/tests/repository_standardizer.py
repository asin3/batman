"""
============================================================
Batman Student

Repository Standardizer

CPS-002B

Purpose

One-time repository migration.

Functions

1. Rename files to Batman naming standard

    physics-textbook.pdf
    physics _textbook8.pdf

            ↓

    physics_textbook.pdf
    physics_textbook8.pdf

2. Update document_registry.json

3. Update metadata.json

This utility should be executed ONCE only.

============================================================
"""

import json
import re
from pathlib import Path

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"

REGISTRY_FILE = DATA_FOLDER / "document_registry.json"

# ----------------------------------------------------------
# LOAD REGISTRY
# ----------------------------------------------------------

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:

    registry = json.load(f)

# ----------------------------------------------------------
# COUNTERS
# ----------------------------------------------------------

renamed_files = 0

updated_registry = 0

updated_metadata = 0

conflicts = 0

# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------

def standardize_name(filename: str) -> str:
    """
    Convert filename into Batman standard.
    """

    stem = Path(filename).stem

    suffix = Path(filename).suffix

    stem = stem.replace("-", "_")

    stem = stem.replace(" ", "_")

    stem = re.sub(r"_+", "_", stem)

    return stem + suffix


def load_json(path: Path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def save_json(path: Path, data):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

# ----------------------------------------------------------
# STANDARDIZE REPOSITORY
# ----------------------------------------------------------

for document in registry:

    old_relative_path = document["path"]

    old_file_name = document["file"]

    old_absolute_path = DATA_FOLDER / old_relative_path

    if not old_absolute_path.exists():

        print(f"[MISSING] {old_relative_path}")

        continue

    new_file_name = standardize_name(old_file_name)

    new_absolute_path = old_absolute_path.with_name(
        new_file_name
    )

    # ----------------------------------------------
    # Rename file
    # ----------------------------------------------

    if old_absolute_path != new_absolute_path:

        if new_absolute_path.exists():

            conflicts += 1

            print(
                f"[CONFLICT] {new_file_name}"
            )

            continue

        old_absolute_path.rename(
            new_absolute_path
        )

        renamed_files += 1

        print(
            f"[RENAMED] {old_file_name}  ->  {new_file_name}"
        )

    # ----------------------------------------------
    # Update registry
    # ----------------------------------------------

    new_relative_path = str(
        new_absolute_path.relative_to(DATA_FOLDER)
    ).replace("\\", "/")

    if (
        document["file"] != new_file_name
        or
        document["path"] != new_relative_path
    ):

        document["file"] = new_file_name

        document["path"] = new_relative_path

        updated_registry += 1

# ----------------------------------------------------------
# SAVE UPDATED REGISTRY
# ----------------------------------------------------------

save_json(
    REGISTRY_FILE,
    registry
)

# ----------------------------------------------------------
# UPDATE METADATA FILES
# ----------------------------------------------------------

metadata_files = list(
    DATA_FOLDER.glob("**/metadata.json")
)

for metadata_file in metadata_files:

    metadata = load_json(
        metadata_file
    )

    changed = False

    for item in metadata:

        new_name = standardize_name(
            item["file"]
        )

        new_path = str(
            Path(item["path"]).with_name(
                new_name
            )
        ).replace("\\", "/")

        if (
            item["file"] != new_name
            or
            item["path"] != new_path
        ):

            item["file"] = new_name

            item["path"] = new_path

            changed = True

    if changed:

        save_json(
            metadata_file,
            metadata
        )

        updated_metadata += 1

# ----------------------------------------------------------
# FINAL VERIFICATION
# ----------------------------------------------------------

print()
print("=" * 60)
print("VERIFYING REPOSITORY")
print("=" * 60)

missing_files = 0

for document in registry:

    file_path = DATA_FOLDER / document["path"]

    if not file_path.exists():

        missing_files += 1

        print(
            f"[MISSING] {document['document_id']} -> {document['path']}"
        )

# ----------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------

print()
print("=" * 60)
print("REPOSITORY STANDARDIZATION COMPLETE")
print("=" * 60)

print(f"Files Renamed      : {renamed_files}")
print(f"Registry Updated   : {updated_registry}")
print(f"Metadata Updated   : {updated_metadata}")
print(f"Conflicts          : {conflicts}")
print(f"Missing Files      : {missing_files}")

print("=" * 60)

# ----------------------------------------------------------
# SAFE EXIT
# ----------------------------------------------------------

if conflicts == 0 and missing_files == 0:

    print()
    print("SUCCESS")
    print("Repository is now using Batman naming standards.")

else:

    print()
    print("WARNING")
    print("Repository completed with issues.")
    print("Review the messages above before continuing.")