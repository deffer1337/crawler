from pathlib import Path
from threading import Lock
from typing import List, Union
from zipfile import ZIP_DEFLATED, ZipFile, is_zipfile

from modules.infrastructure.abstract_archive import Archive

lock = Lock()
file_names = set()


class ZipArchive(Archive):
    def __init__(self, path: Union[str, Path]):
        super().__init__(path)

    def save_file_in_archive(self, file_name: str, data: Union[str, bytes], directory_in_archive: str) -> None:
        lock.acquire()
        with ZipFile(self._path, "a", ZIP_DEFLATED) as zip_file:
            if str(Path(directory_in_archive, file_name)) not in file_names:
                zip_file.writestr(f"{directory_in_archive}/{file_name}", data)

        lock.release()

    def create_directory_in_archive(self, directory_name: str):
        with ZipFile(self._path, "a", ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"/{directory_name}/", b"")

    def create_archive_if_not_exists(self, name: str) -> Path:
        global file_names
        path = Path(self._path)
        if path.exists() and ZipArchive.is_archive(path):
            file_names = set(ZipArchive.get_file_names_from_archive(path))
            return path

        path = Path(path, f"{name}.zip")
        if not path.exists():
            with ZipFile(path, "w", ZIP_DEFLATED):
                pass

        file_names = set(ZipArchive.get_file_names_from_archive(path))

        return path

    @staticmethod
    def is_archive(path) -> bool:
        return is_zipfile(path)

    @staticmethod
    def get_file_names_from_archive(path) -> List[str]:
        with ZipFile(path, "r", ZIP_DEFLATED) as zip_file:
            return zip_file.namelist()
