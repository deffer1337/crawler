import queue

from crawler_package.crawler import Crawler


class TestCrawler():
    def setup_class(self):
        self.crawler = Crawler()

    def test_can_url_fetch_WhenUrlNotInCurrentDomainAndRobotstxtExist_ThenFalse(self):
        self.crawler.robot = self.crawler._get_robot_parser('https://refactoring.guru/robots.txt')
        assert self.crawler._can_url_fetch('https://www.google.com/') is False

    def test_can_url_fetch_WhenUrlInCurrentDomainAndRobotstxtExist_ThenTrue(self):
        self.crawler.robot = self.crawler._get_robot_parser('https://refactoring.guru/robots.txt')
        assert self.crawler._can_url_fetch('https://refactoring.guru/')

    def test_can_url_fetch_WhenUrlInCurrentDomainAndUrlNotAllowAndRobotstxtExist_ThenFalse(self):
        self.crawler.robot = self.crawler._get_robot_parser('https://refactoring.guru/robots.txt')
        assert self.crawler._can_url_fetch('https://refactoring.guru/admin') is False

    def test_can_url_fetch_WhenUrlNotInCurrentDomainAndRobotstxtNotExist_ThenFalse(self):
        self.crawler.robot = self.crawler._get_robot_parser('https://insma.urfu.ru/robots.txt')
        assert self.crawler._can_url_fetch('https://www.google.com/') is False

    def test_can_url_fetch_WhenUrlInCurrentDomainAndRobotstxtNotExist_ThenTrue(self):
        self.crawler.robot = self.crawler._get_robot_parser('https://insma.urfu.ru/robots.txt')
        assert self.crawler._can_url_fetch('https://insma.urfu.ru')

    def test_merge_urls_WhenQueueEmptyLength_ThanListEmpty(self):
        assert len(self.crawler._merger_urls(queue.Queue())) == 0

    def test_merge_urls_WhenQueueNotEmptyLength_ThanListNotEmpty(self):
        queue_set = queue.Queue()
        queue_set.put({'1'})
        assert len(self.crawler._merger_urls(queue_set)) > 0


