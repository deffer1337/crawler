from urllib.parse import urlparse, urljoin


class UrlManager:

    @staticmethod
    def is_absolute(url: str) -> bool:
        return bool(urlparse(url).netloc)

    @staticmethod
    def get_domain_with_protocol(url: str) -> str:
        url_parse = urlparse(url)
        return f'{url_parse.scheme}://{url_parse.netloc}'

    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc

    @staticmethod
    def get_url_robots_txt(url: str) -> str:
        url_parse = urlparse(url)
        return f'{url_parse.scheme}://{url_parse.netloc}/robots.txt'

    @staticmethod
    def get_url_path(url: str) -> str:
        return urlparse(url).path

    @staticmethod
    def url_join(url: str, path: str) -> str:
        return urljoin(url, path)
