import sys
from urllib.parse import urlparse, urljoin

import requests


class UrlManager:

    @staticmethod
    def is_absolute(url: str) -> bool:
        return bool(urlparse(url).netloc)

    @staticmethod
    def get_netloc_with_scheme(url: str) -> str:
        url_parse = urlparse(url)
        return f'{url_parse.scheme}://{url_parse.netloc}'

    @staticmethod
    def is_not_correct_url(url: str):
        """
        Checking the url for correctness

        :param url: Url you need to check
        :return: If url not correct, then return exception msg, else return False
        """
        try:
            requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
            return str(e)

        return False

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
