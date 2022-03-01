from abc import ABC, abstractmethod


class Archive(ABC):
    def __init__(self, path):
        self._path = path

    @abstractmethod
    def create_archive_if_not_exists(self, name):
        pass

    @abstractmethod
    def create_directory_in_archive(self, directory_name):
        pass

    @abstractmethod
    def save_file_in_archive(self, file_name, data, directory_in_archive):
        pass

    @staticmethod
    @abstractmethod
    def is_archive(path):
        pass

    @staticmethod
    @abstractmethod
    def get_file_names_from_archive(path):
        pass
