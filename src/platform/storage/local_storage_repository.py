import json
from pathlib import Path

from src.platform.storage.storage_repository import StorageRepository


class LocalStorageRepository(StorageRepository):

    def __init__(self):

        self.data_root = Path(__file__).resolve().parents[3] / "data"

    # ---------------------------------------------------------

    def read_json(self, path: str):

        file_path = self.data_root / path

        with open(file_path, "r", encoding="utf-8") as file:

            return json.load(file)

    # ---------------------------------------------------------

    def write_json(self, path: str, data: dict):

        file_path = self.data_root / path

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)

    # ---------------------------------------------------------

    def exists(self, path: str):

        return (self.data_root / path).exists()

    # ---------------------------------------------------------

    def delete(self, path: str):

        file_path = self.data_root / path

        if file_path.exists():

            file_path.unlink()

    # ---------------------------------------------------------

    def list(self, folder: str):

        folder_path = self.data_root / folder

        if not folder_path.exists():

            return []

        return [item.name for item in folder_path.iterdir()]

    import json
from pathlib import Path

from src.platform.storage.storage_repository import StorageRepository


class LocalStorageRepository(StorageRepository):

    def __init__(self):

        self.data_root = Path(__file__).resolve().parents[3] / "data"

    # ---------------------------------------------------------

    def read_json(self, path: str):

        file_path = self.data_root / path

        with open(file_path, "r", encoding="utf-8") as file:

            return json.load(file)

    # ---------------------------------------------------------

    def write_json(self, path: str, data: dict):

        file_path = self.data_root / path

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)

    # ---------------------------------------------------------

    def exists(self, path: str):

        return (self.data_root / path).exists()

    # ---------------------------------------------------------

    def delete(self, path: str):

        file_path = self.data_root / path

        if file_path.exists():

            file_path.unlink()

    # ---------------------------------------------------------

    def list(self, folder: str):

        folder_path = self.data_root / folder

        if not folder_path.exists():

            return []

        return [item.name for item in folder_path.iterdir()]
    

######################################
    ## TEST
######################################

if __name__ == "__main__":

    repo = LocalStorageRepository()

    print(repo.exists("users/USR000001/profile.json"))