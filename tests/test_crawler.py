from crawler_package.crawler import Crawler


def test_canUrlFetch_WhenUrlNotInCurrentDomainAndRobotstxtExist():
    crawler = Crawler()
    crawler._get_robot_parser('https://refactoring.guru/robots.txt')
    assert crawler._can_url_fetch('https://www.google.com/') is False


def test_canUrlFetch_WhenUrlNotInCurrentDomainAndRobotstxtNotExist():
    crawler = Crawler()
    crawler._get_robot_parser('https://insma.urfu.ru/robots.txt')
    assert crawler._can_url_fetch('https://www.google.com/') is False


def test_canUrlFetch_WhenUrlInCurrentDomainAndRobotstxtNotExist():
    crawler = Crawler()
    crawler._get_robot_parser('https://insma.urfu.ru/robots.txt')
    assert crawler._can_url_fetch('https://insma.urfu.ru') is True