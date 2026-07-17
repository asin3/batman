"""
============================================================
Batman DOX Import Engine (BDIE)

Schema Registry

Purpose:
Stores the canonical column names used by BDIE.

All document formats normalize to these names.

============================================================
"""

# ==========================================================
# SCHEMA MAP
# ==========================================================

SCHEMA_MAP = {

    # ---------- Groups ----------
    "unit": "group",
    "section": "group",
    "module": "group",
    "semester": "group",

    # ---------- Chapter Number ----------
    "chapter no.": "chapter_number",
    "ch. no.": "chapter_number",
    "lesson no.": "chapter_number",

    # ---------- Chapter ----------
    "chapter": "chapter_title",
    "chapter name": "chapter_title",
    "chapters": "chapter_title",
    "lesson": "chapter_title",

    # ---------- Topics ----------
    "topic": "topics",
    "topics": "topics",

}


# ==========================================================
# NORMALIZE
# ==========================================================

def normalize(header: str) -> str:

    return SCHEMA_MAP.get(
        header.strip().lower(),
        header.strip().lower()
    )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(normalize("Chapter No."))
    print(normalize("Ch. No."))
    print(normalize("Chapter Name"))