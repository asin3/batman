from abc import ABC, abstractmethod


class StorageRepository(ABC):

    @abstractmethod
    def read_json(self, path: str):
        pass

    @abstractmethod
    def write_json(self, path: str, data: dict):
        pass

    @abstractmethod
    def exists(self, path: str):
        pass

    @abstractmethod
    def delete(self, path: str):
        pass

    @abstractmethod
    def list(self, folder: str):
        pass

    ##################################
    # #TEST
    ######################################

    if __name__ == "__main__":
        print("Batman Storage Repository Ready")