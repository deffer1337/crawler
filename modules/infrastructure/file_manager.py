from pathlib import Path
from typing import Union

from modules.infrastructure.abstract_file_manager import AbstractFileManager


class FileManager(AbstractFileManager):
    def __init__(self, path: Union[str, Path]):
        super().__init__(path)

    def save_file(self, data: str) -> None:
        if not Path(self._path).exists():
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(data)

    def make_directory_if_not_exist(self, directory_name: str) -> Path:
        path = Path(self._path, directory_name)
        if not path.exists():
            path.mkdir()

        return path
