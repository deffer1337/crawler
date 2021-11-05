import re
from queue import Queue

import concurrent.futures as pool
import requests
from requests import Response
from bs4 import BeautifulSoup
from reppy.robots import Robots

from crawler_package.file_manager import FileManager
from crawler_package.url_manager import UrlManager


class Crawler:
    def __init__(self):
        self.pattern = re.compile(r'^[\w|\/|\d][\w\d\/:\.-]+[^\.pdf|\.doc|\.docx|\.xls]')
        self.urls = set()
        self.robot = None

    def start(self, url: str, max_recursive: int = 3):
        response_not_ok_msg = self._get_msg_if_response_not_ok(requests.get(url))
        if response_not_ok_msg:
            print(f'{response_not_ok_msg}')
            return
        self.urls.add(url)
        self.robot = self._get_robot_parser(url)
        FileManager.make_directory_if_not_exist(FileManager.get_path_for_domain_directory(url))
        self._scheduler([url], max_recursive)

    def _scheduler(self, urls: list, max_depth: int):
        while max_depth > 0:
            if len(urls) == 0:
                break

            queue_set_urls = Queue()
            with pool.ThreadPoolExecutor(len(urls)) as executer:
                for url in executer.map(self._fetcher, urls):
                    queue_set_urls.put(url)

            urls = self._merger_urls(queue_set_urls)
            max_depth -= 1

        print('Success. All pages are downloaded')

    def _fetcher(self, url: str) -> set:
        response = requests.get(url)
        FileManager.save_file(FileManager.get_path_to_download_file_html(url), response.text)
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

            if self.pattern.fullmatch(link):
                if not UrlManager.is_absolute(link):
                    link = f'{UrlManager.get_domain_with_protocol(url)}{link}'
                    if self._can_url_fetch(link) and link not in self.urls:
                        self.urls.add(link)
                        urls.add(link)

        return urls

    def _merger_urls(self, queue_set_urls: Queue) -> list:
        while queue_set_urls.qsize() > 2:
            queue_set_urls.put(queue_set_urls.get().union(queue_set_urls.get()))

        return list(queue_set_urls.get())

    def _get_robot_parser(self, url: str):
        robots_txt = requests.get(UrlManager.get_url_robots_txt(url))

        if robots_txt.status_code == requests.codes.ok:
            robot_parser = Robots.parse(UrlManager.get_domain_with_protocol(url), robots_txt.text)
        else:
            robot_parser = Robots.parse(UrlManager.get_domain_with_protocol(url), '')

        return robot_parser

    def _can_url_fetch(self, url: str) -> bool:
        return self.robot.allowed(url, '*')


if __name__ == '__main__':
    import time

    start = time.perf_counter()
    c = Crawler()
    c.start('https://refactoring.gur')
    print(time.perf_counter() - start)
