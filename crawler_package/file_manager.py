from pathlib import Path

from crawler_package.url_manager import UrlManager


class FileManager:

    @staticmethod
    def save_file(path, data):
        if not Path(path).exists():
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)

    @staticmethod
    def make_directory_if_not_exist(directory):
        path = Path(directory)
        if not path.exists():
            path.mkdir()

    @staticmethod
    def get_path_for_domain_directory(url: str) -> str:
        return str(Path(Path(__file__).parent.parent, "Pages", UrlManager.get_domain(url)))

    @staticmethod
    def get_path_to_download_file_html(url: str) -> str:
        path = FileManager.get_path_for_domain_directory(url)
        file_name = UrlManager.get_url_path(url).replace('/', '\\')

        return str(Path(path, f"{file_name}.html"))
