"""
============================================================

Batman Student

CPS-003.2

Docling JSON Inspector

Purpose

Inspect Docling JSON structure.

This is an architectural inspection tool.

No Batman integration.

============================================================
"""

import json
from collections import Counter
from pathlib import Path

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

JSON_FILE = (
    PROJECT_ROOT
    / "src"
    / "tests"
    / "docling_test"
    / "output"
    / "document.json"
)

# ----------------------------------------------------------
# LOAD
# ----------------------------------------------------------

with open(JSON_FILE, "r", encoding="utf-8") as f:

    document = json.load(f)

print()
print("=" * 60)
print("DOCLING JSON INSPECTOR")
print("=" * 60)

# ----------------------------------------------------------
# REPORT 1
# ----------------------------------------------------------

print("\nDOCUMENT SUMMARY")
print("-" * 60)

print(f"File : {JSON_FILE.name}")
print(f"Size : {JSON_FILE.stat().st_size:,} bytes")

print("\nRoot Keys")

for key in document.keys():

    print(" -", key)

# ----------------------------------------------------------
# GLOBALS
# ----------------------------------------------------------

NODE_TYPES = Counter()

METADATA_FIELDS = Counter()

FIRST_NODES = []

MAX_PRINT = 40

# ----------------------------------------------------------
# RECURSIVE SCANNER
# ----------------------------------------------------------

def scan_node(node, level=0):

    global FIRST_NODES

    # ------------------------------------------
    # Dictionary
    # ------------------------------------------

    if isinstance(node, dict):

        node_type = None

        for key in ("type", "label", "kind", "name"):

            if key in node and isinstance(node[key], str):

                node_type = node[key]

                break

        if node_type:

            NODE_TYPES[node_type] += 1

            if len(FIRST_NODES) < MAX_PRINT:

                FIRST_NODES.append(
                    (
                        level,
                        node_type
                    )
                )

        for key in node.keys():

            METADATA_FIELDS[key] += 1

        for value in node.values():

            scan_node(
                value,
                level + 1
            )

    # ------------------------------------------
    # List
    # ------------------------------------------

    elif isinstance(node, list):

        for item in node:

            scan_node(
                item,
                level
            )


# ----------------------------------------------------------
# START SCAN
# ----------------------------------------------------------

scan_node(document)

# ----------------------------------------------------------
# REPORT 2
# ----------------------------------------------------------

print()
print("=" * 60)
print("NODE TYPES")
print("=" * 60)

for node_type, count in sorted(
    NODE_TYPES.items()
):

    print(
        f"{node_type:<30} {count}"
    )

# ----------------------------------------------------------
# REPORT 3
# ----------------------------------------------------------

print()
print("=" * 60)
print("FIRST DISCOVERED NODES")
print("=" * 60)

for level, node_type in FIRST_NODES:

    print(
        "    " * level + node_type
    )

# ----------------------------------------------------------
# REPORT 4
# ----------------------------------------------------------

print()
print("=" * 60)
print("METADATA FIELDS")
print("=" * 60)

for field, count in sorted(
    METADATA_FIELDS.items()
):

    print(
        f"{field:<30} {count}"
    )

# ----------------------------------------------------------
# REPORT 5
# ----------------------------------------------------------

print()
print("=" * 60)
print("AUTOMATIC FEATURE DETECTION")
print("=" * 60)

FEATURES = {
    "Heading": False,
    "Paragraph": False,
    "Table": False,
    "Figure": False,
    "Caption": False,
    "Formula": False,
    "Page": False,
    "List": False,
}

for node in NODE_TYPES.keys():

    name = node.lower()

    if "head" in name:
        FEATURES["Heading"] = True

    if "paragraph" in name or name == "text":
        FEATURES["Paragraph"] = True

    if "table" in name:
        FEATURES["Table"] = True

    if "figure" in name or "image" in name:
        FEATURES["Figure"] = True

    if "caption" in name:
        FEATURES["Caption"] = True

    if "formula" in name or "equation" in name or "math" in name:
        FEATURES["Formula"] = True

    if "page" in name:
        FEATURES["Page"] = True

    if "list" in name:
        FEATURES["List"] = True


for feature, available in FEATURES.items():

    print(f"{feature:<15} {'YES' if available else 'NO'}")


# ----------------------------------------------------------
# REPORT 6
# ----------------------------------------------------------

print()
print("=" * 60)
print("CHUNKING FEASIBILITY")
print("=" * 60)

chunk_candidates = []

if FEATURES["Heading"]:
    chunk_candidates.append("Heading")

if FEATURES["Paragraph"]:
    chunk_candidates.append("Paragraph")

if FEATURES["Table"]:
    chunk_candidates.append("Table")

if FEATURES["Figure"]:
    chunk_candidates.append("Figure")

if FEATURES["Caption"]:
    chunk_candidates.append("Caption")

if FEATURES["Formula"]:
    chunk_candidates.append("Formula")

if FEATURES["List"]:
    chunk_candidates.append("List")

print()

if chunk_candidates:

    print("Possible Semantic Chunk Boundaries")

    for item in chunk_candidates:

        print(f"  - {item}")

else:

    print("No semantic chunk boundaries detected.")


# ----------------------------------------------------------
# REPORT 7
# ----------------------------------------------------------

print()
print("=" * 60)
print("BATMAN RECOMMENDATION")
print("=" * 60)

print()

if FEATURES["Heading"]:

    print("✓ Heading-based chunking recommended")

else:

    print("✗ Heading-based chunking unavailable")

if FEATURES["Table"]:

    print("✓ Table artifacts should be preserved")

if FEATURES["Figure"]:

    print("✓ Figure artifacts should be preserved")

if FEATURES["Caption"]:

    print("✓ Figure captions should be linked")

if FEATURES["Formula"]:

    print("✓ Formula artifacts should be preserved")

print()

print("Recommendation")

print("Do NOT use fixed-size character chunking.")

print("Use semantic document structure whenever available.")


# ----------------------------------------------------------
# REPORT 8
# ----------------------------------------------------------

print()
print("=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)

print(f"Unique Node Types     : {len(NODE_TYPES)}")
print(f"Metadata Fields       : {len(METADATA_FIELDS)}")
print(f"Sample Nodes Printed  : {len(FIRST_NODES)}")

print()
print("Batman is ready for semantic ingestion evaluation.")