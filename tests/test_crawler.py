import queue
import re

from modules.crawler_package.crawler import Crawler


class TestCrawler:
    def setup_class(self):
        self.crawler = Crawler()

    def test_can_url_fetch_WhenUrlNotInCurrentDomainAndRobotstxtExist_ThenFalse(self):
        self.crawler._robot = self.crawler._get_robot_parser('https://refactoring.guru')
        assert self.crawler._can_url_fetch('https://www.google.com/') is False

    def test_can_url_fetch_WhenUrlInCurrentDomainAndRobotstxtExist_ThenTrue(self):
        self.crawler._robot = self.crawler._get_robot_parser('https://refactoring.guru')
        assert self.crawler._can_url_fetch('https://refactoring.guru/')

    def test_can_url_fetch_WhenUrlInCurrentDomainAndUrlNotAllowAndRobotstxtExist_ThenFalse(self):
        self.crawler._robot = self.crawler._get_robot_parser('https://refactoring.guru')
        assert self.crawler._can_url_fetch('https://refactoring.guru/admin') is False

    def test_can_url_fetch_WhenUrlNotInCurrentDomainAndRobotstxtNotExist_ThenFalse(self):
        self.crawler._robot = self.crawler._get_robot_parser('https://insma.urfu.ru')
        assert self.crawler._can_url_fetch('https://www.google.com/') is False

    def test_can_url_fetch_WhenUrlInCurrentDomainAndRobotstxtNotExist_ThenTrue(self):
        self.crawler._robot = self.crawler._get_robot_parser('https://insma.urfu.ru')
        assert self.crawler._can_url_fetch('https://insma.urfu.ru')

    def test_merge_urls_WhenQueueEmptyLength_ThanListEmpty(self):
        assert len(self.crawler._merger_urls(queue.Queue())) == 0

    def test_merge_urls_WhenQueueNotEmptyLength_ThanListNotEmpty(self):
        queue_set = queue.Queue()
        queue_set.put({'1'})
        assert len(self.crawler._merger_urls(queue_set)) > 0

    def test_check_link_on_pattern(self):
        link = 'http://localhost/bin/'
        assert re.match(self.crawler._pattern, link) is not None

    def test_get_urls_when_links_is_absolute(self):
        html = '<a href="https://example.com/lectures/">Лекции</a>' \
               '<a href="https://example.com/lectures/networks/">Сети</a>'
        url = 'example.com'
        self.crawler._domains.add(url)
        links = self.crawler._get_urls(html.encode("utf-8"), url)
        assert len(links) == 2

    def test_get_urls_when_links_is_not_absolute(self):
        html = '<a href="/lectures/">Лекции</a>' \
               '<a href="/lectures/networks/">Сети</a>' \
               '<a href="/homeworks/networks/tls/">TLS</a>'
        url = 'example.com'
        self.crawler._domains.add(url)
        links = self.crawler._get_urls(html.encode("utf-8"), url)
        assert len(links) == 3
