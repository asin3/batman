"""
============================================================

Batman Student

CPS-006.1

Document Intelligence Adapter

Purpose

Convert Docling document.json into
Batman Knowledge Objects.

Current Stage

• Load document.json
• Validate JSON
• Return raw document

No parsing yet.

============================================================
"""

import json
from pathlib import Path


# ---------------------------------------------------------
# LOAD DOCUMENT
# ---------------------------------------------------------

def load_document(document_json: Path):

    with open(
        document_json,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
    
# ---------------------------------------------------------
# TEXT OBJECTS
# ---------------------------------------------------------

def get_text_objects(document):

    return document.get(
        "texts",
        []
    )    

# ---------------------------------------------------------
# PICTURE OBJECTS
# ---------------------------------------------------------

def get_picture_objects(document):

    return document.get(
        "pictures",
        []
    )

# ---------------------------------------------------------
# TABLE OBJECTS
# ---------------------------------------------------------

def get_table_objects(document):

    return document.get(
        "tables",
        []
    )

# ---------------------------------------------------------
# NORMALIZED PICTURE OBJECTS
# ---------------------------------------------------------

def normalize_picture_object(item):

    return {

        "id": item.get("self_ref"),

        "label": item.get("label"),

        "page": (

            item["prov"][0]["page_no"]

            if item.get("prov")

            else None

        ),

        "parent": (

            item.get("parent", {})

            .get("cref")

        ),

        "children": [

            child.get("cref")

            for child in item.get(

                "children",

                []

            )

        ],

        "captions": item.get(

            "captions",

            []

        ),

        "references": item.get(

            "references",

            []

        ),

        "has_image": (

            item.get("image")

            is not None

        )

    }


def get_normalized_pictures(document):

    pictures = get_picture_objects(document)

    return [

        normalize_picture_object(

            picture

        )

        for picture in pictures

    ]

# ---------------------------------------------------------
# NORMALIZED TABLE OBJECTS
# ---------------------------------------------------------

def get_normalized_tables(document):

    tables = get_table_objects(document)

    normalized = []

    for table in tables:

        normalized.append(

            {

                "id": table.get("self_ref"),

                "label": table.get("label"),

                "page": (

                    table["prov"][0]["page_no"]

                    if table.get("prov")

                    else None

                ),

                "parent": (

                    table.get("parent", {})

                    .get("cref")

                ),

                "children": [

                    child["cref"]

                    for child in table.get(

                        "children",

                        []

                    )

                ],

                "rows": (

                    table.get(

                        "data",

                        {}

                    ).get(

                        "num_rows"

                    )

                ),

                "cols": (

                    table.get(

                        "data",

                        {}

                    ).get(

                        "num_cols"

                    )

                )

            }

        )

    return normalized

# ---------------------------------------------------------
# PICTURE CAPTIONS
# ---------------------------------------------------------

def get_picture_captions(document):

    texts = get_normalized_texts(document)

    return [

        text

        for text in texts

        if text["label"] == "caption"

    ]

# ---------------------------------------------------------
# PICTURE LOOKUP
# ---------------------------------------------------------

def build_picture_lookup(document):

    lookup = {}

    pictures = get_normalized_pictures(document)

    captions = get_picture_captions(document)

    for picture in pictures:

        lookup[picture["id"]] = picture

    for caption in captions:

        # Caption linking moves to CPS-006.3B.
        #parent = caption["parent"]

        #if parent in lookup:

        #    lookup[parent]["caption"] = caption

     return lookup

# ---------------------------------------------------------
# GROUP OBJECTS
# ---------------------------------------------------------

def get_group_objects(document):

    return document.get(
        "groups",
        []
    )
# ---------------------------------------------------------
# SECTION HEADERS
# ---------------------------------------------------------

def get_section_headers(document):

    texts = get_normalized_texts(
        document
    )

    return [

        text

        for text in texts

        if text["label"] == "section_header"

    ]

# ---------------------------------------------------------
# CONTENT TEXTS
# ---------------------------------------------------------

def get_content_texts(document):

    texts = get_normalized_texts(document)

    return [

        text

        for text in texts

        if text["label"] not in [

            "page_header",

            "page_footer"

        ]

    ]

# ---------------------------------------------------------
# NORMALIZED TEXT OBJECT
# ---------------------------------------------------------

def normalize_text_object(item):

    return {

        "id": item.get("self_ref"),

        "label": item.get("label"),

        "text": item.get("text"),

        "page": (
            item["prov"][0]["page_no"]
            if item.get("prov")
            else None
        ),

        "parent": (
            item.get("parent", {})
            .get("cref")
        ),

        "children": item.get(
            "children",
            []
        )
    }

# ---------------------------------------------------------
# NORMALIZE ALL TEXT OBJECTS
# ---------------------------------------------------------

def get_normalized_texts(document):

    texts = get_text_objects(document)

    return [

        normalize_text_object(text)

        for text in texts

    ]

# ---------------------------------------------------------
# INSPECT DOCUMENT
# ---------------------------------------------------------

def inspect_document(document):

    print()

    print("=" * 60)
    print("DOCUMENT INSPECTION")
    print("=" * 60)

    print()

    print("Top Level Keys")

    print()

    for key in document.keys():

        print("-", key)

    print()

    print("Object Counts")

    print()

    collections = [

        "texts",

        "pictures",

        "tables",

        "pages",

        "groups",

        "body"

    ]

    for name in collections:

        value = document.get(name)

        if isinstance(value, list):

            print(f"{name:12} : {len(value)}")

        else:

            print(f"{name:12} : not-a-list")

    print()

    print("=" * 60)

    print()

    print("FIRST TEXT OBJECT")

    print()

    print(
        json.dumps(
            document["texts"][0],
            indent=4,
            ensure_ascii=False
        )
    )
# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DOCUMENT_JSON = (
        PROJECT_ROOT
        / "data"
        / "class10"
        / "biology"
        / "textbook"
        / "staging"
        / "DOC000013"
        / "document.json"
    )

    document = load_document(
        DOCUMENT_JSON
    )

    adapter = {

        "texts": get_text_objects(document),

        "pictures": get_picture_objects(document),

        "tables": get_table_objects(document),

        "groups": get_group_objects(document),

        "pictures": get_normalized_pictures(document),

        "picture_lookup": build_picture_lookup(document),

        "captions": get_picture_captions(document),

        "tables": get_normalized_tables(document)

    }

    normalized = get_normalized_texts(document)
    
    inspect_document(
        document
    )

    print()

    print("ADAPTER TEST")

    print()

    print(f"Texts    : {len(adapter['texts'])}")
    print(f"Pictures : {len(adapter['pictures'])}")
    print(f"Tables   : {len(adapter['tables'])}")
    print(f"Groups   : {len(adapter['groups'])}")

    print()

    print("FIRST NORMALIZED TEXT")

    print()

    print(
        json.dumps(
            normalized[0],
            indent=4,
            ensure_ascii=False
        )
    )

    sections = get_section_headers(
        document
    )

    print()

    print(f"Section Headers : {len(sections)}")

    content = get_content_texts(
    document
    )

    print()

    print(
        f"Content Texts : {len(content)}"
    )

    print()

    print(f"Normalized Pictures : {len(adapter['pictures'])}")

    print(f"Normalized Tables   : {len(adapter['tables'])}")

    print(
        f"Captions             : {len(adapter['captions'])}"
    )

    print()

    print("=" * 60)
    print("FIRST NORMALIZED PICTURE")
    print("=" * 60)

    print()

    print(

        json.dumps(

            adapter["pictures"][0],

            indent=4,

            ensure_ascii=False

        )

    )

    print()

    print("=" * 60)
    print("FIRST CAPTION OBJECT")

    print()

    print("=" * 60)
    print("FIRST NORMALIZED TABLE")
    print("=" * 60)

    print()

    print(

        json.dumps(

            adapter["tables"][0],

            indent=4,

            ensure_ascii=False

        )

    )
    print("=" * 60)

    print()

    print(
        json.dumps(
            adapter["captions"][0],
            indent=4,
            ensure_ascii=False
        )
    )

    print()

    print(
        f"Picture Lookup       : {len(adapter['picture_lookup'])}"
    )