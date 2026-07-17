##############################################
# IMPORTS
##############################################

import json
from pathlib import Path

from supabase import create_client

from src.platform.storage.storage_repository import StorageRepository

import streamlit as st

##############################################
# LOAD CONFIGURATION
##############################################

###########################################################
# LOAD SUPABASE CONFIG
###########################################################

def load_supabase_config():

    config_path = (
        Path(__file__).resolve().parents[3]
        / "secrets"
        / "supabase.json"
    )

# ------------------------------------------
# Local Development
# ------------------------------------------

    if config_path.exists():

        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

# ------------------------------------------
# Streamlit Cloud
# ------------------------------------------

    return {

        "url": st.secrets["SUPABASE_URL"],

        "service_role_key": st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

    }   


##############################################
# SUPABASE STORAGE REPOSITORY
##############################################

class SupabaseStorageRepository(StorageRepository):

    ##########################################
    # Constructor
    ##########################################

    def __init__(self):

        config = load_supabase_config()

        self.client = create_client(
            config["url"],
            config["service_role_key"],
        )

    ##########################################
    # Split Storage Path
    ##########################################

    def _split_path(self, path: str):

        parts = path.split("/", 1)

        if len(parts) != 2:
            raise ValueError(f"Invalid storage path: {path}")

        return parts[0], parts[1]

    ##########################################
    # Read JSON
    ##########################################

    def read_json(self, path: str):

        bucket, object_name = self._split_path(path)

        data = (
            self.client
            .storage
            .from_(bucket)
            .download(object_name)
        )

        return json.loads(data.decode("utf-8"))

    ##########################################
    # Write JSON
    ##########################################

    def write_json(self, path: str, data: dict):

        bucket, object_name = self._split_path(path)

        payload = json.dumps(
            data,
            indent=4
        ).encode("utf-8")

        storage = self.client.storage.from_(bucket)

        if self.exists(path):

            storage.update(
                object_name,
                payload,
                {
                    "content-type": "application/json"
                }
            )

        else:

            storage.upload(
                object_name,
                payload,
                {
                    "content-type": "application/json"
                }
            )
            
    ##########################################
    # Exists
    ##########################################

    def exists(self, path: str):

        bucket, object_name = self._split_path(path)

        folder = str(Path(object_name).parent)

        filename = Path(object_name).name

        files = (
            self.client
            .storage
            .from_(bucket)
            .list(folder)
        )

        return any(
            file["name"] == filename
            for file in files
        )

    ##########################################
    # Delete
    ##########################################

    def delete(self, path: str):

        bucket, object_name = self._split_path(path)

        self.client.storage.from_(bucket).remove(
            [object_name]
        )

    ##########################################
    # List
    ##########################################

    def list(self, folder: str):

        parts = folder.split("/", 1)

        bucket = parts[0]

        object_path = ""

        if len(parts) == 2:
            object_path = parts[1]

        files = (
            self.client
            .storage
            .from_(bucket)
            .list(object_path)
        )

        return [
            item["name"]
            for item in files
        ]


##############################################
# TEST
##############################################

if __name__ == "__main__":

    repo = SupabaseStorageRepository()

    test_data = {
        "hello": "Batman",
        "version": "1.0"
    }

    print("Writing...")

    repo.write_json(
        "users/test/test.json",
        test_data
    )

    print("Exists:", repo.exists("users/test/test.json"))

    print("Read:", repo.read_json("users/test/test.json"))

    print("List:", repo.list("users/test"))

    repo.delete("users/test/test.json")

    print("Deleted.")