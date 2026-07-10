"""
============================================================
Batman Student

CPS-002C

Rename OCR artifacts inside staging folders.

Purpose
-------
One-time migration.

Renames:
    biology _sq1.txt
        -> biology_sq1.txt

    physics-textbook.txt
        -> physics_textbook.txt

Only files inside any "staging" folder are modified.

No registry updates.
No metadata updates.

============================================================
"""

import re
from pathlib import Path

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"

# ----------------------------------------------------------
# COUNTERS
# ----------------------------------------------------------

renamed = 0
skipped = 0
conflicts = 0

# ----------------------------------------------------------
# HELPER
# ----------------------------------------------------------


def standardize_name(filename: str) -> str:

    stem = Path(filename).stem

    suffix = Path(filename).suffix

    stem = stem.replace("-", "_")

    stem = stem.replace(" ", "_")

    stem = re.sub(r"_+", "_", stem)

    return stem + suffix


# ----------------------------------------------------------
# PROCESS
# ----------------------------------------------------------

for staging_folder in DATA_FOLDER.rglob("staging"):

    if not staging_folder.is_dir():
        continue

    for file in staging_folder.iterdir():

        if not file.is_file():
            continue

        new_name = standardize_name(file.name)

        if new_name == file.name:

            skipped += 1
            continue

        target = file.with_name(new_name)

        if target.exists():

            conflicts += 1

            print(
                f"[CONFLICT] {target.name}"
            )

            continue

        file.rename(target)

        renamed += 1

        print(
            f"[RENAMED] {file.name} -> {target.name}"
        )

# ----------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------

print()
print("=" * 60)
print("STAGING STANDARDIZATION COMPLETE")
print("=" * 60)
print(f"Renamed  : {renamed}")
print(f"Skipped  : {skipped}")
print(f"Conflicts: {conflicts}")
print("=" * 60)

if conflicts == 0:

    print()
    print("SUCCESS")

else:

    print()
    print("WARNING - Resolve conflicts before continuing.")