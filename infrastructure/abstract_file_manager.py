from abc import ABC, abstractmethod


class AbstractFileManager(ABC):

    @staticmethod
    @abstractmethod
    def save_file(path, data):
        pass

    @staticmethod
    @abstractmethod
    def make_directory_if_not_exist(path, directory_name):
        pass

