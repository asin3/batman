import chromadb

# ---------------------------------
# KNOWLEDGE ACCESS LAYER
# ---------------------------------

_COLLECTION_NAME = "icse_class10"
_DB_PATH = "./vector_db"


def get_collection():
    """
    Returns the active Knowledge Base collection.

    Returns:
        Collection object if available.
        None if the Knowledge Base cannot be loaded.
    """

    try:
        db = chromadb.PersistentClient(
            path=_DB_PATH
        )

        return db.get_collection(
            _COLLECTION_NAME
        )

    except Exception as e:

        print(f"[Batman] ERROR: {e}")

        print(
            "[Batman] Knowledge Base not found."
        )

        print(
            "[Batman] Retrieval features are disabled."
        )

        return None
    

        print(
            "[Batman] Knowledge Base not found."
        )

        print(
            "[Batman] Retrieval features are disabled."
        )

        return None