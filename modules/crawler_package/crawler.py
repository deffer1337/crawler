import concurrent.futures as pool
import logging
import re
from pathlib import Path
from queue import Queue
from typing import List

import requests
from bs4 import BeautifulSoup
from reppy.robots import Robots

from modules.crawler_package.url_manager import (
    get_domain,
    get_netloc_with_scheme,
    get_url_path,
    get_url_robots_txt,
    is_absolute,
    url_join,
)
from modules.infrastructure.abstract_archive import Archive
from modules.infrastructure.abstract_file_manager import AbstractFileManager
from modules.infrastructure.program_state import ProgramState
from modules.utils import get_msg_if_response_not_ok, wrapper_requests_get


class Crawler:
    def __init__(self, archive: Archive, file_manager: AbstractFileManager):
        self._pattern = re.compile(r"^[\w|\/|\d][\w\d\/:\.-]+[^\.pdf|\.doc|\.docx|\.xls]")
        self._urls = set()
        self._domains = set()
        self._is_archive_option = False
        self._robot = None
        self._path = None
        self._crawler_state = None
        self._logger = logging.getLogger("crawl")
        self._archive = archive
        self._file_manager = file_manager

    def _init_crawler(
        self, url: str, depth: int, count_threads: int, sites: List[str], path: str, is_archive_option: bool
    ):
        for site in sites:
            self._domains.add(get_domain(site))
        self._is_archive_option = is_archive_option
        self._robot = self._get_robot_parser(url)
        if is_archive_option:
            self._path = self._archive(path).create_archive_if_not_exists(get_domain(url))
        else:
            self._path = self._file_manager(path).make_directory_if_not_exist(get_domain(url))

        self._logger.info("Saved the parameters with which crawling started.")
        self._crawler_state.add_to_param_value("url", url).add_to_param_value("depth", depth).add_to_param_value(
            "count_threads", count_threads
        ).add_to_param_value("sites", sites).add_to_param_value("path", str(path)).add_to_param_value(
            "is_archive_option", is_archive_option
        )

    def start(
        self,
        url: str,
        depth: int,
        count_threads: int,
        sites: List[str],
        path: str,
        is_archive_option: bool,
        crawler_state: ProgramState = None,
    ) -> None:
        """
        Init crawler and start.

        :param url: Url to the site that needs to be bypassed
        :param depth: Site crawl depth
        :param count_threads: The number of streams when downloading pages from the site
        :param sites: Sites that can be crawled
        :param path: The path to save the pages
        :param is_archive_option: An option that specifies whether to archive
        :param crawler_state: The state of the crawler in which there was an error
        :return: None
        """
        url_domain = get_domain(url)
        if not crawler_state:
            self._urls.add(url)
            self._crawler_state = ProgramState(
                Path(Path(__file__).resolve().parent.parent.parent, "States", f"{url_domain}~"),
                Path(Path(Path(__file__).resolve().parent.parent.parent, "States", f"{url_domain}")),
            )
        else:
            self._crawler_state = crawler_state
            self._urls = set(self._crawler_state.get("_urls"))

        urls = [url] if not crawler_state else crawler_state.get("urls")
        self._init_crawler(url, depth, count_threads, sites, path, is_archive_option)

        self._scheduler(urls, depth, count_threads)

        self._logger.info(f"End crawling. All pages are downloaded from {url_domain}.")
        print(f"Success. All pages are downloaded from {url_domain}")

    def _scheduler(self, urls: list, depth: int, count_threads: int):
        while depth > 0:
            if len(urls) == 0:
                break

            queue_set_urls = Queue()
            with pool.ThreadPoolExecutor(count_threads) as executor:
                for set_urls in executor.map(self._fetcher, urls):
                    queue_set_urls.put(set_urls)

            urls = self._merger_urls(queue_set_urls)
            depth -= 1

            self._crawler_state.add_to_param_value("urls", urls)
            self._crawler_state.add_to_param_value("depth", depth)
            self._crawler_state.add_to_param_value("_urls", list(self._urls))
            self._crawler_state.dump()

        self._crawler_state.program_finish()

    def _fetcher(self, url: str) -> set:
        delay = self._robot.agent("*").delay
        response = wrapper_requests_get(url, delay) if delay else requests.get(url)

        msg = get_msg_if_response_not_ok(response)
        if msg:
            self._logger.error(f"Status code is not OK. {msg}")
            return set()

        if self._is_archive_option:
            self._archive(self._path).save_file_in_archive(
                get_url_path(url).replace("/", "\\") + ".html", response.text.encode(), f"/{get_domain(url)}"
            )
            self._logger.info(f"Page {url} downloaded in archive.")
        else:
            self._file_manager(Path(self._path, get_url_path(url).replace("/", "\\") + ".html")).save_file(
                response.text
            )
            self._logger.info(f"Page {url} downloaded.")

        return self._get_urls(response.content, url)

    def _get_urls(self, content, url: str) -> set:
        urls = set()
        soup = BeautifulSoup(content, "html.parser")

        for link in soup.find_all("a"):
            link = str(link.get("href"))

            if self._pattern.fullmatch(link):
                if not is_absolute(link):
                    link = url_join(url, link)

                if (self._can_url_fetch(link) or get_domain(link) in self._domains) and link not in self._urls:
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
        robots_txt = requests.get(get_url_robots_txt(url))

        if robots_txt.status_code == requests.codes.ok:
            robot_parser = Robots.parse(get_netloc_with_scheme(url), robots_txt.text)
        else:
            robot_parser = Robots.parse(get_netloc_with_scheme(url), "")

        return robot_parser

    def _can_url_fetch(self, url: str) -> bool:
        return self._robot.allowed(url, "*")
