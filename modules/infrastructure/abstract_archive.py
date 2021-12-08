from abc import ABC, abstractmethod


class Archive(ABC):
    @staticmethod
    @abstractmethod
    def create_archive_if_not_exists(path, name):
        pass

    @staticmethod
    @abstractmethod
    def create_directory_in_archive(path_to_archive, directory_name):
        pass

    @staticmethod
    @abstractmethod
    def save_file_in_archive(path, file_name, data, directory_in_archive):
        pass

    @staticmethod
    @abstractmethod
    def is_archive(path):
        pass
