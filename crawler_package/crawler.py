import re
from queue import Queue

import concurrent.futures as pool
import requests
from requests import Response
from bs4 import BeautifulSoup
from reppy.robots import Robots
from pathlib import Path

from infrastructure.file_manager import FileManager
from crawler_package.url_manager import UrlManager
from infrastructure.zip_archive import ZipArchive


class Crawler:
    def __init__(self):
        self._pattern = re.compile(r'^[\w|\/|\d][\w\d\/:\.-]+[^\.pdf|\.doc|\.docx|\.xls]')
        self._urls = set()
        self._domains = set()
        self._is_archive_option = False
        self._robot = None
        self._path = None

    def start(self, url: str, max_recursive: int, count_threads: int, sites: list, path: str, is_archive_option: bool) -> None:
        response_not_ok_msg = self._get_msg_if_response_not_ok(requests.get(url))
        if response_not_ok_msg:
            print(f'{response_not_ok_msg}')
            return
        for site in sites:
            self._domains.add(UrlManager.get_domain(site))
        self._is_archive_option = is_archive_option
        self._urls.add(url)
        self._robot = self._get_robot_parser(url)
        if is_archive_option:
            self._path = ZipArchive.create_archive_if_not_exists(path, UrlManager.get_domain(url))
        else:
            self._path = FileManager.make_directory_if_not_exist(path, UrlManager.get_domain(url))

        self._scheduler([url], max_recursive, count_threads)

    def _scheduler(self, urls: list, max_depth: int, count_threads: int):
        while max_depth > 0:
            if len(urls) == 0:
                break

            queue_set_urls = Queue()
            with pool.ThreadPoolExecutor(count_threads) as executer:
                for url in executer.map(self._fetcher, urls):
                    queue_set_urls.put(url)

            urls = self._merger_urls(queue_set_urls)
            max_depth -= 1

        print('Success. All pages are downloaded')

    def _fetcher(self, url: str) -> set:
        response = requests.get(url)
        if self._get_msg_if_response_not_ok(response):
            return set()

        if self._is_archive_option:
            ZipArchive.save_file_in_archive(self._path, UrlManager.get_url_path(url).replace('/', '\\') + ".html",
                                            response.text.encode(), f'/{UrlManager.get_domain(url)}')
        else:
            FileManager.save_file(Path(self._path,
                                       UrlManager.get_url_path(url).replace('/', '\\') + ".html"), response.text)

        return self._get_urls(response, url)

    def _get_msg_if_response_not_ok(self, response: Response) -> str:
        try:
            response.raise_for_status()
        except Exception as e:
            return str(e)

    def _get_urls(self, response, url: str) -> set:
        urls = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            link = str(link.get('href'))

            if self._pattern.fullmatch(link):
                if not UrlManager.is_absolute(link):
                    link = UrlManager.url_join(url, link)
                    if (self._can_url_fetch(link) or UrlManager.get_domain(link) in self._domains) and \
                            link not in self._urls:
                        self._urls.add(link)
                        urls.add(link)

        return urls

    def _merger_urls(self, queue_set_urls: Queue) -> list:
        if queue_set_urls.qsize() == 0:
            return []

        while queue_set_urls.qsize() > 2:
            queue_set_urls.put(queue_set_urls.get().union(queue_set_urls.get()))

        return list(queue_set_urls.get_nowait())

    def _get_robot_parser(self, url: str):
        robots_txt = requests.get(UrlManager.get_url_robots_txt(url))

        if robots_txt.status_code == requests.codes.ok:
            robot_parser = Robots.parse(UrlManager.get_domain_with_protocol(url), robots_txt.text)
        else:
            robot_parser = Robots.parse(UrlManager.get_domain_with_protocol(url), '')

        return robot_parser

    def _can_url_fetch(self, url: str) -> bool:
        return self._robot.allowed(url, '*')

