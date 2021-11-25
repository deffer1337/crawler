from pathlib import Path
from typing import Union

from infrastructure.abstract_file_manager import AbstractFileManager


class FileManager(AbstractFileManager):

    @staticmethod
    def save_file(path: Union[str, Path], data: str) -> None:
        if not Path(path).exists():
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)

    @staticmethod
    def make_directory_if_not_exist(path: Union[str, Path], directory_name: str) -> Path:
        path = Path(path, directory_name)
        if not path.exists():
            path.mkdir()

        return path

