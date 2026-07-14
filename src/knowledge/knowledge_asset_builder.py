"""
============================================================

Batman Student

CPS-006.3A

Knowledge Asset Builder

Purpose

Build Batman Knowledge Assets from
Docling output.

Responsibilities

• Read document.json
• Build knowledge assets
• Export Batman artifacts

This module must never parse PDFs directly.
It consumes Docling artifacts only.

============================================================
"""

import json
import pprint

import sys

from pathlib import Path

# ---------------------------------------------------------
# BOOTSTRAP
# ---------------------------------------------------------

# =========================================================
# 1. BOOTSTRAP
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge.document_adapter import (
    load_document,
    get_content_texts,
    get_normalized_pictures,
    get_normalized_tables,
    get_picture_captions,
)

from src.config.paths import (
    PROJECT_ROOT,
)

REGISTRY_FILE = (
    PROJECT_ROOT
    / "data"
    / "document_registry.json"
)

with open(
    REGISTRY_FILE,
    "r",
    encoding="utf-8"
) as f:

    registry = json.load(f)

# =========================================================
# 2. LOAD ARTIFACTS
# =========================================================

print()

print("=" * 60)
print("KNOWLEDGE ASSET BUILDER")

print()

print("Loading Figure Manifest...")

print("=" * 60)

# ---------------------------------------------------------
# PILOT DOCUMENT
# ---------------------------------------------------------

DOCUMENT_ID = "DOC000013"

document_info = next(

    item

    for item in registry

    if item["document_id"] == DOCUMENT_ID

)

source_pdf = (
    PROJECT_ROOT
    / "data"
    / document_info["path"]
)

DOCUMENT_FOLDER = (
    source_pdf.parent.parent
    / "staging"
    / DOCUMENT_ID
)

DOCUMENT_JSON = (
    DOCUMENT_FOLDER
    / "document.json"
)


document = load_document(
    DOCUMENT_JSON
)

with open(

    DOCUMENT_FOLDER / "figure_manifest.json",

    "r",

    encoding="utf-8"

) as f:

    figure_manifest = json.load(f)

    with open(

        DOCUMENT_FOLDER / "chunks.json",

        "r",

        encoding="utf-8"

    ) as f:

        chunks = json.load(f)

print(

    f"Figures Loaded : "

    f"{len(figure_manifest)}"

)

print(
    f"Chunks Loaded  : "
    f"{len(chunks)}"
)

print()

print("Creating Figure Index...")

# =========================================================
# 3. BUILD LOOKUPS
# =========================================================

figure_index = {

    figure["docling_picture"]: figure

    for figure in figure_manifest

}

knowledge_assets = {

    "texts": get_content_texts(document),

    "pictures": get_normalized_pictures(document),

    "tables": get_normalized_tables(document),

    "captions": get_picture_captions(document)

}

table_index = {

    table["id"]: table

    for table in knowledge_assets["tables"]

}


caption_lookup = {

    caption["parent"]: caption["text"]

    for caption in knowledge_assets["captions"]

}

print(

    f"Figure Index : "

    f"{len(figure_index)}"

)

print()

print("=" * 60)

print("FIRST NORMALIZED TABLE")

print("=" * 60)

print()

if knowledge_assets["tables"]:

    pprint.pp(

        knowledge_assets["tables"][0]

    )

print()

for figure in figure_manifest:

    caption = caption_lookup.get(

        figure["docling_picture"]

    )

    if caption:

        figure["caption"] = caption

print("First Figure Mapping")

print()

first_key = next(

    iter(figure_index)

)

print(first_key)

import pprint

pprint.pp(

    figure_index[first_key]

)

# =========================================================
# 4. KNOWLEDGE LINKING
# =========================================================

print()

print("Linking Figures to Chunks...")

print()
print("Resolving Provenance...")

content_texts = get_content_texts(document)

object_parent_lookup = {

    text["id"]: text["parent"]

    for text in content_texts

}

links_created = 0

table_links_created = 0

for chunk in chunks:

    for source in chunk["source_objects"]:

        parent = object_parent_lookup.get(source)

        if parent in figure_index:

            figure_id = figure_index[parent]["figure_id"]

            if figure_id not in chunk["figure_refs"]:

                chunk["figure_refs"].append(

                    figure_id

                )

                links_created += 1

        elif parent in table_index:

            if parent not in chunk["table_refs"]:

                chunk["table_refs"].append(parent)

                table_links_created += 1

print(

    f"Figure Links Created : "

    f"{links_created}"

)

print(

    f"Table Links Created  : "

    f"{table_links_created}"

)

# =========================================================
# 5. VALIDATION
# =========================================================

print()

print("Validating Knowledge Links...")

chunks_with_figures = 0
total_links = 0
broken_links = 0
missing_png = 0
retry_queued = 0
retry_figures = set()

from pathlib import Path

for chunk in chunks:

    if chunk["figure_refs"]:

        chunks_with_figures += 1

    for fig_id in chunk["figure_refs"]:

        total_links += 1

        figure = next(

            (

                f for f in figure_manifest

                if f["figure_id"] == fig_id

            ),

            None

        )

        if figure is None:

            broken_links += 1

            continue

        if figure["status"] == "RETRY_QUEUED":

            retry_figures.add(
                figure["figure_id"]
            )

            continue

        png_file = (

            DOCUMENT_FOLDER

            / "figures"

            / figure["file"]

        )

        if not png_file.exists():

            missing_png += 1

# =========================================================
# 6. SAVE ARTIFACTS
# =========================================================

with open(

    DOCUMENT_FOLDER / "figure_manifest.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        figure_manifest,

        f,

        indent=4,

        ensure_ascii=False

    )

with open(

    DOCUMENT_FOLDER / "chunks.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        chunks,

        f,

        indent=4,

        ensure_ascii=False

    )

retry_queued = len(
    retry_figures
)

print()

print("=" * 60)

print("KNOWLEDGE LINK VALIDATION")

print("=" * 60)

print()

print(f"Chunks              : {len(chunks)}")
print(f"Chunks With Figures : {chunks_with_figures}")
print(f"Figure Links        : {total_links}")
print(f"Broken Figure Links : {broken_links}")
print(f"Missing PNG         : {missing_png}")
print(f"Retry Queued        : {retry_queued}")

captioned_figures = sum(

    1

    for figure in figure_manifest

    if figure["caption"] is not None

)

print(

    f"Figures With Caption: "

    f"{captioned_figures}"

)

print()

# =========================================================
# 7. REPORTING
# =========================================================

print("=" * 60)
print("FIRST PICTURE")
print("=" * 60)

picture = knowledge_assets["pictures"][0]

print(f"ID          : {picture['id']}")
print(f"Label       : {picture['label']}")
print(f"Page        : {picture['page']}")
print(f"Children    : {len(picture['children'])}")
print(f"Has Image   : {picture['has_image']}")

MANIFEST_FILE = (
    DOCUMENT_FOLDER
    / "manifest.json"
)

manifest = {

    "document_id": DOCUMENT_ID,

    "version": "1.0",

    "status": "building",

    "knowledge_assets": {

        "texts": {
            "count": len(knowledge_assets["texts"])
        },

        "pictures": {
            "count": len(knowledge_assets["pictures"])
        },

        "tables": {
            "count": len(knowledge_assets["tables"])
        },

        "captions": {
            "count": len(knowledge_assets["captions"])
        }

    },

    "pipeline": {

        "docling_extracted": True,

        "chunks_built": True,

        "figures_extracted": True,

        "tables_extracted": True,

        "knowledge_linked": True,

        "validated": True,

        "embeddings_created": False

    }

}

with open(
    MANIFEST_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        manifest,
        f,
        indent=4,
        ensure_ascii=False
    )

print()

print(
    f"Manifest Saved : {MANIFEST_FILE.name}"
)

print()

print(
    f"Document Loaded : {DOCUMENT_ID}"
)

print()

print(f"Content Texts : {len(knowledge_assets['texts'])}")

print(f"Pictures     : {len(knowledge_assets['pictures'])}")

print(f"Tables       : {len(knowledge_assets['tables'])}")

print(f"Captions     : {len(knowledge_assets['captions'])}")
