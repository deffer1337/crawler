from abc import ABC, abstractmethod


class AbstractFileManager(ABC):
    def __init__(self, path):
        self._path = path

    @abstractmethod
    def save_file(self, data):
        pass

    @abstractmethod
    def make_directory_if_not_exist(self, directory_name):
        pass
