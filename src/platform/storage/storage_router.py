##################################################
# IMPORTS
##################################################

import json
from pathlib import Path

from src.platform.storage.local_storage_repository import (
    LocalStorageRepository,
)

from src.platform.storage.supabase_storage_repository import (
    SupabaseStorageRepository,
)

##################################################
# LOAD STORAGE CONFIG
##################################################

def load_storage_config():

    config_path = (
        Path(__file__).resolve().parents[2]
        / "config"
        / "storage.json"
    )

    with open(config_path, "r", encoding="utf-8") as file:

        return json.load(file)


##################################################
# STORAGE ROUTER
##################################################

class StorageRouter:

    @staticmethod
    def get_repository():

        config = load_storage_config()

        backend = config["backend"].lower()

        if backend == "local":

            return LocalStorageRepository()

        if backend == "supabase":

            return SupabaseStorageRepository()

        raise ValueError(
            f"Unknown storage backend: {backend}"
        )


##################################################
# TEST
##################################################

if __name__ == "__main__":

    repository = StorageRouter.get_repository()

    print(type(repository).__name__)