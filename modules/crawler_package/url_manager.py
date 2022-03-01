from urllib.parse import urljoin, urlparse

import requests


def is_absolute(url: str) -> bool:
    """
    Checking url to absolute

    :param url: Url to check
    :return: Is the url absolute
    """
    return bool(urlparse(url).netloc)


def get_netloc_with_scheme(url: str) -> str:
    """

    :param url:
    :return:
    """
    url_parse = urlparse(url)
    return f"{url_parse.scheme}://{url_parse.netloc}"


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


def get_domain(url: str) -> str:
    """
    Get domain from url

    :param url: The url from which to take the domain
    :return: Domain
    """
    return urlparse(url).netloc


def get_url_robots_txt(url: str) -> str:
    """
    Get path to robots.txt in this url

    :param url: Url where to need add the path to robots.txt
    :return: Url with path to robots.txt in this url
    """
    url_parse = urlparse(url)
    return f"{url_parse.scheme}://{url_parse.netloc}/robots.txt"


def get_url_path(url: str) -> str:
    """
    Get path from url

    :param url: Url where to get the path
    :return: Path from url
    """
    return urlparse(url).path


def url_join(url: str, path: str) -> str:
    """
    Url join
    """
    return urljoin(url, path)
