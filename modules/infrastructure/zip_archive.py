from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED
from threading import Lock
from pathlib import Path
from typing import Union, List

from modules.infrastructure.abstract_archive import Archive


lock = Lock()
file_names = set()


class ZipArchive(Archive):
    @staticmethod
    def save_file_in_archive(path: str, file_name: str, data: Union[str, bytes], directory_in_archive: str) -> None:
        lock.acquire()
        with ZipFile(path, 'a', ZIP_DEFLATED) as zip_file:
            if str(Path(directory_in_archive, file_name)) not in file_names:
                zip_file.writestr(f'{directory_in_archive}/{file_name}', data)

        lock.release()

    @staticmethod
    def _get_file_names_from_archive(path: Union[str, Path]) -> List[str]:
        with ZipFile(path, 'r', ZIP_DEFLATED) as zip_file:
            return zip_file.namelist()

    @staticmethod
    def create_directory_in_archive(path_to_archive: Union[str, Path], directory_name: str):
        with ZipFile(path_to_archive, 'a', ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f'/{directory_name}/', b'')

    @staticmethod
    def create_archive_if_not_exists(path: str, name: str) -> Path:
        global file_names
        path = Path(path)
        if path.exists() and ZipArchive.is_archive(path):
            file_names = set(ZipArchive._get_file_names_from_archive(path))
            return path

        path = Path(path, f'{name}.zip')
        if not path.exists():
            with ZipFile(path, 'w', ZIP_DEFLATED):
                pass

        file_names = set(ZipArchive._get_file_names_from_archive(path))

        return path

    @staticmethod
    def is_archive(path: Union[str, Path]) -> bool:
        return is_zipfile(path)
